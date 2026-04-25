import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'
import { FiRefreshCw, FiBarChart2, FiMap } from 'react-icons/fi'
import ExitPollCarousel from '../components/Home/ExitPollCarousel'
import LoadingSpinner from '../components/UI/LoadingSpinner'
import LiveResults from '../components/Elections/LiveResults'
import ComparativeAnalysis from '../components/Elections/ComparativeAnalysis'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts'

export default function ElectionCenter() {
  const [liveResults, setLiveResults] = useState(null)
  const [loading, setLoading] = useState(true)
  const [lastUpdated, setLastUpdated] = useState(null)
  const [comparativeData, setComparativeData] = useState(null)

  useEffect(() => {
    fetchLiveResults()
    fetchComparativeData()
    
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchLiveResults, 30000)
    return () => clearInterval(interval)
  }, [])

  const fetchLiveResults = async () => {
    try {
      const response = await axios.get('/api/elections/live-results?election_id=2024')
      setLiveResults(response.data)
      setLastUpdated(new Date())
    } catch (error) {
      console.error('Error fetching live results:', error)
      // Mock data
      setLiveResults({
        trends: { bjp: 245, inc: 142, others: 156 },
        is_counting_day: true,
        total_seats: 543,
        constituencies_declared: 400
      })
    } finally {
      setLoading(false)
    }
  }

  const fetchComparativeData = async () => {
    try {
      const response = await axios.get('/api/exitpolls/comparative?election_id=2024')
      setComparativeData(response.data)
    } catch (error) {
      console.error('Error fetching comparative data:', error)
    }
  }

  if (loading) return <LoadingSpinner />

  const chartData = [
    { name: '9 AM', bjp: 120, inc: 80, others: 40 },
    { name: '10 AM', bjp: 180, inc: 100, others: 60 },
    { name: '11 AM', bjp: 210, inc: 120, others: 80 },
    { name: '12 PM', bjp: 230, inc: 138, others: 100 },
    { name: '1 PM', bjp: 240, inc: 140, others: 120 },
    { name: '2 PM', bjp: 245, inc: 142, others: 156 },
  ]

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8"
    >
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold">🗳️ Election Center 2024</h1>
        <p className="text-gray-500 mt-2">Live results, exit polls, and analysis</p>
      </div>

      {/* Live Results */}
      <div className="card p-6 mb-8">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold flex items-center gap-2">
            <FiBarChart2 /> Live Counting
          </h2>
          <div className="flex items-center gap-4 text-sm">
            {lastUpdated && (
              <span className="text-gray-500">Last updated: {lastUpdated.toLocaleTimeString()}</span>
            )}
            <button onClick={fetchLiveResults} className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700">
              <FiRefreshCw className={loading ? 'animate-spin' : ''} />
            </button>
          </div>
        </div>

        {liveResults?.is_counting_day ? (
          <>
            <div className="grid grid-cols-3 gap-4 mb-8">
              <div className="bg-orange-50 dark:bg-orange-900/20 rounded-xl p-6 text-center">
                <div className="text-orange-600 text-sm">BJP/NDA</div>
                <div className="text-4xl font-bold text-orange-600 animate-count-up">
                  {liveResults.trends.bjp}
                </div>
              </div>
              <div className="bg-green-50 dark:bg-green-900/20 rounded-xl p-6 text-center">
                <div className="text-green-600 text-sm">INC/INDIA</div>
                <div className="text-4xl font-bold text-green-600">
                  {liveResults.trends.inc}
                </div>
              </div>
              <div className="bg-purple-50 dark:bg-purple-900/20 rounded-xl p-6 text-center">
                <div className="text-purple-600 text-sm">Others</div>
                <div className="text-4xl font-bold text-purple-600">
                  {liveResults.trends.others}
                </div>
              </div>
            </div>

            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="bjp" stroke="#F59E0B" strokeWidth={2} />
                  <Line type="monotone" dataKey="inc" stroke="#00A896" strokeWidth={2} />
                  <Line type="monotone" dataKey="others" stroke="#7C3AED" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div className="mt-4 text-center text-sm text-gray-500">
              {liveResults.constituencies_declared} of {liveResults.total_seats} constituencies declared
            </div>
          </>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500">Counting has not started yet. Check back on result day.</p>
          </div>
        )}
      </div>

      {/* Exit Polls */}
      <div className="mb-8">
        <ExitPollCarousel />
      </div>

      {/* Comparative Analysis */}
      {comparativeData && (
        <div className="card p-6">
          <h2 className="text-2xl font-bold mb-4">📊 Comparative Analysis</h2>
          
          <div className="h-80 mb-6">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={comparativeData.chart_data.agencies.map((agency, idx) => ({
                agency,
                bjp: (comparativeData.chart_data.bjp_min[idx] + comparativeData.chart_data.bjp_max[idx]) / 2,
                inc: (comparativeData.chart_data.inc_min[idx] + comparativeData.chart_data.inc_max[idx]) / 2,
              }))}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="agency" angle={-45} textAnchor="end" height={80} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="bjp" fill="#F59E0B" />
                <Bar dataKey="inc" fill="#00A896" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-blue-50 dark:bg-blue-900/20 rounded-xl p-4">
            <h3 className="font-semibold mb-2">Consensus</h3>
            <p className="text-sm">{comparativeData.consensus.description}</p>
            <div className="flex gap-4 mt-3 text-sm">
              <span>BJP Range: {comparativeData.consensus.bjp_range}</span>
              <span>INC Range: {comparativeData.consensus.inc_range}</span>
              <span>Margin of Error: {comparativeData.consensus.margin_of_error}</span>
            </div>
          </div>
        </div>
      )}
    </motion.div>
  )
}