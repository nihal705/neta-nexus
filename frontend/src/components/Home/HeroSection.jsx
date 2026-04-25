import { motion } from 'framer-motion'
import { FiSearch, FiTrendingUp, FiShield } from 'react-icons/fi'
import { useNavigate } from 'react-router-dom'
import { useState } from 'react'

export default function HeroSection() {
  const [searchQuery, setSearchQuery] = useState('')
  const navigate = useNavigate()

  const handleSearch = (e) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery)}`)
    }
  }

  return (
    <div className="relative overflow-hidden bg-gradient-to-br from-primary-navy via-primary-blue to-primary-teal pt-20">
      {/* Animated background shapes */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-20 left-10 w-72 h-72 bg-white rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-white rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-28">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center"
        >
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
            Know Your Leader,
            <span className="block text-gradient bg-gradient-to-r from-yellow-400 to-orange-400 bg-clip-text text-transparent">
              Before You Vote
            </span>
          </h1>
          <p className="text-xl text-white/80 mb-8 max-w-2xl mx-auto">
            India's most comprehensive political database. Track MPs, MLAs, candidates, their assets, criminal records, and parliamentary performance.
          </p>

          {/* Search Bar */}
          <form onSubmit={handleSearch} className="max-w-2xl mx-auto mb-8">
            <div className="flex flex-col sm:flex-row gap-3">
              <div className="flex-1 relative">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search by name, party, or constituency..."
                  className="w-full px-6 py-4 rounded-xl bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-yellow-400 shadow-lg"
                />
                <FiSearch className="absolute right-4 top-4 text-gray-400" size={20} />
              </div>
              <button type="submit" className="px-8 py-4 bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-semibold rounded-xl transition-all transform hover:scale-105 shadow-lg">
                Search
              </button>
            </div>
          </form>

          {/* Stats */}
          <div className="flex justify-center gap-8 text-white">
            <div className="text-center">
              <div className="text-3xl font-bold">15K+</div>
              <div className="text-sm opacity-80">Candidates Tracked</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold">543</div>
              <div className="text-sm opacity-80">MPs Monitored</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold">4K+</div>
              <div className="text-sm opacity-80">MLAs Covered</div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}