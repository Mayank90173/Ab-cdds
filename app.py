import streamlit as st
import datetime

# Page Configurations
st.set_page_config(page_title="Precision CDSS Pro v3.0", layout="wide")

st.markdown('<h1 style="color:#1E3A8A;">🛡️ Enterprise-Grade Precision Antimicrobial Stewardship CDSS</h1>', unsafe_allow_html=True)
st.caption("Developed by: MAYANK VIRMANI (PharmD Scholar) | Multi-Drug Combination Logic Framework")

# 50+ CLINICAL ANTIMICROBIAL FORMULARY EMBEDDED IN CODE (NO EXTERNAL FILE NEEDED)
@st.cache_data
def get_embedded_db():
    return {
        "Ceftazidime-Avibactam": {"class": "Beta-Lactam/BLI (Recent)", "max_dose": "7.5 g/day", "thresh": 50, "note": "Highly dynamic renal scaling required for CRE coverage."},
        "Meropenem-Vaborbactam": {"class": "Beta-Lactam/BLI (Recent)", "max_dose": "12 g/day", "thresh": 40, "note": "Reduce dose if CrCl < 40 ml/min."},
        "Imipenem-Cilastatin-Relebactam": {"class": "Beta-Lactam/BLI (Recent)", "max_dose": "5 g/day", "thresh": 90, "note": "Requires precise renal tracking from CrCl 15 to 90."},
        "Ceftolozane-Tazobactam": {"class": "Beta-Lactam/BLI (Recent)", "max_dose": "4.5 g/day", "thresh": 50, "note": "Adjust for renal clearance; essential for MDR Pseudomonas."},
        "Piperacillin-Tazobactam": {"class": "Beta-Lactam/BLI", "max_dose": "16 g/day", "thresh": 40, "note": "Reduce dose to 2.25g q6h or q8h if CrCl < 20."},
        "Meropenem": {"class": "Carbapenem", "max_dose": "6 g/day", "thresh": 50, "note": "ICU Sepsis default. Reduce to 1g q12h if CrCl 25-50."},
        "Imipenem": {"class": "Carbapenem", "max_dose": "4 g/day", "thresh": 70, "note": "High dose in renal failure risks CNS toxicity/seizures."},
        "Ertapenem": {"class": "Carbapenem", "max_dose": "1 g/day", "thresh": 30, "note": "Once daily dosing. Reduce to 500mg if CrCl < 30."},
        "Doripenem": {"class": "Carbapenem", "max_dose": "3 g/day", "thresh": 50, "note": "Reduce to 250mg q8h if CrCl 30-50."},
        "Amikacin": {"class": "Aminoglycoside", "max_dose": "15 mg/kg/day", "thresh": 30, "note": "Prolong interval to q48h if CrCl < 30. Check TDM troughs."},
        "Gentamicin": {"class": "Aminoglycoside", "max_dose": "5 mg/kg/day", "thresh": 30, "note": "Prolong interval to q36h or q48h if CrCl < 30."},
        "Tobramycin": {"class": "Aminoglycoside", "max_dose": "5 mg/kg/day", "thresh": 30, "note": "Requires aggressive TDM. High nephrotoxicity risk."},
        "Plazomicin": {"class": "Aminoglycoside (Recent)", "max_dose": "15 mg/kg/day", "thresh": 60, "note": "Next-gen aminoglycoside. Reduce dose if CrCl < 60."},
        "Vancomycin": {"class": "Glycopeptide", "max_dose": "4 g/day", "thresh": 50, "note": "Mandatory AUC/MIC TDM. Target trough 15-20 mcg/mL in severe infections."},
        "Teicoplanin": {"class": "Glycopeptide", "max_dose": "12 mg/kg/q12h", "thresh": 40, "note": "Maintenance dose cut by 50% after day 4 if renal crash."},
        "Telavancin": {"class": "Glycopeptide", "max_dose": "10 mg/kg/day", "thresh": 50, "note": "Black box warning for nephrotoxicity. Avoid if possible."},
        "Dalbavancin": {"class": "Glycopeptide", "max_dose": "1500 mg/dose", "thresh": 30, "note": "Single or two-dose long acting regimen. Reduce dose by 25% if CrCl < 30."},
        "Oritavancin": {"class": "Glycopeptide", "max_dose": "1200 mg/dose", "thresh": 0, "note": "Single dose regimen. No adjustment for mild/moderate renal impairment."},
        "Linezolid": {"class": "Oxazolidinone", "max_dose": "1200 mg/day", "thresh": 0, "note": "No renal adjustment. Monitor CBC for thrombocytopenia if >14 days."},
        "Tedizolid": {"class": "Oxazolidinone", "max_dose": "200 mg/day", "thresh": 0, "note": "Once daily. No renal or hepatic adjustment required."},
        "Daptomycin": {"class": "Lipopeptide", "max_dose": "12 mg/kg/day", "thresh": 30, "note": "Monitor CPK levels weekly. Prolong interval to q48h if CrCl < 30."},
        "Colistin": {"class": "Polymyxin", "max_dose": "300 mg CBA/day", "thresh": 80, "note": "Highly nephrotoxic. Requires strict loading dose and modified maintenance."},
        "Polymyxin B": {"class": "Polymyxin", "max_dose": "25000 units/kg/day", "thresh": 0, "note": "Cleared non-renally. Preferred over Colistin to avoid AKI."},
        "Ceftriaxone": {"class": "Cephalosporin", "max_dose": "4 g/day", "thresh": 10, "note": "No routine renal adjustment needed until severe end-stage."},
        "Ceftazidime": {"class": "Cephalosporin", "max_dose": "6 g/day", "thresh": 50, "note": "Reduce dose significantly if CrCl < 50 to avoid neurotoxicity."},
        "Cefepime": {"class": "Cephalosporin", "max_dose": "6 g/day", "thresh": 60, "note": "High risk of Cefepime-induced encephalopathy if non-adjusted."},
        "Ceftaroline": {"class": "Cephalosporin", "max_dose": "1200 mg/day", "thresh": 50, "note": "MRSA active cephalosporin. Reduce dose if CrCl < 50."},
        "Cefiderocol": {"class": "Cephalosporin", "max_dose": "6 g/day", "thresh": 60, "note": "Siderophore mechanism. Adjust for augmented renal clearance too."},
        "Voriconazole": {"class": "Triazole Antifungal", "max_dose": "8 mg/kg/q12h", "thresh": 50, "note": "IV vehicle (SBECD) accumulates if CrCl < 50. Switch to Oral PO."},
        "Isavuconazole": {"class": "Triazole Antifungal", "max_dose": "200 mg/q8h", "thresh": 0, "note": "No renal adjustment. Predictable kinetics."},
        "Posaconazole": {"class": "Triazole Antifungal", "max_dose": "600 mg/day", "thresh": 50, "note": "IV vehicle accumulates if CrCl < 50. Switch to Oral tablets."},
        "Fluconazole": {"class": "Triazole Antifungal", "max_dose": "800 mg/day", "thresh": 50, "note": "Reduce maintenance dose by 50% if CrCl < 50."},
        "Liposomal Amphotericin B": {"class": "Polyene Antifungal", "max_dose": "5 mg/kg/day", "thresh": 0, "note": "Significantly lower nephrotoxicity than deoxycholate."},
        "Caspofungin": {"class": "Echinocandin", "max_dose": "70 mg/day", "thresh": 0, "note": "Reduce dose to 35mg if moderate/severe hepatic impairment exists."},
        "Micafungin": {"class": "Echinocandin", "max_dose": "150 mg/day", "thresh": 0, "note": "Metabolized hepatically. No adjustment required for renal clearance."},
        "Anidulafungin": {"class": "Echinocandin", "max_dose": "100 mg/day", "thresh": 0, "note": "Spontaneous degradation. Safest antifungal in renal failure."},
        "Ciprofloxacin": {"class": "Fluoroquinolone", "max_dose": "1200 mg/day", "thresh": 30, "note": "Reduce PO/IV dose by 50% if CrCl < 30. Cation chelation risk."},
        "Levofloxacin": {"class": "Fluoroquinolone", "max_dose": "750 mg/day", "thresh": 50, "note": "Requires major adjustments. e.g. 750mg q48h if CrCl < 20."},
        "Moxifloxacin": {"class": "Fluoroquinolone", "max_dose": "400 mg/day", "thresh": 0, "note": "Hepatically cleared. No renal adjustment required."},
        "Tigecycline": {"class": "Tetracycline", "max_dose": "100 mg/day", "thresh": 0, "note": "Broad spectrum but black box warning for increased mortality."},
        "Eravacycline": {"class": "Tetracycline", "max_dose": "2 mg/kg/day", "thresh": 0, "note": "Next-gen tetracycline for cIAI. No renal adjustments."},
        "Omadacycline": {"class": "Tetracycline", "max_dose": "100 mg/day", "thresh": 0, "note": "No renal adjustment needed for CABP or ABSSSI."},
        "Azithromycin": {"class": "Macrolide", "max_dose": "500 mg/day", "thresh": 0, "note": "Hepatic elimination. No renal adjustments required."},
        "Clarithromycin": {"class": "Macrolide", "max_dose": "1000 mg/day", "thresh": 30, "note": "Reduce dose by 50% if CrCl < 30."},
        "Clindamycin": {"class": "Lincosamide", "max_dose": "2700 mg/day", "thresh": 0, "note": "Excellent tissue penetration. No renal dose changes needed."},
        "Metronidazole": {"class": "Nitroimidazole", "max_dose": "1500 mg/day", "thresh": 10, "note": "Anaerobic target default. Minimal renal adjustment required."},
        "Fosfomycin": {"class": "Phosphonic Acid", "max_dose": "24 g/day", "thresh": 40, "note": "IV formulation requires massive dose restructuring in renal failure."},
        "Nitrofurantoin": {"class": "Nitrofuran", "max_dose": "400 mg/day", "thresh": 30, "note": "Contraindicated if CrCl < 30 due to lack of therapeutic urinary concentration."},
        "Trimethoprim-Sulfamethoxazole": {"class": "Sulfonamide", "max_dose": "20 mg/kg/day", "thresh": 30, "note": "Reduce dose by 50% if CrCl 15-30. High hyperkalemia risk."},
        "Aztreonam": {"class": "Monobactam", "max_dose": "8 g/day", "thresh": 30, "note": "Safe for penicillin allergic patients. Reduce dose by 50% if CrCl < 30."},
        "Luluiconazole": {"class": "Imidazole Topical", "max_dose": "Topical application bound", "thresh": 0, "note": "No systemic dosage adjustment required due to negligible absorption."}
    }

db = get_embedded_db()

# Patient Metrics Setup
col1, col2 = st.columns(2)
with col1:
    st.header("🏥 Patient Demographics")
    clinical_setting = st.selectbox("Clinical Environment:", ["ICU (Intensive Care)", "Medical Wards (IPD)", "OPD (Outpatient)"])
    gender = st.selectbox("Biological Sex:", ["Male", "Female"])
    age = st.number_input("Age (Years):", min_value=1, max_value=110, value=65)
    height_cm = st.number_input("Height (cm):", min_value=100, max_value=250, value=170)
    weight_kg = st.number_input("Weight (kg):", min_value=5, max_value=250, value=85)
    scr = st.number_input("Serum Creatinine (mg/dL):", min_value=0.2, max_value=10.0, value=1.6)

    # Ideal Body Weight and Dosing Weight calculations
    height_in = height_cm / 2.54
    ibw = (50.0 if gender == "Male" else 45.5) + (2.3 * (height_in - 60) if height_in > 60 else 0)
    dosing_weight = ibw + 0.4 * (weight_kg - ibw) if weight_kg > (1.3 * ibw) else weight_kg
    cr_cl = round((((140 - age) * dosing_weight) / (72 * scr)) * (0.85 if gender == "Female" else 1.0), 2)
    st.info(f"💡 **Calculated Clearance (CrCl):** {cr_cl} mL/min")

with col2:
    st.header("🧬 Immunological & PGx Markers")
