import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { FiPlay, FiPause, FiChevronLeft, FiChevronRight, FiBarChart2 } from 'react-icons/fi'
import axios from 'axios'

export default function ExitPollCarousel() {
  const [exitPolls, setExitPolls] = useState([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isPlaying, setIsPlaying] = useState(true)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchExitPolls()
  }, [])

  useEffect(() => {
    if (!isPlaying || exitPolls.length === 0) return
    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % exitPolls.length)
    }, 8000)
    return () => clearInterval(interval)
  }, [isPlaying, exitPolls.length])

  const fetchExitPolls = async () => {
    try {
      const response = await axios.get('/api/exitpolls/media?election_id=2024')
      setExitPolls(response.data)
    } catch (error) {
      console.error('Error fetching exit polls:', error)
      setExitPolls([
        { source_name: 'Axis My India', prediction_data: { BJP: '295-315', INC: '125-145', Others: '55-75', margin_error: '±5%' }, color: '#00A896' },
        { source_name: 'C-Voter', prediction_data: { BJP: '287-305', INC: '132-150', Others: '45-55', margin_error: '±4%' }, color: '#2B6CB0' },
        { source_name: 'Today\'s Chanakya', prediction_data: { BJP: '305-325', INC: '105-125', Others: '60-70', margin_error: '±3%' }, color: '#F59E0B' },
        { source_name: 'Republic TV', prediction_data: { BJP: '290-310', INC: '130-148', Others: '48-58', margin_error: '±4%' }, color: '#DC2626' },
        { source_name: 'Times Now', prediction_data: { BJP: '285-300', INC: '135-155', Others: '50-60', margin_error: '±5%' }, color: '#7C3AED' },
      ])
    } finally {
      setLoading(false)
    }
  }

  const nextPoll = () => {
    setCurrentIndex((prev) => (prev + 1) % exitPolls.length)
    setIsPlaying(false)
  }

  const prevPoll = () => {
    setCurrentIndex((prev) => (prev - 1 + exitPolls.length) % exitPolls.length)
    setIsPlaying(false)
  }

  if (loading) {
    return (
      <div className="card p-8">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/3"></div>
          <div className="h-32 bg-gray-200 dark:bg-gray-700 rounded"></div>
        </div>
      </div>
    )
  }

  const current = exitPolls[currentIndex]

  return (
    <div className="card overflow-hidden">
      <div className="bg-gradient-to-r from-primary-blue to-primary-teal px-6 py-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-2">
            <FiBarChart2 className="text-white" size={20} />
            <h3 className="text-white font-bold text-lg">Media Exit Polls 2024</h3>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className="p-2 rounded-full bg-white/20 hover:bg-white/30 transition"
            >
              {isPlaying ? <FiPause className="text-white" size={16} /> : <FiPlay className="text-white" size={16} />}
            </button>
          </div>
        </div>
      </div>

      <div className="p-6">
        <div className="flex justify-between items-center mb-6">
          <button onClick={prevPoll} className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition">
            <FiChevronLeft size={24} />
          </button>
          
          <AnimatePresence mode="wait">
            <motion.div
              key={currentIndex}
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -50 }}
              transition={{ duration: 0.5 }}
              className="flex-1 text-center"
            >
              <h4 className="text-2xl font-bold mb-4" style={{ color: current.color }}>
                {current.source_name}
              </h4>

              <div className="grid grid-cols-3 gap-4 mb-6">
                <div className="bg-orange-50 dark:bg-orange-900/20 rounded-xl p-4">
                  <div className="text-sm text-gray-600 dark:text-gray-400">BJP/NDA</div>
                  <div className="text-2xl md:text-3xl font-bold text-orange-600">
                    {current.prediction_data.BJP}
                  </div>
                </div>
                <div className="bg-green-50 dark:bg-green-900/20 rounded-xl p-4">
                  <div className="text-sm text-gray-600 dark:text-gray-400">INC/INDIA</div>
                  <div className="text-2xl md:text-3xl font-bold text-green-600">
                    {current.prediction_data.INC}
                  </div>
                </div>
                <div className="bg-purple-50 dark:bg-purple-900/20 rounded-xl p-4">
                  <div className="text-sm text-gray-600 dark:text-gray-400">Others</div>
                  <div className="text-2xl md:text-3xl font-bold text-purple-600">
                    {current.prediction_data.Others}
                  </div>
                </div>
              </div>

              <div className="text-sm text-gray-500">
                Margin of Error: {current.prediction_data.margin_error || '±5%'}
              </div>
            </motion.div>
          </AnimatePresence>

          <button onClick={nextPoll} className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition">
            <FiChevronRight size={24} />
          </button>
        </div>

        {/* Dots Indicator */}
        <div className="flex justify-center gap-2 mt-4">
          {exitPolls.map((_, idx) => (
            <button
              key={idx}
              onClick={() => {
                setCurrentIndex(idx)
                setIsPlaying(false)
              }}
              className={`h-2 rounded-full transition-all ${
                idx === currentIndex ? 'w-6 bg-primary-teal' : 'w-2 bg-gray-300 dark:bg-gray-600'
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  )
}