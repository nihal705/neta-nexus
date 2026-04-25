import { Link } from 'react-router-dom'
import { FiTrash2, FiArrowRight, FiCheck, FiX, FiTrendingUp, FiAlertCircle } from 'react-icons/fi'

export default function ComparisonTable({ candidates, onRemove, loading }) {
  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="animate-pulse">Loading comparison data...</div>
      </div>
    )
  }

  if (!candidates || candidates.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Add candidates to start comparing</p>
      </div>
    )
  }

  // Helper to determine best/worst values
  const getBestValue = (field, values) => {
    if (field === 'criminal_cases') return Math.min(...values)
    if (field === 'assets_value') return Math.max(...values)
    if (field === 'election_wins') return Math.max(...values)
    if (field === 'attendance') return Math.max(...values)
    return null
  }

  const parseAssetValue = (assetStr) => {
    if (!assetStr || assetStr === 'N/A') return 0
    const num = parseFloat(assetStr.toString().replace(/[₹,]/g, ''))
    return isNaN(num) ? 0 : num
  }

  const rows = [
    { 
      label: 'Party', 
      key: 'party',
      getValue: (c) => c.party || 'Independent',
      isComparison: false
    },
    { 
      label: 'Age', 
      key: 'age',
      getValue: (c) => c.age || 'N/A',
      isComparison: false
    },
    { 
      label: 'Education', 
      key: 'education',
      getValue: (c) => c.education || 'N/A',
      isComparison: false
    },
    { 
      label: 'Profession', 
      key: 'profession',
      getValue: (c) => c.profession || 'N/A',
      isComparison: false
    },
    { 
      label: 'Total Assets', 
      key: 'assets_value',
      getValue: (c) => c.total_assets || 'N/A',
      format: (v) => v,
      compare: true,
      better: 'higher'
    },
    { 
      label: 'Criminal Cases', 
      key: 'criminal_cases',
      getValue: (c) => c.criminal_cases || 0,
      format: (v) => v,
      compare: true,
      better: 'lower',
      icon: <FiAlertCircle className="text-red-500" size={14} />
    },
    { 
      label: 'Election Wins', 
      key: 'election_wins',
      getValue: (c) => c.election_wins || 0,
      format: (v) => v,
      compare: true,
      better: 'higher',
      icon: <FiTrendingUp className="text-green-500" size={14} />
    },
    { 
      label: 'Parliamentary Score', 
      key: 'parliamentary_score',
      getValue: (c) => c.parliamentary_score?.composite_score || 'N/A',
      format: (v) => typeof v === 'number' ? `${v}%` : v,
      compare: true,
      better: 'higher'
    },
  ]

  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse">
        {/* Header */}
        <thead>
          <tr>
            <th className="p-4 text-left bg-gray-50 dark:bg-gray-800 rounded-l-lg w-48">
              Attribute
            </th>
            {candidates.map((candidate, idx) => (
              <th key={idx} className="p-4 text-left bg-gray-50 dark:bg-gray-800 min-w-[220px]">
                <div className="flex justify-between items-start">
                  <div>
                    <div className="font-semibold text-lg">{candidate.name}</div>
                    <div className="text-sm text-gray-500">{candidate.party}</div>
                  </div>
                  <button
                    onClick={() => onRemove?.(idx)}
                    className="text-red-500 hover:text-red-700 transition p-1"
                    title="Remove from comparison"
                  >
                    <FiTrash2 size={16} />
                  </button>
                </div>
              </th>
            ))}
          </tr>
        </thead>

        {/* Body */}
        <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
          {rows.map((row, rowIdx) => {
            // Get values for comparison
            const values = candidates.map(c => {
              const val = row.getValue(c)
              if (row.key === 'assets_value') return parseAssetValue(val)
              if (typeof val === 'string' && val.includes('%')) return parseFloat(val)
              return val
            })
            
            const bestValue = row.compare ? getBestValue(row.key, values) : null
            
            return (
              <tr key={rowIdx} className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition">
                <td className="p-4 font-medium border-r border-gray-200 dark:border-gray-700">
                  <div className="flex items-center gap-2">
                    {row.icon}
                    {row.label}
                  </div>
                </td>
                {candidates.map((candidate, colIdx) => {
                  const rawValue = row.getValue(candidate)
                  const displayValue = row.format ? row.format(rawValue) : rawValue
                  const numericValue = values[colIdx]
                  const isBest = row.compare && numericValue === bestValue && bestValue !== null && bestValue !== 0
                  const isWorst = row.compare && row.better === 'higher' && numericValue === Math.min(...values) && values.some(v => v > 0)
                  
                  let bgClass = ''
                  if (isBest && row.better === 'higher') bgClass = 'bg-green-50 dark:bg-green-900/20'
                  if (isBest && row.better === 'lower') bgClass = 'bg-green-50 dark:bg-green-900/20'
                  if (isWorst && row.better === 'higher') bgClass = 'bg-red-50 dark:bg-red-900/20'
                  
                  return (
                    <td key={colIdx} className={`p-4 ${bgClass}`}>
                      <div className="flex items-center justify-between gap-2">
                        <span className={isBest ? 'font-semibold text-green-700 dark:text-green-400' : ''}>
                          {displayValue}
                        </span>
                        {isBest && row.compare && (
                          <span className="text-xs bg-green-500 text-white px-1.5 py-0.5 rounded-full">
                            Best
                          </span>
                        )}
                      </div>
                    </td>
                  )
                })}
              </tr>
            )
          })}
        </tbody>

        {/* Footer with View Profile Links */}
        <tfoot>
          <tr>
            <td className="p-4 font-medium bg-gray-50 dark:bg-gray-800">Actions</td>
            {candidates.map((candidate, idx) => (
              <td key={idx} className="p-4 bg-gray-50 dark:bg-gray-800">
                <Link
                  to={`/candidate/${candidate.id}`}
                  className="inline-flex items-center gap-2 text-primary-teal hover:underline text-sm"
                >
                  View Full Profile <FiArrowRight size={14} />
                </Link>
              </td>
            ))}
          </tr>
        </tfoot>
      </table>
    </div>
  )
}