import { Link } from 'react-router-dom'
import { FaGithub, FaTwitter, FaLinkedin, FaHeart } from 'react-icons/fa'

export default function Footer() {
  return (
    <footer className="bg-gray-900 dark:bg-gray-950 text-gray-300 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div>
            <h3 className="text-2xl font-bold bg-gradient-to-r from-primary-teal to-primary-blue bg-clip-text text-transparent mb-4">
              NetaNexus
            </h3>
            <p className="text-sm text-gray-400">
              India's most comprehensive political database. Empowering citizens with transparent information.
            </p>
            <div className="flex space-x-4 mt-4">
              <a href="#" className="text-gray-400 hover:text-primary-teal transition">
                <FaTwitter size={20} />
              </a>
              <a href="#" className="text-gray-400 hover:text-primary-teal transition">
                <FaGithub size={20} />
              </a>
              <a href="#" className="text-gray-400 hover:text-primary-teal transition">
                <FaLinkedin size={20} />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-semibold text-white mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm">
              <li><Link to="/search" className="hover:text-primary-teal transition">Search Candidates</Link></li>
              <li><Link to="/elections" className="hover:text-primary-teal transition">Election Results</Link></li>
              <li><Link to="/compare" className="hover:text-primary-teal transition">Compare Candidates</Link></li>
              <li><Link to="/states" className="hover:text-primary-teal transition">State-wise Data</Link></li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h4 className="font-semibold text-white mb-4">Resources</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="hover:text-primary-teal transition">About Us</a></li>
              <li><a href="#" className="hover:text-primary-teal transition">Data Sources</a></li>
              <li><a href="#" className="hover:text-primary-teal transition">API Documentation</a></li>
              <li><a href="#" className="hover:text-primary-teal transition">Privacy Policy</a></li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-semibold text-white mb-4">Contact</h4>
            <ul className="space-y-2 text-sm">
              <li>Email: admin@netanexus.com</li>
              <li>Follow us for updates</li>
              <li className="text-gray-500 text-xs mt-2">Data sourced from ADR & ECI</li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm text-gray-500">
          <p className="flex items-center justify-center gap-1">
            Made with <FaHeart className="text-red-500" /> for Indian Democracy
          </p>
          <p className="mt-2">© 2026 NetaNexus. All data is publicly available from Election Commission of India.</p>
          <p className="text-xs mt-2">Disclaimer: We are an independent, non-partisan platform not affiliated with any political party.</p>
        </div>
      </div>
    </footer>
  )
}