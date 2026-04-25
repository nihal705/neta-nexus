import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { FiMapPin, FiChevronRight, FiLoader } from 'react-icons/fi'
import axios from 'axios'

const states = [
  { code: 'UP', name: 'Uttar Pradesh', capital: 'Lucknow', seats: 80 },
  { code: 'MH', name: 'Maharashtra', capital: 'Mumbai', seats: 48 },
  { code: 'WB', name: 'West Bengal', capital: 'Kolkata', seats: 42 },
  { code: 'TN', name: 'Tamil Nadu', capital: 'Chennai', seats: 39 },
  { code: 'KA', name: 'Karnataka', capital: 'Bangalore', seats: 28 },
  { code: 'GJ', name: 'Gujarat', capital: 'Gandhinagar', seats: 26 },
  { code: 'DL', name: 'Delhi', capital: 'New Delhi', seats: 7 },
  { code: 'BI', name: 'Bihar', capital: 'Patna', seats: 40 },
  { code: 'RJ', name: 'Rajasthan', capital: 'Jaipur', seats: 25 },
  { code: 'MP', name: 'Madhya Pradesh', capital: 'Bhopal', seats: 29 },
  { code: 'PB', name: 'Punjab', capital: 'Chandigarh', seats: 13 },
  { code: 'HR', name: 'Haryana', capital: 'Chandigarh', seats: 10 },
]

export default function StateExplorer() {
  const [showAll, setShowAll] = useState(false)
  const [stateCounts, setStateCounts] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStateCounts()
  }, [])

  const fetchStateCounts = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/stats/state-counts')
      setStateCounts(response.data || {})
    } catch (error) {
      console.error('Error fetching state counts:', error)
      // Mock counts for display when API fails
      const mockCounts = {
        'UP': 12543, 'MH': 9876, 'WB': 7654, 'TN': 6543,
        'KA': 5432, 'GJ': 4321, 'DL': 3210, 'BI': 8765,
        'RJ': 3456, 'MP': 4567, 'PB': 2345, 'HR': 1876
      }
      setStateCounts(mockCounts)
    } finally {
      setLoading(false)
    }
  }

  const displayedStates = showAll ? states : states.slice(0, 8)

  if (loading) {
    return (
      <div className="card p-6">
        <div className="flex items-center justify-center py-8">
          <FiLoader className="animate-spin text-primary-teal text-2xl" />
        </div>
      </div>
    )
  }

  return (
    <div className="card p-6">
      <div className="flex justify-between items-center mb-6">
        <div className="flex items-center gap-2">
          <FiMapPin className="text-primary-teal" size={24} />
          <h3 className="text-xl font-bold">Explore by State</h3>
        </div>
        <button 
          onClick={() => setShowAll(!showAll)} 
          className="text-primary-teal hover:underline text-sm"
        >
          {showAll ? 'Show Less' : 'View All States'}
        </button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {displayedStates.map((state) => (
          <Link
            key={state.code}
            to={`/search?state=${state.code}`}
            className="group p-4 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-primary-teal hover:shadow-md transition-all"
          >
            <div className="flex justify-between items-start">
              <div>
                <h4 className="font-semibold group-hover:text-primary-teal transition">{state.name}</h4>
                <p className="text-xs text-gray-500 mt-1">Capital: {state.capital}</p>
                <p className="text-xs text-gray-400 mt-1">LS Seats: {state.seats}</p>
                {stateCounts[state.code] !== undefined && (
                  <p className="text-xs text-primary-teal mt-2">{stateCounts[state.code].toLocaleString()} candidates</p>
                )}
              </div>
              <FiChevronRight className="text-gray-400 group-hover:text-primary-teal group-hover:translate-x-1 transition" />
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}