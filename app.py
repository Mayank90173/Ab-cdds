import streamlit as st

# ==========================================
# SYSTEM CORE INTEGRATION & METADATA CONFIG
# ==========================================
st.set_page_config(
    page_title="Precision CDSS Master Engine v4.0", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Deep Medical Infrastructure High-Fidelity Custom Themes
st.markdown("""
    <style>
    .main-title { font-size: 34px; font-weight: 800; color: #1E3A8A; text-align: center; margin-bottom: 2px; }
    .sub-title { font-size: 15px; color: #4B5563; text-align: center; margin-bottom: 20px; font-style: italic; }
    .section-header { font-size: 22px; font-weight: 700; color: #1E3A8A; border-bottom: 3px solid #3B82F6; padding-bottom: 5px; margin-top: 20px; }
    .model-card { background-color: #F8FAFC; padding: 18px; border-radius: 10px; border: 1px solid #CBD5E1; margin-bottom: 15px; }
    .status-block { font-size: 24px; font-weight: 800; text-align: center; padding: 15px; border-radius: 8px; margin-top: 15px; }
    /* Micro-alert layouts matching patent-ready architecture blueprints */
    .critical-box { background-color: #FEF2F2; padding: 15px; border-radius: 8px; border-left: 6px solid #DC2626; color: #991B1B; margin-bottom: 12px; }
    .warning-box { background-color: #FFFBEB; padding: 15px; border-radius: 8px; border-left: 6px solid #D97706; color: #92400E; margin-bottom: 12px; }
    .success-box { background-color: #ECFDF5; padding: 15px; border-radius: 8px; border-left: 6px solid #059669; color: #065F46; margin-bottom: 12px; }
    .info-box { background-color: #F0F9FF; padding: 15px; border-radius: 8px; border-left: 6px solid #0284C7; color: #075985; margin-bottom: 12px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ Integrated Precision Antimicrobial Stewardship Model Framework</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Lead Investigator: MAYANK VIRMANI (PharmD Scholar) | Academic CDSS Production Paradigm v4.0.0 (Patent Stable)</div>', unsafe_allow_html=True)

# Mandatory Translational Learning Core Disclaimers
with st.expander("⚠️ CORE MODEL INTELLECTUAL PROPERTY & SIMULATION PROTOCOLS", expanded=False):
    st.markdown("""
    **Translational Clinical Paradigm:** This model represents an end-to-end digital health architecture. It integrates complex multi-compartmental pharmacokinetic clearances with targeted genomic allele penetration weights. Designed strictly for educational modeling, simulations, and intellectual exploration within secondary clinical pharmacy paradigms. 
    
    *Full Process Logic Mapping, Multi-Variable Interlocking Tree & System State Architecture © Patent-Pending 2026.*
    """)

# ==========================================
# REPOSITORY KNOWLEDGE BASE: 50+ DRUGS COMPREHENSIVE REGISTRY
# ==========================================
@st.cache_data
def load_system_formulary_model():
    return {
        # 1. NEWER BL-BLI NOVEL BLOCKBUSTERS
        "Ceftazidime-Avibactam": {"class": "BL-BLI Combination", "max_dose": "7.5 g/day", "thresh": 50, "mechanism": "Inhibits Class A, C, and some D beta-lactamases", "note": "Target: KPC, OXA-48 CRE, and DTR-Pseudomonas. Dynamic renal titrations critical."},
        "Meropenem-Vaborbactam": {"class": "BL-BLI Combination", "max_dose": "12 g/day", "thresh": 40, "mechanism": "Boronic acid BLI protecting carbapenem frame", "note": "Engineered directly against Klebsiella pneumoniae carbapenemases (KPC). Titrate if CrCl < 40."},
        "Imipenem-Cilastatin-Relebactam": {"class": "BL-BLI Combination", "max_dose": "5 g/day", "thresh": 60, "mechanism": "Diazabicyclooctane BLI combination matrix", "note": "Covers MDR Gram-negative rods. Requires proactive monitoring from CrCl 15 to 60."},
        "Ceftolozane-Tazobactam": {"class": "BL-BLI Combination", "max_dose": "4.5 g/day", "thresh": 50, "mechanism": "Advanced cephalosporin with classic BLI anchor", "note": "Highly effective against complex multi-drug resistant Pseudomonas aeruginosa profiles."},
        "Piperacillin-Tazobactam": {"class": "Penicillin/BLI", "max_dose": "18 g/day", "thresh": 20, "mechanism": "Extended-spectrum penicillin + suicide inhibitor", "note": "Empiric IPD/ICU standard. High AKI correlation marker when paired with Vancomycin."},
        
        # 2. THE CARBAPENEMS (HIGH END SEPSis MONOTHERAPIES)
        "Meropenem": {"class": "Carbapenem", "max_dose": "6 g/day", "thresh": 50, "mechanism": "Binds PBP-2 and PBP-3 to halt cell-wall synthesis", "note": "ICU Severe Sepsis primary defense line. Scale down systematically if CrCl drops under 50."},
        "Imipenem-Cilastatin": {"class": "Carbapenem", "max_dose": "4 g/day", "thresh": 70, "mechanism": "Carbapenem paired with renal dehydropeptidase inhibitor", "note": "High unadjusted renal serum concentrations severely lower seizure threshold (CNS neurotoxicity)."},
        "Ertapenem": {"class": "Carbapenem", "max_dose": "1 g/day", "thresh": 30, "mechanism": "Group 1 Carbapenem with long half-life clearance", "note": "Lacks active coverage boundaries for Pseudomonas or Acinetobacter. Once daily dosing default."},
        "Doripenem": {"class": "Carbapenem", "max_dose": "3 g/day", "thresh": 50, "mechanism": "Ultra-broad carbapenem configuration", "note": "Indicated for complex intra-abdominal pathologies and nosocomial pneumonia frameworks."},
        
        # 3. HIGH TOXICITY CEILING AMINOGLYCOSIDES
        "Amikacin": {"class": "Aminoglycoside", "max_dose": "1.5 g/day", "thresh": 60, "mechanism": "Irreversibly binds 30S ribosomal subunit causing misreading", "note": "Requires extended intervals (q36h/q48h) matched with active TDM charts to mitigate AKI / Ototoxicity."},
        "Gentamicin": {"class": "Aminoglycoside", "max_dose": "Based on TDM calculations", "thresh": 60, "mechanism": "Binds 30S subunit inhibiting protein translation", "note": "Requires target peak/trough validation. Highly synergistic with Beta-Lactams for Endocarditis."},
        "Tobramycin": {"class": "Aminoglycoside", "max_dose": "Based on weight/TDM", "thresh": 60, "mechanism": "Binds 30S subunit causing cell membrane disruption", "note": "High nephrotoxic ceiling. Primary utilization via inhalation pathways for Cystic Fibrosis management."},
        "Plazomicin": {"class": "Aminoglycoside", "max_dose": "Based on PK profiles", "thresh": 60, "mechanism": "Next-gen aminoglycoside engineered against AMEs", "note": "Designed molecularly to evade common Aminoglycoside-Modifying Enzymes (AMEs). Target: cUTI."},
        
        # 4. GLYCOPEPTIDES & LIPOGLYCOPEPTIDES
        "Vancomycin": {"class": "Glycopeptide", "max_dose": "Based on AUC curves", "thresh": 50, "mechanism": "Inhibits cell wall synthesis by binding D-Ala-D-Ala terminus", "note": "Gold standard for MRSA. Maintain precise AUC/MIC ratios (400-600) via TDM troughs to avoid nephrotoxicity."},
        "Teicoplanin": {"class": "Glycopeptide", "max_dose": "1.2 g/day", "thresh": 50, "mechanism": "Glycopeptide with lipophilic side chain", "note": "Extremely long half-life profile. Reduce subsequent maintenance parameters by 50% past day 4 if clearance drops."},
        "Dalbavancin": {"class": "Lipoglycopeptide", "max_dose": "1500 mg/course", "thresh": 30, "note": "Two-week biological half-life. Ideal for ambulatory care transitions. Lower dose by 25% if CrCl < 30."},
        "Oritavancin": {"class": "Lipoglycopeptide", "max_dose": "1200 mg single dose", "thresh": 0, "note": "Single-dose absolute protocol. No adjustments needed. Caution: causes artificial laboratory aPTT prolongation."},
        
        # 5. CYCLIC LIPOPEPTIDES & OXAZOLIDINONES
        "Linezolid": {"class": "Oxazolidinone", "max_dose": "1.2 g/day", "thresh": 0, "note": "No renal adjustments. Track baseline CBC for severe myelosuppression/thrombocytopenia if used past 14 days."},
        "Tedizolid": {"class": "Oxazolidinone", "max_dose": "200 mg/day", "thresh": 0, "note": "Once-daily highly bioavailable strategy. Displays structural optimization minimizing myelosuppression."},
        "Daptomycin": {"class": "Lipopeptide", "max_dose": "12 mg/kg/day", "thresh": 30, "note": "Inactivated by surfactant (Do NOT use in Pneumonia). Extend intervals to q48h if CrCl < 30. Track weekly CPK."},
        
        # 6. POLYMYXINS & BACKUPS
        "Polymyxin B": {"class": "Polymyxin", "max_dose": "Weight-optimized bounds", "thresh": 0, "note": "Eliminated via non-renal pathways. Preferred over Colistin to mitigate Acute Kidney Injury profiles in MDR Gram-negatives."},
        "Colistin (CMS)": {"class": "Polymyxin", "max_dose": "9 million IU loading", "thresh": 50, "note": "Administered as an inactive prodrug. Highly volatile clearance profiles require rigorous continuous calculations."},
        "Tigecycline": {"class": "Tetracycline", "max_dose": "100 mg/day", "thresh": 0, "note": "Massive volume of tissue distribution leads to low serum values. Avoid in primary bacteremias."},
        "Eravacycline": {"class": "Tetracycline", "max_dose": "Weight tracking defaults", "thresh": 0, "note": "Engineered to bypass standard ribosomal protection efflux mechanics in intra-abdominal settings."},
        "Omadacycline": {"class": "Tetracycline", "max_dose": "300 mg daily oral", "thresh": 0, "note": "Once-daily profile with excellent lung tissue clearance configurations. No renal titration required."},
        
        # 7. ADVANCED CEPHALOSPORINS
        "Ceftriaxone": {"class": "Cephalosporin", "max_dose": "4 g/day", "thresh": 0, "note": "Dual biliary/renal clearance. No routine titration needed. Contraindicated in neonates due to biliary sludge hazards."},
        "Ceftazidime": {"class": "Cephalosporin", "max_dose": "6 g/day", "thresh": 50, "note": "Anti-pseudomonal coverage. Requires systematic titration to prevent neurotoxic/encephalopathy events."},
