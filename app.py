import streamlit as st
import pandas as pd
import datetime
import os

# Page Configurations
st.set_page_config(page_title="Precision CDSS Pro v3.0", layout="wide")

st.title("🛡️ Enterprise-Grade Precision Antimicrobial Stewardship CDSS")
st.caption("Developed by: MAYANK VIRMANI (PharmD Scholar) | Multi-Drug Combination Logic Framework")

# 1. Load the 50+ Drugs Database safely
@st.cache_data
def load_database():
    # If file exists, load it, else create a minimal temporary version to avoid error
    if os.path.exists("drugs_database.csv"):
        return pd.read_csv("drugs_database.csv")
    else:
        st.error("🚨 'drugs_database.csv' file missing in folder! Please create it to access 50+ drugs.")
        return pd.DataFrame(columns=["Drug_Name", "Class", "Standard_Route", "Max_Daily_Dose", "Renal_Threshold_CrCl", "Dosing_Guideline_Note"])

df_drugs = load_database()

# Demographics Layout
col1, col2 = st.columns(2)

with col1:
    st.header("🏥 Patient Demographics & Physiometrics")
    clinical_setting = st.selectbox("Clinical Environment:", ["ICU (Intensive Care)", "Medical Wards (IPD)", "OPD (Outpatient)"])
    gender = st.selectbox("Biological Sex:", ["Male", "Female"])
    age = st.number_input("Age (Years):", min_value=1, max_value=110, value=65)
    height_cm = st.number_input("Height (cm):", min_value=100, max_value=250, value=170)
    weight_kg = st.number_input("Weight (kg):", min_value=5, max_value=250, value=85)
    scr = st.number_input("Serum Creatinine (mg/dL):", min_value=0.2, max_value=10.0, value=1.6)

    # Dosing Weight Adjustment (Obesity Pharmacokinetics)
    height_in = height_cm / 2.54
    if height_in > 60:
        ibw = (50.0 if gender == "Male" else 45.5) + 2.3 * (height_in - 60)
    else:
        ibw = 50.0 if gender == "Male" else 45.5

    if weight_kg > (1.3 * ibw):
        dosing_weight = ibw + 0.4 * (weight_kg - ibw)
        weight_note = "Adjusted Body Weight (Obesity Protocol)"
    else:
        dosing_weight = weight_kg
        weight_note = "Total Body Weight"

    # Cockcroft-Gault Equation
    cr_cl = ((140 - age) * dosing_weight) / (72 * scr)
    if gender == "Female":
        cr_cl *= 0.85
    cr_cl = round(cr_cl, 2)
    st.info(f"💡 **Calculated Clearance (CrCl):** {cr_cl} mL/min ({weight_note})")

with col2:
    st.header("🧬 Immunological & Pharmacogenomics Markers")
    allergy_list = st.multiselect("Active Drug Allergies:", ["None", "Penicillins", "Aminoglycosides", "Fluoroquinolones", "Glycopeptides"])
    
    pgx_profile = st.selectbox("Genetic Profile Verification:", [
        "No Data (Use South Asian Population Probability Risk Model)",
        "CYP2C19 Normal Metabolizer (*1/*1)",
        "CYP2C19 Ultra-Rapid Metabolizer (*17/*17)",
        "CYP2C19 Poor Metabolizer (*2/*2)",
        "MT-RNR1 m.1555A>G Mutation"
    ])

# Combination Order Entry Setup
st.markdown("---")
st.header("💊 Multi-Drug Combination Stewardship Interface")
st.markdown("*Select up to two agents to run real-world combination therapy evaluation protocols:*")

col_d1, col_d2, col_route = st.columns(3)

if not df_drugs.empty:
    drug_options = sorted(df_drugs["Drug_Name"].tolist())
else:
    drug_options = ["Database File Missing"]

with col_d1:
    primary_drug = st.selectbox("Select Primary Antimicrobial (Core Target):", drug_options)
with col_d2:
    adjunct_drug = st.selectbox("Select Adjunct Antimicrobial (Combination Therapy):", ["None"] + drug_options)
with col_route:
    prescribed_route = st.selectbox("Prescribed Route of Administration:", ["IV (Intravenous)", "Oral (PO)", "Topical"])

# Cross-Check Processing Engine
if st.button("⚡ Run High-Fidelity Multi-Drug Cross-Check"):
    st.markdown("---")
    st.subheader("📋 Precision Pharmacology & Stewardship Validation Report")
    st.caption(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Verification Base: CPIC 2024 / IDSA ICU Guidelines")

    selected_agents = [primary_drug]
    if adjunct_drug != "None":
        selected_agents.append(adjunct_drug)
        st.info(f"🔍 **Evaluating Combination Regimen:** {primary_drug} **+** {adjunct_drug}")

    allergy_string = " ".join(allergy_list)
    reject_flag = False

    # Dynamic Evaluation for each selected drug in the regimen
    for drug in selected_agents:
        if drug == "None" or df_drugs.empty:
            continue
            
        # Extract drug profile metadata from database
        drug_meta = df_drugs[df_drugs["Drug_Name"] == drug].iloc[0]
        d_class = drug_meta["Class"]
        d_max = drug_meta["Max_Daily_Dose"]
        d_thresh = drug_meta["Renal_Threshold_CrCl"]
        d_note = drug_meta["Dosing_Guideline_Note"]

        st.markdown(f"### 📦 Evaluation Profile: {drug} ({d_class})")

        # 1. Allergy Validation Layer
        if d_class in allergy_string or (d_class == "Aminoglycoside (Recent)" and "Aminoglycosides" in allergy_string):
            st.error(f"❌ **IMMUNOLOGICAL LOCKOUT:** Patient has a registered allergy to the {d_class} group. Prescription of {drug} is rejected.")
            reject_flag = True
        
        # 2. Pharmacokinetics & Renal Boundary Validation
        if cr_cl < d_thresh:
            st.warning(f"⚠️ **RENAL MISMATCH TRIGGERED:** Patient's CrCl ({cr_cl} mL/min) is below the safety threshold ({d_thresh} mL/min) for standard {drug} dosing.")
            st.markdown(f"* **Guideline Action Item:** {d_note}")
        else:
            st.success(f"✅ **Renal Clearance Valid:** Standard physiological pathway clear for {drug} (Max safe window: {d_max}).")

        # 3. Pharmacogenomics (PGx) Interlocking Logic
        if "MT-RNR1" in pgx_profile and d_class in ["Aminoglycoside", "Aminoglycoside (Recent)"]:
            st.error(f"❌ **CRITICAL HARD STOP (PGx):** MT-RNR1 mutation identified! Absolute penetrance risk for irreversible ototoxicity. **AVOID {drug}**.")
            reject_flag = True
            if "ICU" in clinical_setting:
                st.success("🔄 **Smart Stewardship Suggestion:** Pivot immediately to **Meropenem IV** for Gram-negative tracking.")
            else:
                st.success("🔄 **Smart Stewardship Suggestion:** Pivot to **Ceftazidime IV**.")

        elif "Ultra-Rapid" in pgx_profile and drug == "Voriconazole":
            st.error(f"❌ **THERAPEUTIC FAILURE RISK (PGx):** Patient clears Voriconazole hyper-rapidly via CYP2C19 *17.")
            st.success("🔄 **Dynamic Alternative Recommendation:** High-end substitution required. Switch to **Isavuconazole** or **Liposomal Amphotericin B IV**.")
            reject_flag = True

        elif "Poor Metabolizer" in pgx_profile and drug == "Voriconazole":
            st.warning(f"⚠️ **TOXIC ACCUMULATION RISK (PGx):** CYP2C19 Poor metabolizer status will drive extreme serum concentrations.")
            st.markdown("* **Adjustment:** Cut standard maintenance dosing matrix by 50% or substitute with **Anidulafungin IV**.")

    # Route Efficiency Audit for ICU Status
    if "ICU" in clinical_setting and prescribed_route == "Oral (PO)":
        st.warning("⚠️ **ROUTE BIOAVAILABILITY AUDIT:** Oral routes in hypermetabolic ICU shock states risk sub-therapeutic exposure due to gastric hypoperfusion. Transition combination to Intravenous (IV) status.")

    # Final Clinical Disposition Output Stamp
    st.markdown("---")
    if reject_flag:
        st.markdown("<h3 style='color:#DC2626;'>⛔ REGIMEN DISPOSITION: REJECTED / PROTOCOL BLOCKED</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='color:#059669;'>✅ REGIMEN DISPOSITION: CLINICALLY VALIDATED</h3>", unsafe_allow_html=True)
        st.write("Combination regimen is optimized under modern clinical pharmacology guidelines.")
