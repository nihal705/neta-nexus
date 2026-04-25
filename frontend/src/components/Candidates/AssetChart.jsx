import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts'

export default function AssetChart({ affidavit }) {
  if (!affidavit) return null

  // Parse asset values (remove currency symbols)
  const parseValue = (value) => {
    if (!value) return 0
    const num = parseFloat(value.toString().replace(/[₹,]/g, ''))
    return isNaN(num) ? 0 : num
  }

  const movable = parseValue(affidavit.movable_assets)
  const immovable = parseValue(affidavit.immovable_assets)
  const total = movable + immovable

  const data = [
    { name: 'Movable Assets', value: movable, color: '#00A896' },
    { name: 'Immovable Assets', value: immovable, color: '#2B6CB0' },
  ]

  const COLORS = ['#00A896', '#2B6CB0']

  return (
    <div>
      <div className="grid md:grid-cols-2 gap-6">
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
                dataKey="value"
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => `₹${value.toLocaleString()}`} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="space-y-3">
          <div className="flex justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <span className="text-gray-600 dark:text-gray-300">Total Assets:</span>
            <span className="font-bold text-primary-teal">₹{total.toLocaleString()}</span>
          </div>
          <div className="flex justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <span className="text-gray-600 dark:text-gray-300">Movable Assets:</span>
            <span>₹{movable.toLocaleString()}</span>
          </div>
          <div className="flex justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <span className="text-gray-600 dark:text-gray-300">Immovable Assets:</span>
            <span>₹{immovable.toLocaleString()}</span>
          </div>
          {affidavit.total_liabilities && (
            <div className="flex justify-between p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
              <span className="text-gray-600 dark:text-gray-300">Liabilities:</span>
              <span className="text-red-600">₹{parseValue(affidavit.total_liabilities).toLocaleString()}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}