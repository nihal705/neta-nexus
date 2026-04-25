import { Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Layout from './components/Layout/Layout'
import HomePage from './pages/HomePage'
import SearchResults from './pages/SearchResults'
import CandidateProfilePage from './pages/CandidateProfilePage'
import ElectionCenter from './pages/ElectionCenter'
import ComparePage from './pages/ComparePage'

function App() {
  return (
    <>
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 3000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            duration: 3000,
            iconTheme: {
              primary: '#00A896',
              secondary: '#fff',
            },
          },
        }}
      />
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="/search" element={<SearchResults />} />
          <Route path="/candidate/:id" element={<CandidateProfilePage />} />
          <Route path="/elections" element={<ElectionCenter />} />
          <Route path="/compare" element={<ComparePage />} />
        </Route>
      </Routes>
    </>
  )
}

export default App