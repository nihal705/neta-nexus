import { useState } from 'react'
import { FiAlertCircle, FiChevronDown, FiChevronUp } from 'react-icons/fi'

export default function CriminalRecord({ cases }) {
  const [expanded, setExpanded] = useState(false)

  if (!cases || cases.length === 0) {
    return (
      <div className="bg-green-50 dark:bg-green-900/20 rounded-xl p-4 flex items-center gap-3">
        <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
          <FiAlertCircle className="text-white" size={16} />
        </div>
        <div>
          <p className="font-medium text-green-700 dark:text-green-400">No Criminal Cases Reported</p>
          <p className="text-sm text-green-600 dark:text-green-500">As per self-sworn affidavit filed with Election Commission</p>
        </div>
      </div>
    )
  }

  const displayCases = expanded ? cases : cases.slice(0, 3)

  return (
    <div>
      <div className="bg-red-50 dark:bg-red-900/20 rounded-xl p-4 mb-4">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center">
            <FiAlertCircle className="text-white" size={16} />
          </div>
          <div>
            <p className="font-medium text-red-700 dark:text-red-400">{cases.length} Criminal Case(s) Reported</p>
            <p className="text-sm text-red-600 dark:text-red-500">As declared in election affidavit</p>
          </div>
        </div>
      </div>

      <div className="space-y-3">
        {displayCases.map((case_, idx) => (
          <div key={idx} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
            <div className="flex justify-between items-start">
              <div>
                <p className="font-medium">{case_.case_number || `Case ${idx + 1}`}</p>
                <p className="text-sm text-gray-500 mt-1">Sections: {case_.sections || 'IPC Section(s)'}</p>
              </div>
              {case_.filed_before_election && (
                <span className="text-xs bg-orange-100 dark:bg-orange-900/30 text-orange-600 px-2 py-1 rounded">
                  Filed before election
                </span>
              )}
            </div>
            <p className="text-sm mt-2 text-gray-600 dark:text-gray-400">{case_.case_details || 'Details pending'}</p>
            <p className="text-xs text-gray-400 mt-2">Court: {case_.court_name || 'Unknown'} | Status: {case_.status || 'Pending'}</p>
          </div>
        ))}
      </div>

      {cases.length > 3 && (
        <button
          onClick={() => setExpanded(!expanded)}
          className="mt-4 text-primary-teal hover:underline flex items-center gap-1"
        >
          {expanded ? <FiChevronUp /> : <FiChevronDown />}
          {expanded ? 'Show Less' : `Show ${cases.length - 3} More Cases`}
        </button>
      )}
    </div>
  )
}