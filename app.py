import streamlit as st
import datetime

# Page Configuration for High-Tier Display
st.set_page_config(page_title="Precision CDSS Pro v3.5", layout="wide", initial_sidebar_state="expanded")

# Inject Custom Medical Theme Styling via CSS
st.markdown("""
    <style>
    .main-title { font-size: 34px; font-weight: 800; color: #1E3A8A; text-align: center; margin-bottom: 2px; }
    .sub-title { font-size: 16px; color: #4B5563; text-align: center; margin-bottom: 25px; font-style: italic; }
    .section-header { font-size: 22px; font-weight: 700; color: #1E3A8A; border-bottom: 2px solid #E5E7EB; padding-bottom: 5px; margin-top: 20px; }
    .metric-box { background-color: #F8FAFC; padding: 15px; border-radius: 10px; border: 1px solid #E2E8F0; text-align: center; }
    .card-critical { background-color: #FEF2F2; padding: 20px; border-radius: 8px; border-left: 6px solid #DC2626; margin-bottom: 15px; }
    .card-warning { background-color: #FFFBEB; padding: 20px; border-radius: 8px; border-left: 6px solid #D97706; margin-bottom: 15px; }
    .card-success { background-color: #ECFDF5; padding: 20px; border-radius: 8px; border-left: 6px solid #059669; margin-bottom: 15px; }
    .card-info { background-color: #F0F9FF; padding: 20px; border-radius: 8px; border-left: 6px solid #0284C7; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ Translational Precision Antimicrobial Stewardship & CDSS</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Lead Investigator: MAYANK VIRMANI (PharmD Scholar) | Core Protocol Framework v3.5.0 (Patent-Pending Architecture)</div>', unsafe_allow_html=True)

# Embedded 50+ Modern Clinical Antimicrobials Knowledge Engine
@st.cache_data
def get_comprehensive_database():
    return {
        "Ceftazidime-Avibactam": {"class": "Beta-Lactam/BLI Combination (Recent)", "max_dose": "7.5 g/day", "thresh": 50, "note": "Target: Carbapenem-Resistant Enterobacteriaceae (CRE) & DTR-Pseudomonas. Dynamic renal titrations critical."},
        "Meropenem-Vaborbactam": {"class": "Beta-Lactam/BLI Combination (Recent)", "max_dose": "12 g/day", "thresh": 40, "note": "Engineered against KPC-producing organisms. Downward titration mandated if CrCl < 40 mL/min."},
        "Imipenem-Cilastatin-Relebactam": {"class": "Beta-Lactam/BLI Combination (Recent)", "max_dose": "5 g/day", "thresh": 60, "note": "Covers multi-drug resistant Gram-negative rods. Requires proactive monitoring from CrCl 15 to 60."},
        "Ceftolozane-Tazobactam": {"class": "Beta-Lactam/BLI Combination (Recent)", "max_dose": "4.5 g/day", "thresh": 50, "note": "Highly effective against complex multi-drug resistant Pseudomonas aeruginosa profiles."},
        "Piperacillin-Tazobactam": {"class": "Extended Penicillin / BLI Backbone", "max_dose": "18 g/day", "thresh": 20, "note": "Empiric ICU standard. Monitor for high Acute Kidney Injury (AKI) correlation when paired with Vancomycin."},
        "Meropenem": {"class": "High-End Carbapenem", "max_dose": "6 g/day", "thresh": 50, "note": "ICU Severe Sepsis primary defense line. Scale down systematically if CrCl drops under 50 mL/min."},
        "Imipenem-Cilastatin": {"class": "High-End Carbapenem", "max_dose": "4 g/day", "thresh": 70, "note": "High serum concentrations in unadjusted renal impairment significantly lower seizure threshold (CNS toxicity)."},
        "Ertapenem": {"class": "Group 1 Carbapenem", "max_dose": "1 g/day", "thresh": 30, "note": "Lacks active coverage boundaries for Pseudomonas or Acinetobacter. Adjust maintenance if CrCl < 30."},
        "Doripenem": {"class": "High-End Carbapenem", "max_dose": "3 g/day", "thresh": 50, "note": "Indicated for complex intra-abdominal pathologies and nosocomial pneumonia frameworks."},
        "Amikacin": {"class": "Aminoglycoside Architecture", "max_dose": "1.5 g/day", "thresh": 60, "note": "High toxicity risks. Requires broad dosing interval extensions (q36h/q48h) matched with active baseline TDM charts."},
        "Gentamicin": {"class": "Aminoglycoside Architecture", "max_dose": "Based on TDM calculations", "thresh": 60, "note": "Requires target peak/trough validation. Highly synergistic with Beta-Lactams for Endocarditis."},
        "Tobramycin": {"class": "Aminoglycoside Architecture", "max_dose": "Based on weight/TDM", "thresh": 60, "note": "High nephrotoxic ceiling. Primary utilization via inhalation pathways for Cystic Fibrosis management."},
        "Plazomicin": {"class": "Next-Gen Aminoglycoside (Recent)", "max_dose": "Based on PK profiles", "thresh": 60, "note": "Designed molecularly to evade common Aminoglycoside-Modifying Enzymes (AMEs)."},
        "Vancomycin": {"class": "Glycopeptide Class", "max_dose": "Based on continuous AUC calculations", "thresh": 50, "note": "Gold standard for MRSA. Maintain precise AUC/MIC ratios (400-600) via TDM troughs to avoid nephrotoxicity."},
        "Teicoplanin": {"class": "Glycopeptide Class", "max_dose": "1.2 g/day", "thresh": 50, "note": "Extremely long half-life profile. Reduce subsequent maintenance parameters by 50% past day 4 if clearance drops."},
        "Dalbavancin": {"class": "Lipoglycopeptide Complex (Recent)", "max_dose": "1500 mg/course", "thresh": 30, "note": "Two-week biological half-life. Ideal for ambulatory care transitions. Lower dose by 25% if CrCl < 30."},
        "Oritavancin": {"class": "Lipoglycopeptide Complex (Recent)", "max_dose": "1200 mg single dose", "thresh": 0, "note": "Single-dose absolute protocol. No adjustments needed. Caution: causes artificial laboratory aPTT prolongation."},
        "Linezolid": {"class": "Oxazolidinone Class", "max_dose": "1.2 g/day", "thresh": 0, "note": "No renal adjustments. Track baseline CBC for severe myelosuppression/thrombocytopenia if used past 14 days."},
        "Tedizolid": {"class": "Next-Gen Oxazolidinone (Recent)", "max_dose": "200 mg/day", "thresh": 0, "note": "Once-daily highly bioavailable strategy. Displays structural optimization minimizing myelosuppression."},
        "Daptomycin": {"class": "Cyclic Lipopeptide Class", "max_dose": "12 mg/kg/day", "thresh": 30, "note": "Inactivated by surfactant (Do NOT use in Pneumonia). Extend intervals to q48h if CrCl < 30. Track weekly CPK."},
        "Polymyxin B": {"class": "Polymyxin System", "max_dose": "Based on weight metrics", "thresh": 0, "note": "Eliminated via non-renal pathways. Preferred over Colistin to mitigate Acute Kidney Injury profiles in MDR Gram-negatives."},
        "Colistin (CMS)": {"class": "Polymyxin System", "max_dose": "9 million IU loading baseline", "thresh": 50, "note": "Administered as an inactive prodrug. Highly volatile clearance profiles require rigorous continuous calculations."},
        "Ceftriaxone": {"class": "3rd Gen Cephalosporin", "max_dose": "4 g/day", "thresh": 0, "note": "Dual biliary/renal clearance. No routine titration needed. Contraindicated in neonates due to biliary sludge hazards."},
        "Ceftazidime": {"class": "3rd Gen Cephalosporin", "max_dose": "6 g/day", "thresh": 50, "note": "Anti-pseudomonal coverage. Requires systematic titration to prevent neurotoxic/encephalopathy events."},
        "Cefepime": {"class": "4th Gen Cephalosporin", "max_dose": "6 g/day", "thresh": 50, "note": "High-risk correlation with Cefepime-Induced Encephalopathy (NCSE) if renal clearance parameters drop unadjusted."},
        "Ceftaroline": {"class": "Advanced Gen MRSA Cephalosporin", "max_dose": "1.2 g/day", "thresh": 50, "note": "The only beta-lactam displaying advanced binding affinity for MRSA PBP2a targets."},
        "Cefiderocol": {"class": "Siderophore Cephalosporin (Recent)", "max_dose": "6 g/day", "thresh": 60, "note": "Trojan-horse iron transport binding mechanism. Requires dynamic updates for both failure and augmented renal states."},
        "Voriconazole": {"class": "Triazole Antifungal Architecture", "max_dose": "Based on trough testing", "thresh": 50, "note": "IV vehicle (SBECD) accumulates during renal failure. Pivot immediately to Oral (PO) route if CrCl < 50."},
        "Isavuconazole": {"class": "Triazole Antifungal Architecture (Recent)", "max_dose": "200 mg/day maintenance", "thresh": 0, "note": "Predictable pharmacokinetic architecture. Shortens QTc intervals. Safe across complex renal clearances."},
        "Posaconazole": {"class": "Triazole Antifungal Architecture", "max_dose": "600 mg/day", "thresh": 50, "note": "IV formulation vehicle accumulates during renal drop-offs. Transition to targeted oral options."},
        "Fluconazole": {"class": "Triazole Antifungal Architecture", "max_dose": "800 mg/day", "thresh": 50, "note": "Highly water soluble with excellent urinary penetration. Reduce maintenance by 50% if CrCl < 50."},
        "Liposomal Amphotericin B": {"class": "Polyene Antifungal Matrix", "max_dose": "10 mg/kg/day", "thresh": 0, "note": "Broadest spectrum choice. Significantly lower nephrotoxicity ceiling than standard deoxycholate models."},
        "Caspofungin": {"class": "Echinocandin Architecture", "max_dose": "70 mg loading threshold", "thresh": 0, "note": "Inhibits 1,3-beta-D-glucan wall synthesis. Reduce maintenance parameters if Child-Pugh score is severe."},
        "Micafungin": {"class": "Echinocandin Architecture", "max_dose": "150 mg/day", "thresh": 0, "note": "Metabolized hepatically. Demonstrates an excellent safety index in acute renal failure models."},
        "Anidulafungin": {"class": "Echinocandin Architecture", "max_dose": "100 mg/day maintenance", "thresh": 0, "note": "Undergoes spontaneous non-enzymatic degradation in blood. The safest antifungal in mixed hepatic/renal crashes."},
        "Ciprofloxacin": {"class": "Fluoroquinolone System", "max_dose": "1.2 g/day (IV)", "thresh": 30, "note": "Cut dose by 50% if CrCl < 30. High risk for multi-valent cation chelation via oral pathways."},
