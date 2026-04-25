import { useState, useEffect } from 'react'
import axios from 'axios'

export function useSearch(query, filters = {}) {
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [total, setTotal] = useState(0)

  useEffect(() => {
    if (!query || query.length < 2) {
      setResults([])
      return
    }

    const search = async () => {
      setLoading(true)
      setError(null)
      try {
        const response = await axios.get('/api/search/', {
          params: { q: query, ...filters, per_page: 20 }
        })
        setResults(response.data.candidates)
        setTotal(response.data.total)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    const debounce = setTimeout(search, 300)
    return () => clearTimeout(debounce)
  }, [query, JSON.stringify(filters)])

  return { results, loading, error, total }
}