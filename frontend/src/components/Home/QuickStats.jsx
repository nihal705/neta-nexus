import { motion } from 'framer-motion'
import { FiUsers, FiMapPin, FiAlertCircle, FiTrendingUp } from 'react-icons/fi'
import { useEffect, useState } from 'react'
import axios from 'axios'

export default function QuickStats() {
  const [stats, setStats] = useState({
    totalCandidates: 15234,
    totalMps: 543,
    totalMlas: 4123,
    totalCriminalCases: 2847
  })

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const response = await axios.get('/api/search/trending')
      // Update stats based on response
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  const statItems = [
    { icon: FiUsers, label: 'Candidates Tracked', value: stats.totalCandidates.toLocaleString(), color: 'from-blue-500 to-cyan-500' },
    { icon: FiMapPin, label: 'Constituencies', value: '5,432', color: 'from-green-500 to-teal-500' },
    { icon: FiAlertCircle, label: 'Criminal Cases Reported', value: stats.totalCriminalCases.toLocaleString(), color: 'from-red-500 to-orange-500' },
    { icon: FiTrendingUp, label: 'Elections Analyzed', value: '24', color: 'from-purple-500 to-pink-500' },
  ]

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-10 relative z-10">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {statItems.map((stat, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 hover:shadow-xl transition-all"
          >
            <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${stat.color} flex items-center justify-center mb-4`}>
              <stat.icon className="text-white" size={24} />
            </div>
            <div className="text-2xl font-bold text-gray-900 dark:text-white">{stat.value}</div>
            <div className="text-sm text-gray-500 dark:text-gray-400">{stat.label}</div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}