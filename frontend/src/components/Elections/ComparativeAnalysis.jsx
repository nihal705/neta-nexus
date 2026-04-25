import { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts'
import { FiTrendingUp, FiInfo, FiBarChart2 } from 'react-icons/fi'
import axios from 'axios'

export default function ComparativeAnalysis() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeAgency, setActiveAgency] = useState(null)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const response = await axios.get('/api/exitpolls/comparative?election_id=2024')
      setData(response.data)
    } catch (error) {
      console.error('Error fetching comparative data:', error)
      // Mock data for display
      setData({
        chart_data: {
          agencies: ['Axis My India', 'C-Voter', "Today's Chanakya", 'Republic TV', 'Times Now'],
          bjp_min: [295, 287, 305, 290, 285],
          bjp_max: [315, 305, 325, 310, 300],
          inc_min: [125, 132, 105, 130, 135],
          inc_max: [145, 150, 125, 148, 155]
        },
        consensus: {
          bjp_range: '290-310',
          inc_range: '130-145',
          description: 'Most polls predict BJP crossing 280 seats, INC improving from 2019',
          margin_of_error: '±4%'
        }
      })
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="card p-8">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/3"></div>
          <div className="h-64 bg-gray-200 dark:bg-gray-700 rounded"></div>
        </div>
      </div>
    )
  }

  // Prepare chart data
  const chartData = data?.chart_data?.agencies?.map((agency, idx) => ({
    agency,
    bjp_avg: (data.chart_data.bjp_min[idx] + data.chart_data.bjp_max[idx]) / 2,
    inc_avg: (data.chart_data.inc_min[idx] + data.chart_data.inc_max[idx]) / 2,
    bjp_range: `${data.chart_data.bjp_min[idx]}-${data.chart_data.bjp_max[idx]}`,
    inc_range: `${data.chart_data.inc_min[idx]}-${data.chart_data.inc_max[idx]}`
  })) || []

  const colors = {
    bjp: '#F59E0B',
    inc: '#00A896'
  }

  return (
    <div className="card p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold flex items-center gap-2">
          <FiBarChart2 className="text-primary-teal" />
          Comparative Exit Poll Analysis
        </h2>
        <div className="flex items-center gap-1 text-xs text-gray-400">
          <FiInfo /> Based on published exit polls
        </div>
      </div>

      {/* Chart */}
      <div className="h-96 mb-8">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis 
              dataKey="agency" 
              angle={-45} 
              textAnchor="end" 
              height={80}
              interval={0}
              tick={{ fontSize: 12 }}
            />
            <YAxis label={{ value: 'Seat Projections', angle: -90, position: 'insideLeft' }} />
            <Tooltip 
              content={({ active, payload, label }) => {
                if (active && payload && payload.length) {
                  const dataPoint = chartData.find(d => d.agency === label)
                  return (
                    <div className="bg-white dark:bg-gray-800 p-3 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
                      <p className="font-semibold mb-2">{label}</p>
                      <div className="space-y-1 text-sm">
                        <p className="text-orange-600">BJP: {dataPoint?.bjp_range}</p>
                        <p className="text-green-600">INC: {dataPoint?.inc_range}</p>
                      </div>
                    </div>
                  )
                }
                return null
              }}
            />
            <Legend 
              verticalAlign="top" 
              height={36}
              formatter={(value) => <span className="text-sm font-medium">{value === 'bjp_avg' ? 'BJP/NDA' : 'INC/INDIA'}</span>}
            />
            <Bar dataKey="bjp_avg" name="BJP/NDA" fill={colors.bjp} radius={[4, 4, 0, 0]} />
            <Bar dataKey="inc_avg" name="INC/INDIA" fill={colors.inc} radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Consensus Section */}
      {data?.consensus && (
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-xl p-6">
          <h3 className="font-bold text-lg mb-3 flex items-center gap-2">
            <FiTrendingUp className="text-primary-teal" />
            Consensus Analysis
          </h3>
          <p className="text-gray-700 dark:text-gray-300 mb-4">{data.consensus.description}</p>
          <div className="flex flex-wrap gap-6">
            <div>
              <div className="text-sm text-gray-500">BJP Range</div>
              <div className="text-2xl font-bold text-orange-600">{data.consensus.bjp_range}</div>
            </div>
            <div>
              <div className="text-sm text-gray-500">INC Range</div>
              <div className="text-2xl font-bold text-green-600">{data.consensus.inc_range}</div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Margin of Error</div>
              <div className="text-2xl font-bold text-gray-700">{data.consensus.margin_of_error || '±5%'}</div>
            </div>
          </div>
        </div>
      )}

      {/* Agency Cards */}
      <div className="mt-6">
        <h3 className="font-semibold mb-3">Individual Agency Predictions</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
          {chartData.map((agency, idx) => (
            <button
              key={idx}
              onClick={() => setActiveAgency(activeAgency === idx ? null : idx)}
              className="p-3 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-primary-teal hover:shadow-md transition-all text-left"
            >
              <div className="font-medium text-sm mb-2">{agency.agency}</div>
              <div className="space-y-1 text-xs">
                <div className="flex justify-between">
                  <span className="text-orange-600">BJP:</span>
                  <span>{agency.bjp_range}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-green-600">INC:</span>
                  <span>{agency.inc_range}</span>
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}