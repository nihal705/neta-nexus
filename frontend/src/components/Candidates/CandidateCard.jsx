import { Link } from 'react-router-dom'
import { FiUser, FiMapPin, FiBriefcase } from 'react-icons/fi'

export default function CandidateCard({ candidate }) {
  // Generate avatar from name
  const getInitials = (name) => {
    return name ? name.charAt(0).toUpperCase() : '?'
  }

  const getAvatarColor = (id) => {
    const colors = ['from-blue-500 to-cyan-500', 'from-green-500 to-teal-500', 'from-purple-500 to-pink-500', 'from-orange-500 to-red-500', 'from-indigo-500 to-purple-500']
    return colors[id % colors.length]
  }

  return (
    <Link to={`/candidate/${candidate.id}`}>
      <div className="card p-4 hover:shadow-xl transition-all group">
        <div className="flex gap-4">
          {/* Avatar */}
          <div className={`w-16 h-16 bg-gradient-to-br ${getAvatarColor(candidate.id)} rounded-full flex items-center justify-center text-white text-2xl font-bold shadow-md`}>
            {getInitials(candidate.name)}
          </div>
          
          <div className="flex-1">
            <h3 className="font-semibold text-lg group-hover:text-primary-teal transition">{candidate.name}</h3>
            <p className="text-sm text-gray-500">{candidate.party || 'Independent'}</p>
            
            <div className="flex flex-wrap gap-3 mt-2 text-xs text-gray-400">
              {candidate.age && (
                <span className="flex items-center gap-1"><FiUser size={12} /> {candidate.age} yrs</span>
              )}
              {candidate.constituency_name && (
                <span className="flex items-center gap-1"><FiMapPin size={12} /> {candidate.constituency_name}</span>
              )}
              {candidate.profession && (
                <span className="flex items-center gap-1"><FiBriefcase size={12} /> {candidate.profession}</span>
              )}
            </div>
            
            {/* Criminal cases badge */}
            {candidate.criminal_cases > 0 && (
              <span className="inline-block mt-2 text-xs bg-red-100 text-red-600 px-2 py-0.5 rounded-full">
                ⚠️ {candidate.criminal_cases} case(s)
              </span>
            )}
          </div>
        </div>
      </div>
    </Link>
  )
}