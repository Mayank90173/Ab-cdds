import streamlit as st
import datetime

# Page Configuration
st.set_page_config(page_title="Precision CDSS v2.5", layout="wide")

st.title("🛡️ Integrated Precision Antimicrobial Stewardship & CDSS")
st.caption("Developed by: MAYANK VIRMANI (PharmD Scholar) | Core Framework: CPIC & IDSA Precision Logistics with Adaptive Substitution Architecture")

st.markdown("""
> **⚠️ ACADEMIC SIMULATION DISCLAIMER:** This software is a functional prototype developed strictly for educational and learning purposes. It does NOT constitute medical advice.
""")

# Layout Setup
col_left, col_right = st.columns(2)

with col_left:
    st.header("🏥 1. Patient Clinical Metrics & Triage")
    clinical_setting = st.selectbox("Select Patient Location/Ward:", ["ICU (Intensive Care Unit)", "Medical Ward (General IPD)", "OPD (Outpatient)"])
    gender = st.selectbox("Biological Sex:", ["Male", "Female"])
    age = st.number_input("Patient Age (Years):", min_value=1, max_value=110, value=65)
    height_cm = st.number_input("Height (cm):", min_value=100, max_value=250, value=170)
    weight_kg = st.number_input("Weight (kg):", min_value=5, max_value=200, value=80)
    scr = st.number_input("Serum Creatinine (mg/dL):", min_value=0.2, max_value=10.0, value=1.4)

    # Core Pharmacokinetics: Ideal Body Weight & Adjusted Weight Logic
    height_in = height_cm / 2.54
    if height_in > 60:
        if gender == "Male":
            ibw = 50.0 + 2.3 * (height_in - 60)
        else:
            ibw = 45.5 + 2.3 * (height_in - 60)
    else:
        ibw = 50.0 if gender == "Male" else 45.5

    # Obesity Adjuster Trigger
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

    st.info(f"💡 **Calculated CrCl:** {cr_cl} mL/min ({weight_note})")

with col_right:
    st.header("🧬 2. Immunological & Genetic Layer")
    allergy_list = st.multiselect("Documented Drug Allergies:", ["None", "Penicillins", "Aminoglycosides", "Fluoroquinolones"])
    
    pgx_mode = st.radio("Genetic Profile Option:", ["Population-Based Probability (South Asian)", "Confirmed Genotype Assay"])

    predicted_phenotype = "Normal Metabolizer"
    if pgx_mode == "Population-Based Probability (South Asian)":
        st.warning("⚠️ Pre-emptive Risk Active: Localized CYP2C19 *2/*3 prevalence estimated at ~32%.")
        predicted_phenotype = "Population Risk Model"
    else:
        predicted_phenotype = st.selectbox("Select Confirmed Genotype Variant:", [
            "CYP2C19 Normal Metabolizer (*1/*1)",
            "CYP2C19 Ultra-Rapid Metabolizer (*17/*17)", 
            "CYP2C19 Poor Metabolizer (*2/*2, *2/*3)", 
            "MT-RNR1 m.1555A>G Mutation"
        ])

# Medication Order Selection
st.markdown("---")
st.header("💊 3. Medication Order Interface")
col_drug, col_route = st.columns(2)
with col_drug:
    selected_drug = st.selectbox("Select Target Antimicrobial Agent:", [
        "Amikacin (Aminoglycoside)", 
        "Voriconazole (Antifungal)", 
        "Ciprofloxacin (Fluoroquinolone)"
    ])
with col_route:
    selected_route = st.selectbox("Select Intended Route:", ["IV (Intravenous)", "Oral (PO)", "Topical"])

# Clinical Decision Execution Engine
if st.button("⚡ Execute High-Fidelity Clinical Cross-Check"):
    st.markdown("---")
    st.subheader("📋 Precision Clinical Pharmacology Evaluation Report")
    st.caption(f"Audit Trail Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Core Verification: CPIC v2024 / IDSA Guidelines")

    allergy_blocked = False
    pgx_blocked = False
    renal_adjusted = False
    best_alternative = None
    alt_route = "IV (Intravenous)" # Default for high-end ICU/IPD backups
    
    # 1. Allergy Screen
    allergy_string = " ".join(allergy_list)
    if "Aminoglycosides" in allergy_string and "Amikacin" in selected_drug:
        st.error("❌ **IMMUNOLOGICAL CRITICAL BREAK:** Patient profile lists severe allergy to Aminoglycosides. Choice rejected.")
        allergy_blocked = True
        best_alternative = "Meropenem" if "ICU" in clinical_setting else "Ceftazidime"
    elif "Fluoroquinolones" in allergy_string and "Ciprofloxacin" in selected_drug:
        st.error("❌ **IMMUNOLOGICAL CRITICAL BREAK:** Patient profile lists severe allergy to Fluoroquinolones. Choice rejected.")
        allergy_blocked = True
        best_alternative = "Ceftriaxone"
    else:
        st.success("✅ **Immunological Screen Cleared:** No class hypersensitivities flagged.")

    # 2. Pharmacogenomics (PGx) Logic
    if "MT-RNR1" in predicted_phenotype and "Amikacin" in selected_drug:
        st.error("❌ **HARD STOP — CRITICAL PGx WARNING (CPIC 2024):** Patient carries the **MT-RNR1 m.1555A>G variant**. Near 100% risk of irreversible ototoxicity (deafness). **AVOID AMIKACIN**.")
        pgx_blocked = True
        # Smart Alternative Selection based on Clinical Setting
        if "ICU" in clinical_setting:
            best_alternative = "Meropenem"
            st.info("🔄 **Adaptive Substitution Triggered:** Due to ICU Sepsis status, high-end Broad-Spectrum Carbapenem is selected to cover nosocomial pathogens.")
        else:
            best_alternative = "Ceftazidime"
            st.info("🔄 **Adaptive Substitution Triggered:** Patient is stable in General IPD/OPD, Ceftazidime (3rd Gen Cephalosporin) handles Gram-negative targets safely.")
            
    elif "Ultra-Rapid" in predicted_phenotype and "Voriconazole" in selected_drug:
        st.warning("⚠️ **PGx ALERT — THERAPEUTIC FAILURE RISK:** Patient is a **CYP2C19 Ultra-Rapid Metabolizer (*17/*17)**. Accelerated clearance leads to sub-therapeutic levels.")
        if "ICU" in clinical_setting:
            best_alternative = "Liposomal Amphotericin B"
            st.info("🔄 **Adaptive Substitution Triggered:** High-end systemic antifungal selected for hyper-acute ICU status.")
        else:
            best_alternative = "Isavuconazole"
            
    elif "Poor Metabolizer" in predicted_phenotype and "Voriconazole" in selected_drug:
        st.error("⚠️ **PGx ALERT — TOXICITY ACCUMULATION RISK:** Patient is a **CYP2C19 Poor Metabolizer (*2/*2)**. High risk of visual hallucinations and hepatotoxicity.")
        best_alternative = "Anidulafungin"

    elif "Population Risk Model" in predicted_phenotype and "Voriconazole" in selected_drug:
        st.info("💡 **Pre-emptive Insight:** Demographic features high risk of CYP2C19 variation. Standard dosing allowed, but order a steady-state trough concentration level on Day 3.")

    # 3. Pharmacokinetics / Renal Clearance Logic
    if "Amikacin" in selected_drug:
        if cr_cl < 30:
            st.error(f"❌ **CRITICAL RENAL PATHWAY MISMATCH (CrCl: {cr_cl} mL/min):** Standard q24h dosing will cause acute kidney injury. Interval must be prolonged to **every 48 hours (q48h)**.")
            renal_adjusted = True
            if "ICU" in clinical_setting and not pgx_blocked:
                st.info("💡 **Clinical Stewardship Note:** Consider switching to **Meropenem** if TDM (Therapeutic Drug Monitoring) for Amikacin is unavailable in your ICU setup.")
        elif 30 <= cr_cl <= 60:
            st.warning(f"⚠️ **MODERATE RENAL MISMATCH (CrCl: {cr_cl} mL/min):** Adjust administration interval safely to **every 36 hours (q36h)**.")
            renal_adjusted = True
            
    elif "Ciprofloxacin" in selected_drug and cr_cl < 30:
        st.warning(f"⚠️ **RENAL DOSING MODIFICATION MANDATED (CrCl: {cr_cl} mL/min):** Reduce daily dose by 50% to prevent accumulation and lowering of seizure threshold.")
        renal_adjusted = True

    # 4. Route Validation and Ancillary Drug Interactions
    st.markdown("#### 🔄 Route & Administration Safety Check")
    if "ICU" in clinical_setting and selected_route in ["Oral (PO)", "Topical"] and "Ciprofloxacin" in selected_drug:
        st.warning("⚠️ **ROUTE EFFICIENCY WARNING:** Patient is in a critical ICU setting. Oral absorption may be erratic due to gastroparesis or hypoperfusion. **Switching to IV route is highly recommended for systemic bacteremia.**")
    
    if "Ciprofloxacin" in selected_drug:
        st.warning("🥛 **CRITICAL GASTROINTESTINAL CHELATION:** Avoid PO co-administration with enteral feeds, milk products, or antacids. Chelates drug and reduces gut absorption by up to 60%. Monitor for FDA Boxed Warning risks (tendon rupture).")

    # Final Clinical Disposition & Smart Recommendation Display
    st.markdown("---")
    if allergy_blocked or pgx_blocked:
        st.markdown("<h3 style='color:#DC2626;'>⛔ FINAL STATUS: PRESCRIPTION REJECTED / LOCKED OUT</h3>", unsafe_allow_html=True)
        if best_alternative:
            st.success(f"🎯 **OPTIMAL SITUATION-BASED RECOMMENDATION:**")
            st.markdown(f"""
            * **Best Substitute Drug:** **{best_alternative}** (High-end safety matched)
            * **Recommended Route:** **{alt_route}** (Optimized for systemic bioavailability in {clinical_setting})
            * **Pharmacological Justification:** Avoids the genetic/allergic toxicity path while safely maintaining empirical coverage tailored to a CrCl of **{cr_cl} mL/min**.
            """)
    elif renal_adjusted:
        st.markdown("<h3 style='color:#D97706;'>⚠️ FINAL STATUS: MODIFIED APPROVAL / INTERVENTION REQUIRED</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='color:#059669;'>✅ FINAL STATUS: ORDER VALIDATED (CPIC & IDSA ALIGNED)</h3>", unsafe_allow_html=True)
        st.write(f"Prescription completely validated for **{selected_drug}** via **{selected_route}** route.")
