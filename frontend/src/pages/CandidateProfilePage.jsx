import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import axios from 'axios'
import { 
  FiCalendar, FiMapPin, FiBriefcase, FiBookOpen, 
  FiAlertCircle, FiTrendingUp, FiAward, FiShare2, 
  FiBookmark, FiChevronLeft, FiDollarSign, FiHome,
  FiUserCheck, FiFileText, FiStar, FiBarChart2, FiCheckCircle, FiXCircle
} from 'react-icons/fi'
import LoadingSpinner from '../components/UI/LoadingSpinner'
import toast from 'react-hot-toast'

export default function CandidateProfilePage() {
  const { id } = useParams()
  const [candidate, setCandidate] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')
  const [bookmarked, setBookmarked] = useState(false)

  useEffect(() => {
    fetchCandidate()
    const bookmarks = JSON.parse(localStorage.getItem('bookmarks') || '[]')
    setBookmarked(bookmarks.includes(parseInt(id)))
  }, [id])

  const fetchCandidate = async () => {
    try {
      const response = await axios.get(`/api/candidates/${id}`)
      setCandidate(response.data)
    } catch (error) {
      console.error('Error fetching candidate:', error)
      toast.error('Failed to load candidate data')
    } finally {
      setLoading(false)
    }
  }

  const handleBookmark = () => {
    const bookmarks = JSON.parse(localStorage.getItem('bookmarks') || '[]')
    if (bookmarked) {
      const newBookmarks = bookmarks.filter(b => b !== parseInt(id))
      localStorage.setItem('bookmarks', JSON.stringify(newBookmarks))
      setBookmarked(false)
      toast.success('Removed from bookmarks')
    } else {
      bookmarks.push(parseInt(id))
      localStorage.setItem('bookmarks', JSON.stringify(bookmarks))
      setBookmarked(true)
      toast.success('Added to bookmarks')
    }
  }

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href)
    toast.success('Link copied to clipboard!')
  }

  // Generate avatar
  const getInitials = (name) => name ? name.charAt(0).toUpperCase() : '?'
  const getAvatarColor = (id) => {
    const colors = ['from-blue-500 to-cyan-500', 'from-green-500 to-teal-500', 'from-purple-500 to-pink-500', 'from-orange-500 to-red-500']
    return colors[id % colors.length]
  }

  if (loading) return <LoadingSpinner />

  if (!candidate) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Candidate not found</p>
        <Link to="/" className="text-primary-teal hover:underline mt-4 inline-block">← Back to Home</Link>
      </div>
    )
  }

  const tabs = [
    { id: 'overview', label: 'Overview', icon: <FiUserCheck /> },
    { id: 'affidavit', label: 'Assets & Affidavit', icon: <FiFileText /> },
    { id: 'criminal', label: 'Criminal Records', icon: <FiAlertCircle /> },
    { id: 'elections', label: 'Election History', icon: <FiTrendingUp /> },
    { id: 'performance', label: 'Performance', icon: <FiStar /> },
  ]

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8"
    >
      {/* Back Button */}
      <Link to="/search" className="inline-flex items-center gap-2 text-gray-500 hover:text-primary-teal mb-4 transition">
        <FiChevronLeft /> Back to Search
      </Link>

      {/* Header Card */}
      <div className="card overflow-hidden mb-8">
        <div className="bg-gradient-to-r from-primary-navy via-primary-blue to-primary-teal px-6 py-8">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div className="flex items-center gap-4">
              {/* Large Avatar */}
              <div className={`w-20 h-20 bg-gradient-to-br ${getAvatarColor(candidate.id)} rounded-full flex items-center justify-center text-white text-3xl font-bold shadow-lg`}>
                {getInitials(candidate.name)}
              </div>
              <div>
                <h1 className="text-3xl md:text-4xl font-bold text-white">{candidate.name}</h1>
                <p className="text-white/80 mt-1 text-lg">{candidate.party || 'Independent'}</p>
                <div className="flex flex-wrap gap-2 mt-2">
                  {candidate.is_current && (
                    <span className="bg-green-500 text-white text-xs px-3 py-1 rounded-full">Current Representative</span>
                  )}
                  {candidate.criminal_cases?.length > 0 && (
                    <span className="bg-red-500 text-white text-xs px-3 py-1 rounded-full">
                      ⚠️ {candidate.criminal_cases.length} Criminal Case(s)
                    </span>
                  )}
                </div>
              </div>
            </div>
            <div className="flex gap-2">
              <button onClick={handleBookmark} className="p-2 bg-white/20 rounded-full hover:bg-white/30 transition">
                <FiBookmark className={bookmarked ? 'fill-yellow-400 text-yellow-400' : 'text-white'} size={20} />
              </button>
              <button onClick={handleShare} className="p-2 bg-white/20 rounded-full hover:bg-white/30 transition">
                <FiShare2 className="text-white" size={20} />
              </button>
            </div>
          </div>
        </div>
        
        {/* Quick Info Grid */}
        <div className="p-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-primary-teal/10 rounded-full flex items-center justify-center">
                <FiCalendar className="text-primary-teal" />
              </div>
              <div>
                <div className="text-xs text-gray-400">Age</div>
                <div className="font-semibold">{candidate.age || 'Not specified'}</div>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-primary-teal/10 rounded-full flex items-center justify-center">
                <FiMapPin className="text-primary-teal" />
              </div>
              <div>
                <div className="text-xs text-gray-400">Constituency</div>
                <div className="font-semibold">{candidate.constituency_name || 'Not assigned'}</div>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-primary-teal/10 rounded-full flex items-center justify-center">
                <FiBriefcase className="text-primary-teal" />
              </div>
              <div>
                <div className="text-xs text-gray-400">Profession</div>
                <div className="font-semibold">{candidate.profession || 'Politician'}</div>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-primary-teal/10 rounded-full flex items-center justify-center">
                <FiBookOpen className="text-primary-teal" />
              </div>
              <div>
                <div className="text-xs text-gray-400">Education</div>
                <div className="font-semibold truncate max-w-[150px]">{candidate.education || 'Not specified'}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 dark:border-gray-700 mb-6 overflow-x-auto">
        <div className="flex gap-1 min-w-max">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-t-lg transition ${
                activeTab === tab.id
                  ? 'bg-primary-teal text-white'
                  : 'text-gray-500 hover:text-primary-teal hover:bg-gray-100 dark:hover:bg-gray-800'
              }`}
            >
              {tab.icon}
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Tab Content */}
      <div className="space-y-6">
        {activeTab === 'overview' && (
          <div className="grid lg:grid-cols-2 gap-6">
            <div className="card p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <FiFileText /> Profile Summary
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between py-2 border-b">
                  <span className="text-gray-500">Full Name</span>
                  <span className="font-medium">{candidate.name}</span>
                </div>
                <div className="flex justify-between py-2 border-b">
                  <span className="text-gray-500">Party Affiliation</span>
                  <span className="font-medium">{candidate.party || 'Independent'}</span>
                </div>
                <div className="flex justify-between py-2 border-b">
                  <span className="text-gray-500">Gender</span>
                  <span className="font-medium">{candidate.gender || 'Not specified'}</span>
                </div>
                <div className="flex justify-between py-2 border-b">
                  <span className="text-gray-500">Education</span>
                  <span className="font-medium">{candidate.education || 'Not specified'}</span>
                </div>
                <div className="flex justify-between py-2 border-b">
                  <span className="text-gray-500">Profession</span>
                  <span className="font-medium">{candidate.profession || 'Not specified'}</span>
                </div>
                <div className="flex justify-between py-2 border-b">
                  <span className="text-gray-500">Status</span>
                  <span className="font-medium">{candidate.is_current ? 'Currently in Office' : 'Former Representative'}</span>
                </div>
              </div>
            </div>
            
            <div className="card p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <FiBarChart2 /> Quick Statistics
              </h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="text-2xl font-bold text-primary-teal">{candidate.election_results?.length || 0}</div>
                  <div className="text-xs text-gray-500">Elections Contested</div>
                </div>
                <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="text-2xl font-bold text-primary-teal">
                    {candidate.election_results?.filter(r => r.winner).length || 0}
                  </div>
                  <div className="text-xs text-gray-500">Elections Won</div>
                </div>
                <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="text-2xl font-bold text-red-500">{candidate.criminal_cases?.length || 0}</div>
                  <div className="text-xs text-gray-500">Criminal Cases</div>
                </div>
                <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="text-2xl font-bold text-primary-teal">
                    {candidate.parliamentary_score?.composite_score || 'N/A'}
                  </div>
                  <div className="text-xs text-gray-500">Performance Score</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'affidavit' && candidate.affidavit && (
          <div className="card p-6">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <FiAward /> Assets Declaration
            </h2>
            
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div className="bg-green-50 dark:bg-green-900/20 rounded-xl p-4">
                  <div className="text-sm text-gray-500">Total Assets</div>
                  <div className="text-2xl font-bold text-green-600">{candidate.affidavit.total_assets || 'N/A'}</div>
                </div>
                <div className="bg-blue-50 dark:bg-blue-900/20 rounded-xl p-4">
                  <div className="text-sm text-gray-500">Movable Assets</div>
                  <div className="text-xl font-bold">{candidate.affidavit.movable_assets || 'N/A'}</div>
                </div>
                <div className="bg-purple-50 dark:bg-purple-900/20 rounded-xl p-4">
                  <div className="text-sm text-gray-500">Immovable Assets</div>
                  <div className="text-xl font-bold">{candidate.affidavit.immovable_assets || 'N/A'}</div>
                </div>
              </div>
              <div className="space-y-4">
                <div className="bg-red-50 dark:bg-red-900/20 rounded-xl p-4">
                  <div className="text-sm text-gray-500">Total Liabilities</div>
                  <div className="text-xl font-bold text-red-600">{candidate.affidavit.total_liabilities || 'None'}</div>
                </div>
                <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-xl p-4">
                  <div className="text-sm text-gray-500">Annual Income</div>
                  <div className="text-xl font-bold">{candidate.affidavit.annual_income || 'N/A'}</div>
                </div>
              </div>
            </div>
            
            {candidate.affidavit.education_details && (
              <div className="mt-4 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <p className="text-sm text-gray-600 dark:text-gray-300">{candidate.affidavit.education_details}</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'criminal' && (
          <div className="card p-6">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <FiAlertCircle className="text-red-500" /> Criminal Records
            </h2>
            {candidate.criminal_cases && candidate.criminal_cases.length > 0 ? (
              <div className="space-y-4">
                {candidate.criminal_cases.map((case_, idx) => (
                  <div key={idx} className="border border-red-200 dark:border-red-800 rounded-lg p-4 bg-red-50 dark:bg-red-900/10">
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="font-semibold text-red-700 dark:text-red-400">{case_.case_number || `Case ${idx + 1}`}</p>
                        <p className="text-sm mt-1">IPC Sections: {case_.sections || 'Not specified'}</p>
                        <p className="text-sm">Court: {case_.court_name || 'Unknown'}</p>
                        <p className="text-sm">Status: {case_.status || 'Pending'}</p>
                      </div>
                      {case_.filed_before_election && (
                        <span className="text-xs bg-orange-100 text-orange-600 px-2 py-1 rounded">Filed before election</span>
                      )}
                    </div>
                    {case_.case_details && (
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">{case_.case_details}</p>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="bg-green-50 dark:bg-green-900/20 rounded-xl p-6 text-center">
                <FiCheckCircle className="text-green-500 text-4xl mx-auto mb-2" />
                <p className="text-green-700 dark:text-green-400 font-medium">No Criminal Cases Reported</p>
                <p className="text-sm text-green-600 dark:text-green-500 mt-1">As per self-sworn affidavit filed with Election Commission</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'elections' && candidate.election_results && candidate.election_results.length > 0 && (
          <div className="card p-6">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <FiTrendingUp /> Election History
            </h2>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th className="px-4 py-3 text-left text-sm font-semibold">Year</th>
                    <th className="px-4 py-3 text-left text-sm font-semibold">Type</th>
                    <th className="px-4 py-3 text-left text-sm font-semibold">Votes</th>
                    <th className="px-4 py-3 text-left text-sm font-semibold">Percentage</th>
                    <th className="px-4 py-3 text-left text-sm font-semibold">Result</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                  {candidate.election_results.map((result, idx) => (
                    <tr key={idx} className="hover:bg-gray-50 dark:hover:bg-gray-800 transition">
                      <td className="px-4 py-3">{result.election_year}</td>
                      <td className="px-4 py-3">{result.election_type || 'General Election'}</td>
                      <td className="px-4 py-3">{result.votes_received?.toLocaleString()}</td>
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-2">
                          <span>{result.vote_percentage}%</span>
                          <div className="w-20 bg-gray-200 rounded-full h-1.5">
                            <div className="bg-primary-teal h-1.5 rounded-full" style={{ width: `${Math.min(result.vote_percentage, 100)}%` }}></div>
                          </div>
                        </div>
                      </td>
                      <td className="px-4 py-3">
                        {result.winner ? (
                          <span className="bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs font-medium">🏆 Won</span>
                        ) : (
                          <span className="bg-gray-100 text-gray-500 px-2 py-1 rounded-full text-xs">Lost</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'performance' && (
          <div className="card p-6">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <FiStar /> Parliamentary Performance
            </h2>
            {candidate.parliamentary_score ? (
              <div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                    <div className="text-2xl font-bold text-primary-teal">{candidate.parliamentary_score.attendance_percentage}%</div>
                    <div className="text-xs text-gray-500">Attendance</div>
                  </div>
                  <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                    <div className="text-2xl font-bold text-primary-teal">{candidate.parliamentary_score.questions_asked}</div>
                    <div className="text-xs text-gray-500">Questions Asked</div>
                  </div>
                  <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                    <div className="text-2xl font-bold text-primary-teal">{candidate.parliamentary_score.debates_participated}</div>
                    <div className="text-xs text-gray-500">Debates Participated</div>
                  </div>
                  <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                    <div className="text-2xl font-bold text-primary-teal">{candidate.parliamentary_score.private_member_bills}</div>
                    <div className="text-xs text-gray-500">Private Bills</div>
                  </div>
                </div>
                
                <div className="bg-gradient-to-r from-primary-blue to-primary-teal rounded-xl p-6 text-white">
                  <div className="text-center">
                    <div className="text-sm opacity-80">Composite Performance Score</div>
                    <div className="text-5xl font-bold">{candidate.parliamentary_score.composite_score}</div>
                    <div className="text-sm opacity-80 mt-2">out of 100</div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <p>Parliamentary performance data not available for this candidate</p>
                <p className="text-sm mt-2">This candidate may be from State Assembly or data not yet updated</p>
              </div>
            )}
          </div>
        )}
      </div>
    </motion.div>
  )
}