import React, { useState } from "react"
import {
  Search,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Info,
  Plus,
  Trash2,
  Pill,
  Shield,
  Activity,
} from "lucide-react"

interface DrugInteraction {
  drug1: string
  drug2: string
  severity: "minor" | "moderate" | "major" | "contraindicated"
  description: string
  clinical_effects: string
  management: string
}

interface DrugSummary {
  name: string
  generic_name: string
  drug_class: string
  indications: string[]
  contraindications: string[]
  common_side_effects: string[]
  dosage_info: string
}

const DrugInteractions: React.FC = () => {
  const [medications, setMedications] = useState<string[]>([""])
  const [interactions, setInteractions] = useState<DrugInteraction[]>([])
  const [drugSummaries, setDrugSummaries] = useState<DrugSummary[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const addMedication = () => {
    setMedications([...medications, ""])
  }

  const removeMedication = (index: number) => {
    if (medications.length > 1) {
      setMedications(medications.filter((_, i) => i !== index))
    }
  }

  const updateMedication = (index: number, value: string) => {
    const updated = [...medications]
    updated[index] = value
    setMedications(updated)
  }

  const checkInteractions = async () => {
    const validMedications = medications.filter((med) => med.trim() !== "")

    if (validMedications.length < 2) {
      setError("Please enter at least 2 medications to check for interactions")
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await fetch("http://localhost:8000/drugs/interactions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(validMedications),
      })

      if (!response.ok) {
        throw new Error("Failed to check drug interactions")
      }

      const data = await response.json()
      setInteractions(data)

      // Also fetch drug summaries
      const summaryPromises = validMedications.map(async (med) => {
        const summaryResponse = await fetch(
          `http://localhost:8000/drugs/summary?drug_name=${encodeURIComponent(
            med
          )}`
        )
        if (summaryResponse.ok) {
          return summaryResponse.json()
        }
        return null
      })

      const summaries = await Promise.all(summaryPromises)
      setDrugSummaries(summaries.filter(Boolean))
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred")
    } finally {
      setLoading(false)
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "minor":
        return "text-yellow-600 bg-yellow-50 border-yellow-200"
      case "moderate":
        return "text-orange-600 bg-orange-50 border-orange-200"
      case "major":
        return "text-red-600 bg-red-50 border-red-200"
      case "contraindicated":
        return "text-red-800 bg-red-100 border-red-300"
      default:
        return "text-gray-600 bg-gray-50 border-gray-200"
    }
  }

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case "minor":
        return <Info className="h-4 w-4" />
      case "moderate":
        return <AlertTriangle className="h-4 w-4" />
      case "major":
        return <XCircle className="h-4 w-4" />
      case "contraindicated":
        return <XCircle className="h-4 w-4" />
      default:
        return <Info className="h-4 w-4" />
    }
  }

  return (
    <div className="mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 fade-in">
        <div className="flex items-start space-x-3 mb-4">
          <div className="lg:w-12 lg:h-12 w-8 h-8 p-2 bg-gradient-to-br from-medical-500 to-medical-700 rounded-xl flex items-center justify-center shadow-medical">
            <Pill className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl text-left font-bold text-gray-900">
              Drug Interaction Checker
            </h1>
            <p className="text-gray-600 text-left">
              Check for potential drug interactions and get detailed medication
              information
            </p>
          </div>
        </div>
      </div>

      {/* Medication Input Section */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 slide-up">
        <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Search className="h-5 w-5 mr-2 text-medical-600" />
          Enter Medications
        </h2>

        <div className="space-y-4">
          {medications.map((medication, index) => (
            <div key={index} className="flex items-center space-x-3">
              <div className="flex-1">
                <input
                  type="text"
                  value={medication}
                  onChange={(e) => updateMedication(index, e.target.value)}
                  placeholder="Enter medication name (e.g., Warfarin, Aspirin)"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-medical-500 focus:border-medical-500"
                />
              </div>
              {medications.length > 1 && (
                <button
                  onClick={() => removeMedication(index)}
                  className="p-3 text-red-500 hover:text-red-700 hover:bg-red-50 rounded-lg transition-colors"
                >
                  <Trash2 className="h-5 w-5" />
                </button>
              )}
            </div>
          ))}

          <button
            onClick={addMedication}
            className="flex items-center space-x-2 text-medical-600 hover:text-medical-700 font-medium"
          >
            <Plus className="h-4 w-4" />
            <span>Add Another Medication</span>
          </button>
        </div>

        <div className="mt-6">
          <button
            onClick={checkInteractions}
            disabled={
              loading ||
              medications.filter((med) => med.trim() !== "").length < 2
            }
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Checking Interactions...</span>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Shield className="h-4 w-4" />
                <span>Check Drug Interactions</span>
              </div>
            )}
          </button>
        </div>

        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center">
              <XCircle className="h-5 w-5 text-red-500 mr-2" />
              <span className="text-red-700">{error}</span>
            </div>
          </div>
        )}
      </div>

      {/* Results Section */}
      {interactions.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <AlertTriangle className="h-5 w-5 mr-2 text-red-600" />
            Drug Interactions Found
          </h2>

          <div className="space-y-4">
            {interactions.map((interaction, index) => (
              <div
                key={index}
                className="border border-gray-200 rounded-lg p-4"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    <div
                      className={`p-2 rounded-lg border ${getSeverityColor(
                        interaction.severity
                      )}`}
                    >
                      {getSeverityIcon(interaction.severity)}
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">
                        {interaction.drug1} + {interaction.drug2}
                      </h3>
                      <span
                        className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(
                          interaction.severity
                        )}`}
                      >
                        {interaction.severity.toUpperCase()}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="space-y-3">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-1">
                      Description
                    </h4>
                    <p className="text-gray-700">{interaction.description}</p>
                  </div>

                  <div>
                    <h4 className="font-medium text-gray-900 mb-1">
                      Clinical Effects
                    </h4>
                    <p className="text-gray-700">
                      {interaction.clinical_effects}
                    </p>
                  </div>

                  <div>
                    <h4 className="font-medium text-gray-900 mb-1">
                      Management
                    </h4>
                    <p className="text-gray-700">{interaction.management}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Drug Summaries Section */}
      {drugSummaries.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Activity className="h-5 w-5 mr-2 text-medical-600" />
            Medication Information
          </h2>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {drugSummaries.map((summary, index) => (
              <div
                key={index}
                className="border border-gray-200 rounded-lg p-4"
              >
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-10 h-10 bg-medical-100 rounded-lg flex items-center justify-center">
                    <Pill className="h-5 w-5 text-medical-600" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">
                      {summary.name}
                    </h3>
                    <p className="text-sm text-gray-600">
                      {summary.generic_name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {summary.drug_class}
                    </p>
                  </div>
                </div>

                <div className="space-y-3">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-1">
                      Indications
                    </h4>
                    <p className="text-sm text-gray-700">
                      {summary.indications.join(", ")}
                    </p>
                  </div>

                  <div>
                    <h4 className="font-medium text-gray-900 mb-1">
                      Common Side Effects
                    </h4>
                    <p className="text-sm text-gray-700">
                      {summary.common_side_effects.join(", ")}
                    </p>
                  </div>

                  <div>
                    <h4 className="font-medium text-gray-900 mb-1">
                      Dosage Information
                    </h4>
                    <p className="text-sm text-gray-700">
                      {summary.dosage_info}
                    </p>
                  </div>

                  {summary.contraindications.length > 0 && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-1">
                        Contraindications
                      </h4>
                      <p className="text-sm text-red-600">
                        {summary.contraindications.join(", ")}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* No Interactions Message */}
      {interactions.length === 0 &&
        !loading &&
        medications.filter((med) => med.trim() !== "").length >= 2 && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-6">
            <div className="flex items-center">
              <CheckCircle className="h-6 w-6 text-green-600 mr-3" />
              <div>
                <h3 className="font-semibold text-green-800">
                  No Drug Interactions Found
                </h3>
                <p className="text-green-700">
                  The medications you entered do not have any known significant
                  interactions.
                </p>
              </div>
            </div>
          </div>
        )}
    </div>
  )
}

export default DrugInteractions
