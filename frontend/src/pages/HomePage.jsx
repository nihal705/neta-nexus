import { motion } from 'framer-motion'
import HeroSection from '../components/Home/HeroSection'
import QuickStats from '../components/Home/QuickStats'
import TrendingSearch from '../components/Home/TrendingSearch'
import ExitPollCarousel from '../components/Home/ExitPollCarousel'
import StateExplorer from '../components/Home/StateExplorer'

export default function HomePage() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <HeroSection />
      <QuickStats />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <TrendingSearch />
          </div>
          <div>
            <div className="bg-gradient-to-br from-blue-600 to-teal-500 rounded-2xl p-6 text-white">
              <h3 className="text-xl font-bold mb-3">Why NetaNexus?</h3>
              <p className="text-sm opacity-90 mb-4">
                India's most comprehensive political database. Track your representatives, compare candidates, and make informed voting decisions.
              </p>
              <ul className="space-y-2 text-sm">
                <li className="flex items-center gap-2">✓ 8,000+ Candidates Tracked</li>
                <li className="flex items-center gap-2">✓ Real Affidavit Data</li>
                <li className="flex items-center gap-2">✓ Election Results</li>
                <li className="flex items-center gap-2">✓ Criminal Record Tracking</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="mt-12">
          <ExitPollCarousel />
        </div>

        <div className="mt-12">
          <StateExplorer />
        </div>
      </div>
    </motion.div>
  )
}