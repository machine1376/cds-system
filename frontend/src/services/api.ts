import axios from "axios"
import type { ClinicalQuery, ClinicalResponse } from "../types/api"

const API_BASE_URL = "http://localhost:8000"

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
})

// Request interceptor for auth (future)
api.interceptors.request.use((config) => {
  // Add auth token when available
  // const token = localStorage.getItem('auth_token');
  // if (token) {
  //   config.headers.Authorization = `Bearer ${token}`;
  // }
  return config
})

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error)
    return Promise.reject(error)
  }
)

export const clinicalAPI = {
  // Submit clinical query
  submitQuery: async (query: ClinicalQuery): Promise<ClinicalResponse> => {
    const response = await api.post("/clinical/query", query)
    return response.data
  },

  // Check drug interactions
  checkDrugInteractions: async (medications: string[]) => {
    const response = await api.post("/drugs/interactions", medications)
    return response.data
  },

  // Get supported specialties
  getSpecialties: async () => {
    const response = await api.get("/clinical/specialties")
    return response.data
  },

  // Health check
  healthCheck: async () => {
    const response = await api.get("/health")
    return response.data
  },
}

export const knowledgeRepositoryAPI = {
  // Get repository overview
  getOverview: async () => {
    const response = await api.get("/knowledge-repository/")
    return response.data
  },

  // Search documents
  searchDocuments: async (searchRequest: any) => {
    const response = await api.post(
      "/knowledge-repository/search",
      searchRequest
    )
    return response.data
  },

  // Get document details
  getDocumentDetails: async (documentId: string) => {
    const response = await api.get(
      `/knowledge-repository/document/${documentId}`
    )
    return response.data
  },

  // Get quality report
  getQualityReport: async () => {
    const response = await api.get("/knowledge-repository/quality/report")
    return response.data
  },

  // Get knowledge sources
  getKnowledgeSources: async () => {
    const response = await api.get("/knowledge-repository/sources")
    return response.data
  },

  // Export bibliography
  exportBibliography: async (
    documentIds: string[],
    format: string = "bibtex"
  ) => {
    const response = await api.get(
      `/knowledge-repository/export/bibliography`,
      {
        params: {
          document_ids: documentIds.join(","),
          format: format,
        },
      }
    )
    return response.data
  },

  // Get usage analytics
  getUsageAnalytics: async () => {
    const response = await api.get("/knowledge-repository/analytics/usage")
    return response.data
  },
}

export default api
