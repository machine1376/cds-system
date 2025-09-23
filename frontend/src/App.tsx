import { useState, useEffect, useCallback } from "react"
import {
  Stethoscope,
  Shield,
  BookOpen,
  Settings,
  Search,
  Bell,
  User,
  LogOut,
  ChevronDown,
  FileText,
} from "lucide-react"
import ClinicalQuery from "./components/ClinicalQuery"
import DrugInteractions from "./components/DrugInteractions"
import GuidelinesExplorer from "./components/GuidelinesExplorer"
import KnowledgeRepository from "./components/KnowledgeRepository"
import "./App.css"

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [sidebarClosing, setSidebarClosing] = useState(false)
  const [userMenuOpen, setUserMenuOpen] = useState(false)
  const [currentPage, setCurrentPage] = useState("clinical-query")

  // Handle sidebar closing animation
  const closeSidebar = useCallback(() => {
    console.log(
      "closeSidebar called - sidebarOpen:",
      sidebarOpen,
      "sidebarClosing:",
      sidebarClosing
    )

    // Start closing animation
    setSidebarClosing(true)

    // Complete the close after animation
    setTimeout(() => {
      setSidebarOpen(false)
      setSidebarClosing(false)
    }, 300) // Match the animation duration
  }, [sidebarOpen, sidebarClosing])

  // Handle sidebar opening
  const openSidebar = () => {
    setSidebarOpen(true)
    setSidebarClosing(false)
  }

  // Handle escape key to close sidebar
  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape" && sidebarOpen) {
        closeSidebar()
      }
    }

    if (sidebarOpen) {
      document.addEventListener("keydown", handleEscape)
    }

    return () => {
      document.removeEventListener("keydown", handleEscape)
    }
  }, [sidebarOpen, closeSidebar])

  // Handle click outside to close user menu
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (userMenuOpen) {
        const target = event.target as Element
        if (!target.closest("[data-user-menu]")) {
          setUserMenuOpen(false)
        }
      }
    }

    if (userMenuOpen) {
      document.addEventListener("mousedown", handleClickOutside)
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside)
    }
  }, [userMenuOpen])

  const navigation = [
    {
      name: "Clinical Query",
      href: "#",
      icon: Search,
      current: currentPage === "clinical-query",
      description: "AI-powered clinical decisions",
      page: "clinical-query",
    },
    {
      name: "Drug Interactions",
      href: "#",
      icon: Shield,
      current: currentPage === "drug-interactions",
      description: "Check medication interactions",
      page: "drug-interactions",
    },
    {
      name: "Clinical Guidelines",
      href: "#",
      icon: BookOpen,
      current: currentPage === "guidelines-explorer",
      description: "Evidence-based guidelines",
      page: "guidelines-explorer",
    },
    {
      name: "Knowledge Base",
      href: "#",
      icon: FileText,
      current: currentPage === "knowledge-base",
      description: "Medical knowledge repository",
      page: "knowledge-base",
    },
  ]

  const getPageTitle = (page: string) => {
    switch (page) {
      case "clinical-query":
        return "Clinical Query"
      case "drug-interactions":
        return "Drug Interactions"
      case "guidelines-explorer":
        return "Clinical Guidelines"
      case "knowledge-base":
        return "Knowledge Base"
      default:
        return "Clinical Decision Support"
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile menu overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 lg:hidden"
          onClick={closeSidebar}
        />
      )}

      {/* Mobile dropdown menu */}
      {sidebarOpen && (
        <div
          className={`mobile-menu-panel fixed top-24 mx-8 left-0 right-0 bg-white shadow-xl transform transition-transform duration-300 ease-in-out z-10 ${
            sidebarClosing ? "slide-out-to-top" : "slide-in-from-top"
          }`}
        >
          {/* Mobile menu header */}
          <div className="flex items-center p-4 border-b border-gray-200">
            <div className="w-8 h-8 bg-gradient-to-br from-medical-500 to-medical-700 rounded-lg flex items-center justify-center shadow-medical">
              <Stethoscope className="w-5 h-5 text-white" />
            </div>
            <div className="ml-3 text-left">
              <h2 className="text-lg font-bold text-gray-900">CDS System</h2>
              <p className="text-xs text-gray-600 font-medium">
                Clinical Decision Support
              </p>
            </div>
          </div>

          {/* Mobile menu content */}
          <div className="mobile-menu-content max-h-[calc(100vh-4rem)] overflow-y-auto pt-4">
            {/* Mobile navigation */}
            <nav className="px-4 py-4 space-y-2">
              {navigation.map((item, index) => (
                <button
                  key={item.name}
                  onClick={() => {
                    if (item.page) {
                      setCurrentPage(item.page)
                      closeSidebar()
                    }
                  }}
                  className={`mobile-menu-item w-full ${
                    item.current
                      ? "bg-medical-100 text-medical-800 border-r-4 border-medical-600 shadow-md font-semibold"
                      : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                  } group flex items-center px-4 py-3 text-left text-sm font-medium rounded-lg transition-all duration-200`}
                  style={{ animationDelay: `${index * 0.05}s` }}
                >
                  <item.icon
                    className={`${
                      item.current
                        ? "text-medical-700"
                        : "text-gray-400 group-hover:text-gray-500"
                    } mr-3 h-5 w-5 flex-shrink-0`}
                  />
                  <div className="flex-1">
                    <div className="font-medium">{item.name}</div>
                    <div className="text-xs text-gray-500">
                      {item.description}
                    </div>
                  </div>
                </button>
              ))}
            </nav>
          </div>
        </div>
      )}

      <div className="flex h-screen">
        {/* Desktop Sidebar */}
        <div className="hidden lg:flex lg:flex-col lg:w-64 lg:bg-white lg:shadow-xl">
          <div className="flex flex-col h-full">
            {/* Logo and close button */}
            <div className="flex items-center justify-between p-4 border-b border-gray-200">
              <div className="flex items-start">
                <div className="w-10 h-10 bg-gradient-to-br from-medical-500 to-medical-700 rounded-xl flex items-center justify-center shadow-medical">
                  <Stethoscope className="w-6 h-6 text-white" />
                </div>
                <div className="ml-4 flex-1 text-left">
                  <h1 className="text-2xl font-bold text-gray-900">
                    CDS System
                  </h1>
                  <p className="text-sm text-gray-600 font-medium">
                    Clinical Decision Support
                  </p>
                  <div className="flex items-center mt-2">
                    <div className="w-2 h-2 bg-success-500 rounded-full animate-pulse"></div>
                    <span className="text-xs text-success-600 ml-2 font-semibold">
                      System Online
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Enhanced Navigation */}
            <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
              {navigation.map((item) => (
                <button
                  key={item.name}
                  onClick={() => {
                    if (item.page) {
                      setCurrentPage(item.page)
                    }
                  }}
                  className={`w-full ${
                    item.current
                      ? "bg-medical-100 text-medical-800 border-r-4 border-medical-600 shadow-md font-semibold"
                      : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                  } group flex items-start px-5 py-3 text-left text-sm font-medium rounded-lg transition-all duration-200`}
                >
                  <item.icon
                    className={`${
                      item.current
                        ? "text-medical-700"
                        : "text-gray-400 group-hover:text-gray-500"
                    } mr-4 h-5 w-5 flex-shrink-0`}
                  />
                  <div className="flex-1">
                    <div className="font-medium">{item.name}</div>
                    <div className="text-xs text-gray-500">
                      {item.description}
                    </div>
                  </div>
                </button>
              ))}
            </nav>

            {/* User section */}
            <div className="p-4 border-t border-gray-200">
              <div className="flex items-start">
                <div className="w-8 h-8 bg-medical-100 rounded-full flex items-center justify-center">
                  <User className="w-4 h-4 text-medical-600" />
                </div>
                <div className="ml-3 flex-1">
                  <p className="text-sm font-medium text-gray-900">Dr. Smith</p>
                  <p className="text-xs text-gray-500">Cardiologist</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Main content */}
        <div className="flex-1 flex flex-col min-w-0">
          {/* Header */}
          <header className="bg-white shadow-sm border-b border-gray-200 relative z-40">
            <div className="flex items-center justify-between px-4 sm:px-6 lg:px-8 h-16">
              <div className="flex text-left items-start">
                <button
                  onClick={() => (sidebarOpen ? closeSidebar() : openSidebar())}
                  className="lg:hidden p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-medical-500 relative w-10 h-10 flex items-center justify-center"
                >
                  {/* Animated hamburger/X icon */}
                  <div className="w-6 h-6 relative">
                    {/* Top line */}
                    <span
                      className={`hamburger-line-1 absolute top-1 left-0 w-6 h-0.5 bg-current ${
                        sidebarOpen
                          ? "rotate-45 translate-y-2"
                          : "rotate-0 translate-y-0"
                      }`}
                    />
                    {/* Middle line */}
                    <span
                      className={`hamburger-line-2 absolute top-2.5 left-0 w-6 h-0.5 bg-current ${
                        sidebarOpen
                          ? "opacity-0 scale-0"
                          : "opacity-100 scale-100"
                      }`}
                    />
                    {/* Bottom line */}
                    <span
                      className={`hamburger-line-3 absolute top-4 left-0 w-6 h-0.5 bg-current ${
                        sidebarOpen
                          ? "-rotate-45 -translate-y-1"
                          : "rotate-0 translate-y-0"
                      }`}
                    />
                  </div>
                </button>
                <div className="ml-4 lg:ml-0">
                  <h1 className="text-xl font-semibold text-gray-900">
                    {getPageTitle(currentPage)}
                  </h1>
                  <p className="text-sm text-gray-500">
                    {navigation.find((item) => item.page === currentPage)
                      ?.description || "Clinical Decision Support System"}
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-4">
                {/* Notifications */}
                <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-full focus:outline-none focus:ring-2 focus:ring-medical-500">
                  <Bell className="h-5 w-5" />
                </button>

                {/* User menu */}
                <div className="relative" data-user-menu>
                  <button
                    onClick={() => setUserMenuOpen(!userMenuOpen)}
                    className="flex items-center space-x-3 p-2 text-sm rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-medical-500"
                  >
                    <div className="w-8 h-8 bg-medical-100 rounded-full flex items-center justify-center">
                      <User className="w-4 h-4 text-medical-600" />
                    </div>
                    <div className="hidden sm:block text-left">
                      <p className="font-medium text-gray-900">Dr. Smith</p>
                      <p className="text-xs text-gray-500">Cardiologist</p>
                    </div>
                    <ChevronDown className="w-4 h-4 text-gray-400" />
                  </button>

                  {userMenuOpen && (
                    <div className="user-dropdown absolute right-0 top-full mt-2 w-56 max-w-[calc(100vw-2rem)] bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-50">
                      <div className="md:hidden block px-4 py-2 justify-items-start border-b border-gray-100">
                        <p className="text-sm font-medium text-gray-900">
                          Dr. Smith
                        </p>
                        <p className="text-xs text-gray-500">Cardiologist</p>
                      </div>
                      <div className="py-1">
                        <button className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                          <Settings className="w-4 h-4 mr-3" />
                          Settings
                        </button>
                        <button className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                          <LogOut className="w-4 h-4 mr-3" />
                          Sign out
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </header>

          {/* Enhanced Main Content Area */}
          <main className="flex-1 flex flex-col lg:flex-row">
            {/* Main Content */}
            <div className="flex-1 min-w-0 max-w-full">
              {currentPage === "clinical-query" && <ClinicalQuery />}
              {currentPage === "drug-interactions" && <DrugInteractions />}
              {currentPage === "guidelines-explorer" && <GuidelinesExplorer />}
              {currentPage === "knowledge-base" && <KnowledgeRepository />}
            </div>

            {/* Quick Actions Sidebar */}
            <div className="hidden xl:block w-80 2xl:w-96 bg-white border-l border-gray-200 p-4 lg:p-6 flex-shrink-0">
              <div className="space-y-6">
                {/* Quick Actions Panel */}
                <div className="bg-gradient-to-br from-medical-50 to-medical-100 rounded-xl p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Quick Actions
                  </h3>
                  <div className="space-y-3">
                    <button className="w-full flex items-start p-3 text-left bg-white rounded-lg hover:bg-gray-50 transition-colors">
                      <Search className="w-5 h-5 text-medical-600 mr-3" />
                      <div>
                        <div className="font-medium text-gray-900">
                          New Clinical Query
                        </div>
                        <div className="text-sm text-gray-500">
                          Ask a clinical question
                        </div>
                      </div>
                    </button>
                    <button className="w-full flex items-start p-3 text-left bg-white rounded-lg hover:bg-gray-50 transition-colors">
                      <Shield className="w-5 h-5 text-medical-600 mr-3" />
                      <div>
                        <div className="font-medium text-gray-900">
                          Check Interactions
                        </div>
                        <div className="text-sm text-gray-500">
                          Verify drug safety
                        </div>
                      </div>
                    </button>
                    <button className="w-full flex items-start p-3 text-left bg-white rounded-lg hover:bg-gray-50 transition-colors">
                      <BookOpen className="w-5 h-5 text-medical-600 mr-3" />
                      <div>
                        <div className="font-medium text-gray-900">
                          View Guidelines
                        </div>
                        <div className="text-sm text-gray-500">
                          Browse best practices
                        </div>
                      </div>
                    </button>
                  </div>
                </div>

                {/* Recent Activity */}
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Recent Activity
                  </h3>
                  <div className="space-y-4">
                    <div className="flex items-start">
                      <div className="w-2 h-2 bg-success-500 rounded-full mt-2 mr-3"></div>
                      <div className="flex-1">
                        <p className="text-left text-sm text-gray-900">
                          Completed drug interaction check
                        </p>
                        <p className="text-left text-xs text-gray-500">
                          2 minutes ago
                        </p>
                      </div>
                    </div>
                    <div className="flex items-start">
                      <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3"></div>
                      <div className="flex-1">
                        <p className="text-left text-sm text-gray-900">
                          Viewed hypertension guidelines
                        </p>
                        <p className="text-left text-xs text-gray-500">
                          15 minutes ago
                        </p>
                      </div>
                    </div>
                    <div className="flex items-start">
                      <div className="w-2 h-2 bg-warning-500 rounded-full mt-2 mr-3"></div>
                      <div className="flex-1">
                        <p className="text-left text-sm text-gray-900">
                          Clinical query pending review
                        </p>
                        <p className="text-left text-xs text-gray-500">
                          1 hour ago
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* System Status */}
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    System Status
                  </h3>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">API Status</span>
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-success-100 text-success-800">
                        Online
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Database</span>
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-success-100 text-success-800">
                        Healthy
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">AI Models</span>
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-success-100 text-success-800">
                        Active
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Last Update</span>
                      <span className="text-left text-xs text-gray-500">
                        2 min ago
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
  )
}

export default App
