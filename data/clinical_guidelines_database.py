
"""
Comprehensive mock clinical guidelines database for Clinical Decision Support System
Based on real clinical practice guidelines from major medical organizations
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
import json

@dataclass
class ClinicalGuideline:
    id: str
    title: str
    organization: str
    specialty: str
    publication_year: int
    evidence_level: str
    last_updated: str
    summary: str
    content: str
    key_recommendations: List[Dict[str, Any]]
    contraindications: List[str]
    monitoring_requirements: List[str]
    patient_populations: List[str]
    clinical_scenarios: List[str]
    references: List[str]
    doi: Optional[str] = None
    url: Optional[str] = None

class ClinicalGuidelinesDatabase:
    """Comprehensive database of clinical practice guidelines"""
    
    def __init__(self):
        self.guidelines = self._build_guidelines_database()
        self.specialty_mapping = self._build_specialty_mapping()
        
    def _build_guidelines_database(self) -> Dict[str, ClinicalGuideline]:
        """Build comprehensive clinical guidelines database"""
        
        guidelines = {}
        
        # CARDIOLOGY GUIDELINES
        
        # Acute Coronary Syndrome
        acs_guideline = ClinicalGuideline(
            id="aha_acc_2023_acs",
            title="2023 AHA/ACC/ACCP/ASPC/NLA/PCNA Guideline for the Management of Patients with Chronic Coronary Disease",
            organization="AHA/ACC",
            specialty="cardiology",
            publication_year=2023,
            evidence_level="A",
            last_updated="2023-07-15",
            summary="Comprehensive evidence-based recommendations for diagnosis and management of chronic coronary disease, including risk stratification, medical therapy, and revascularization strategies.",
            content="""
            EXECUTIVE SUMMARY:
            
            1. INITIAL EVALUATION AND RISK ASSESSMENT
            - Obtain detailed history focusing on chest pain characteristics, functional capacity, and cardiovascular risk factors
            - Perform cardiovascular examination including assessment for heart failure signs
            - Obtain 12-lead ECG and basic metabolic panel, lipid profile, HbA1c, and troponin if acute presentation
            - Risk stratification using validated tools (ASCVD Risk Calculator, Duke Treadmill Score)
            
            2. DIAGNOSTIC TESTING
            - Stress testing (exercise ECG, stress echo, or nuclear imaging) for symptomatic patients with intermediate pretest probability
            - Coronary CT angiography (CCTA) reasonable alternative for low-intermediate risk patients
            - Invasive coronary angiography for high-risk patients or those with high-risk stress test results
            
            3. MEDICAL THERAPY
            - Antiplatelet therapy: Aspirin 81mg daily unless contraindicated
            - Statin therapy: High-intensity statin for established CAD (atorvastatin 40-80mg or rosuvastatin 20-40mg)
            - ACE inhibitor or ARB for patients with diabetes, hypertension, or LV dysfunction
            - Beta-blocker for patients with prior MI or heart failure with reduced ejection fraction
            
            4. LIFESTYLE MODIFICATIONS
            - Cardiac rehabilitation for all eligible patients
            - Mediterranean or DASH diet pattern
            - Regular aerobic exercise (150 minutes moderate intensity per week)
            - Smoking cessation counseling and pharmacotherapy
            - Weight management for overweight/obese patients
            
            5. REVASCULARIZATION INDICATIONS
            - PCI or CABG for left main disease (≥50% stenosis)
            - Revascularization for symptomatic patients with significant stenosis despite optimal medical therapy
            - CABG preferred for complex multivessel disease, especially with diabetes
            - PCI appropriate for focal lesions in patients with suitable anatomy
            """,
            key_recommendations=[
                {
                    "recommendation": "Aspirin 81mg daily for secondary prevention",
                    "class": "I",
                    "level_of_evidence": "A",
                    "rationale": "Reduces cardiovascular events by 20-25% in patients with established CAD"
                },
                {
                    "recommendation": "High-intensity statin therapy for all patients with clinical CAD",
                    "class": "I", 
                    "level_of_evidence": "A",
                    "rationale": "LDL reduction to <70 mg/dL associated with improved outcomes"
                },
                {
                    "recommendation": "Cardiac rehabilitation participation within 12 months",
                    "class": "I",
                    "level_of_evidence": "A",
                    "rationale": "Reduces mortality and improves quality of life"
                }
            ],
            contraindications=[
                "Active bleeding for antiplatelet therapy",
                "Severe liver disease for high-dose statins",
                "Unstable heart failure for beta-blockers"
            ],
            monitoring_requirements=[
                "Lipid panel 4-6 weeks after statin initiation",
                "Liver enzymes with statin therapy",
                "Blood pressure with ACE inhibitors",
                "Heart rate and symptoms with beta-blockers"
            ],
            patient_populations=["adults", "elderly", "diabetics", "post-MI", "stable angina"],
            clinical_scenarios=["chest pain", "stable angina", "post-MI", "coronary artery disease"],
            references=[
                "Circulation. 2023;148(5):e9-e119",
                "PMID: 37471501"
            ],
            doi="10.1161/CIR.0000000000001168",
            url="https://www.ahajournals.org/doi/10.1161/CIR.0000000000001168"
        )
        guidelines[acs_guideline.id] = acs_guideline
        
        # Heart Failure Guidelines
        hf_guideline = ClinicalGuideline(
            id="aha_acc_hfsa_2022_hf",
            title="2022 AHA/ACC/HFSA Guideline for the Management of Heart Failure",
            organization="AHA/ACC/HFSA",
            specialty="cardiology",
            publication_year=2022,
            evidence_level="A",
            last_updated="2022-04-01",
            summary="Evidence-based recommendations for diagnosis, evaluation, and management of heart failure with reduced and preserved ejection fraction.",
            content="""
            HEART FAILURE MANAGEMENT GUIDELINES:
            
            1. CLASSIFICATION AND STAGING
            - Stage A: At risk for HF (hypertension, diabetes, CAD)
            - Stage B: Structural heart disease without symptoms
            - Stage C: Symptomatic heart failure
            - Stage D: Advanced/refractory heart failure
            
            2. DIAGNOSTIC EVALUATION
            - BNP or NT-proBNP measurement for diagnostic confirmation
            - Echocardiography to assess LV function and structure
            - Chest X-ray to evaluate pulmonary congestion
            - CBC, comprehensive metabolic panel, liver function tests
            - Thyroid function tests if indicated
            
            3. HEART FAILURE WITH REDUCED EJECTION FRACTION (HFrEF) THERAPY
            - ACE inhibitor or ARB (if ACE inhibitor not tolerated)
            - Beta-blocker (metoprolol succinate, carvedilol, or bisoprolol)
            - Aldosterone receptor antagonist (spironolactone or eplerenone)
            - SGLT2 inhibitor (dapagliflozin or empagliflozin)
            - Diuretics for volume overload
            
            4. HEART FAILURE WITH PRESERVED EJECTION FRACTION (HFpEF) THERAPY
            - SGLT2 inhibitor for patients with diabetes
            - Diuretics for volume management
            - Treatment of underlying conditions (hypertension, diabetes, obesity)
            - ACE inhibitor or ARB may be considered
            
            5. DEVICE THERAPY
            - ICD for primary prevention if EF ≤35% despite optimal medical therapy
            - CRT for QRS ≥150ms with LBBB pattern and EF ≤35%
            - CRT-D combines both therapies when indicated
            
            6. ADVANCED THERAPIES
            - Heart transplantation evaluation for eligible patients with end-stage HF
            - Mechanical circulatory support (LVAD) as bridge to transplant or destination therapy
            - Palliative care consultation for symptom management
            """,
            key_recommendations=[
                {
                    "recommendation": "ACE inhibitor or ARB for all HFrEF patients unless contraindicated",
                    "class": "I",
                    "level_of_evidence": "A",
                    "rationale": "Reduces mortality and hospitalizations"
                },
                {
                    "recommendation": "Evidence-based beta-blocker for all HFrEF patients",
                    "class": "I",
                    "level_of_evidence": "A", 
                    "rationale": "Improves survival and reduces sudden cardiac death"
                },
                {
                    "recommendation": "SGLT2 inhibitor for HFrEF patients with or without diabetes",
                    "class": "I",
                    "level_of_evidence": "A",
                    "rationale": "Reduces cardiovascular death and heart failure hospitalizations"
                }
            ],
            contraindications=[
                "Severe hyperkalemia for ACE inhibitors/ARBs",
                "Severe bradycardia or heart block for beta-blockers",
                "Severe kidney disease for aldosterone antagonists"
            ],
            monitoring_requirements=[
                "Serum creatinine and potassium within 1-2 weeks of medication changes",
                "Daily weights for volume status",
                "Functional capacity assessment",
                "Medication adherence counseling"
            ],
            patient_populations=["adults", "elderly", "diabetics", "hypertensive", "post-MI"],
            clinical_scenarios=["dyspnea", "fatigue", "edema", "reduced exercise tolerance"],
            references=[
                "Circulation. 2022;145(18):e895-e1032",
                "PMID: 35363499"
            ],
            doi="10.1161/CIR.0000000000001063"
        )
        guidelines[hf_guideline.id] = hf_guideline
        
        # ENDOCRINOLOGY GUIDELINES
        
        # Diabetes Management
        diabetes_guideline = ClinicalGuideline(
            id="ada_2024_diabetes",
            title="Standards of Care in Diabetes—2024",
            organization="American Diabetes Association",
            specialty="endocrinology",
            publication_year=2024,
            evidence_level="A",
            last_updated="2024-01-01",
            summary="Comprehensive evidence-based standards for diabetes care including glycemic targets, medication selection, and complication prevention.",
            content="""
            DIABETES STANDARDS OF CARE 2024:
            
            1. GLYCEMIC TARGETS
            - HbA1c <7% for most adults
            - HbA1c <6.5% for healthy adults with long life expectancy
            - HbA1c <8% for complex/poor health adults
            - Preprandial glucose 80-130 mg/dL
            - Peak postprandial glucose <180 mg/dL
            
            2. TYPE 2 DIABETES MEDICATION ALGORITHM
            First-line: Metformin + lifestyle modifications
            Second-line options based on clinical characteristics:
            - ASCVD/CKD: GLP-1 RA or SGLT2 inhibitor
            - Heart failure: SGLT2 inhibitor
            - Weight management priority: GLP-1 RA
            - Cost considerations: Sulfonylurea or TZD
            - Insulin if severely hyperglycemic
            
            3. CARDIOVASCULAR RISK REDUCTION
            - Statin therapy for adults with diabetes age 40-75 years
            - ACE inhibitor or ARB for hypertension or albuminuria
            - Aspirin 75-100mg daily for high cardiovascular risk
            - Blood pressure target <130/80 mmHg
            
            4. CHRONIC KIDNEY DISEASE MANAGEMENT
            - Annual urine albumin screening
            - ACE inhibitor or ARB for albuminuria
            - SGLT2 inhibitor for CKD protection
            - Avoid metformin if eGFR <30 mL/min/1.73m²
            
            5. DIABETIC RETINOPATHY SCREENING
            - Annual dilated eye exam or retinal photography
            - More frequent if proliferative retinopathy present
            - Optimize glycemic and blood pressure control
            
            6. DIABETIC NEUROPATHY
            - Annual foot examination
            - Pregabalin or gabapentin for neuropathic pain
            - Proper foot care education
            - Consider referral to podiatry
            
            7. TECHNOLOGY INTEGRATION
            - Continuous glucose monitoring (CGM) for insulin users
            - Insulin pumps for motivated patients with T1DM
            - Automated insulin delivery systems when appropriate
            """,
            key_recommendations=[
                {
                    "recommendation": "Metformin as first-line therapy for type 2 diabetes",
                    "class": "I",
                    "level_of_evidence": "A",
                    "rationale": "Proven efficacy, safety profile, and cardiovascular benefits"
                },
                {
                    "recommendation": "GLP-1 receptor agonist for patients with ASCVD or high cardiovascular risk",
                    "class": "I",
                    "level_of_evidence": "A",
                    "rationale": "Reduces major adverse cardiovascular events"
                },
                {
                    "recommendation": "SGLT2 inhibitor for patients with heart failure or CKD",
                    "class": "I",
                    "level_of_evidence": "A",
                    "rationale": "Proven kidney and heart failure benefits"
                }
            ],
            contraindications=[
                "Severe kidney disease (eGFR <30) for metformin",
                "Type 1 diabetes for most oral medications",
                "Diabetic ketoacidosis for SGLT2 inhibitors"
            ],
            monitoring_requirements=[
                "HbA1c every 3-6 months",
                "Annual comprehensive foot exam",
                "Annual dilated eye exam",
                "Annual urine microalbumin",
                "Lipid panel annually"
            ],
            patient_populations=["adults", "elderly", "adolescents", "pregnant women", "CKD patients"],
            clinical_scenarios=["newly diagnosed diabetes", "uncontrolled diabetes", "diabetic complications"],
            references=[
                "Diabetes Care. 2024;47(Suppl 1):S1-S321",
                "PMID: 38078584"
            ],
            doi="10.2337/dc24-Sint",
            url="https://care.diabetesjournals.org/content/47/Supplement_1"
        )
        guidelines[diabetes_guideline.id] = diabetes_guideline
        
        # EMERGENCY MEDICINE GUIDELINES
        
        # Sepsis Management
        sepsis_guideline = ClinicalGuideline(
            id="sccm_esicm_2021_sepsis",
            title="Surviving Sepsis Campaign: International Guidelines for Management of Sepsis and Septic Shock 2021",
            organization="SCCM/ESICM",
            specialty="emergency_medicine",
            publication_year=2021,
            evidence_level="A",
            last_updated="2021-10-01",
            summary="Evidence-based guidelines for early recognition and management of sepsis and septic shock to improve patient outcomes.",
            content="""
            SEPSIS AND SEPTIC SHOCK MANAGEMENT:
            
            1. EARLY RECOGNITION AND SCREENING
            - Use qSOFA or SIRS criteria for screening
            - Sepsis = suspected infection + SOFA score ≥2
            - Septic shock = sepsis + vasopressor requirement + lactate >2 mmol/L
            - Rapid identification within 1 hour of presentation
            
            2. HOUR-1 BUNDLE (WITHIN 1 HOUR)
            - Measure lactate level
            - Obtain blood cultures before antibiotics
            - Administer broad-spectrum antibiotics
            - Begin rapid administration of crystalloid for hypotension or lactate ≥4 mmol/L
            - Apply vasopressors if hypotensive during/after fluid resuscitation
            
            3. FLUID RESUSCITATION
            - Initial: 30 mL/kg crystalloid within 3 hours
            - Reassess hemodynamic status frequently
            - Use dynamic measures (passive leg raise, fluid responsiveness)
            - Avoid routine use of albumin for initial resuscitation
            
            4. ANTIMICROBIAL THERAPY
            - Broad-spectrum antibiotics within 1 hour
            - Target likely pathogens based on clinical syndrome
            - Consider local resistance patterns
            - De-escalate based on culture results
            - Duration typically 7-10 days
            
            5. VASOPRESSOR THERAPY
            - Norepinephrine as first-line vasopressor
            - Target MAP ≥65 mmHg
            - Add vasopressin or epinephrine as second agent
            - Consider dobutamine for myocardial dysfunction
            
            6. CORTICOSTEROID THERAPY
            - Hydrocortisone 200mg/day for patients with septic shock requiring high-dose vasopressors
            - Do not use if shock reverses quickly
            - Taper when vasopressors no longer needed
            
            7. SUPPORTIVE CARE
            - Lung-protective ventilation if mechanically ventilated
            - Conservative fluid strategy after initial resuscitation
            - VTE prophylaxis unless contraindicated
            - Stress ulcer prophylaxis for high-risk patients
            """,
            key_recommendations=[
                {
                    "recommendation": "Administer broad-spectrum antibiotics within 1 hour of sepsis recognition",
                    "class": "Strong",
                    "level_of_evidence": "Moderate",
                    "rationale": "Each hour delay increases mortality risk"
                },
                {
                    "recommendation": "Initial fluid resuscitation with 30 mL/kg crystalloid",
                    "class": "Strong", 
                    "level_of_evidence": "Low",
                    "rationale": "Improves tissue perfusion and hemodynamics"
                },
                {
                    "recommendation": "Norepinephrine as first-line vasopressor",
                    "class": "Strong",
                    "level_of_evidence": "Moderate",
                    "rationale": "Superior outcomes compared to dopamine"
                }
            ],
            contraindications=[
                "Allergy to specific antibiotics",
                "Severe heart failure for aggressive fluid resuscitation",
                "Aortic stenosis for vasodilating agents"
            ],
            monitoring_requirements=[
                "Vital signs every 15 minutes initially",
                "Urine output hourly",
                "Serial lactate levels",
                "Blood cultures at 48-72 hours",
                "Organ function assessment"
            ],
            patient_populations=["adults", "elderly", "immunocompromised", "ICU patients"],
            clinical_scenarios=["fever with hypotension", "altered mental status", "organ dysfunction"],
            references=[
                "Intensive Care Med. 2021;47(11):1181-1247",
                "PMID: 34599691"
            ],
            doi="10.1007/s00134-021-06506-y"
        )
        guidelines[sepsis_guideline.id] = sepsis_guideline
        
        # INFECTIOUS DISEASE GUIDELINES
        
        # Pneumonia Treatment
        pneumonia_guideline = ClinicalGuideline(
            id="idsa_ats_2019_cap",
            title="Diagnosis and Treatment of Adults with Community-acquired Pneumonia",
            organization="IDSA/ATS",
            specialty="infectious_disease",
            publication_year=2019,
            evidence_level="A",
            last_updated="2019-07-01",
            summary="Evidence-based recommendations for diagnosis and antimicrobial treatment of community-acquired pneumonia in adults.",
            content="""
            COMMUNITY-ACQUIRED PNEUMONIA MANAGEMENT:
            
            1. DIAGNOSIS AND SEVERITY ASSESSMENT
            - Chest imaging (X-ray or CT) for suspected pneumonia
            - Consider CURB-65 or PSI for severity assessment
            - Procalcitonin may help distinguish bacterial from viral
            - Blood cultures for severe CAP or specific risk factors
            
            2. OUTPATIENT TREATMENT
            Previously healthy, no antibiotic use in 90 days:
            - Amoxicillin 1g TID or
            - Macrolide (azithromycin, clarithromycin) or
            - Doxycycline
            
            Comorbidities or recent antibiotic use:
            - Amoxicillin/clavulanate + macrolide or
            - Cephalosporin + macrolide or
            - Fluoroquinolone alone
            
            3. INPATIENT NON-ICU TREATMENT
            - Ampicillin/sulbactam + macrolide or
            - Ceftriaxone + macrolide or
            - Fluoroquinolone alone
            
            4. ICU TREATMENT
            - β-lactam (ceftriaxone, ampicillin/sulbactam) + macrolide or
            - β-lactam + fluoroquinolone
            
            Special considerations for Pseudomonas risk:
            - Piperacillin/tazobactam + ciprofloxacin/levofloxacin or
            - Carbapenem + fluoroquinolone
            
            5. MRSA COVERAGE INDICATIONS
            - Previous MRSA infection
            - Severe necrotizing pneumonia
            - Add vancomycin or linezolid
            
            6. DURATION OF THERAPY
            - Minimum 5 days of treatment
            - Patient should be afebrile 48-72 hours
            - No more than one CAP-associated sign of clinical instability
            - Procalcitonin guidance may shorten duration
            
            7. PREVENTION
            - Pneumococcal vaccination (PCV13, PPSV23)
            - Annual influenza vaccination
            - Smoking cessation counseling
            """,
            key_recommendations=[
                {
                    "recommendation": "Amoxicillin as first-line for uncomplicated outpatient CAP",
                    "class": "Strong",
                    "level_of_evidence": "Moderate",
                    "rationale": "Effective against S. pneumoniae with good safety profile"
                },
                {
                    "recommendation": "Minimum 5 days of antibiotic therapy",
                    "class": "Strong",
                    "level_of_evidence": "Moderate",
                    "rationale": "Shorter courses associated with treatment failure"
                },
                {
                    "recommendation": "Pneumococcal and influenza vaccination",
                    "class": "Strong",
                    "level_of_evidence": "High",
                    "rationale": "Proven reduction in pneumonia incidence"
                }
            ],
            contraindications=[
                "Penicillin allergy for amoxicillin",
                "Severe kidney disease for certain antibiotics",
                "QT prolongation for fluoroquinolones"
            ],
            monitoring_requirements=[
                "Clinical response assessment at 48-72 hours",
                "Temperature and oxygen saturation",
                "Kidney function with certain antibiotics",
                "Culture results and antibiotic adjustment"
            ],
            patient_populations=["adults", "elderly", "immunocompromised", "COPD patients"],
            clinical_scenarios=["cough with fever", "dyspnea", "chest pain", "infiltrate on chest imaging"],
            references=[
                "Clin Infect Dis. 2019;68(12):e13-e94",
                "PMID: 30566567"
            ],
            doi="10.1093/cid/ciy866"
        )
        guidelines[pneumonia_guideline.id] = pneumonia_guideline
        
        # NEUROLOGY GUIDELINES
        
        # Stroke Management
        stroke_guideline = ClinicalGuideline(
            id="aha_asa_2019_stroke",
            title="2019 Update to the 2018 Guidelines for the Early Management of Acute Ischemic Stroke",
            organization="AHA/ASA",
            specialty="neurology",
            publication_year=2019,
            evidence_level="A",
            last_updated="2019-12-01",
            summary="Evidence-based guidelines for rapid evaluation and treatment of acute ischemic stroke including thrombolysis and thrombectomy.",
            content="""
            ACUTE ISCHEMIC STROKE MANAGEMENT:
            
            1. RAPID ASSESSMENT AND DIAGNOSIS
            - NIH Stroke Scale (NIHSS) assessment
            - Noncontrast CT within 20 minutes of arrival
            - CT angiography for large vessel occlusion screening
            - Laboratory studies: glucose, creatinine, PT/PTT, platelet count
            
            2. INTRAVENOUS THROMBOLYSIS (ALTEPLASE)
            Inclusion criteria:
            - Onset within 4.5 hours (3 hours if >80 years old)
            - Measurable neurologic deficit
            - CT shows no hemorrhage
            - No contraindications present
            
            Exclusion criteria:
            - Intracranial hemorrhage
            - Recent major surgery (14 days)
            - Recent stroke (3 months)
            - Anticoagulation with elevated INR
            - Platelet count <100,000
            
            3. MECHANICAL THROMBECTOMY
            - Large vessel occlusion (ICA, M1, M2 MCA)
            - Within 6 hours of symptom onset
            - Extend to 24 hours with perfusion imaging
            - NIHSS ≥6 for anterior circulation
            - mTICI 2b/3 reperfusion goal
            
            4. BLOOD PRESSURE MANAGEMENT
            Thrombolysis candidates:
            - Target <185/110 mmHg before treatment
            - Target <180/105 mmHg post-treatment
            
            Non-thrombolysis candidates:
            - Permissive hypertension unless >220/120 mmHg
            - Avoid precipitous drops in BP
            
            5. ANTITHROMBOTIC THERAPY
            - Aspirin 325mg within 24-48 hours (after thrombolysis)
            - Dual antiplatelet therapy for minor stroke/TIA
            - Anticoagulation for atrial fibrillation (delayed if large stroke)
            
            6. SECONDARY PREVENTION
            - Statin therapy for LDL >100 mg/dL
            - Blood pressure control <130/80 mmHg
            - Diabetes management HbA1c <7%
            - Smoking cessation
            - Anticoagulation for atrial fibrillation
            """,
            key_recommendations=[
                {
                    "recommendation": "IV alteplase within 4.5 hours for eligible patients",
                    "class": "I",
                    "level_of_evidence": "A",
                    "rationale": "Significant improvement in functional outcomes"
                },
                {
                    "recommendation": "Mechanical thrombectomy for large vessel occlusion within 6 hours",
                    "class": "I",
                    "level_of_evidence": "A",
                    "rationale": "Superior outcomes compared to medical therapy alone"
                },
                {
                    "recommendation": "Aspirin 325mg within 24-48 hours",
                    "class": "I", 
                    "level_of_evidence": "A",
                    "rationale": "Reduces risk of recurrent stroke"
                }
            ],
            contraindications=[
                "Active bleeding for thrombolysis",
                "Recent surgery for thrombolysis",
                "Severe hypertension >185/110 for thrombolysis"
            ],
            monitoring_requirements=[
                "Neurologic checks every 15 minutes x 2 hours post-thrombolysis",
                "Blood pressure monitoring",
                "Signs of intracranial hemorrhage",
                "Swallowing assessment before oral intake"
            ],
            patient_populations=["adults", "elderly", "atrial fibrillation patients"],
            clinical_scenarios=["acute neurologic deficit", "facial droop", "arm weakness", "speech difficulty"],
            references=[
                "Stroke. 2019;50(12):e344-e418", 
                "PMID: 31662037"
            ],
            doi="10.1161/STR.0000000000000211"
        )
        guidelines[stroke_guideline.id] = stroke_guideline
        
        return guidelines
    
    def _build_specialty_mapping(self) -> Dict[str, List[str]]:
        """Build mapping of specialties to their guideline IDs"""
        mapping = {}
        
        for guideline_id, guideline in self.guidelines.items():
            specialty = guideline.specialty
            if specialty not in mapping:
                mapping[specialty] = []
            mapping[specialty].append(guideline_id)
        
        return mapping
    
    def get_guideline(self, guideline_id: str) -> Optional[ClinicalGuideline]:
        """Get specific guideline by ID"""
        return self.guidelines.get(guideline_id)
    
    def get_guidelines_by_specialty(self, specialty: str) -> List[ClinicalGuideline]:
        """Get all guidelines for a specific specialty"""
        guideline_ids = self.specialty_mapping.get(specialty, [])
        return [self.guidelines[gid] for gid in guideline_ids]
    
    def search_guidelines(
        self, 
        query: str, 
        specialty: Optional[str] = None,
        organization: Optional[str] = None,
        min_year: Optional[int] = None
    ) -> List[ClinicalGuideline]:
        """Search guidelines by query terms and filters"""
        results = []
        query_lower = query.lower()
        
        for guideline in self.guidelines.values():
            # Apply filters
            if specialty and guideline.specialty != specialty:
                continue
            if organization and organization.lower() not in guideline.organization.lower():
                continue
            if min_year and guideline.publication_year < min_year:
                continue
            
            # Search in title, summary, and clinical scenarios
            searchable_text = (
                guideline.title.lower() + " " +
                guideline.summary.lower() + " " +
                " ".join(guideline.clinical_scenarios).lower() + " " +
                " ".join(guideline.patient_populations).lower()
            )
            
            if query_lower in searchable_text:
                results.append(guideline)
        
        # Sort by publication year (newest first)
        results.sort(key=lambda g: g.publication_year, reverse=True)
        return results
    
    def get_guidelines_for_clinical_scenario(self, scenario: str) -> List[ClinicalGuideline]:
        """Get guidelines relevant to a specific clinical scenario"""
        relevant_guidelines = []
        scenario_lower = scenario.lower()
        
        for guideline in self.guidelines.values():
            # Check if scenario matches any clinical scenarios in the guideline
            for clinical_scenario in guideline.clinical_scenarios:
                if scenario_lower in clinical_scenario.lower() or clinical_scenario.lower() in scenario_lower:
                    relevant_guidelines.append(guideline)
                    break
        
        return relevant_guidelines
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about the guidelines database"""
        specialty_counts = {}
        org_counts = {}
        year_counts = {}
        evidence_level_counts = {}
        
        for guideline in self.guidelines.values():
            # Count by specialty
            specialty_counts[guideline.specialty] = specialty_counts.get(guideline.specialty, 0) + 1
            
            # Count by organization
            org_counts[guideline.organization] = org_counts.get(guideline.organization, 0) + 1
            
            # Count by publication year
            year_counts[guideline.publication_year] = year_counts.get(guideline.publication_year, 0) + 1
            
            # Count by evidence level
            evidence_level_counts[guideline.evidence_level] = evidence_level_counts.get(guideline.evidence_level, 0) + 1
        
        return {
            "total_guidelines": len(self.guidelines),
            "specialties": specialty_counts,
            "organizations": org_counts,
            "publication_years": year_counts,
            "evidence_levels": evidence_level_counts,
            "latest_year": max(year_counts.keys()) if year_counts else None,
            "oldest_year": min(year_counts.keys()) if year_counts else None
        }

# Initialize global database instance
clinical_guidelines_db = ClinicalGuidelinesDatabase()

# Convenience functions for API use
def get_guideline_by_id(guideline_id: str) -> Optional[ClinicalGuideline]:
    """Get specific guideline by ID"""
    return clinical_guidelines_db.get_guideline(guideline_id)

def search_clinical_guidelines(
    query: str,
    specialty: Optional[str] = None,
    organization: Optional[str] = None,
    min_year: Optional[int] = None
) -> List[ClinicalGuideline]:
    """Search clinical guidelines"""
    return clinical_guidelines_db.search_guidelines(query, specialty, organization, min_year)

def get_guidelines_for_specialty(specialty: str) -> List[ClinicalGuideline]:
    """Get all guidelines for a specialty"""
    return clinical_guidelines_db.get_guidelines_by_specialty(specialty)

def get_guidelines_for_scenario(scenario: str) -> List[ClinicalGuideline]:
    """Get guidelines for clinical scenario"""
    return clinical_guidelines_db.get_guidelines_for_clinical_scenario(scenario)

def get_guidelines_database_stats() -> Dict[str, Any]:
    """Get database statistics"""
    return clinical_guidelines_db.get_database_stats()

# Example usage and testing
if __name__ == "__main__":
    print("Testing Clinical Guidelines Database...")
    
    # Test search functionality
    print("\n=== Search Tests ===")
    
    # Search for heart failure guidelines
    hf_guidelines = search_clinical_guidelines("heart failure")
    print(f"Heart failure guidelines found: {len(hf_guidelines)}")
    for guideline in hf_guidelines:
        print(f"- {guideline.title} ({guideline.organization}, {guideline.publication_year})")
    
    # Search by specialty
    cardiology_guidelines = get_guidelines_for_specialty("cardiology")
    print(f"\nCardiology guidelines: {len(cardiology_guidelines)}")
    
    # Search by clinical scenario
    chest_pain_guidelines = get_guidelines_for_scenario("chest pain")
    print(f"Guidelines for chest pain: {len(chest_pain_guidelines)}")
    
    # Get database statistics
    stats = get_guidelines_database_stats()
    print(f"\n=== Database Statistics ===")
    print(f"Total guidelines: {stats['total_guidelines']}")
    print(f"Specialties covered: {list(stats['specialties'].keys())}")
    print(f"Organizations: {list(stats['organizations'].keys())}")
    print(f"Publication years: {sorted(stats['publication_years'].keys())}")
    
    # Test specific guideline retrieval
    print(f"\n=== Specific Guideline Test ===")
    diabetes_guideline = get_guideline_by_id("ada_2024_diabetes")
    if diabetes_guideline:
        print(f"Retrieved: {diabetes_guideline.title}")
        print(f"Key recommendations: {len(diabetes_guideline.key_recommendations)}")
        print(f"First recommendation: {diabetes_guideline.key_recommendations[0]['recommendation']}")