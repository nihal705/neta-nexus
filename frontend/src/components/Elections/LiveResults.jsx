import { useState, useEffect, useRef } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, AreaChart } from 'recharts'
import { FiRefreshCw, FiTrendingUp, FiAward, FiMapPin, FiBarChart2, FiAlertCircle } from 'react-icons/fi'
import axios from 'axios'

export default function LiveResults() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(true)
  const [lastUpdated, setLastUpdated] = useState(null)
  const [historicalData, setHistoricalData] = useState([])
  const [wsConnected, setWsConnected] = useState(false)
  const wsRef = useRef(null)

  useEffect(() => {
    fetchResults()
    setupWebSocket()
    
    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [])

  const setupWebSocket = () => {
    try {
      const ws = new WebSocket('ws://localhost:8000/ws/live-results')
      
      ws.onopen = () => {
        console.log('WebSocket connected')
        setWsConnected(true)
      }
      
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          setResults({
            trends: { bjp: data.bjp, inc: data.inc, others: data.others },
            is_counting_day: true,
            total_seats: data.total_seats || 543,
            constituencies_declared: (data.bjp + data.inc + data.others)
          })
          setLastUpdated(new Date())
          
          // Update historical data for chart
          setHistoricalData(prev => {
            const newPoint = {
              time: new Date().toLocaleTimeString(),
              bjp: data.bjp,
              inc: data.inc,
              others: data.others
            }
            const updated = [...prev, newPoint]
            return updated.slice(-15)
          })
        } catch (err) {
          console.error('Error parsing WebSocket message:', err)
        }
      }
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        setWsConnected(false)
        // Fallback to polling
        startPolling()
      }
      
      ws.onclose = () => {
        console.log('WebSocket disconnected')
        setWsConnected(false)
        // Reconnect after 5 seconds
        setTimeout(setupWebSocket, 5000)
      }
      
      wsRef.current = ws
    } catch (err) {
      console.error('WebSocket setup error:', err)
      startPolling()
    }
  }

  const startPolling = () => {
    const interval = setInterval(() => {
      fetchResults()
    }, 30000)
    return () => clearInterval(interval)
  }

  const fetchResults = async () => {
    try {
      const response = await axios.get('/api/elections/live-results?election_id=2024')
      setResults(response.data)
      setLastUpdated(new Date())
      setLoading(false)
    } catch (error) {
      console.error('Error fetching results:', error)
      // Mock data for demo/fallback
      setResults({
        trends: { bjp: 245, inc: 142, others: 156 },
        is_counting_day: true,
        total_seats: 543,
        constituencies_declared: 400
      })
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/3"></div>
          <div className="grid grid-cols-3 gap-4">
            <div className="h-24 bg-gray-200 dark:bg-gray-700 rounded"></div>
            <div className="h-24 bg-gray-200 dark:bg-gray-700 rounded"></div>
            <div className="h-24 bg-gray-200 dark:bg-gray-700 rounded"></div>
          </div>
          <div className="h-64 bg-gray-200 dark:bg-gray-700 rounded"></div>
        </div>
      </div>
    )
  }

  if (!results?.is_counting_day) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-12 text-center">
        <FiBarChart2 className="text-6xl text-gray-300 dark:text-gray-600 mx-auto mb-4" />
        <h3 className="text-xl font-semibold mb-2">Counting Not Started</h3>
        <p className="text-gray-500">Live results will appear here on election counting day.</p>
        <p className="text-sm text-gray-400 mt-4">Check back on result day for real-time updates</p>
      </div>
    )
  }

  const totalSeats = results.total_seats || 543
  const declared = results.constituencies_declared || 0
  const remaining = totalSeats - declared
  const bjpLead = results.trends.bjp
  const incLead = results.trends.inc
  const othersLead = results.trends.others
  const bjpPercent = (bjpLead / totalSeats) * 100
  const incPercent = (incLead / totalSeats) * 100

  // Chart data with trend
  const chartData = historicalData.length > 0 ? historicalData : [
    { time: '9 AM', bjp: 120, inc: 80, others: 40 },
    { time: '10 AM', bjp: 160, inc: 100, others: 60 },
    { time: '11 AM', bjp: 195, inc: 115, others: 80 },
    { time: '12 PM', bjp: 220, inc: 130, others: 100 },
    { time: '1 PM', bjp: 235, inc: 138, others: 120 },
    { time: 'Now', bjp: bjpLead, inc: incLead, others: othersLead },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center flex-wrap gap-4">
        <div>
          <h2 className="text-2xl font-bold flex items-center gap-2">
            <FiTrendingUp className="text-primary-teal" />
            Live Election Results 2024
          </h2>
          <p className="text-sm text-gray-500 mt-1">
            {declared} of {totalSeats} constituencies declared • {remaining} remaining
          </p>
        </div>
        <div className="flex items-center gap-4">
          {/* WebSocket Status */}
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${wsConnected ? 'bg-green-500 animate-pulse' : 'bg-yellow-500'}`}></div>
            <span className="text-xs text-gray-500">{wsConnected ? 'Live' : 'Polling'}</span>
          </div>
          {lastUpdated && (
            <div className="text-right">
              <div className="text-xs text-gray-400">Last updated</div>
              <div className="text-sm font-medium">{lastUpdated.toLocaleTimeString()}</div>
            </div>
          )}
          <button 
            onClick={fetchResults}
            className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition"
            title="Refresh"
          >
            <FiRefreshCw className={loading ? 'animate-spin' : ''} size={18} />
          </button>
        </div>
      </div>

      {/* Seat Count Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl p-6 text-white transform hover:scale-105 transition duration-300 shadow-lg">
          <div className="flex justify-between items-start">
            <div>
              <div className="text-sm opacity-80">BJP / NDA</div>
              <div className="text-5xl font-bold animate-count-up">{bjpLead}</div>
              <div className="text-sm opacity-80 mt-2">{bjpPercent.toFixed(1)}% of seats</div>
            </div>
            <FiAward className="text-4xl opacity-50" />
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-6 text-white transform hover:scale-105 transition duration-300 shadow-lg">
          <div className="flex justify-between items-start">
            <div>
              <div className="text-sm opacity-80">INC / INDIA</div>
              <div className="text-5xl font-bold animate-count-up">{incLead}</div>
              <div className="text-sm opacity-80 mt-2">{incPercent.toFixed(1)}% of seats</div>
            </div>
            <FiAward className="text-4xl opacity-50" />
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-6 text-white transform hover:scale-105 transition duration-300 shadow-lg">
          <div className="flex justify-between items-start">
            <div>
              <div className="text-sm opacity-80">Others / Regional</div>
              <div className="text-5xl font-bold animate-count-up">{othersLead}</div>
              <div className="text-sm opacity-80 mt-2">{((othersLead / totalSeats) * 100).toFixed(1)}% of seats</div>
            </div>
            <FiMapPin className="text-4xl opacity-50" />
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-4 shadow">
        <div className="flex justify-between text-sm mb-2">
          <span className="text-orange-600">BJP/NDA: {bjpLead} seats</span>
          <span className="text-green-600">INC/INDIA: {incLead} seats</span>
          <span className="text-purple-600">Others: {othersLead} seats</span>
        </div>
        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
          <div 
            className="h-full bg-orange-500 float-left transition-all duration-500"
            style={{ width: `${(bjpLead / totalSeats) * 100}%` }}
          />
          <div 
            className="h-full bg-green-500 float-left transition-all duration-500"
            style={{ width: `${(incLead / totalSeats) * 100}%` }}
          />
          <div 
            className="h-full bg-purple-500 float-left transition-all duration-500"
            style={{ width: `${(othersLead / totalSeats) * 100}%` }}
          />
        </div>
      </div>

      {/* Trend Chart */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow">
        <h3 className="font-semibold mb-4 flex items-center gap-2">
          <FiBarChart2 /> Seat Trend Throughout the Day
        </h3>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="time" />
              <YAxis label={{ value: 'Seats', angle: -90, position: 'insideLeft' }} />
              <Tooltip 
                contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', border: 'none', borderRadius: '8px', color: '#fff' }}
              />
              <Legend />
              <Area type="monotone" dataKey="bjp" stackId="1" stroke="#F59E0B" fill="#F59E0B" fillOpacity={0.6} />
              <Area type="monotone" dataKey="inc" stackId="1" stroke="#00A896" fill="#00A896" fillOpacity={0.6} />
              <Area type="monotone" dataKey="others" stackId="1" stroke="#7C3AED" fill="#7C3AED" fillOpacity={0.6} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Live Indicator */}
      <div className="flex items-center justify-center gap-2 text-sm">
        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
        <span className="text-gray-500">Live updates via WebSocket • Auto-refreshing every 30 seconds</span>
      </div>
    </div>
  )
}