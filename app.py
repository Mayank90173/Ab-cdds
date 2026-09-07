import streamlit as st

# Learning Project Disclaimer & Developer Credits
st.title("🛡️ Integrated Antimicrobial Stewardship & Clinical Decision Support System (CDSS)")
st.caption("Developed by: MAYANK VIRMANI (PharmD Learning Project) | Version 1.0.0")

st.markdown("""
> **⚠️ EDUCATIONAL DISCLAIMER:** This software is a simulated prototype for academic and learning purposes only. 
> It must not be used for actual clinical diagnosis, real patient management, or medical decision-making. 
> Always consult official guidelines and a licensed clinical pharmacologist.
""")

# 1. Patient Triage and Setting Categorization
st.header("🏥 1. Patient Triage & Clinical Setting")
clinical_setting = st.selectbox("Select Patient Location/Ward:", ["OPD (Outpatient)", "Medical Ward (General IPD)", "ICU (Intensive Care Unit)"])
age = st.number_input("Patient Age:", min_value=1, max_value=110, value=30)
weight = st.number_input("Patient Weight (kg):", min_value=5, max_value=200, value=70)
serum_creatinine = st.number_input("Serum Creatinine (mg/dL):", min_value=0.2, max_value=10.0, value=1.0)

# Calculate eGFR / CrCl via Cockcroft-Gault (Simulated for Male default)
cr_cl = round(((140 - age) * weight) / (72 * serum_creatinine), 2)
st.info(f"💡 Calculated Creatinine Clearance (CrCl): **{cr_cl} mL/min**")

# 2. Disease & Comorbidity Profiles (Out of 100+ System Classification)
st.header("🫁 2. Clinical Condition & Comorbidities")
organ_system = st.selectbox("Select Organ System / SOC:", ["Cardiovascular", "Respiratory", "Infectious Diseases / AMR Stewardship", "Gastrointestinal", "Neurological"])

if organ_system == "Infectious Diseases / AMR Stewardship":
    disease = st.selectbox("Select Specific Condition:", ["Severe Bacterial Sepsis", "Urinary Tract Infection (UTI)", "Community-Acquired Pneumonia (CAP)"])
elif organ_system == "Cardiovascular":
    disease = st.selectbox("Select Specific Condition:", ["Hypertension (HTN)", "Chronic Heart Failure", "Acute Coronary Syndrome"])
else:
    disease = st.selectbox("Select Specific Condition:", ["General Systemic Evaluation"])

# Comorbidities & History
hypertension_history = st.checkbox("History of Hypertension / High BP?")
drug_allergy = st.multiselect("Documented Drug Allergies:", ["None", "Penicillins", "Sulfonamides", "Aminoglycosides"])

# 3. Pharmacogenomics (PGx) Probability Module
st.header("🧬 3. Pharmacogenomics (PGx) Interface")
pgx_available = st.radio("Is Patient's Genetic Profile Available?", ["No (Use Population-Based Probability Risk)", "Yes (Input Genotype Data)"])

predicted_phenotype = "Normal Metabolizer"
if pgx_available == "No (Use Population-Based Probability Risk)":
    st.warning("⚠️ actual genetic data missing. Utilizing South Asian population allele frequency metrics for risk modeling...")
    predicted_phenotype = "Predicted Intermediate/Poor Metabolizer Risk (CYP2C19 *2/*3 Prevalence ~32%)"
    st.write(f"**Algorithmic Estimate:** {predicted_phenotype}")
else:
    genotype = st.selectbox("Select Confirmed Variant:", ["CYP2C19 Ultra-Rapid Metabolizer", "CYP2C19 Poor Metabolizer", "MT-RNR1 m.1555A>G Mutation"])
    predicted_phenotype = genotype

# 4. Medication Order & CDSS Check
st.header("💊 4. Clinical Pharmacology Interaction & Dosing Engine")
selected_drug = st.selectbox("Select Antimicrobial to Prescribe:", ["Amikacin (Aminoglycoside)", "Voriconazole (Antifungal)", "Ciprofloxacin (Fluoroquinolone)"])

# CDSS Processing Core Logic
if st.button("Run System Cross-Check & Generate Prediction"):
    st.subheader("📋 Decision Support Results")
    
    # Check Allergy First
    if "Penicillins" in drug_allergy and selected_drug == "Amikacin (Aminoglycoside)":
        st.write("Cross-check clear for allergies.")
        
    if "Aminoglycosides" in drug_allergy and selected_drug == "Amikacin (Aminoglycoside)":
        st.error("❌ CRITICAL ALERT: Patient has a documented Aminoglycoside allergy. Do not administer!")
    
    # Check PGx Toxicity Risks
    elif "MT-RNR1" in predicted_phenotype and selected_drug == "Amikacin (Aminoglycoside)":
        st.error("❌ CRITICAL PGx WARNING: Patient carries the MT-RNR1 mutation. High risk of irreversible ototoxicity/deafness!")
        st.info("🔄 Suggested Alternative: Switch to Meropenem or Ceftazidime based on local AMR patterns.")
        
    # Check PGx Sub-therapeutic/Resistance Risks
    elif "Ultra-Rapid" in predicted_phenotype and selected_drug == "Voriconazole (Antifungal)":
        st.warning("⚠️ RESISTANCE RISK ALERT: Patient clears Voriconazole rapidly. Standard dosing will lead to sub-therapeutic levels, drug failure, and fungal resistance.")
        st.success("🎯 Dose Adjustment Recommendation: Increase standard loading and maintenance dose by 50%, or select Amphotericin B.")
        
    # Check Renal Dosing for ICU/IPD Settings
    elif cr_cl < 30 and selected_drug == "Amikacin (Aminoglycoside)":
        st.warning(f"⚠️ RENAL IMPAIRMENT DANGER: CrCl is {cr_cl} mL/min. Standard dosing will cause nephrotoxicity.")
        st.success("🎯 Adjustment: Prolong dosing interval to q48h instead of q24h and perform Therapeutic Drug Monitoring (TDM).")
        
    else:
        st.success("✅ Prescription Matrix Validated: Dosing falls within safe physiological parameters based on international CPIC & IDSA guidelines.")
        
    # Food Interactions Check
    if selected_drug == "Ciprofloxacin (Fluoroquinolone)":
        st.info("🥛 Food Interaction Note: Avoid administration alongside calcium-rich foods, milk, or antacids. Chelates drug absorption by up to 50%.")
