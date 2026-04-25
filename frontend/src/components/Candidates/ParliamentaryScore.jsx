import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, Tooltip } from 'recharts'

export default function ParliamentaryScore({ score }) {
  if (!score) return null

  const data = [
    { subject: 'Attendance', value: score.attendance_percentage || 0, fullMark: 100 },
    { subject: 'Questions', value: Math.min((score.questions_asked || 0) / 100 * 100, 100), fullMark: 100 },
    { subject: 'Debates', value: Math.min((score.debates_participated || 0) / 50 * 100, 100), fullMark: 100 },
    { subject: 'Bills', value: Math.min((score.private_member_bills || 0) / 10 * 100, 100), fullMark: 100 },
  ]

  const getScoreColor = (composite) => {
    if (composite >= 75) return 'text-green-600'
    if (composite >= 50) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <div className="bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900 rounded-xl p-4">
      <div className="text-center mb-4">
        <div className="text-sm text-gray-500">Parliamentary Performance Score</div>
        <div className={`text-4xl font-bold ${getScoreColor(score.composite_score)}`}>
          {score.composite_score?.toFixed(1)}
        </div>
        <div className="text-xs text-gray-400">out of 100</div>
      </div>

      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
            <PolarGrid />
            <PolarAngleAxis dataKey="subject" tick={{ fontSize: 10 }} />
            <PolarRadiusAxis angle={30} domain={[0, 100]} />
            <Radar name="Score" dataKey="value" stroke="#00A896" fill="#00A896" fillOpacity={0.6} />
            <Tooltip />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-2 gap-2 text-center text-sm mt-4">
        <div className="bg-white dark:bg-gray-700 rounded-lg p-2">
          <div className="text-gray-500">Attendance</div>
          <div className="font-semibold">{score.attendance_percentage}%</div>
        </div>
        <div className="bg-white dark:bg-gray-700 rounded-lg p-2">
          <div className="text-gray-500">Questions Asked</div>
          <div className="font-semibold">{score.questions_asked}</div>
        </div>
        <div className="bg-white dark:bg-gray-700 rounded-lg p-2">
          <div className="text-gray-500">Debates</div>
          <div className="font-semibold">{score.debates_participated}</div>
        </div>
        <div className="bg-white dark:bg-gray-700 rounded-lg p-2">
          <div className="text-gray-500">Private Bills</div>
          <div className="font-semibold">{score.private_member_bills}</div>
        </div>
      </div>
    </div>
  )
}