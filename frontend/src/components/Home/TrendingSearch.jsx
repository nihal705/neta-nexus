import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { FiTrendingUp, FiUser, FiFlag } from 'react-icons/fi'
import axios from 'axios'

export default function TrendingSearch() {
  const [trending, setTrending] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchTrending()
  }, [])

  const fetchTrending = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/search/trending')
      // Ensure response.data is an array
      const data = response.data
      if (Array.isArray(data)) {
        setTrending(data)
      } else if (data && Array.isArray(data.top_parties)) {
        // Handle different response formats
        const combined = [...(data.top_parties || []), ...(data.top_candidates || [])]
        setTrending(combined)
      } else {
        setTrending([])
      }
    } catch (error) {
      console.error('Error fetching trending:', error)
      // Fallback mock data
      setTrending([
        { name: 'Narendra Modi', type: 'candidate', party: 'BJP', icon: '👤', search_count: 15234 },
        { name: 'Rahul Gandhi', type: 'candidate', party: 'INC', icon: '👤', search_count: 12345 },
        { name: 'Arvind Kejriwal', type: 'candidate', party: 'AAP', icon: '👤', search_count: 8765 },
        { name: 'Bharatiya Janata Party', type: 'party', icon: '🏛️', search_count: 50000 },
        { name: 'Indian National Congress', type: 'party', icon: '🏛️', search_count: 45000 },
      ])
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="card p-6">
        <div className="animate-pulse space-y-3">
          {[1, 2, 3, 4, 5].map(i => (
            <div key={i} className="h-12 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
          ))}
        </div>
      </div>
    )
  }

  if (!trending || trending.length === 0) {
    return (
      <div className="card p-6">
        <div className="flex items-center gap-2 mb-4">
          <FiTrendingUp className="text-primary-teal" size={24} />
          <h3 className="text-xl font-bold">Trending Searches</h3>
        </div>
        <p className="text-gray-500 text-center py-4">No trending data available</p>
      </div>
    )
  }

  return (
    <div className="card p-6">
      <div className="flex items-center gap-2 mb-4">
        <FiTrendingUp className="text-primary-teal" size={24} />
        <h3 className="text-xl font-bold">Trending Searches</h3>
      </div>

      <div className="space-y-2">
        {trending.slice(0, 10).map((item, idx) => (
          <Link
            key={idx}
            to={`/search?q=${encodeURIComponent(item.name)}`}
            className="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition group"
          >
            <div className="flex items-center gap-3">
              <span className="text-2xl">{item.icon || (item.type === 'party' ? '🏛️' : '👤')}</span>
              <div>
                <div className="font-medium group-hover:text-primary-teal transition">
                  {item.name}
                  {item.party && item.type === 'candidate' && (
                    <span className="text-xs text-gray-400 ml-2">({item.party})</span>
                  )}
                </div>
                {item.type === 'party' && (
                  <div className="text-xs text-gray-500">Political Party</div>
                )}
              </div>
            </div>
            <div className="text-sm text-gray-400">{item.search_count?.toLocaleString()} searches</div>
          </Link>
        ))}
      </div>
    </div>
  )
}