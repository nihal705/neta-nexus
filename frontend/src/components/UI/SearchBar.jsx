import { useState, useEffect, useRef } from 'react'
import { FiSearch } from 'react-icons/fi'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

export default function SearchBar({ placeholder = "Search candidates, parties, constituencies..." }) {
  const [query, setQuery] = useState('')
  const [suggestions, setSuggestions] = useState([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const navigate = useNavigate()
  const wrapperRef = useRef(null)

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setShowSuggestions(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  useEffect(() => {
    const fetchSuggestions = async () => {
      if (query.length < 2) {
        setSuggestions([])
        return
      }
      try {
        const response = await axios.get(`/api/search/autocomplete?q=${encodeURIComponent(query)}`)
        setSuggestions(response.data)
        setShowSuggestions(true)
      } catch (error) {
        console.error('Error fetching suggestions:', error)
      }
    }

    const debounce = setTimeout(fetchSuggestions, 300)
    return () => clearTimeout(debounce)
  }, [query])

  const handleSearch = (e) => {
    e.preventDefault()
    if (query.trim()) {
      navigate(`/search?q=${encodeURIComponent(query)}`)
      setShowSuggestions(false)
    }
  }

  const handleSuggestionClick = (suggestion) => {
    if (suggestion.type === 'candidate') {
      navigate(`/candidate/${suggestion.id}`)
    } else {
      navigate(`/search?q=${encodeURIComponent(suggestion.name)}`)
    }
    setShowSuggestions(false)
    setQuery('')
  }

  return (
    <div ref={wrapperRef} className="relative w-full">
      <form onSubmit={handleSearch}>
        <div className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onFocus={() => query.length >= 2 && setSuggestions.length > 0 && setShowSuggestions(true)}
            placeholder={placeholder}
            className="w-full px-4 py-3 pl-10 rounded-xl border border-gray-200 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-primary-teal dark:bg-gray-800"
          />
          <FiSearch className="absolute left-3 top-3.5 text-gray-400" size={18} />
          <button type="submit" className="absolute right-2 top-1.5 px-4 py-1.5 bg-primary-teal text-white rounded-lg text-sm hover:bg-opacity-90">
            Search
          </button>
        </div>
      </form>

      {showSuggestions && suggestions.length > 0 && (
        <div className="absolute z-50 mt-2 w-full bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
          {suggestions.map((suggestion, idx) => (
            <button
              key={idx}
              onClick={() => handleSuggestionClick(suggestion)}
              className="w-full text-left px-4 py-2 hover:bg-gray-50 dark:hover:bg-gray-700 transition flex items-center justify-between"
            >
              <div>
                <div className="font-medium">{suggestion.name}</div>
                {suggestion.party && <div className="text-xs text-gray-500">{suggestion.party}</div>}
              </div>
              <div className="text-xs text-gray-400">
                {suggestion.type === 'candidate' ? 'Candidate' : 'Party'}
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}