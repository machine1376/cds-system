import React, { useState, useEffect } from "react"
import {
  Search,
  BookOpen,
  Calendar,
  Users,
  AlertTriangle,
  CheckCircle,
  ExternalLink,
} from "lucide-react"

interface Guideline {
  id: string
  title: string
  organization: string
  specialty: string
  publication_year: number
  evidence_level: string
  last_updated: string
  summary: string
  url?: string
  doi?: string
}

interface DetailedGuideline extends Guideline {
  content: string
  key_recommendations: Array<{
    recommendation: string
    class: string
    level_of_evidence: string
    rationale: string
  }>
  contraindications: string[]
  monitoring_requirements: string[]
  patient_populations: string[]
  clinical_scenarios: string[]
  references: string[]
}

interface DatabaseStats {
  total_guidelines: number
  specialties_count: number
  last_updated: string
  coverage_percentage: number
  specialties: Record<string, number>
  latest_year: number
  evidence_levels: {
    A: number
    B: number
    C: number
    D: number
  }
}

interface GuidelinesAPIClient {
  searchGuidelines: (query: string, specialty?: string) => Promise<Guideline[]>
  getGuideline: (id: string) => Promise<DetailedGuideline>
  getGuidelinesBySpecialty: (specialty: string) => Promise<Guideline[]>
  getDatabaseStats: () => Promise<DatabaseStats>
}

const guidelinesAPI: GuidelinesAPIClient = {
  searchGuidelines: async (query: string, specialty?: string) => {
    const params = new URLSearchParams({ query })
    if (specialty) params.append("specialty", specialty)

    const response = await fetch(`http://localhost:8000/guidelines/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, specialty, max_results: 20 }),
    })
    return response.json()
  },

  getGuideline: async (id: string) => {
    const response = await fetch(`http://localhost:8000/guidelines/${id}`)
    return response.json()
  },

  getGuidelinesBySpecialty: async (specialty: string) => {
    const response = await fetch(
      `http://localhost:8000/guidelines/specialty/${specialty}`
    )
    return response.json()
  },

  getDatabaseStats: async () => {
    const response = await fetch(
      `http://localhost:8000/guidelines/stats/database`
    )
    return response.json()
  },
}

const GuidelinesExplorer: React.FC = () => {
  const [guidelines, setGuidelines] = useState<Guideline[]>([])
  const [selectedGuideline, setSelectedGuideline] =
    useState<DetailedGuideline | null>(null)
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedSpecialty, setSelectedSpecialty] = useState("")
  const [loading, setLoading] = useState(false)
  const [stats, setStats] = useState<DatabaseStats | null>(null)

  const specialties = [
    "cardiology",
    "endocrinology",
    "emergency_medicine",
    "infectious_disease",
    "neurology",
  ]

  useEffect(() => {
    loadInitialData()
  }, [])

  const loadInitialData = async () => {
    try {
      const [initialGuidelines, databaseStats] = await Promise.all([
        guidelinesAPI.searchGuidelines(""),
        guidelinesAPI.getDatabaseStats(),
      ])
      setGuidelines(initialGuidelines)
      setStats(databaseStats)
    } catch (error) {
      console.error("Error loading initial data:", error)
    }
  }

  const handleSearch = async () => {
    if (!searchQuery.trim() && !selectedSpecialty) return

    setLoading(true)
    try {
      const results = selectedSpecialty
        ? await guidelinesAPI.getGuidelinesBySpecialty(selectedSpecialty)
        : await guidelinesAPI.searchGuidelines(searchQuery, selectedSpecialty)

      setGuidelines(results)
    } catch (error) {
      console.error("Error searching guidelines:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleGuidelineSelect = async (guideline: Guideline) => {
    setLoading(true)
    try {
      const detailed = await guidelinesAPI.getGuideline(guideline.id)
      setSelectedGuideline(detailed)
    } catch (error) {
      console.error("Error loading guideline details:", error)
    } finally {
      setLoading(false)
    }
  }

  const getEvidenceLevelColor = (level: string) => {
    switch (level.toUpperCase()) {
      case "A":
        return "bg-green-100 text-green-800"
      case "B":
        return "bg-yellow-100 text-yellow-800"
      case "C":
        return "bg-red-100 text-red-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const getRecommendationClassColor = (recClass: string) => {
    switch (recClass.toUpperCase()) {
      case "I":
      case "STRONG":
        return "bg-green-100 text-green-800"
      case "IIA":
      case "MODERATE":
        return "bg-blue-100 text-blue-800"
      case "IIB":
      case "WEAK":
        return "bg-yellow-100 text-yellow-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  return (
    <div className="w-full max-w-7xl mx-auto p-4 sm:p-6 space-y-4 sm:space-y-6">
      {/* Header */}
      <div className="text-center px-2 sm:px-0 fade-in">
        <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-2">
          Clinical Practice Guidelines
        </h1>
        <p className="text-sm sm:text-base text-gray-600 max-w-3xl mx-auto">
          Evidence-based recommendations from major medical organizations
        </p>
      </div>

      {/* Statistics Cards */}
      {stats && (
        <div className="grid grid-cols-2 2xl:grid-cols-4 gap-3 sm:gap-4">
          <div className="bg-white rounded-xl p-4 sm:p-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow slide-up">
            <div className="flex items-start">
              <BookOpen className="w-6 h-6 sm:w-8 sm:h-8 text-medical-600 mr-2 sm:mr-3 flex-shrink-0" />
              <div className="min-w-0">
                <p className="text-xs sm:text-sm font-medium text-gray-600 truncate">
                  Total Guidelines
                </p>
                <p className="text-lg sm:text-2xl font-bold text-gray-900">
                  {stats.total_guidelines}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-4 sm:p-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow slide-up">
            <div className="flex items-start">
              <Users className="w-6 h-6 sm:w-8 sm:h-8 text-blue-600 mr-2 sm:mr-3 flex-shrink-0" />
              <div className="min-w-0">
                <p className="text-xs sm:text-sm font-medium text-gray-600 truncate">
                  Specialties
                </p>
                <p className="text-lg sm:text-2xl font-bold text-gray-900">
                  {Object.keys(stats.specialties).length}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-4 sm:p-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow slide-up">
            <div className="flex items-start">
              <Calendar className="w-6 h-6 sm:w-8 sm:h-8 text-green-600 mr-2 sm:mr-3 flex-shrink-0" />
              <div className="min-w-0">
                <p className="text-xs sm:text-sm font-medium text-gray-600 truncate">
                  Latest Year
                </p>
                <p className="text-lg sm:text-2xl font-bold text-gray-900">
                  {stats.latest_year}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-4 sm:p-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow slide-up">
            <div className="flex items-start">
              <CheckCircle className="w-6 h-6 sm:w-8 sm:h-8 text-purple-600 mr-2 sm:mr-3 flex-shrink-0" />
              <div className="min-w-0">
                <p className="text-xs sm:text-sm font-medium text-gray-600 truncate">
                  Level A Evidence
                </p>
                <p className="text-lg sm:text-2xl font-bold text-gray-900">
                  {stats.evidence_levels?.A || 0}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Search Interface */}
      <div className="bg-white rounded-xl p-4 sm:p-6 shadow-sm border border-gray-200 slide-up">
        <div className="flex items-start mb-4">
          <Search className="w-5 h-5 text-medical-600 mr-2 flex-shrink-0" />
          <h2 className="text-lg sm:text-xl font-semibold text-gray-900">
            Search Clinical Guidelines
          </h2>
        </div>

        <div className="space-y-4 sm:space-y-0 sm:grid sm:grid-cols-12 sm:gap-4">
          <div className="sm:col-span-5">
            <label className="block text-left text-sm font-medium text-gray-700 mb-2">
              Search Query
            </label>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="e.g., diabetes management, acute coronary syndrome..."
              className="w-full px-4 py-3 text-base border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-medical-500 focus:border-medical-500 bg-gray-50 focus:bg-white transition-all duration-200"
              onKeyPress={(e) => e.key === "Enter" && handleSearch()}
            />
          </div>

          <div className="sm:col-span-4">
            <label className="block text-left text-sm font-medium text-gray-700 mb-2">
              Medical Specialty
            </label>
            <div className="relative">
              <select
                value={selectedSpecialty}
                onChange={(e) => setSelectedSpecialty(e.target.value)}
                className="w-full px-4 py-3 text-base border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-medical-500 focus:border-medical-500 bg-gray-50 focus:bg-white transition-all duration-200 appearance-none cursor-pointer"
                style={{
                  backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e")`,
                  backgroundPosition: "right 12px center",
                  backgroundRepeat: "no-repeat",
                  backgroundSize: "16px",
                }}
              >
                <option value="">All Specialties</option>
                {specialties.map((specialty) => (
                  <option key={specialty} value={specialty}>
                    {specialty
                      .replace("_", " ")
                      .replace(/\b\w/g, (l) => l.toUpperCase())}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="sm:col-span-3">
            <label className="block text-sm font-medium text-gray-700 mb-2 sm:hidden">
              Search
            </label>
            <div className="sm:pt-7">
              <button
                onClick={handleSearch}
                disabled={loading}
                className="w-full px-6 py-3 bg-medical-600 text-white font-semibold rounded-lg hover:bg-medical-700 focus:outline-none focus:ring-2 focus:ring-medical-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-sm hover:shadow-md"
              >
                {loading ? "Searching..." : "Search"}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:gap-6">
        {/* Guidelines List */}
        <div className="xl:col-span-1 order-2 xl:order-1">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 h-96 sm:h-[32rem] xl:h-96 overflow-hidden flex flex-col slide-up">
            <div className="p-4 sm:p-6 border-b border-gray-200 flex-shrink-0">
              <h3 className="text-left text-lg font-semibold text-gray-900">
                Guidelines ({guidelines.length})
              </h3>
            </div>

            <div className="flex-1 overflow-y-auto p-4 sm:p-6 pt-0 sm:pt-0">
              {guidelines.length === 0 ? (
                  <div className="flex flex-col items-start justify-center h-full text-left py-8 px-4">
                  <BookOpen className="w-12 h-12 text-gray-300 mb-4" />
                  <p className="text-gray-500 text-sm sm:text-base">
                    No guidelines found. Try searching or selecting a specialty.
                  </p>
                </div>
              ) : (
                <div className="space-y-3">
                  {guidelines.map((guideline) => (
                    <div
                      key={guideline.id}
                      onClick={() => handleGuidelineSelect(guideline)}
                      className={`p-3 sm:p-4 border rounded-lg cursor-pointer transition-all duration-200 hover:shadow-sm ${
                        selectedGuideline?.id === guideline.id
                          ? "border-medical-500 bg-medical-50 shadow-sm"
                          : "border-gray-200 hover:border-gray-300"
                      }`}
                    >
                      <div className="flex items-start justify-between mb-2">
                        <h4 className="font-medium text-left text-sm sm:text-base leading-tight text-gray-900 pr-2">
                          {guideline.title}
                        </h4>
                        <span
                          className={`px-2 py-1 rounded text-left text-xs font-medium flex-shrink-0 ${getEvidenceLevelColor(
                            guideline.evidence_level
                          )}`}
                        >
                          Level {guideline.evidence_level}
                        </span>
                      </div>

                      <div className="text-left text-xs sm:text-sm text-gray-600 space-y-1">
                        <div className="truncate">
                          {guideline.organization} •{" "}
                          {guideline.publication_year}
                        </div>
                        <div className="capitalize">
                          {guideline.specialty.replace("_", " ")}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Detailed Guideline View */}
        <div className="xl:col-span-2 order-1 xl:order-2">
          {selectedGuideline ? (
            <div className="space-y-4 sm:space-y-6">
              {/* Guideline Header */}
              <div className="bg-white rounded-xl p-4 sm:p-6 shadow-sm border border-gray-200 slide-up">
                <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between mb-4 space-y-3 sm:space-y-0">
                  <div className="flex-1 min-w-0">
                    <h2 className="text-left text-lg sm:text-xl lg:text-2xl font-bold text-gray-900 mb-2 leading-tight">
                      {selectedGuideline.title}
                    </h2>
                    <div className="flex flex-wrap items-center gap-2 sm:gap-4 text-sm text-gray-600">
                      <span className="truncate">
                        {selectedGuideline.organization}
                      </span>
                      <span className="hidden sm:inline">•</span>
                      <span>{selectedGuideline.publication_year}</span>
                      <span className="hidden sm:inline">•</span>
                      <span className="capitalize">
                        {selectedGuideline.specialty.replace("_", " ")}
                      </span>
                    </div>
                  </div>

                  <div className="flex flex-col sm:flex-row items-start sm:items-center space-y-2 sm:space-y-0 sm:space-x-2">
                    <span
                      className={`px-3 py-1 rounded-full text-left text-xs sm:text-sm font-medium ${getEvidenceLevelColor(
                        selectedGuideline.evidence_level
                      )}`}
                    >
                      Evidence Level {selectedGuideline.evidence_level}
                    </span>
                    {selectedGuideline.url && (
                      <a
                        href={selectedGuideline.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="p-2 text-medical-600 hover:bg-medical-50 rounded-lg transition-colors"
                        aria-label="Open guideline in new tab"
                      >
                        <ExternalLink className="w-4 h-4" />
                      </a>
                    )}
                  </div>
                </div>

                <p className="text-left text-sm sm:text-base text-gray-700 leading-relaxed">
                  {selectedGuideline.summary}
                </p>

                {selectedGuideline.patient_populations.length > 0 && (
                  <div className="mt-4">
                    <h4 className="font-medium text-left text-gray-900 mb-2 text-sm sm:text-base">
                      Patient Populations:
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {selectedGuideline.patient_populations.map(
                        (population, index) => (
                          <span
                            key={index}
                            className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs sm:text-sm"
                          >
                            {population}
                          </span>
                        )
                      )}
                    </div>
                  </div>
                )}
              </div>

              {/* Key Recommendations */}
              {selectedGuideline.key_recommendations.length > 0 && (
                <div className="bg-white rounded-xl p-4 sm:p-6 shadow-sm border border-gray-200 slide-up">
                  <h3 className="text-lg font-semibold mb-4 text-gray-900">
                    Key Recommendations
                  </h3>
                  <div className="space-y-4">
                    {selectedGuideline.key_recommendations.map((rec, index) => (
                      <div
                        key={index}
                        className="border-l-4 border-medical-500 pl-4 py-2"
                      >
                        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between mb-2 space-y-2 sm:space-y-0">
                          <p className="font-medium text-left text-gray-900 text-sm sm:text-base leading-relaxed pr-2">
                            {rec.recommendation}
                          </p>
                          <span
                            className={`px-2 py-1 rounded text-left text-xs font-medium flex-shrink-0 ${getRecommendationClassColor(
                              rec.class
                            )}`}
                          >
                            Class {rec.class}
                          </span>
                        </div>
                        <p className="text-left text-xs sm:text-sm text-gray-600 mb-1">
                          <strong>Evidence Level:</strong>{" "}
                          {rec.level_of_evidence}
                        </p>
                        {rec.rationale && (
                          <p className="text-left text-xs sm:text-sm text-gray-600">
                            <strong>Rationale:</strong> {rec.rationale}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Contraindications and Monitoring */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
                {selectedGuideline.contraindications.length > 0 && (
                  <div className="bg-red-50 border border-red-200 rounded-xl p-4 sm:p-6 slide-up">
                    <div className="flex items-center mb-3">
                      <AlertTriangle className="w-5 h-5 text-red-600 mr-2 flex-shrink-0" />
                      <h3 className="text-lg font-semibold text-red-900">
                        Contraindications
                      </h3>
                    </div>
                    <ul className="list-disc list-inside text-left text-red-800 space-y-1">
                      {selectedGuideline.contraindications.map(
                        (contraindication, index) => (
                          <li key={index} className="text-left text-sm leading-relaxed">
                            {contraindication}
                          </li>
                        )
                      )}
                    </ul>
                  </div>
                )}

                {selectedGuideline.monitoring_requirements.length > 0 && (
                  <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 sm:p-6 slide-up">
                    <div className="flex items-center mb-3">
                      <CheckCircle className="w-5 h-5 text-blue-600 mr-2 flex-shrink-0" />
                      <h3 className="text-lg font-semibold text-blue-900">
                        Monitoring Requirements
                      </h3>
                    </div>
                    <ul className="list-disc list-inside text-left text-blue-800 space-y-1">
                      {selectedGuideline.monitoring_requirements.map(
                        (requirement, index) => (
                          <li key={index} className="text-left text-sm leading-relaxed">
                            {requirement}
                          </li>
                        )
                      )}
                    </ul>
                  </div>
                )}
              </div>

              {/* Clinical Scenarios */}
              {selectedGuideline.clinical_scenarios.length > 0 && (
                <div className="bg-white rounded-xl p-4 sm:p-6 shadow-sm border border-gray-200 slide-up">
                  <h3 className="text-lg font-semibold mb-3 text-gray-900">
                    Applicable Clinical Scenarios
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {selectedGuideline.clinical_scenarios.map(
                      (scenario, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs sm:text-sm"
                        >
                          {scenario}
                        </span>
                      )
                    )}
                  </div>
                </div>
              )}

              {/* References */}
              {selectedGuideline.references.length > 0 && (
                <div className="bg-white rounded-xl p-4 sm:p-6 shadow-sm border border-gray-200 slide-up">
                  <h3 className="text-lg font-semibold mb-3 text-gray-900">
                    References
                  </h3>
                  <div className="space-y-2">
                    {selectedGuideline.references.map((reference, index) => (
                      <div
                        key={index}
                        className="text-left text-xs sm:text-sm text-gray-600 border-l-2 border-gray-200 pl-3 leading-relaxed"
                      >
                        {reference}
                      </div>
                    ))}
                  </div>
                  {selectedGuideline.doi && (
                    <div className="mt-3 pt-3 border-t border-gray-200">
                      <p className="text-left text-xs sm:text-sm text-gray-600">
                        <strong>DOI:</strong> {selectedGuideline.doi}
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>
          ) : (
            <div className="bg-white rounded-xl h-96 sm:h-[32rem] xl:h-96 flex items-center justify-center shadow-sm border border-gray-200 slide-up">
              <div className="text-left text-gray-500 px-4">
                <BookOpen className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                <p className="text-lg font-medium mb-2">
                  Select a guideline to view details
                </p>
                <p className="text-sm">
                  Choose from the list to see comprehensive recommendations
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default GuidelinesExplorer

// Add this component to your main App.tsx or create a separate route
// Example integration in App.tsx:

/*
import GuidelinesExplorer from './components/GuidelinesExplorer';

// Add to your routing or main component
<Route path="/guidelines" component={GuidelinesExplorer} />
*/
