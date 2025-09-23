import React, { useState } from "react"
import {
  Search,
  User,
  AlertTriangle,
  Clock,
  CheckCircle,
  Plus,
  X,
  ChevronDown,
  ChevronUp,
  Stethoscope,
  Activity,
  Shield,
  BookOpen,
  AlertCircle,
} from "lucide-react"
import { clinicalAPI } from "../services/api"
import type {
  ClinicalQuery as ClinicalQueryType,
  PatientContext,
  ClinicalResponse,
} from "../types/api"

const ClinicalQuery: React.FC = () => {
  const [query, setQuery] = useState("")
  const [patientContext, setPatientContext] = useState<PatientContext>({})
  const [isLoading, setIsLoading] = useState(false)
  const [response, setResponse] = useState<ClinicalResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [showPatientContext, setShowPatientContext] = useState(false)
  const [queryHistory, setQueryHistory] = useState<string[]>([])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!query.trim()) {
      setError("Please enter a clinical query")
      return
    }

    setIsLoading(true)
    setError(null)
    setResponse(null)

    try {
      const queryData: ClinicalQueryType = {
        query: query.trim(),
        patient_context:
          Object.keys(patientContext).length > 0 ? patientContext : undefined,
        query_type: "general",
        urgency: "routine",
      }

      const result = await clinicalAPI.submitQuery(queryData)
      setResponse(result)

      // Add to query history
      if (!queryHistory.includes(query.trim())) {
        setQueryHistory((prev) => [query.trim(), ...prev.slice(0, 4)])
      }
    } catch (err) {
      setError("Error processing clinical query. Please try again.")
      console.error("Query error:", err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleQuerySelect = (selectedQuery: string) => {
    setQuery(selectedQuery)
    setError(null)
  }

  const clearForm = () => {
    setQuery("")
    setPatientContext({})
    setResponse(null)
    setError(null)
  }

  const updatePatientContext = (
    field: keyof PatientContext,
    value: string | number | string[] | undefined
  ) => {
    setPatientContext((prev) => ({ ...prev, [field]: value }))
  }

  const addMedication = () => {
    const medications = patientContext.current_medications || []
    setPatientContext((prev) => ({
      ...prev,
      current_medications: [...medications, ""],
    }))
  }

  const updateMedication = (index: number, value: string) => {
    const medications = [...(patientContext.current_medications || [])]
    medications[index] = value
    setPatientContext((prev) => ({ ...prev, current_medications: medications }))
  }

  const removeMedication = (index: number) => {
    const medications =
      patientContext.current_medications?.filter((_, i) => i !== index) || []
    setPatientContext((prev) => ({ ...prev, current_medications: medications }))
  }

  return (
    <div className="container section">
      {/* Hero Section */}
      <div className="text-center mb-12 fade-in">
        <div className="flex justify-center mb-8">
          <div className="w-24 h-24 bg-gradient-to-br from-medical-500 to-medical-700 rounded-3xl flex items-center justify-center shadow-medical-lg">
            <Stethoscope className="w-12 h-12 text-white" />
          </div>
        </div>
        <h1 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
          Clinical Decision Support
        </h1>
        <p className="text-lg lg:text-xl text-gray-600 max-w-4xl mx-auto leading-relaxed">
          AI-powered evidence-based clinical recommendations to support your
          medical decision-making with confidence and precision
        </p>
        <div className="flex justify-center justify-space-between mt-8">
          <div className="flex items-center lg:space-x-6 space-x-2 text-sm text-gray-500">
            <div className="flex text-left items-center">
              <div className="w-2 h-2 bg-success-500 rounded-full mr-2"></div>
              <span>HIPAA Compliant</span>
            </div>
            <div className="flex text-left items-center">
              <div className="w-2 h-2 bg-medical-500 rounded-full mr-2"></div>
              <span>Evidence-Based</span>
            </div>
            <div className="flex text-left items-center">
              <div className="w-2 h-2 bg-info-500 rounded-full mr-2"></div>
              <span>Real-time Analysis</span>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto space-y-10">
        {/* Query Form */}
        <div className="card-medical slide-up">
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-start">
              <div className="lg:w-14 lg:h-14 w-8 h-8 bg-gradient-to-br from-medical-500 to-medical-700 rounded-2xl flex items-center justify-center p-2 mr-6 shadow-medical">
                <Search className="lg:w-7 lg:h-7 w-4 h-4 text-white" />
              </div>
              <div className="text-left">
                <h2 className="text-2xl font-bold text-gray-900">
                  Clinical Query
                </h2>
                <p className="text-base text-gray-600 mt-1">
                  Enter your clinical question or scenario for AI-powered
                  analysis
                </p>
              </div>
            </div>
            {query && (
              <button
                onClick={clearForm}
                className="btn-ghost text-sm flex items-center"
              >
                <X className="w-4 h-4 mr-1" />
                Clear Form
              </button>
            )}
          </div>

          <form onSubmit={handleSubmit} className="space-y-10">
            {/* Query History */}
            {queryHistory.length > 0 && !query && (
              <div className="form-group">
                <label className="form-label text-base font-semibold flex items-center">
                  <Clock className="w-4 h-4 mr-2 text-medical-600" />
                  Recent Queries
                </label>
                <div className="grid grid-cols-1 gap-3 mt-4">
                  {queryHistory.slice(0, 3).map((historyQuery, index) => (
                    <button
                      key={index}
                      type="button"
                      onClick={() => handleQuerySelect(historyQuery)}
                      className="text-left p-4 rounded-lg border border-gray-200 hover:border-medical-300 hover:bg-medical-50 transition-all duration-200 group"
                    >
                      <p className="text-sm text-gray-700 group-hover:text-gray-900 leading-relaxed">
                        {historyQuery}
                      </p>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Main Query Input */}
            <div className="form-group">
              <label className="form-label form-label-required text-base font-semibold flex items-center">
                <Stethoscope className="w-4 h-4 mr-2 text-medical-600" />
                Clinical Question or Scenario
              </label>
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g., 65-year-old male with chest pain, elevated troponins, and ECG changes. What is the differential diagnosis and recommended workup?"
                className="input-field-medical h-40 resize-none mt-3 text-base leading-relaxed"
                required
              />
              <p className="form-help mt-3 flex items-start">
                <AlertCircle className="w-4 h-4 mr-2 text-gray-400 mt-0.5 flex-shrink-0" />
                Be specific about patient demographics, symptoms, and clinical
                findings for more accurate AI-powered recommendations
              </p>
            </div>

            {/* Patient Context Toggle */}
            <div className="form-section">
              <button
                type="button"
                onClick={() => setShowPatientContext(!showPatientContext)}
                className="flex items-center justify-between w-full p-6 rounded-xl border border-gray-200 hover:border-medical-300 hover:bg-medical-50 transition-all duration-200 group"
              >
                <div className="flex items-start">
                  <div className="lg:w-12 lg:h-12 w-8 h-8 p-2 bg-gradient-to-br from-medical-100 to-medical-200 rounded-xl flex items-center justify-center mr-4 group-hover:from-medical-200 group-hover:to-medical-300 transition-all duration-200">
                    <User className="w-6 h-6 text-medical-700" />
                  </div>
                  <div className="text-left">
                    <h3 className="font-bold text-gray-900 text-lg">
                      Patient Context
                    </h3>
                    <p className="text-sm text-gray-600 mt-1">
                      Add patient demographics and medications for enhanced
                      analysis (optional)
                    </p>
                  </div>
                </div>
                {showPatientContext ? (
                  <ChevronUp className="w-6 h-6 text-medical-600" />
                ) : (
                  <ChevronDown className="w-6 h-6 text-gray-400 group-hover:text-medical-600" />
                )}
              </button>

              {showPatientContext && (
                <div className="mt-8 space-y-8 slide-up">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="form-group">
                      <label className="form-label text-sm font-semibold flex items-center">
                        <Activity className="w-4 h-4 mr-2 text-medical-600" />
                        Age
                      </label>
                      <input
                        type="number"
                        value={patientContext.age || ""}
                        onChange={(e) =>
                          updatePatientContext(
                            "age",
                            parseInt(e.target.value) || undefined
                          )
                        }
                        placeholder="Years"
                        className="input-field-medical mt-2"
                        min="0"
                        max="150"
                      />
                    </div>

                    <div className="form-group">
                      <label className="form-label text-sm font-semibold flex items-center">
                        <User className="w-4 h-4 mr-2 text-medical-600" />
                        Gender
                      </label>
                      <select
                        value={patientContext.gender || ""}
                        onChange={(e) =>
                          updatePatientContext(
                            "gender",
                            e.target.value || undefined
                          )
                        }
                        className="input-field-medical mt-2"
                      >
                        <option value="">Select gender</option>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                        <option value="other">Other</option>
                      </select>
                    </div>

                    <div className="form-group">
                      <label className="form-label text-sm font-semibold flex items-center">
                        <Activity className="w-4 h-4 mr-2 text-medical-600" />
                        Weight (kg)
                      </label>
                      <input
                        type="number"
                        value={patientContext.weight_kg || ""}
                        onChange={(e) =>
                          updatePatientContext(
                            "weight_kg",
                            parseFloat(e.target.value) || undefined
                          )
                        }
                        placeholder="kg"
                        className="input-field-medical mt-2"
                        min="0"
                        step="0.1"
                      />
                    </div>
                  </div>

                  {/* Current Medications */}
                  <div className="form-group">
                    <div className="flex items-center justify-between mb-6">
                      <label className="form-label text-sm font-semibold flex items-center">
                        <Shield className="w-4 h-4 mr-2 text-medical-600" />
                        Current Medications
                      </label>
                      <button
                        type="button"
                        onClick={addMedication}
                        className="btn-ghost text-sm flex items-center"
                      >
                        <Plus className="w-4 h-4 mr-1" />
                        Add Medication
                      </button>
                    </div>

                    {patientContext.current_medications?.map(
                      (medication, index) => (
                        <div key={index} className="flex gap-3 mb-4">
                          <input
                            type="text"
                            value={medication}
                            onChange={(e) =>
                              updateMedication(index, e.target.value)
                            }
                            placeholder="Medication name and dosage"
                            className="input-field-medical flex-1"
                          />
                          <button
                            type="button"
                            onClick={() => removeMedication(index)}
                            className="btn-danger px-4 py-3 flex items-center rounded-lg"
                          >
                            <X className="w-4 h-4" />
                          </button>
                        </div>
                      )
                    )}
                  </div>
                </div>
              )}
            </div>

            {/* Submit Button */}
            <div className="flex justify-end pt-8 border-t border-gray-200">
              <button
                type="submit"
                disabled={isLoading || !query.trim()}
                className="btn-primary flex items-center text-base px-8 py-4"
              >
                {isLoading ? (
                  <>
                    <div className="loading-spinner w-5 h-5 mr-3"></div>
                    Processing Query...
                  </>
                ) : (
                  <>
                    <Search className="w-5 h-5 mr-3" />
                    Get Clinical Recommendations
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Error Display */}
        {error && (
          <div className="alert-error slide-up">
            <div className="flex items-center">
              <AlertTriangle className="w-6 h-6 mr-4 flex-shrink-0" />
              <div>
                <h3 className="font-semibold text-lg">
                  Error Processing Query
                </h3>
                <p className="text-sm mt-1">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Results Display */}
        {response && (
          <div className="space-y-8 fade-in">
            {/* Query Status */}
            <div className="alert-success">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <CheckCircle className="w-6 h-6 mr-4 flex-shrink-0" />
                  <div>
                    <h3 className="font-bold text-lg">
                      Query Processed Successfully
                    </h3>
                    <p className="text-base mt-1">
                      AI analysis completed with high confidence
                    </p>
                  </div>
                </div>
                <div className="flex items-center text-sm bg-white bg-opacity-50 px-3 py-1 rounded-full">
                  <Clock className="w-4 h-4 mr-2" />
                  {response.processing_time_ms
                    ? `${response.processing_time_ms.toFixed(0)}ms`
                    : "N/A"}
                </div>
              </div>
            </div>

            {/* Recommendations */}
            {response.recommendations.map((rec, index) => (
              <div key={index} className="card-medical slide-up">
                <div className="flex items-start justify-between mb-8">
                  <div className="flex items-center">
                    <div className="w-14 h-14 bg-gradient-to-br from-medical-500 to-medical-700 rounded-2xl flex items-center justify-center mr-6 shadow-medical">
                      <Activity className="w-7 h-7 text-white" />
                    </div>
                    <div>
                      <h3 className="text-2xl font-bold text-gray-900">
                        Clinical Recommendation{" "}
                        {response.recommendations.length > 1 ? index + 1 : ""}
                      </h3>
                      <p className="text-base text-gray-600 mt-1">
                        Evidence-based guidance from medical literature
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <span
                      className={`badge ${
                        rec.evidence_level === "A"
                          ? "badge-success"
                          : rec.evidence_level === "B"
                          ? "badge-warning"
                          : "badge-error"
                      }`}
                    >
                      Level {rec.evidence_level}
                    </span>
                    <span className="badge-medical">
                      {(rec.confidence_score * 100).toFixed(0)}% confidence
                    </span>
                  </div>
                </div>

                <div className="space-y-8">
                  <div className="bg-gradient-to-br from-medical-50 to-white rounded-xl p-6 border border-medical-200">
                    <h4 className="font-bold text-gray-900 mb-4 flex items-center text-lg">
                      <Shield className="w-6 h-6 mr-3 text-medical-600" />
                      Recommendation
                    </h4>
                    <p className="text-gray-700 leading-relaxed text-base">
                      {rec.recommendation}
                    </p>
                  </div>

                  <div>
                    <h4 className="font-bold text-gray-900 mb-4 flex items-center text-lg">
                      <BookOpen className="w-6 h-6 mr-3 text-medical-600" />
                      Clinical Reasoning
                    </h4>
                    <p className="text-gray-700 leading-relaxed text-base">
                      {rec.reasoning}
                    </p>
                  </div>

                  {rec.considerations.length > 0 && (
                    <div>
                      <h4 className="font-bold text-gray-900 mb-4 flex items-center">
                        <Activity className="w-5 h-5 mr-2 text-medical-600" />
                        Key Considerations
                      </h4>
                      <ul className="space-y-3">
                        {rec.considerations.map((consideration, i) => (
                          <li key={i} className="flex items-start">
                            <div className="w-2 h-2 bg-medical-500 rounded-full mt-2.5 mr-4 flex-shrink-0"></div>
                            <span className="text-gray-700 leading-relaxed">
                              {consideration}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {rec.contraindications.length > 0 && (
                    <div className="alert-critical">
                      <h4 className="font-bold text-error-900 mb-4 flex items-center">
                        <AlertTriangle className="w-5 h-5 mr-2" />
                        Contraindications
                      </h4>
                      <ul className="space-y-3">
                        {rec.contraindications.map((contraindication, i) => (
                          <li key={i} className="flex items-start">
                            <div className="w-2 h-2 bg-error-600 rounded-full mt-2.5 mr-4 flex-shrink-0"></div>
                            <span className="text-error-800 leading-relaxed font-medium">
                              {contraindication}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {rec.monitoring.length > 0 && (
                    <div>
                      <h4 className="font-bold text-gray-900 mb-4 flex items-center">
                        <Activity className="w-5 h-5 mr-2 text-info-600" />
                        Monitoring Requirements
                      </h4>
                      <ul className="space-y-3">
                        {rec.monitoring.map((monitor, i) => (
                          <li key={i} className="flex items-start">
                            <div className="w-2 h-2 bg-info-500 rounded-full mt-2.5 mr-4 flex-shrink-0"></div>
                            <span className="text-gray-700 leading-relaxed">
                              {monitor}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            ))}

            {/* Drug Interactions */}
            {response.drug_interactions.length > 0 && (
              <div className="alert-warning slide-up">
                <h3 className="text-lg font-bold text-warning-900 mb-4 flex items-center">
                  <AlertTriangle className="w-6 h-6 mr-3" />
                  Drug Interactions Detected
                </h3>
                <div className="space-y-4">
                  {response.drug_interactions.map((interaction, index) => (
                    <div
                      key={index}
                      className="bg-white p-6 rounded-lg border border-warning-300 shadow-sm"
                    >
                      <div className="flex items-center justify-between mb-3">
                        <span className="font-bold text-gray-900 text-lg">
                          {interaction.drug1} + {interaction.drug2}
                        </span>
                        <span
                          className={`badge ${
                            interaction.severity === "contraindicated"
                              ? "badge-critical"
                              : interaction.severity === "major"
                              ? "badge-error"
                              : interaction.severity === "moderate"
                              ? "badge-warning"
                              : "badge-gray"
                          }`}
                        >
                          {interaction.severity.toUpperCase()}
                        </span>
                      </div>
                      <p className="text-gray-700 mb-3 leading-relaxed">
                        {interaction.description}
                      </p>
                      <p className="text-sm text-gray-600 bg-gray-50 p-3 rounded-lg">
                        <strong>Management:</strong> {interaction.management}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Additional Information */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {response.differential_diagnoses.length > 0 && (
                <div className="card slide-up">
                  <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
                    <Activity className="w-5 h-5 mr-2 text-medical-600" />
                    Differential Diagnoses
                  </h3>
                  <ul className="space-y-3">
                    {response.differential_diagnoses.map((diagnosis, index) => (
                      <li key={index} className="flex items-start">
                        <div className="w-2 h-2 bg-gray-400 rounded-full mt-2.5 mr-4 flex-shrink-0"></div>
                        <span className="text-gray-700 leading-relaxed">
                          {diagnosis}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {response.next_steps.length > 0 && (
                <div className="card slide-up">
                  <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
                    <CheckCircle className="w-5 h-5 mr-2 text-success-600" />
                    Recommended Next Steps
                  </h3>
                  <ul className="space-y-3">
                    {response.next_steps.map((step, index) => (
                      <li key={index} className="flex items-start">
                        <div className="w-2 h-2 bg-success-500 rounded-full mt-2.5 mr-4 flex-shrink-0"></div>
                        <span className="text-gray-700 leading-relaxed">
                          {step}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Red Flags */}
            {response.red_flags.length > 0 && (
              <div className="alert-critical slide-up">
                <div className="flex items-center mb-4">
                  <AlertTriangle className="w-6 h-6 mr-3" />
                  <h3 className="text-xl font-bold text-error-900">
                    Critical Warnings & Red Flags
                  </h3>
                </div>
                <ul className="space-y-4">
                  {response.red_flags.map((flag, index) => (
                    <li key={index} className="flex items-start">
                      <div className="w-2 h-2 bg-error-600 rounded-full mt-2.5 mr-4 flex-shrink-0"></div>
                      <span className="text-error-800 font-semibold leading-relaxed">
                        {flag}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default ClinicalQuery
