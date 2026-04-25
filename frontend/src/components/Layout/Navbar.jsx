import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { FiSearch, FiMenu, FiX, FiSun, FiMoon, FiUser, FiTrendingUp, FiBarChart2, FiHome } from 'react-icons/fi'

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false)
  const [darkMode, setDarkMode] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [scrolled, setScrolled] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  useEffect(() => {
    const isDark = localStorage.getItem('darkMode') === 'true'
    setDarkMode(isDark)
    if (isDark) {
      document.documentElement.classList.add('dark')
    }
  }, [])

  const handleSearch = (e) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery)}`)
      setSearchQuery('')
      setIsOpen(false)
    }
  }

  const toggleDarkMode = () => {
    const newDarkMode = !darkMode
    setDarkMode(newDarkMode)
    localStorage.setItem('darkMode', newDarkMode)
    if (newDarkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  return (
    <nav className={`fixed top-0 w-full z-50 transition-all duration-300 ${
      scrolled ? 'bg-white/95 dark:bg-gray-900/95 backdrop-blur-md shadow-lg' : 'bg-white dark:bg-gray-900 shadow-md'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 group">
            <span className="text-2xl font-bold bg-gradient-to-r from-primary-teal to-primary-blue bg-clip-text text-transparent">
              NetaNexus
            </span>
            <span className="text-xs bg-primary-teal/10 text-primary-teal px-2 py-0.5 rounded-full">Beta</span>
          </Link>

          {/* Desktop Navigation Links */}
          <div className="hidden md:flex items-center space-x-6">
            <Link to="/" className="text-gray-600 dark:text-gray-300 hover:text-primary-teal transition">Home</Link>
            <Link to="/elections" className="text-gray-600 dark:text-gray-300 hover:text-primary-teal transition flex items-center gap-1">
              <FiBarChart2 /> Elections
            </Link>
            <Link to="/compare" className="text-gray-600 dark:text-gray-300 hover:text-primary-teal transition flex items-center gap-1">
              <FiTrendingUp /> Compare
            </Link>
          </div>

          {/* Desktop Search */}
          <form onSubmit={handleSearch} className="hidden md:flex flex-1 max-w-md mx-4">
            <div className="relative w-full">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search MLA, MP, Candidate by name, party, or constituency..."
                className="w-full px-4 py-2 pl-10 rounded-full border border-gray-200 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-primary-teal dark:bg-gray-800"
              />
              <FiSearch className="absolute left-3 top-2.5 text-gray-400" size={18} />
            </div>
          </form>

          {/* Desktop Actions */}
          <div className="hidden md:flex items-center space-x-3">
            <button onClick={toggleDarkMode} className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800">
              {darkMode ? <FiSun className="text-yellow-500" size={18} /> : <FiMoon size={18} />}
            </button>
            <button className="flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-primary-teal to-primary-blue text-white hover:shadow-lg transition">
              <FiUser size={16} />
              <span>Sign In</span>
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button onClick={() => setIsOpen(!isOpen)} className="md:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800">
            {isOpen ? <FiX size={24} /> : <FiMenu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden bg-white dark:bg-gray-900 border-t dark:border-gray-800 shadow-lg">
          <div className="px-4 py-4 space-y-3">
            <form onSubmit={handleSearch}>
              <div className="relative">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search..."
                  className="w-full px-4 py-3 pl-10 rounded-xl border border-gray-200 dark:border-gray-700 dark:bg-gray-800"
                />
                <FiSearch className="absolute left-3 top-3.5 text-gray-400" />
              </div>
            </form>
            <Link to="/" className="block py-2 text-gray-600 dark:text-gray-300" onClick={() => setIsOpen(false)}>🏠 Home</Link>
            <Link to="/elections" className="block py-2 text-gray-600 dark:text-gray-300" onClick={() => setIsOpen(false)}>🗳️ Elections</Link>
            <Link to="/compare" className="block py-2 text-gray-600 dark:text-gray-300" onClick={() => setIsOpen(false)}>📊 Compare</Link>
            <button onClick={toggleDarkMode} className="block w-full text-left py-2 text-gray-600 dark:text-gray-300">
              {darkMode ? '☀️ Light Mode' : '🌙 Dark Mode'}
            </button>
            <button className="w-full py-3 rounded-xl bg-gradient-to-r from-primary-teal to-primary-blue text-white font-semibold">
              Sign In
            </button>
          </div>
        </div>
      )}
    </nav>
  )
}