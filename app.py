import streamlit as st
import datetime

# ==========================================
# PAGE CONFIGURATION & THEME STYLING
# ==========================================
st.set_page_config(
    page_title="Precision Stewardship CDSS v2.0", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom Styling for Medical Interface
st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    .sub-title { font-size: 16px; color: #4B5563; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ Integrated Precision Antimicrobial Stewardship & Clinical Decision Support System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title"><b>Lead Investigator:</b> MAYANK VIRMANI (PharmD Scholar) | <b>Core Framework:</b> Translational Pharmacogenomics & Pharmacokinetics Engine (v2.0.0)</div>', unsafe_allow_html=True)

# Formal Academic & Legal Boundary Disclaimers
with st.expander("⚠️ MANDATORY ACADEMIC DISCLAIMER & INTELLECTUAL PROPERTY NOTICE", expanded=False):
    st.markdown("""
    **Educational Simulation Prototype Only:** This platform is engineered strictly as an educational learning framework and clinical architecture simulation. It does **not** constitute medical advice, real-world diagnosis, or active prescription authorization. Clinical teams must defer to verified local institutional antibiograms, active **CPIC/DPWG** consensus statements, and direct specialist consultation. 
    
    *Patent-Pending Architectural Logic Framework © 2026. All Rights Reserved.*
    """)

# ==========================================
# SIDEBAR: ADVANCED PHARMACOKINETICS (PK) CALCULATION ENGINE
# ==========================================
st.sidebar.header("🏥 Patient Demographics & Physiometrics")
biological_sex = st.sidebar.selectbox("Biological Sex:", ["Male", "Female"])
age_yrs = st.sidebar.number_input("Patient Age (Years):", min_value=1, max_value=115, value=65)
height_cm = st.sidebar.number_input("Patient Height (cm):", min_value=100, max_value=250, value=172)
weight_kg = st.sidebar.number_input("Total Body Weight (TBW) (kg):", min_value=10.0, max_value=250.0, value=88.0)
scr_mg_dl = st.sidebar.number_input("Serum Creatinine (S_cr) (mg/dL):", min_value=0.2, max_value=12.0, value=1.5, step=0.1)

# Advanced Pharmacokinetic Weight Stratification Logic (Crucial for Obese ICU Settings)
# Ideal Body Weight (IBW) via Devine Formula (1974)
height_in_inches = height_cm / 2.54
if height_in_inches > 60:
    inches_above_60 = height_in_inches - 60
    if biological_sex == "Male":
        ibw = 50.0 + (2.3 * inches_above_60)
    else:
        ibw = 45.5 + (2.3 * inches_above_60)
else:
    if biological_sex == "Male":
        ibw = 50.0
    else:
        ibw = 45.5

# Body Mass Index (BMI) & Obesity Trigger Check (>30% of IBW requires Adjusted Body Weight)
bmi = weight_kg / ((height_cm / 100) ** 2)
is_obese = weight_kg > (1.3 * ibw)

if is_obese:
    # Adjusted Body Weight (ABW) with a 0.4 correction factor
    dosing_weight = ibw + 0.4 * (weight_kg - ibw)
    weight_protocol = "Adjusted Body Weight (Obesity Pharmacokinetic Protocol Active)"
else:
    dosing_weight = weight_kg
    weight_protocol = "Total Body Weight (Standard Kinetics)"

# Cockcroft-Gault Equation Execution (1976)
cr_cl_base = ((140 - age_yrs) * dosing_weight) / (72 * scr_mg_dl)
if biological_sex == "Female":
    cr_cl_base *= 0.85
cr_cl = round(cr_cl_base, 2)

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Dynamic Renal Clearance Metrics")
st.sidebar.metric(label="Calculated Creatinine Clearance (CrCl)", value=f"{cr_cl} mL/min")
st.sidebar.caption(f"**Selected Weight Variant:** {weight_protocol}")
st.sidebar.caption(f"**Computed Patient BMI:** {round(bmi, 2)} kg/m²")

# ==========================================
# MAIN INTERFACE: PATIENT PROFILE GENERATION
# ==========================================
layout_col1, layout_col2 = st.columns(2)

with layout_col1:
    st.header("📌 1. Clinical Environment & Acuity Triage")
    clinical_setting = st.selectbox("Clinical Location / Patient Acuity Status:", [
        "ICU (Intensive Care Unit) - Hyper-Acute Hypermetabolic Protocol",
        "Medical Ward (General IPD) - Standard Clearance Monitoring",
        "OPD (Outpatient Department) - Ambulatory & Adherence Screening"
    ])
    
    organ_system = st.selectbox("System Organ Class (SOC) Pathology Type:", [
        "Infectious Diseases / AMR Stewardship Core",
        "Cardiovascular / Hemodynamic Compromise",
        "Gastrointestinal / Hepatic Elimination Shift"
    ])
    
    if "Infectious Diseases" in organ_system:
        clinical_indication = st.selectbox("Presumptive or Confirmed Target Diagnosis:", [
            "Severe Bacterial Sepsis / Septic Shock (Empiric Protocol)",
            "Urinary Tract Infection (UTI) with Secondary Bacteremia Risk",
            "Nosocomial / Community-Acquired Pneumonia (CAP)"
        ])
    else:
        clinical_indication = st.selectbox("Presumptive Diagnosis:", ["General Systemic Pathogen Secondary Prophylaxis"])

with layout_col2:
    st.header("🧬 2. Translational Pharmacogenomics (PGx)")
    immunological_history = st.multiselect("Documented Immunological Allergen Violations:", [
        "None / NKDA (No Known Drug Allergies)",
        "Penicillins (Beta-Lactam Cross-Sensitivity Class)",
        "Sulfonamides / Cotrimoxazole Reactions",
        "Aminoglycosides (Direct Nephro/Ototoxic Class Hypersensitivity)",
        "Fluoroquinolones (Tendinopathy/Hypersensitivity Markers)"
    ])
    
    pgx_stratification_mode = st.radio(
        "Genotypic Data Acquisition Method at Point-of-Care:",
        ["Deploy Population-Based Probability Risk Models", "Input Patient-Specific Verified Genotypic Assay Data"]
    )

    assigned_phenotype = "Normal Metabolizer"
    if pgx_stratification_mode == "Deploy Population-Based Probability Risk Models":
        st.warning("⚠️ **Pre-Emptive Machine Alert:** Direct DNA sequencing absent. Triggering localized South Asian population allele frequency metrics.")
        assigned_phenotype = "Probabilistic Risk Model: High-Risk Genotype Spectrum (CYP2C19 *2/*3 Loss-of-Function Allele Prevalence ~32% in Target Geographic Cluster)"
        st.markdown(f"**Algorithmic Estimate Assessment:** *{assigned_phenotype}*")
    else:
        molecular_genotype = st.selectbox("Verified Patient Genotype Blueprint (CPIC / PharmGKB Standardized):", [
            "CYP2C19 *1/*1 (Normal Drug Clearance Kinetics Phenotype)",
            "CYP2C19 *17/*17 (Ultra-Rapid Clearance Variant Profile)",
            "CYP2C19 *2/*2 or *2/*3 (Poor Drug Clearance / Metabolic Shutdown Variant)",
            "MT-RNR1 m.1555A>G Homoplasmic Mutation (High-Penetrance Toxicity Variant)"
        ])
        assigned_phenotype = molecular_genotype

# ==========================================
# PRESCRIPTION ENTRY LAYER
# ==========================================
st.markdown("---")
st.header("💊 3. Medication Order Interface")
selected_therapeutic_agent = st.selectbox("Target Antimicrobial Substance for Validation:", [
    "Amikacin (Aminoglycoside Protocol - High Toxicity Ceiling)",
    "Voriconazole (Triazole Antifungal Protocol - CYP Dependent)",
    "Ciprofloxacin (Fluoroquinolone Protocol - Cation Vulnerable)"
])

# ==========================================
# ADVANCED LOGIC PROCESSING & AUDIT GENERATION
# ==========================================
if st.button("⚡ Run High-Fidelity Cross-Check & Generate Audit Trail"):
    st.markdown("---")
    st.markdown("### 📋 Clinical Pharmacology Validation Audit & Executive Summary")
    st.caption(f"**System Systemic Timestamp:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | **Core Logic Protocols:** CPIC Guidelines v2024 / IDSA Sepsis Mandates / FDA Boxed Warning Matrix")
    
    # State Flag Initialization
    allergy_breach = False
    pgx_breach_critical = False
    renal_intervention_required = False
    
    # ------------------------------------------
    # BLOCK A: SYSTEMIC IMMUNOLOGICAL SCREEN
    # ------------------------------------------
    st.markdown("#### 🛑 1. Immunological Safety / Allergy Screening Layer")
    
    # Convert list elements to string to verify safely
    allergy_str = " ".join(immunological_history)
    
    if "Aminoglycosides" in allergy_str and "Amikacin" in selected_therapeutic_agent:
        st.error("❌ **CRITICAL ALLERGY BREAK:** Absolute Contraindication. Patient profile indicates an active, severe Type I or Type IV hyper-reactivity to the Aminoglycoside class.")
        st.caption("**Compendia Anchor:** *ISMP National Medication Error Warnings / FDA Approved Package Insert Labeling*")
        allergy_breach = True
    elif "Fluoroquinolones" in allergy_str and "Ciprofloxacin" in selected_therapeutic_agent:
        st.error("❌ **CRITICAL ALLERGY BREAK:** Absolute Contraindication. Patient profile indicates cross-sensitivity markers to the Fluoroquinolone class.")
        allergy_breach = True
    else:
        st.success("✅ **Immunological Screen Cleared:** No direct immunoglobulin-mediated or secondary delayed hypersensitivity signals matched the target compound.")

    # ------------------------------------------
    # BLOCK B: PHARMACOGENOMICS (PGx) SCREEN
    # ------------------------------------------
    st.markdown("#### 🧬 2. Translational Pharmacogenomics (PGx) Risk Boundary Matrix")
    
    if "MT-RNR1" in assigned_phenotype and "Amikacin" in selected_therapeutic_agent:
        st.error("❌ **HARD CLINICAL STOP — METABOLIC TOXICITY THREAT DETECTED:**")
        st.markdown("""
