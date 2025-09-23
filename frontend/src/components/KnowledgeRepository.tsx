import React, { useState, useEffect } from "react"
import {
  BookOpen,
  Search,
  Filter,
  Download,
  RefreshCw,
  BarChart3,
  TrendingUp,
  Shield,
  AlertCircle,
  Eye,
  ExternalLink,
  FileText,
  ChevronDown,
  ChevronUp,
  Clock,
  CheckCircle,
} from "lucide-react"
import { knowledgeRepositoryAPI } from "../services/api"

interface RepositoryStats {
  total_documents: number
  document_types: Record<string, number>
  evidence_levels: Record<string, number>
  access_levels: Record<string, number>
  quality_metrics: {
    average_quality_score: number
    peer_reviewed_percentage: number
    open_access_percentage: number
    recent_content_percentage: number
  }
  content_coverage: Record<string, any>
  processing_status: Record<string, number>
}

interface DocumentSummary {
  document_id: string
  title: string
  document_type: string
  evidence_level: string
  publication_date: string
  authors: string[]
  journal: string
  abstract: string
  specialties: string[]
  quality_score: number
  citation_count: number
  access_level: string
}

interface QualityReport {
  report_generated: string
  quality_assessment: {
    overall_quality_score: number
    evidence_quality_score: number
    content_freshness: {
      recent_content_5y: number
      very_recent_content_2y: number
      freshness_score: number
    }
    source_diversity: {
      unique_journals: number
      unique_publishers: number
      diversity_score: number
    }
    access_quality: {
      open_access_percentage: number
      peer_reviewed_percentage: number
      subscription_access_percentage: number
    }
    processing_quality: {
      average_confidence: number
      validation_rate: number
      embedding_completion: number
    }
    coverage_analysis: Record<string, any>
    recommendations: string[]
  }
  summary: {
    overall_grade: string
    strengths: string[]
    improvement_areas: string[]
  }
}

const KnowledgeRepository: React.FC = () => {
  const [stats, setStats] = useState<RepositoryStats | null>(null)
  const [documents, setDocuments] = useState<DocumentSummary[]>([])
  const [qualityReport, setQualityReport] = useState<QualityReport | null>(null)
  const [searchQuery, setSearchQuery] = useState("")
  const [filters, setFilters] = useState({
    specialty: "",
    document_type: "",
    evidence_level: "",
    access_level: "",
  })
  const [loading, setLoading] = useState(true)
  const [searchLoading, setSearchLoading] = useState(false)
  const [activeTab, setActiveTab] = useState("overview")
  const [showFilters, setShowFilters] = useState(false)
  const [selectedDocuments, setSelectedDocuments] = useState<string[]>([])

  useEffect(() => {
    loadRepositoryData()
  }, [])

  const loadRepositoryData = async () => {
    setLoading(true)
    try {
      const [statsData, qualityData] = await Promise.all([
        knowledgeRepositoryAPI.getOverview(),
        knowledgeRepositoryAPI.getQualityReport(),
      ])

      setStats(statsData)
      setQualityReport(qualityData)
    } catch (error) {
      console.error("Error loading repository data:", error)
    } finally {
      setLoading(false)
    }
  }

  const searchDocuments = async () => {
    setSearchLoading(true)
    try {
      const searchRequest = {
        query: searchQuery,
        ...filters,
        max_results: 50,
      }

      const results = await knowledgeRepositoryAPI.searchDocuments(
        searchRequest
      )
      setDocuments(results)
    } catch (error) {
      console.error("Error searching documents:", error)
    } finally {
      setSearchLoading(false)
    }
  }

  const exportBibliography = async (format: string = "bibtex") => {
    if (selectedDocuments.length === 0) {
      alert("Please select documents to export")
      return
    }

    try {
      const data = await knowledgeRepositoryAPI.exportBibliography(
        selectedDocuments,
        format
      )

      // Create and download file
      const blob = new Blob([data.bibliography.join("\n\n")], {
        type: "text/plain",
      })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `bibliography.${format}`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error("Error exporting bibliography:", error)
    }
  }

  const getQualityColor = (score: number) => {
    if (score >= 0.9) return "text-green-600 bg-green-100"
    if (score >= 0.8) return "text-blue-600 bg-blue-100"
    if (score >= 0.7) return "text-yellow-600 bg-yellow-100"
    return "text-red-600 bg-red-100"
  }

  const getEvidenceLevelColor = (level: string) => {
    switch (level.toUpperCase()) {
      case "A":
        return "bg-green-100 text-green-800"
      case "B":
        return "bg-blue-100 text-blue-800"
      case "C":
        return "bg-yellow-100 text-yellow-800"
      case "D":
        return "bg-red-100 text-red-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const getGradeColor = (grade: string) => {
    switch (grade) {
      case "A":
        return "text-green-600 bg-green-50"
      case "B":
        return "text-blue-600 bg-blue-50"
      case "C":
        return "text-yellow-600 bg-yellow-50"
      case "D":
        return "text-red-600 bg-red-50"
      default:
        return "text-gray-600 bg-gray-50"
    }
  }

  const toggleDocumentSelection = (docId: string) => {
    setSelectedDocuments((prev) =>
      prev.includes(docId)
        ? prev.filter((id) => id !== docId)
        : [...prev, docId]
    )
  }

  if (loading && !stats) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-medical-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-left text-gray-900">
            Knowledge Repository
          </h1>
          <p className="text-left text-gray-600">
            Manage and explore medical literature database
          </p>
        </div>
        <div className="flex items-center space-x-3">
          {selectedDocuments.length > 0 && (
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-600">
                {selectedDocuments.length} selected
              </span>
              <button
                onClick={() => exportBibliography("bibtex")}
                className="btn-secondary flex items-center text-sm"
              >
                <Download className="w-4 h-4 mr-2" />
                Export BibTeX
              </button>
              <button
                onClick={() => exportBibliography("apa")}
                className="btn-secondary flex items-center text-sm"
              >
                <Download className="w-4 h-4 mr-2" />
                Export APA
              </button>
            </div>
          )}
          <button
            onClick={loadRepositoryData}
            className="btn-secondary flex items-center"
          >
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </button>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="flex space-x-8">
          {[
            { id: "overview", label: "Overview", icon: BarChart3 },
            { id: "search", label: "Search Documents", icon: Search },
            { id: "quality", label: "Quality Report", icon: Shield },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? "border-medical-500 text-medical-600"
                  : "border-transparent text-gray-500 hover:text-gray-700"
              }`}
            >
              <tab.icon className="w-4 h-4 mr-2" />
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Overview Tab */}
      {activeTab === "overview" && stats && (
        <div className="space-y-6">
          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="card flex justify-center">
              <div className="flex items-start">
                <BookOpen className="w-8 h-8 text-medical-600 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-600">
                    Total Documents
                  </p>
                  <p className="text-2xl font-bold text-gray-900">
                    {stats.total_documents.toLocaleString()}
                  </p>
                </div>
              </div>
            </div>

            <div className="card flex justify-center">
              <div className="flex items-start">
                <Shield className="w-8 h-8 text-green-600 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-600">
                    Avg Quality Score
                  </p>
                  <p className="text-2xl font-bold text-gray-900">
                    {stats.quality_metrics.average_quality_score?.toFixed(2)}
                  </p>
                </div>
              </div>
            </div>

            <div className="card flex justify-center">
              <div className="flex items-start">
                <TrendingUp className="w-8 h-8 text-blue-600 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-600">
                    Peer Reviewed
                  </p>
                  <p className="text-2xl font-bold text-gray-900">
                    {stats.quality_metrics.peer_reviewed_percentage?.toFixed(0)}
                    %
                  </p>
                </div>
              </div>
            </div>

            <div className="card flex justify-center">
              <div className="flex items-start">
                <Eye className="w-8 h-8 text-purple-600 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-600">
                    Open Access
                  </p>
                  <p className="text-2xl font-bold text-gray-900">
                    {stats.quality_metrics.open_access_percentage?.toFixed(0)}%
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Distribution Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card">
              <h3 className="text-lg font-semibold mb-4">Document Types</h3>
              <div className="space-y-2">
                {Object.entries(stats.document_types).map(([type, count]) => (
                  <div key={type} className="flex justify-between items-center">
                    <span className="text-sm capitalize">
                      {type.replace("_", " ")}
                    </span>
                    <div className="flex items-center">
                      <div className="w-20 bg-gray-200 rounded-full h-2 mr-2">
                        <div
                          className="bg-medical-600 h-2 rounded-full"
                          style={{
                            width: `${(count / stats.total_documents) * 100}%`,
                          }}
                        ></div>
                      </div>
                      <span className="text-sm font-medium">{count}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold mb-4">Evidence Levels</h3>
              <div className="space-y-2">
                {Object.entries(stats.evidence_levels).map(([level, count]) => (
                  <div
                    key={level}
                    className="flex justify-between items-center"
                  >
                    <span
                      className={`text-sm px-2 py-1 rounded ${getEvidenceLevelColor(
                        level
                      )}`}
                    >
                      Level {level}
                    </span>
                    <div className="flex items-center">
                      <div className="w-20 bg-gray-200 rounded-full h-2 mr-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full"
                          style={{
                            width: `${(count / stats.total_documents) * 100}%`,
                          }}
                        ></div>
                      </div>
                      <span className="text-sm font-medium">{count}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Search Tab */}
      {activeTab === "search" && (
        <div className="space-y-6">
          {/* Search Interface */}
          <div className="card">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold">
                  Search Medical Literature
                </h3>
                <button
                  onClick={() => setShowFilters(!showFilters)}
                  className="btn-secondary flex items-center text-sm"
                >
                  <Filter className="w-4 h-4 mr-2" />
                  Filters
                  {showFilters ? (
                    <ChevronUp className="w-4 h-4 ml-1" />
                  ) : (
                    <ChevronDown className="w-4 h-4 ml-1" />
                  )}
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                <div className="md:col-span-2">
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search medical literature..."
                    className="input-field"
                    onKeyPress={(e) => e.key === "Enter" && searchDocuments()}
                  />
                </div>
                <button
                  onClick={searchDocuments}
                  disabled={searchLoading}
                  className="btn-primary disabled:opacity-50"
                >
                  {searchLoading ? "Searching..." : "Search"}
                </button>
              </div>

              {/* Advanced Filters */}
              {showFilters && (
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 pt-4 border-t border-gray-200">
                  <select
                    value={filters.specialty}
                    onChange={(e) =>
                      setFilters({ ...filters, specialty: e.target.value })
                    }
                    className="input-field"
                  >
                    <option value="">All Specialties</option>
                    <option value="cardiology">Cardiology</option>
                    <option value="endocrinology">Endocrinology</option>
                    <option value="infectious_disease">
                      Infectious Disease
                    </option>
                    <option value="emergency_medicine">
                      Emergency Medicine
                    </option>
                    <option value="oncology">Oncology</option>
                    <option value="neurology">Neurology</option>
                  </select>

                  <select
                    value={filters.document_type}
                    onChange={(e) =>
                      setFilters({ ...filters, document_type: e.target.value })
                    }
                    className="input-field"
                  >
                    <option value="">All Document Types</option>
                    <option value="research_paper">Research Paper</option>
                    <option value="clinical_guideline">
                      Clinical Guideline
                    </option>
                    <option value="systematic_review">Systematic Review</option>
                    <option value="case_study">Case Study</option>
                    <option value="meta_analysis">Meta Analysis</option>
                  </select>

                  <select
                    value={filters.evidence_level}
                    onChange={(e) =>
                      setFilters({ ...filters, evidence_level: e.target.value })
                    }
                    className="input-field"
                  >
                    <option value="">All Evidence Levels</option>
                    <option value="A">Level A</option>
                    <option value="B">Level B</option>
                    <option value="C">Level C</option>
                    <option value="D">Level D</option>
                  </select>

                  <select
                    value={filters.access_level}
                    onChange={(e) =>
                      setFilters({ ...filters, access_level: e.target.value })
                    }
                    className="input-field"
                  >
                    <option value="">All Access Levels</option>
                    <option value="open_access">Open Access</option>
                    <option value="subscription">Subscription</option>
                    <option value="institutional">Institutional</option>
                  </select>
                </div>
              )}
            </div>
          </div>

          {/* Search Results */}
          {documents.length > 0 && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold">
                  Search Results ({documents.length})
                </h3>
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-gray-600">
                    {selectedDocuments.length} selected
                  </span>
                  <button
                    onClick={() =>
                      setSelectedDocuments(documents.map((d) => d.document_id))
                    }
                    className="text-sm text-medical-600 hover:text-medical-700"
                  >
                    Select All
                  </button>
                  <button
                    onClick={() => setSelectedDocuments([])}
                    className="text-sm text-gray-600 hover:text-gray-700"
                  >
                    Clear
                  </button>
                </div>
              </div>

              {documents.map((doc) => (
                <div
                  key={doc.document_id}
                  className="card border-l-4 border-medical-500"
                >
                  <div className="flex items-start space-x-4">
                    <input
                      type="checkbox"
                      checked={selectedDocuments.includes(doc.document_id)}
                      onChange={() => toggleDocumentSelection(doc.document_id)}
                      className="mt-1 h-4 w-4 text-medical-600 focus:ring-medical-500 border-gray-300 rounded"
                    />

                    <div className="flex-1">
                      <div className="flex justify-between items-start mb-3">
                        <div className="flex-1">
                          <h4 className="font-semibold text-lg text-gray-900 mb-1">
                            {doc.title}
                          </h4>
                          <div className="flex items-center space-x-4 text-sm text-gray-600 mb-2">
                            <span>
                              {doc.authors.slice(0, 3).join(", ")}
                              {doc.authors.length > 3 ? " et al." : ""}
                            </span>
                            <span>•</span>
                            <span>{doc.journal}</span>
                            <span>•</span>
                            <span>
                              {new Date(doc.publication_date).getFullYear()}
                            </span>
                          </div>
                        </div>

                        <div className="flex items-center space-x-2 ml-4">
                          <span
                            className={`px-2 py-1 rounded text-xs font-medium ${getEvidenceLevelColor(
                              doc.evidence_level
                            )}`}
                          >
                            Level {doc.evidence_level}
                          </span>
                          <span
                            className={`px-2 py-1 rounded text-xs font-medium ${getQualityColor(
                              doc.quality_score
                            )}`}
                          >
                            Quality: {(doc.quality_score * 100).toFixed(0)}%
                          </span>
                        </div>
                      </div>

                      <p className="text-gray-700 text-sm mb-3 line-clamp-3">
                        {doc.abstract}
                      </p>

                      <div className="flex justify-between items-center">
                        <div className="flex items-center space-x-4 text-xs text-gray-500">
                          <span className="capitalize">
                            {doc.document_type.replace("_", " ")}
                          </span>
                          <span>Citations: {doc.citation_count}</span>
                          <span className="capitalize">
                            {doc.access_level.replace("_", " ")}
                          </span>
                          {doc.specialties.length > 0 && (
                            <span>
                              Specialties:{" "}
                              {doc.specialties.slice(0, 2).join(", ")}
                            </span>
                          )}
                        </div>

                        <div className="flex space-x-2">
                          <button className="text-medical-600 hover:text-medical-700 text-sm">
                            View Details
                          </button>
                          <button className="text-gray-600 hover:text-gray-700">
                            <ExternalLink className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {documents.length === 0 && !searchLoading && (
            <div className="text-center py-12">
              <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                No documents found
              </h3>
              <p className="text-gray-600">
                Try adjusting your search terms or filters
              </p>
            </div>
          )}
        </div>
      )}

      {/* Quality Tab */}
      {activeTab === "quality" && qualityReport && (
        <div className="space-y-6">
          <div className="card">
            <h3 className="text-lg font-semibold mb-4">
              Repository Quality Assessment
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div
                className={`text-center p-4 rounded-lg ${getGradeColor(
                  qualityReport.summary.overall_grade
                )}`}
              >
                <div className="text-3xl font-bold">
                  {qualityReport.summary.overall_grade}
                </div>
                <div className="text-sm">Overall Grade</div>
                <div className="text-xs text-gray-600 mt-1">
                  High Quality Repository
                </div>
              </div>

              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <div className="text-3xl font-bold text-blue-600">
                  {qualityReport.quality_assessment.overall_quality_score.toFixed(
                    2
                  )}
                </div>
                <div className="text-sm text-blue-600">Quality Score</div>
                <div className="text-xs text-gray-600 mt-1">Above Average</div>
              </div>

              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <div className="text-3xl font-bold text-purple-600">
                  {qualityReport.quality_assessment.content_freshness.recent_content_5y.toFixed(
                    0
                  )}
                  %
                </div>
                <div className="text-sm text-purple-600">Recent Content</div>
                <div className="text-xs text-gray-600 mt-1">Last 5 Years</div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card">
              <h4 className="font-semibold mb-3 flex items-center">
                <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
                Quality Strengths
              </h4>
              <ul className="space-y-2">
                {qualityReport.summary.strengths.map((strength, index) => (
                  <li key={index} className="flex items-center text-green-600">
                    <Shield className="w-4 h-4 mr-2" />
                    {strength}
                  </li>
                ))}
              </ul>
            </div>

            <div className="card">
              <h4 className="font-semibold mb-3 flex items-center">
                <AlertCircle className="w-5 h-5 text-orange-600 mr-2" />
                Improvement Areas
              </h4>
              <ul className="space-y-2">
                {qualityReport.summary.improvement_areas.map((area, index) => (
                  <li key={index} className="flex items-center text-orange-600">
                    <AlertCircle className="w-4 h-4 mr-2" />
                    {area}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Detailed Quality Metrics */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="card">
              <h4 className="font-semibold mb-3">Content Freshness</h4>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Recent (5y)</span>
                  <span className="text-sm font-medium">
                    {qualityReport.quality_assessment.content_freshness.recent_content_5y.toFixed(
                      1
                    )}
                    %
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">
                    Very Recent (2y)
                  </span>
                  <span className="text-sm font-medium">
                    {qualityReport.quality_assessment.content_freshness.very_recent_content_2y.toFixed(
                      1
                    )}
                    %
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-green-600 h-2 rounded-full"
                    style={{
                      width: `${
                        qualityReport.quality_assessment.content_freshness
                          .freshness_score * 100
                      }%`,
                    }}
                  ></div>
                </div>
              </div>
            </div>

            <div className="card">
              <h4 className="font-semibold mb-3">Source Diversity</h4>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Unique Journals</span>
                  <span className="text-sm font-medium">
                    {
                      qualityReport.quality_assessment.source_diversity
                        .unique_journals
                    }
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">
                    Unique Publishers
                  </span>
                  <span className="text-sm font-medium">
                    {
                      qualityReport.quality_assessment.source_diversity
                        .unique_publishers
                    }
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full"
                    style={{
                      width: `${
                        qualityReport.quality_assessment.source_diversity
                          .diversity_score * 100
                      }%`,
                    }}
                  ></div>
                </div>
              </div>
            </div>

            <div className="card">
              <h4 className="font-semibold mb-3">Processing Quality</h4>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Avg Confidence</span>
                  <span className="text-sm font-medium">
                    {qualityReport.quality_assessment.processing_quality.average_confidence.toFixed(
                      2
                    )}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Validation Rate</span>
                  <span className="text-sm font-medium">
                    {qualityReport.quality_assessment.processing_quality.validation_rate.toFixed(
                      1
                    )}
                    %
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">
                    Embedding Complete
                  </span>
                  <span className="text-sm font-medium">
                    {qualityReport.quality_assessment.processing_quality.embedding_completion.toFixed(
                      1
                    )}
                    %
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Recommendations */}
          {qualityReport.quality_assessment.recommendations.length > 0 && (
            <div className="card">
              <h4 className="font-semibold mb-3 flex items-center">
                <TrendingUp className="w-5 h-5 text-medical-600 mr-2" />
                Recommendations
              </h4>
              <ul className="space-y-2">
                {qualityReport.quality_assessment.recommendations.map(
                  (recommendation, index) => (
                    <li key={index} className="flex items-start">
                      <Clock className="w-4 h-4 text-medical-600 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-left text-sm text-gray-700">
                        {recommendation}
                      </span>
                    </li>
                  )
                )}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default KnowledgeRepository
