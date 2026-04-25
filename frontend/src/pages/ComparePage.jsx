import { useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import axios from 'axios'
import { FiPlus, FiTrash2, FiArrowRight } from 'react-icons/fi'
import SearchBar from '../components/UI/SearchBar'
import LoadingSpinner from '../components/UI/LoadingSpinner'
import toast from 'react-hot-toast'

export default function ComparePage() {
  const [searchParams] = useSearchParams()
  const [selectedIds, setSelectedIds] = useState(() => {
    const ids = searchParams.get('ids')
    return ids ? ids.split(',').map(Number) : []
  })
  const [candidates, setCandidates] = useState([])
  const [loading, setLoading] = useState(false)
  const [showAdd, setShowAdd] = useState(false)

  const handleAddCandidate = (candidateId) => {
    if (selectedIds.length >= 5) {
      toast.error('Maximum 5 candidates can be compared')
      return
    }
    if (!selectedIds.includes(candidateId)) {
      setSelectedIds([...selectedIds, candidateId])
      setShowAdd(false)
      fetchCandidates([...selectedIds, candidateId])
    } else {
      toast.error('Candidate already added')
    }
  }

  const handleRemoveCandidate = (index) => {
    const newIds = selectedIds.filter((_, i) => i !== index)
    setSelectedIds(newIds)
    fetchCandidates(newIds)
  }

  const fetchCandidates = async (ids) => {
    if (ids.length === 0) {
      setCandidates([])
      return
    }
    setLoading(true)
    try {
      const response = await axios.post('/api/compare/', { candidate_ids: ids })
      setCandidates(response.data.candidates)
    } catch (error) {
      console.error('Error fetching candidates:', error)
      toast.error('Failed to load candidates')
    } finally {
      setLoading(false)
    }
  }

  const handleCandidateSelect = (candidate) => {
    handleAddCandidate(candidate.id)
  }

  const getWorstValue = (field, values) => {
    if (field === 'criminal_cases') return Math.max(...values)
    if (field === 'total_assets') return Math.max(...values)
    return null
  }

  const getBestValue = (field, values) => {
    if (field === 'criminal_cases') return Math.min(...values)
    if (field === 'total_assets') return Math.max(...values)
    return null
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8"
    >
      <div className="mb-8">
        <h1 className="text-3xl font-bold">📊 Compare Candidates</h1>
        <p className="text-gray-500 mt-2">Compare up to 5 candidates side by side</p>
      </div>

      {/* Add Candidate Button */}
      {selectedIds.length < 5 && (
        <div className="mb-6">
          {!showAdd ? (
            <button
              onClick={() => setShowAdd(true)}
              className="flex items-center gap-2 px-4 py-2 border-2 border-dashed border-primary-teal rounded-lg text-primary-teal hover:bg-primary-teal/10 transition"
            >
              <FiPlus /> Add Candidate
            </button>
          ) : (
            <div className="card p-4">
              <div className="flex justify-between items-center mb-3">
                <h3 className="font-semibold">Search Candidate to Add</h3>
                <button onClick={() => setShowAdd(false)} className="text-gray-500">✕</button>
              </div>
              <SearchBar onSelect={handleCandidateSelect} />
            </div>
          )}
        </div>
      )}

      {loading && <LoadingSpinner />}

      {candidates.length > 0 && (
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr>
                <th className="p-3 text-left bg-gray-50 dark:bg-gray-800 rounded-l-lg">Attribute</th>
                {candidates.map((candidate, idx) => (
                  <th key={idx} className="p-3 text-left bg-gray-50 dark:bg-gray-800 min-w-[200px]">
                    <div className="flex justify-between items-center">
                      <div>
                        <div className="font-semibold">{candidate.name}</div>
                        <div className="text-sm text-gray-500">{candidate.party}</div>
                      </div>
                      <button onClick={() => handleRemoveCandidate(idx)} className="text-red-500 hover:text-red-700">
                        <FiTrash2 size={16} />
                      </button>
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <tr className="border-b">
                <td className="p-3 font-medium">Age</td>
                {candidates.map((c, idx) => (
                  <td key={idx} className="p-3">{c.age || 'N/A'}</td>
                ))}
              </tr>
              <tr className="border-b">
                <td className="p-3 font-medium">Education</td>
                {candidates.map((c, idx) => (
                  <td key={idx} className="p-3">{c.education || 'N/A'}</td>
                ))}
              </tr>
              <tr className="border-b">
                <td className="p-3 font-medium">Profession</td>
                {candidates.map((c, idx) => (
                  <td key={idx} className="p-3">{c.profession || 'N/A'}</td>
                ))}
              </tr>
              <tr className="border-b">
                <td className="p-3 font-medium">Total Assets</td>
                {candidates.map((c, idx) => {
                  const assetValue = parseFloat(c.total_assets?.toString().replace(/[₹,]/g, '') || 0)
                  const maxAsset = Math.max(...candidates.map(c => parseFloat(c.total_assets?.toString().replace(/[₹,]/g, '') || 0)))
                  const isBest = assetValue === maxAsset && maxAsset > 0
                  return (
                    <td key={idx} className={`p-3 ${isBest ? 'bg-green-50 dark:bg-green-900/20 font-semibold' : ''}`}>
                      {c.total_assets || 'N/A'}
                      {isBest && <span className="ml-2 text-green-600 text-xs">🏆 Best</span>}
                    </td>
                  )
                })}
              </tr>
              <tr className="border-b">
                <td className="p-3 font-medium">Criminal Cases</td>
                {candidates.map((c, idx) => {
                  const caseCount = c.criminal_cases?.length || 0
                  const minCases = Math.min(...candidates.map(c => c.criminal_cases?.length || 0))
                  const isBest = caseCount === minCases
                  return (
                    <td key={idx} className={`p-3 ${isBest ? 'bg-green-50 dark:bg-green-900/20' : caseCount > 0 ? 'bg-red-50 dark:bg-red-900/20' : ''}`}>
                      {caseCount}
                      {isBest && caseCount === 0 && <span className="ml-2 text-green-600 text-xs">✓ Clean</span>}
                    </td>
                  )
                })}
              </tr>
              <tr className="border-b">
                <td className="p-3 font-medium">Election Wins</td>
                {candidates.map((c, idx) => {
                  const wins = c.election_results?.filter(r => r.winner).length || 0
                  const maxWins = Math.max(...candidates.map(c => c.election_results?.filter(r => r.winner).length || 0))
                  const isBest = wins === maxWins && maxWins > 0
                  return (
                    <td key={idx} className={`p-3 ${isBest ? 'bg-green-50 dark:bg-green-900/20 font-semibold' : ''}`}>
                      {wins}
                      {isBest && <span className="ml-2 text-green-600 text-xs">🏆 Most</span>}
                    </td>
                  )
                })}
              </tr>
              <tr>
                <td className="p-3 font-medium">Action</td>
                {candidates.map((c, idx) => (
                  <td key={idx} className="p-3">
                    <a href={`/candidate/${c.id}`} className="text-primary-teal hover:underline flex items-center gap-1">
                      View Profile <FiArrowRight size={14} />
                    </a>
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>
      )}

      {candidates.length === 0 && !loading && (
        <div className="text-center py-12">
          <p className="text-gray-500">Add candidates to start comparing</p>
        </div>
      )}
    </motion.div>
  )
}