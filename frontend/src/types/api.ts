// Frontend API types
export interface PatientContext {
  age?: number
  gender?: string
  weight_kg?: number
  height_cm?: number
  allergies?: string[]
  current_medications?: string[]
  medical_conditions?: string[]
  lab_values?: Record<string, string | number>
}

export interface ClinicalQuery {
  query: string
  patient_context?: PatientContext
  query_type?: string
  urgency?: string
}

export interface Source {
  title: string
  url?: string
  type: string
  evidence_level: "A" | "B" | "C"
}

export interface ClinicalRecommendation {
  recommendation: string
  confidence_score: number
  evidence_level: "A" | "B" | "C"
  reasoning: string
  considerations: string[]
  contraindications: string[]
  monitoring: string[]
  sources: Source[]
}

export interface DrugInteraction {
  drug1: string
  drug2: string
  severity: "contraindicated" | "major" | "moderate" | "minor"
  description: string
  mechanism?: string
  management: string
  sources: string[]
}

export interface ClinicalResponse {
  query_id: string
  recommendations: ClinicalRecommendation[]
  drug_interactions: DrugInteraction[]
  differential_diagnoses: string[]
  red_flags: string[]
  next_steps: string[]
  timestamp: string
  processing_time_ms?: number
}
