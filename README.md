# 🛡️ Integrated Precision Antimicrobial Stewardship & Clinical Decision Support System (CDSS)

### 🏥 Point-of-Care Digital Solution for IPD, OPD, and ICU Settings
**Developed by:** MAYANK VIRMANI (PharmD Scholar)  
**Project Category:** Clinical Pharmacology / Digital Health Learning Project  
**Target Focus:** Mitigating Drug Toxicities and Preventing Antimicrobial Resistance (AMR)

---

## ⚠️ Academic & Learning Disclaimer
This software is a functional prototype developed strictly for educational, academic, and simulation purposes as part of a PharmD learning workflow. It does **NOT** constitute medical advice and must **NOT** be used for actual patient diagnosis, real-world prescribing, or clinical management. Always defer to official hospital protocols, international guidelines (CPIC, IDSA), and licensed clinical pharmacologists.

---

## 🎯 Project Overview
In modern healthcare settings—especially within the Intensive Care Unit (ICU)—the "Golden Hour" of treating severe sepsis is highly critical. However, standard empirical prescription frameworks often fail due to patient-specific physiological fluctuations and underlying **host genetic variations (Pharmacogenomics - PGx)**. 

This CDSS tool provides a scalable framework to bridge clinical parameters with genetic risk probabilities right at the time of admission or consultation, effectively preventing:
1. **Sub-therapeutic Under-dosing:** Which fails to clear infections and actively accelerates Antimicrobial Resistance (AMR).
2. **Supratherapeutic Over-dosing:** Which triggers catastrophic organ toxicities (e.g., permanent ototoxicity or nephrotoxicity).

---

## ⚡ Core System Architecture & Features

### 1. Multi-Setting Clinical Triage
Categorizes workflows based on patient acuity and clinical location:
* **OPD (Outpatient Department):** Focuses on standard dosing, common drug-food interactions (e.g., Fluoroquinolones with calcium/dairy), and basic allergy cross-checks.
* **Medical Wards (General IPD):** Monitors maintenance dosing and organ clearance boundaries.
* **ICU (Intensive Care Unit):** Prioritizes hyper-acute sepsis protocols, real-time physiological calculations, and high-risk toxicity mitigation.

### 2. Pharmacokinetics Dosing Engine (CrCl Clearance)
* Automatically calculates **Creatinine Clearance (CrCl)** using the Cockcroft-Gault equation based on user-inputted Age, Weight, and Serum Creatinine.
* Dynamically triggers interval adjustments (e.g., prolonging Amikacin from q24h to q48h) if renal impairment is detected.

### 3. Pre-Emptive & Simulated Pharmacogenomics (PGx) Matrix
Recognizing that real-time genetic sequencing data is often unavailable at bedside in low- and middle-income countries (LMICs), the app features a dual-mode logic:
* **Pre-emptive Risk Modeling:** Utilizes peer-reviewed population allele frequency data (e.g., South Asian *CYP2C19* distribution) to warn clinicians of potential rapid or poor drug metabolism.
* **Confirmed Genotype Interface:** Executes precise dosing overrides based on official **CPIC (Clinical Pharmacogenetics Implementation Consortium)** guidelines:
  * **Pathogen Treatment Failure:** Adjusts Voriconazole dosing for *CYP2C19* Ultra-Rapid Metabolizers to prevent sub-therapeutic dosing and subsequent fungal resistance.
  * **Irreversible Ototoxicity Prevention:** Issues hard stop alerts against Aminoglycosides (Amikacin/Gentamicin) if the mitochondrial *MT-RNR1* m.1555A>G mutation is flagged.

### 4. Advanced Interaction & Allergy Layer
* Cross-references targeted antimicrobially classified drugs against critical patient histories.
* Integrates immediate warnings regarding severe **Drug-Food Interactions** (e.g., chelation profiles impacting absolute absorption rates).
* Provides explicit algorithmic clinical alternatives if a first-line drug is locked out due to toxic/allergic indicators.

---

## 🛠️ Technology Stack & Free Deployment
* **Language:** Python 3.x
* **Frontend/UI Framework:** Streamlit (Open-source, low-latency UI engine)
* **Hosting Environment:** Streamlit Community Cloud (Hosted completely Free of Charge)

---

## 🚀 How to Run this Project Locally

1. Clone or download this repository to your local system.
2. Ensure you have Python installed, then open your terminal and install the dependencies:
   ```bash
   pip install streamlit
   ```
3. Run the application using the following command:
   ```bash
   streamlit run app.py
   ```
   
