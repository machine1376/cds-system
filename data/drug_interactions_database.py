
"""
Comprehensive mock drug interaction database for Clinical Decision Support System
Based on real clinical drug interaction patterns and severity classifications
"""

from typing import Dict, List, Any
from backend.models.schemas import SeverityLevel

class DrugInteractionDatabase:
    """Mock database containing realistic drug interaction data"""
    
    def __init__(self):
        self.interactions = self._build_interaction_database()
        self.drug_aliases = self._build_drug_aliases()
    
    def _build_interaction_database(self) -> Dict[str, Dict]:
        """Build comprehensive drug interaction database"""
        return {
            # CONTRAINDICATED INTERACTIONS (Most severe)
            ("warfarin", "phenytoin"): {
                "severity": SeverityLevel.CONTRAINDICATED,
                "description": "Phenytoin significantly increases warfarin metabolism, leading to unpredictable INR changes and high bleeding or clotting risk",
                "mechanism": "CYP2C9 enzyme induction by phenytoin dramatically alters warfarin clearance",
                "management": "Avoid combination. If absolutely necessary, use alternative anticoagulant or antiepileptic. Requires intensive INR monitoring if used together.",
                "onset": "2-7 days",
                "documentation": "Well-documented",
                "sources": ["Micromedex", "Drug Facts & Comparisons", "Clinical studies"]
            },
            
            ("metformin", "iodinated_contrast"): {
                "severity": SeverityLevel.CONTRAINDICATED,
                "description": "Risk of contrast-induced nephropathy leading to lactic acidosis",
                "mechanism": "Contrast agents may cause acute kidney injury, impairing metformin elimination",
                "management": "Discontinue metformin 48 hours before contrast administration. Resume only after confirming normal kidney function.",
                "onset": "Immediate to 48 hours",
                "documentation": "Well-documented",
                "sources": ["FDA warnings", "Radiology guidelines", "Endocrine society"]
            },
            
            ("simvastatin", "gemfibrozil"): {
                "severity": SeverityLevel.CONTRAINDICATED,
                "description": "Severe risk of rhabdomyolysis and acute kidney failure",
                "mechanism": "Gemfibrozil inhibits simvastatin glucuronidation, increasing plasma levels 3-4 fold",
                "management": "Contraindicated combination. Use alternative statin (atorvastatin, rosuvastatin) if fibrate needed.",
                "onset": "Days to weeks",
                "documentation": "Well-documented",
                "sources": ["FDA contraindication", "Cardiology guidelines", "Case reports"]
            },

            # MAJOR INTERACTIONS
            ("warfarin", "aspirin"): {
                "severity": SeverityLevel.MAJOR,
                "description": "Significantly increased bleeding risk due to additive anticoagulant and antiplatelet effects",
                "mechanism": "Warfarin inhibits vitamin K synthesis; aspirin irreversibly inhibits platelet aggregation",
                "management": "Use with extreme caution. Consider low-dose aspirin (81mg) only if clear indication. Monitor INR closely and watch for bleeding signs.",
                "onset": "1-7 days",
                "documentation": "Well-documented",
                "sources": ["Cardiology guidelines", "Anticoagulation studies", "Meta-analyses"]
            },
            
            ("digoxin", "amiodarone"): {
                "severity": SeverityLevel.MAJOR,
                "description": "Amiodarone doubles digoxin plasma levels, risk of digoxin toxicity",
                "mechanism": "Amiodarone inhibits P-glycoprotein transport and reduces renal digoxin clearance",
                "management": "Reduce digoxin dose by 50% when starting amiodarone. Monitor digoxin levels and signs of toxicity (nausea, vision changes, arrhythmias).",
                "onset": "1-2 weeks",
                "documentation": "Well-documented",
                "sources": ["Cardiology studies", "Pharmacokinetic data", "Clinical trials"]
            },
            
            ("lithium", "ace_inhibitors"): {
                "severity": SeverityLevel.MAJOR,
                "description": "ACE inhibitors can increase lithium levels leading to toxicity",
                "mechanism": "ACE inhibitors reduce kidney function and lithium clearance",
                "management": "Monitor lithium levels closely. May need lithium dose reduction. Watch for signs of lithium toxicity.",
                "onset": "1-4 weeks",
                "documentation": "Well-documented",
                "sources": ["Psychiatry guidelines", "Nephrology studies", "Case series"]
            },
            
            ("clopidogrel", "omeprazole"): {
                "severity": SeverityLevel.MAJOR,
                "description": "Omeprazole reduces clopidogrel antiplatelet effect, increasing cardiovascular events",
                "mechanism": "Omeprazole inhibits CYP2C19, preventing clopidogrel activation to active metabolite",
                "management": "Avoid omeprazole with clopidogrel. Use pantoprazole or H2 blocker if acid suppression needed.",
                "onset": "Days",
                "documentation": "Well-documented",
                "sources": ["FDA warnings", "Cardiology guidelines", "Large studies"]
            },

            # MODERATE INTERACTIONS
            ("metformin", "furosemide"): {
                "severity": SeverityLevel.MODERATE,
                "description": "Furosemide may increase metformin levels and risk of lactic acidosis",
                "mechanism": "Furosemide competes with metformin for renal tubular secretion",
                "management": "Monitor kidney function and blood glucose. Watch for signs of lactic acidosis if used together.",
                "onset": "Days",
                "documentation": "Moderate",
                "sources": ["Pharmacokinetic studies", "Diabetes guidelines"]
            },
            
            ("atorvastatin", "diltiazem"): {
                "severity": SeverityLevel.MODERATE,
                "description": "Diltiazem increases atorvastatin levels, potential for muscle toxicity",
                "mechanism": "Diltiazem inhibits CYP3A4 metabolism of atorvastatin",
                "management": "Consider lower atorvastatin dose (max 20mg daily). Monitor for muscle pain or weakness.",
                "onset": "1-2 weeks",
                "documentation": "Well-documented",
                "sources": ["Cardiology studies", "Pharmacokinetic data"]
            },
            
            ("levothyroxine", "calcium_carbonate"): {
                "severity": SeverityLevel.MODERATE,
                "description": "Calcium reduces levothyroxine absorption, potential hypothyroidism",
                "mechanism": "Calcium forms insoluble complexes with levothyroxine in the gut",
                "management": "Separate administration by 4 hours. Take levothyroxine on empty stomach, calcium with meals.",
                "onset": "Weeks to months",
                "documentation": "Well-documented",
                "sources": ["Endocrine guidelines", "Absorption studies"]
            },
            
            ("amlodipine", "simvastatin"): {
                "severity": SeverityLevel.MODERATE,
                "description": "Amlodipine increases simvastatin levels, risk of myopathy",
                "mechanism": "Amlodipine inhibits CYP3A4 metabolism of simvastatin",
                "management": "Limit simvastatin dose to 20mg daily when used with amlodipine. Monitor for muscle symptoms.",
                "onset": "1-4 weeks",
                "documentation": "Well-documented",
                "sources": ["FDA recommendations", "Statin guidelines"]
            },

            # MINOR INTERACTIONS
            ("metformin", "metoprolol"): {
                "severity": SeverityLevel.MINOR,
                "description": "Beta-blockers may mask hypoglycemia symptoms",
                "mechanism": "Beta-blockade reduces tachycardia and other adrenergic symptoms of hypoglycemia",
                "management": "Educate patient about non-adrenergic hypoglycemia symptoms. Monitor blood glucose closely.",
                "onset": "Immediate",
                "documentation": "Well-documented",
                "sources": ["Diabetes guidelines", "Cardiology texts"]
            },
            
            ("lisinopril", "potassium_chloride"): {
                "severity": SeverityLevel.MINOR,
                "description": "ACE inhibitors may increase potassium levels",
                "mechanism": "ACE inhibitors reduce aldosterone, decreasing potassium excretion",
                "management": "Monitor serum potassium levels. May need to adjust potassium supplementation.",
                "onset": "Days to weeks",
                "documentation": "Well-documented",
                "sources": ["Cardiology guidelines", "Electrolyte studies"]
            },
            
            ("aspirin", "ibuprofen"): {
                "severity": SeverityLevel.MINOR,
                "description": "Ibuprofen may reduce cardioprotective effects of low-dose aspirin",
                "mechanism": "Ibuprofen competes for COX-1 binding site, blocking aspirin's irreversible inhibition",
                "management": "Take aspirin 2 hours before ibuprofen, or use alternative anti-inflammatory.",
                "onset": "Hours",
                "documentation": "Moderate",
                "sources": ["Cardiology studies", "Pharmacology research"]
            },

            # Additional high-frequency clinical interactions
            ("warfarin", "ciprofloxacin"): {
                "severity": SeverityLevel.MAJOR,
                "description": "Ciprofloxacin significantly increases warfarin effect and bleeding risk",
                "mechanism": "Ciprofloxacin inhibits CYP1A2 and CYP3A4 warfarin metabolism",
                "management": "Monitor INR closely. May need warfarin dose reduction of 25-50%. Consider alternative antibiotic.",
                "onset": "2-5 days",
                "documentation": "Well-documented",
                "sources": ["Anticoagulation guidelines", "Infectious disease studies"]
            },
            
            ("phenytoin", "valproic_acid"): {
                "severity": SeverityLevel.MAJOR,
                "description": "Complex bidirectional interaction affecting both drug levels",
                "mechanism": "Valproic acid displaces phenytoin from protein binding and inhibits metabolism",
                "management": "Monitor both drug levels and clinical response. Expect phenytoin level changes.",
                "onset": "1-2 weeks",
                "documentation": "Well-documented",
                "sources": ["Neurology guidelines", "Epilepsy studies"]
            },
            
            ("insulin", "beta_blockers"): {
                "severity": SeverityLevel.MODERATE,
                "description": "Beta-blockers mask hypoglycemia symptoms and may prolong recovery",
                "mechanism": "Beta-blockade prevents sympathetic response to hypoglycemia",
                "management": "Monitor blood glucose frequently. Educate on non-adrenergic hypoglycemia symptoms.",
                "onset": "Immediate",
                "documentation": "Well-documented",
                "sources": ["Diabetes guidelines", "Endocrine society"]
            },
            
            ("sildenafil", "nitroglycerin"): {
                "severity": SeverityLevel.CONTRAINDICATED,
                "description": "Severe hypotension and cardiovascular collapse risk",
                "mechanism": "Both drugs cause vasodilation through nitric oxide pathways",
                "management": "Absolute contraindication. Never use together. Wait 24-48 hours between administration.",
                "onset": "Minutes to hours",
                "documentation": "Well-documented",
                "sources": ["FDA contraindication", "Cardiology warnings", "Urology guidelines"]
            },
            
            ("theophylline", "ciprofloxacin"): {
                "severity": SeverityLevel.MAJOR,
                "description": "Ciprofloxacin significantly increases theophylline levels and toxicity risk",
                "mechanism": "Ciprofloxacin inhibits CYP1A2 theophylline metabolism",
                "management": "Reduce theophylline dose by 50%. Monitor levels and signs of toxicity (seizures, arrhythmias).",
                "onset": "2-5 days",
                "documentation": "Well-documented",
                "sources": ["Pulmonology guidelines", "Drug interaction studies"]
            }
        }
    
    def _build_drug_aliases(self) -> Dict[str, List[str]]:
        """Build dictionary of drug name aliases and brand names"""
        return {
            "warfarin": ["coumadin", "jantoven", "warfarin sodium"],
            "aspirin": ["acetylsalicylic acid", "ASA", "bayer", "ecotrin"],
            "metformin": ["glucophage", "fortamet", "glumetza", "riomet"],
            "simvastatin": ["zocor", "flolipid"],
            "atorvastatin": ["lipitor", "atorvastatin calcium"],
            "digoxin": ["lanoxin", "digitek", "digox"],
            "amiodarone": ["cordarone", "pacerone"],
            "lithium": ["lithobid", "eskalith", "lithium carbonate"],
            "clopidogrel": ["plavix"],
            "omeprazole": ["prilosec", "zegerid"],
            "pantoprazole": ["protonix"],
            "furosemide": ["lasix", "furosemide injection"],
            "diltiazem": ["cardizem", "tiazac", "cartia"],
            "amlodipine": ["norvasc", "katerzia"],
            "levothyroxine": ["synthroid", "levoxyl", "tirosint"],
            "calcium_carbonate": ["tums", "caltrate", "os-cal"],
            "metoprolol": ["lopressor", "toprol-xl"],
            "lisinopril": ["prinivil", "zestril"],
            "potassium_chloride": ["klor-con", "k-dur", "micro-k"],
            "ibuprofen": ["advil", "motrin", "brufen"],
            "ciprofloxacin": ["cipro", "cipro xr"],
            "phenytoin": ["dilantin", "phenytek"],
            "valproic_acid": ["depakote", "depakene", "stavzor"],
            "insulin": ["humalog", "novolog", "lantus", "levemir"],
            "sildenafil": ["viagra", "revatio"],
            "nitroglycerin": ["nitrostat", "nitro-dur", "minitran"],
            "theophylline": ["theo-dur", "uniphyl", "theochron"],
            "gemfibrozil": ["lopid"],
            "ace_inhibitors": ["lisinopril", "enalapril", "captopril", "ramipril"],
            "beta_blockers": ["metoprolol", "atenolol", "propranolol", "carvedilol"],
            "iodinated_contrast": ["iohexol", "iopamidol", "iodixanol", "contrast dye"]
        }
    
    def normalize_drug_name(self, drug_name: str) -> str:
        """Normalize drug name to standard form"""
        drug_lower = drug_name.lower().strip()
        
        # Check if it's already a standard name
        if drug_lower in [key for interaction_pair in self.interactions.keys() for key in interaction_pair]:
            return drug_lower
        
        # Check aliases
        for standard_name, aliases in self.drug_aliases.items():
            if drug_lower in [alias.lower() for alias in aliases]:
                return standard_name
        
        return drug_lower
    
    def get_interaction(self, drug1: str, drug2: str) -> Dict[str, Any]:
        """Get interaction data between two drugs"""
        norm_drug1 = self.normalize_drug_name(drug1)
        norm_drug2 = self.normalize_drug_name(drug2)
        
        # Check both directions
        interaction = (
            self.interactions.get((norm_drug1, norm_drug2)) or 
            self.interactions.get((norm_drug2, norm_drug1))
        )
        
        if interaction:
            return {
                **interaction,
                "drug1": drug1,
                "drug2": drug2,
                "normalized_drug1": norm_drug1,
                "normalized_drug2": norm_drug2
            }
        
        return None
    
    def check_multiple_drugs(self, drug_list: List[str]) -> List[Dict[str, Any]]:
        """Check for interactions among multiple drugs"""
        interactions = []
        
        for i, drug1 in enumerate(drug_list):
            for drug2 in drug_list[i+1:]:
                interaction = self.get_interaction(drug1, drug2)
                if interaction:
                    interactions.append(interaction)
        
        # Sort by severity (most severe first)
        severity_order = {
            SeverityLevel.CONTRAINDICATED: 0,
            SeverityLevel.MAJOR: 1,
            SeverityLevel.MODERATE: 2,
            SeverityLevel.MINOR: 3
        }
        
        interactions.sort(key=lambda x: severity_order.get(x['severity'], 4))
        
        return interactions
    
    def get_drug_interaction_summary(self, drug_name: str) -> Dict[str, Any]:
        """Get summary of all known interactions for a specific drug"""
        norm_drug = self.normalize_drug_name(drug_name)
        drug_interactions = []
        
        for (drug1, drug2), interaction_data in self.interactions.items():
            if norm_drug in (drug1, drug2):
                other_drug = drug2 if norm_drug == drug1 else drug1
                drug_interactions.append({
                    "interacting_drug": other_drug,
                    "severity": interaction_data["severity"],
                    "description": interaction_data["description"]
                })
        
        # Group by severity
        by_severity = {}
        for interaction in drug_interactions:
            severity = interaction["severity"]
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(interaction)
        
        return {
            "drug": drug_name,
            "normalized_name": norm_drug,
            "total_interactions": len(drug_interactions),
            "by_severity": by_severity,
            "all_interactions": drug_interactions
        }

# Initialize global database instance
drug_interaction_db = DrugInteractionDatabase()

# Convenience functions for API use
def check_drug_interaction(drug1: str, drug2: str) -> Dict[str, Any]:
    """Check interaction between two drugs"""
    return drug_interaction_db.get_interaction(drug1, drug2)

def check_drug_list_interactions(drugs: List[str]) -> List[Dict[str, Any]]:
    """Check for interactions in a list of drugs"""
    return drug_interaction_db.check_multiple_drugs(drugs)

def get_drug_summary(drug_name: str) -> Dict[str, Any]:
    """Get interaction summary for a drug"""
    return drug_interaction_db.get_drug_interaction_summary(drug_name)

# Example usage and testing
if __name__ == "__main__":
    # Test the database
    print("Testing Drug Interaction Database...")
    
    # Test individual interaction
    interaction = check_drug_interaction("warfarin", "aspirin")
    if interaction:
        print(f"\nInteraction found:")
        print(f"Drugs: {interaction['drug1']} + {interaction['drug2']}")
        print(f"Severity: {interaction['severity']}")
        print(f"Description: {interaction['description']}")
        print(f"Management: {interaction['management']}")
    
    # Test multiple drug list
    test_drugs = ["warfarin", "aspirin", "metformin", "lisinopril"]
    interactions = check_drug_list_interactions(test_drugs)
    print(f"\nFound {len(interactions)} interactions in drug list {test_drugs}")
    
    for interaction in interactions:
        print(f"- {interaction['drug1']} + {interaction['drug2']}: {interaction['severity']}")
    
    # Test drug summary
    warfarin_summary = get_drug_summary("warfarin")
    print(f"\nWarfarin has {warfarin_summary['total_interactions']} known interactions")
    print("By severity:", {k.value: len(v) for k, v in warfarin_summary['by_severity'].items()})