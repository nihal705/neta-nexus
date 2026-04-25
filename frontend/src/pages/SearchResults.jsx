import { useState, useEffect } from 'react'
import { useSearchParams, Link } from 'react-router-dom'
import axios from 'axios'
import { FiFilter, FiX } from 'react-icons/fi'

export default function SearchResults() {
  const [searchParams, setSearchParams] = useSearchParams()
  const query = searchParams.get('q') || ''
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(true)
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [filters, setFilters] = useState({
    state: searchParams.get('state') || '',
    party: searchParams.get('party') || '',
  })
  const [filterOptions, setFilterOptions] = useState({ states: [], parties: [] })
  const [showFilters, setShowFilters] = useState(false)

  useEffect(() => {
    fetchFilters()
  }, [])

  useEffect(() => {
    searchCandidates()
  }, [query, page, filters.state, filters.party]) // Re-run when filters change

  const fetchFilters = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/search/filters')
      setFilterOptions(response.data)
    } catch (error) {
      console.error('Error fetching filters:', error)
    }
  }

  const searchCandidates = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (query) params.append('q', query)
      if (filters.state) params.append('state', filters.state)
      if (filters.party) params.append('party', filters.party)
      params.append('page', page)
      params.append('per_page', 24)
      
      const response = await axios.get(`http://localhost:8000/api/search/?${params}`)
      console.log('Search response:', response.data)
      setResults(response.data.candidates || [])
      setTotal(response.data.total || 0)
    } catch (error) {
      console.error('Search error:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (key, value) => {
    const newFilters = { ...filters, [key]: value }
    setFilters(newFilters)
    setPage(1)
    
    // Update URL
    const newParams = new URLSearchParams()
    if (query) newParams.set('q', query)
    if (value && key === 'state') newParams.set('state', value)
    if (newFilters.party) newParams.set('party', newFilters.party)
    setSearchParams(newParams)
  }

  const clearFilters = () => {
    setFilters({ state: '', party: '' })
    setPage(1)
    setSearchParams({ q: query })
  }

  const totalPages = Math.ceil(total / 24)

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold">Search Results</h1>
          <p className="text-gray-500 mt-1">Found {total.toLocaleString()} candidates</p>
        </div>
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="flex items-center gap-2 px-4 py-2 border rounded-lg hover:bg-gray-50"
        >
          <FiFilter /> Filters
          {(filters.state || filters.party) && (
            <span className="bg-primary-teal text-white text-xs px-2 py-0.5 rounded-full">
              {(filters.state ? 1 : 0) + (filters.party ? 1 : 0)}
            </span>
          )}
        </button>
      </div>

      {/* Filters Panel */}
      {showFilters && (
        <div className="bg-gray-50 dark:bg-gray-800 rounded-xl p-4 mb-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-semibold">Filters</h3>
            <button onClick={clearFilters} className="text-sm text-red-500 hover:underline">
              Clear All
            </button>
          </div>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="text-sm text-gray-500 block mb-1">State</label>
              <select
                value={filters.state}
                onChange={(e) => handleFilterChange('state', e.target.value)}
                className="w-full p-2 border rounded-lg dark:bg-gray-700"
              >
                <option value="">All States</option>
                {filterOptions.states?.map(state => (
                  <option key={state.code} value={state.code}>
                    {state.name} ({state.count?.toLocaleString()} candidates)
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-sm text-gray-500 block mb-1">Party</label>
              <select
                value={filters.party}
                onChange={(e) => handleFilterChange('party', e.target.value)}
                className="w-full p-2 border rounded-lg dark:bg-gray-700"
              >
                <option value="">All Parties</option>
                {filterOptions.parties?.map(party => (
                  <option key={party.name} value={party.name}>
                    {party.name} ({party.count?.toLocaleString()} candidates)
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      )}

      {/* Active Filters */}
      {(filters.state || filters.party) && (
        <div className="flex flex-wrap gap-2 mb-6">
          {filters.state && (
            <span className="flex items-center gap-1 bg-primary-teal/10 text-primary-teal px-3 py-1 rounded-full text-sm">
              State: {filterOptions.states?.find(s => s.code === filters.state)?.name || filters.state}
              <button onClick={() => handleFilterChange('state', '')}>
                <FiX size={14} />
              </button>
            </span>
          )}
          {filters.party && (
            <span className="flex items-center gap-1 bg-primary-teal/10 text-primary-teal px-3 py-1 rounded-full text-sm">
              Party: {filters.party}
              <button onClick={() => handleFilterChange('party', '')}>
                <FiX size={14} />
              </button>
            </span>
          )}
        </div>
      )}

      {/* Results */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1,2,3,4,5,6].map(i => (
            <div key={i} className="bg-white dark:bg-gray-800 rounded-xl p-4 animate-pulse h-32"></div>
          ))}
        </div>
      ) : results.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500">No candidates found. Try different filters.</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {results.map((candidate) => (
              <Link
                key={candidate.id}
                to={`/candidate/${candidate.id}`}
                className="bg-white dark:bg-gray-800 rounded-xl p-4 shadow hover:shadow-lg transition group"
              >
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-primary-teal to-primary-blue rounded-full flex items-center justify-center text-white font-bold">
                    {candidate.name?.charAt(0) || '?'}
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold group-hover:text-primary-teal transition">
                      {candidate.name}
                    </h3>
                    <p className="text-sm text-gray-500">{candidate.party || 'Independent'}</p>
                    {candidate.state_name && (
                      <p className="text-xs text-gray-400 mt-1">📍 {candidate.state_name}</p>
                    )}
                    {candidate.constituency_name && (
                      <p className="text-xs text-gray-400">🗳️ {candidate.constituency_name}</p>
                    )}
                    <div className="flex gap-3 mt-2 text-xs">
                      {candidate.age && <span>{candidate.age} yrs</span>}
                      {candidate.criminal_cases_count > 0 && (
                        <span className="text-red-500">⚠️ {candidate.criminal_cases_count} cases</span>
                      )}
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex justify-center gap-2 mt-8">
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
                className="px-3 py-1 border rounded-lg disabled:opacity-50"
              >
                Previous
              </button>
              <span className="px-3 py-1">Page {page} of {totalPages}</span>
              <button
                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="px-3 py-1 border rounded-lg disabled:opacity-50"
              >
                Next
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}