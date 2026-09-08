# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import io
from datetime import datetime

# ==============================================================================
# PRECISION CDSS MASTER PRODUCTION MODEL v22.0 (PORTFOLIO PRO VERSION - FIXED)
# ==============================================================================
st.set_page_config(page_title="Precision CDSS Pro v22.0", layout="wide")

# Custom Medical CSS Theme for High-Performance Clinical Dashboards
st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: 800; color: #1E3A8A; text-align: center; margin-bottom: 2px; }
    .sub-title { font-size: 15px; color: #4B5563; text-align: center; margin-bottom: 20px; font-style: italic; }
    .section-header { font-size: 20px; font-weight: 700; color: #1E3A8A; border-bottom: 3px solid #3B82F6; padding-bottom: 5px; margin-top: 25px; margin-bottom: 15px; }
    .card-critical { background-color: #FEF2F2; padding: 15px; border-radius: 8px; border-left: 6px solid #DC2626; margin-bottom: 12px; color: #991B1B; font-weight: 500; }
    .card-warning { background-color: #FFFBEB; padding: 15px; border-radius: 8px; border-left: 6px solid #D97706; margin-bottom: 12px; color: #92400E; font-weight: 500; }
    .card-success { background-color: #ECFDF5; padding: 15px; border-radius: 8px; border-left: 6px solid #059669; margin-bottom: 12px; color: #065F46; font-weight: 500; }
    .card-info { background-color: #F0F9FF; padding: 15px; border-radius: 8px; border-left: 6px solid #0284C7; margin-bottom: 12px; color: #075985; font-weight: 500; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Translational Precision Antimicrobial Stewardship Framework Model</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Lead Investigator: MAYANK VIRMANI (PharmD, PV Scientist) | GitHub Portfolio Engine v22.0</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 1. CLINICAL SIDEBAR COHORT MATRIX
# ------------------------------------------------------------------------------
st.sidebar.header("👤 Patient Demographics & Vitals")
pt_id = st.sidebar.text_input("Patient ID/MRN", "PT-90823")
age = st.sidebar.slider("Age (Years)", 18, 100, 68)
gender = st.sidebar.radio("Biological Gender", ["Male", "Female"])
weight = st.sidebar.number_input("Total Body Weight (kg)", min_value=30.0, max_value=200.0, value=75.0)

st.sidebar.markdown("---")
st.sidebar.header("🧪 Biomarkers & Organ Functions")
scr = st.sidebar.number_input("Serum Creatinine (mg/dL)", min_value=0.3, max_value=10.0, value=1.8, step=0.1)
ast_lab = st.sidebar.number_input("AST (SGOT) (U/L)", min_value=5, max_value=2000, value=35)
alt_lab = st.sidebar.number_input("ALT (SGPT) (U/L)", min_value=5, max_value=2000, value=42)

st.sidebar.markdown("---")
st.sidebar.header("🏥 Ward Acuity Level")
ward_type = st.sidebar.selectbox("Select Location Type:", ["OPD (Outpatient)", "IPD General Ward", "ICU (Intensive Care Unit)"])

st.sidebar.markdown("---")
st.sidebar.header("🩺 Comorbidities & Risks")
comorbidities = st.sidebar.multiselect(
    "Select Pathologies:",
    ["None", "Decompensated Liver Cirrhosis", "Severe Neutropenia", "Chronic Kidney Disease (CKD)", "Epilepsy History"]
)

st.sidebar.markdown("---")
st.sidebar.header("💊 Concomitant Medications (DDI Check)")
concurrent_meds = st.sidebar.multiselect(
    "Select Current Medications:",
    ["None", "Warfarin", "Antacids / Calcium Supplements", "SSRI Antidepressants"]
)

st.sidebar.markdown("---")
st.sidebar.header("🧬 Actionable PGx Biomarkers")
pgx_variant = st.sidebar.selectbox(
    "Patient Genomic Status:",
    ["Wild Type", "MT-RNR1 m.1555A>G Carrier", "CYP2C19 Poor Metabolizer"]
)

# Cockcroft-Gault Engine
if gender == "Male":
    crcl = ((140 - age) * weight) / (72 * scr)
else:
    crcl = (((140 - age) * weight) / (72 * scr)) * 0.85

st.sidebar.metric(label="Calculated GFR / CrCl", value=f"{crcl:.1f} mL/min", delta=f"{crcl-90:.1f} vs Normal")

# ------------------------------------------------------------------------------
# 2. EXTENDED ANTIMICROBIAL KNOWLEDGE BASE
# ------------------------------------------------------------------------------
drug_list = ["Ceftazidime-Avibactam", "Meropenem", "Amikacin", "Vancomycin", "Linezolid", "Ciprofloxacin"]
st.markdown('<div class="section-header">🔍 Live Clinical Drug Decision Matrix</div>', unsafe_allow_html=True)
selected_drug = st.selectbox("Select Target Antimicrobial Agent for Evaluation:", drug_list)

# Initializing data values statically
threshold, tox_score, base_peak = 50, 4, 50.0
drug_class, food_adv, advisory, tox_desc, path_res, resistance_risk = "", "", "", "", "", "Low"

if selected_drug == "Ceftazidime-Avibactam":
    drug_class, threshold, tox_score, base_peak = "Beta-Lactam/BLI Combination", 50, 4, 80.0
    food_adv = "Independent of meals. Gut transit food metrics do not alter bio-efficacy tracking lines."
    advisory = "Reduce regimen to 1.25g q8h if CrCl drops within 30-50 mL/min."
    tox_desc = "Risk of high concentration induced neurotoxicity and CDAD tracking profiles."
    path_res = "Strong coverage profiles verified against KPC and OXA-48 CRE lines; fails against MBL strains."
    resistance_risk = "Medium"

elif selected_drug == "Meropenem":
    drug_class, threshold, tox_score, base_peak = "High-End Carbapenem", 50, 4, 60.0
    food_adv = "Intravenous administration vector. Stable across varied nutritional backgrounds."
    advisory = "Severe high-acuity empiric line weapon. Drop systematically down to 500mg q12h if CrCl < 10."
    tox_desc = "GABA-A binding structures lower seizure threshold profiles in renal failure lines."
    path_res = "Susceptible to active structural blockages from Carbapenem-Resistant Enterobacteriaceae (CRE)."
    resistance_risk = "High"

elif selected_drug == "Amikacin":
    drug_class, threshold, tox_score, base_peak = "Aminoglycoside Architecture", 60, 9, 45.0
    food_adv = "Injected asset profile. Unaffected by systemic metabolic oral gut food barriers."
    advisory = "Threat vector high. Require extended single dosing schedule loops (15mg/kg) paired with daily TDM lines."
    tox_desc = "Irreversible bilateral cochlear-vestibular auditory toxicity and direct tubular injury panels."
    path_res = "Strong tracking metrics against hyper-resistant gram-negative pathogens as short empiric blockades."
    resistance_risk = "Low"

elif selected_drug == "Vancomycin":
    drug_class, threshold, tox_score, base_peak = "Glycopeptide Class", 50, 7, 35.0
    food_adv = "IV administration setup. No gastrointestinal food dependencies mapped."
    advisory = "Enforce explicit therapeutic target ranges of 400-600 AUC/MIC via strict plasma trough tracks."
    tox_desc = "Dose-dependent Acute Tubular Necrosis (ATN) nephrotoxicity risks; histamine-driven Red Man Syndrome."
    path_res = "Requires active monitoring tracking profiles targeting emerging VRE and VISA isolates."
    resistance_risk = "High"

elif selected_drug == "Linezolid":
    drug_class, threshold, tox_score, base_peak = "Oxazolidinone Class", 30, 5, 20.0
    food_adv = "CRITICAL ALERT: Strictly avoid tyramine-rich foods (aged cheese, soy sauce) to prevent hypertensive crisis."
    advisory = "100% oral absorption efficiency switch option. Does not require adjustment profiles for dropping GFR values."
    tox_desc = "Time-dependent bone marrow suppression leading to progressive thrombocytopenia if cycles cross 14 days."
    path_res = "Monitor tracking parameters closely for progressive optrA/cfr mutation clusters in MRSA stocks."
    resistance_risk = "Medium"

else:
    drug_class, threshold, tox_score, base_peak = "Fluoroquinolone System", 30, 5, 5.0
    food_adv = "CRITICAL ALERT: Do not consume dairy assets or calcium supplements within 2 hours. Chelation failure risk."
    advisory = "Switch maintenance tracking lines down to q24h intervals if clearance indices slip under 30."
    tox_desc = "Black box alerts: Tendon rupture hazards, acute aortic dissection risks, and glycemic volatility."
    path_res = "Widespread structural resistance shifts seen in standard community urinary tracking profiles via gyrA defects."
    resistance_risk = "Critical"

# ------------------------------------------------------------------------------
# 3. HIGH-ACUITY STEWARDSHIP CLOUD INTERCEPTS
# ------------------------------------------------------------------------------
st.markdown("### 🛑 Multi-Layer Stewardship Intercept Shields")

if ward_type == "ICU (Intensive Care Unit)":
    st.markdown('<div class="card-info">ℹ️ ACUITY WARPING ALERT: Intensive Care status alters volume of distribution fields. Initial loading doses should be scaled dynamically.</div>', unsafe_allow_html=True)

if "Decompensated Liver Cirrhosis" in comorbidities and selected_drug in ["Linezolid"]:
    st.markdown('<div class="card-critical">🚨 HEPATIC METABOLISM FAILURE: Advanced cirrhosis detected. Clearances minimized; step down tracking frequencies.</div>', unsafe_allow_html=True)
    tox_score += 1

st.markdown(f'<div class="card-warning">🍏 DIETARY CROSSOVER SAFETY BARRIER: {food_adv}</div>', unsafe_allow_html=True)

if "Warfarin" in concurrent_meds and selected_drug in ["Ciprofloxacin"]:
    st.markdown('<div class="card-critical">🚨 METABOLIC DDI INTERCEPT: Co-administration halts CYP2C9 tracking cycles. Major risk of internal bleeding. Check INR fields.</div>', unsafe_allow_html=True)

if "SSRI Antidepressants" in concurrent_meds and selected_drug == "Linezolid":
    st.markdown('<div class="card-critical">🚨 TOXICOLOGICAL SHIELD BREAK: Linezolid acts as a selective MAOI asset. High risk of precipitating Serotonin Syndrome.</div>', unsafe_allow_html=True)

if "Antacids / Calcium Supplements" in concurrent_meds and selected_drug == "Ciprofloxacin":
