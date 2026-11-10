import React, { useState, useEffect } from 'react'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import ImageUpload from './components/ImageUpload'
import ResultCard from './components/ResultCard'
import PredictionHistory from './components/PredictionHistory'
import BreedCatalog from './components/BreedCatalog'
import BreedComparison from './components/BreedComparison'
import Footer from './components/Footer'
import { checkBackendHealth, predictBreed } from './services/api'

export default function App() {
  const [category, setCategory] = useState('cattle')
  const [selectedFile, setSelectedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [activeSampleName, setActiveSampleName] = useState(null)
  const [isScanning, setIsScanning] = useState(false)
  const [currentResult, setCurrentResult] = useState(null)
  const [history, setHistory] = useState([])
  const [isBackendOnline, setIsBackendOnline] = useState(false)
  const [activeTab, setActiveTab] = useState('scanner') // 'scanner' | 'catalog' | 'comparison'

  // Check backend health periodically
  useEffect(() => {
    let isMounted = true
    const checkHealth = async () => {
      const status = await checkBackendHealth()
      if (isMounted) {
        setIsBackendOnline(status.online)
      }
    }
    checkHealth()
    const timer = setInterval(checkHealth, 15000)
    return () => {
      isMounted = false
      clearInterval(timer)
    }
  }, [])

  const handleImageSelected = (file, customPreviewUrl = null, sampleName = null) => {
    setSelectedFile(file)
    setActiveSampleName(sampleName)
    if (customPreviewUrl) {
      setPreviewUrl(customPreviewUrl)
    } else {
      setPreviewUrl(URL.createObjectURL(file))
    }
    // Clear previous single result on new image
    setCurrentResult(null)
  }

  const handleImageRemoved = () => {
    if (previewUrl && !previewUrl.startsWith('data:')) {
      URL.revokeObjectURL(previewUrl)
    }
    setSelectedFile(null)
    setPreviewUrl(null)
    setActiveSampleName(null)
    setCurrentResult(null)
  }

  const handleScan = async () => {
    if (!selectedFile) return
    setIsScanning(true)
    try {
      const result = await predictBreed(selectedFile, category, activeSampleName)
      setCurrentResult(result)
      setHistory((prev) => [result, ...prev.slice(0, 9)])
    } catch (err) {
      console.error('Scan error:', err)
    } finally {
      setIsScanning(false)
    }
  }

  const handleSelectBreedForTest = (breedName) => {
    setActiveTab('scanner')
    // Set appropriate category
    const isBuffalo = ['Murrah', 'Jaffrabadi', 'Mehsana', 'Surti', 'Nili-Ravi', 'Banni'].includes(breedName)
    setCategory(isBuffalo ? 'buffalo' : 'cattle')

    // Create virtual sample file
    const mockFile = new File([breedName], `${breedName.toLowerCase()}_sample.jpg`, { type: 'image/jpeg' })
    const sampleUri = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300"><rect fill="%232563eb" width="400" height="300"/><circle cx="200" cy="150" r="85" fill="%231d4ed8"/><text x="50%25" y="50%25" text-anchor="middle" dy=".3em" fill="%23ffffff" font-size="22" font-family="sans-serif" font-weight="bold">${breedName} Reference</text></svg>`
    handleImageSelected(mockFile, sampleUri, breedName)

    // Scroll to scanner workspace smoothly
    window.scrollTo({ top: 400, behavior: 'smooth' })
  }

  return (
    <div className="app">
      <Navbar isBackendOnline={isBackendOnline} />
      <main>
        <Hero />

        {/* Global Navigation Tabs */}
        <div className="container" style={{ marginTop: '-1rem', marginBottom: '1.5rem' }}>
          <div style={{
            display: 'flex',
            gap: '0.75rem',
            justifyContent: 'center',
            backgroundColor: '#fff',
            padding: '0.5rem',
            borderRadius: '12px',
            boxShadow: '0 1px 4px rgba(0,0,0,0.06)',
            border: '1px solid var(--slate-200)',
            maxWidth: '650px',
            margin: '0 auto'
          }}>
            <button
              type="button"
              className={`toggle-btn ${activeTab === 'scanner' ? 'active' : ''}`}
              onClick={() => setActiveTab('scanner')}
              style={{ flex: 1, padding: '0.65rem 1rem', fontSize: '0.9rem', fontWeight: 700 }}
            >
              🔬 Live Breed Scanner
            </button>
            <button
              type="button"
              className={`toggle-btn ${activeTab === 'catalog' ? 'active' : ''}`}
              onClick={() => setActiveTab('catalog')}
              style={{ flex: 1, padding: '0.65rem 1rem', fontSize: '0.9rem', fontWeight: 700 }}
            >
              📚 14 Breeds Encyclopedia
            </button>
            <button
              type="button"
              className={`toggle-btn ${activeTab === 'comparison' ? 'active' : ''}`}
              onClick={() => setActiveTab('comparison')}
              style={{ flex: 1, padding: '0.65rem 1rem', fontSize: '0.9rem', fontWeight: 700 }}
            >
              ⚖️ Breed Comparator
            </button>
          </div>
        </div>

        {/* Tab 1: Live Breed Scanner */}
        {activeTab === 'scanner' && (
          <>
            <div className="container">
              <div className="workspace-grid">
                <ImageUpload
                  selectedFile={selectedFile}
                  previewUrl={previewUrl}
                  category={category}
                  onCategoryChange={(cat) => {
                    setCategory(cat)
                    handleImageRemoved()
                  }}
                  onImageSelected={handleImageSelected}
                  onImageRemoved={handleImageRemoved}
                  onScan={handleScan}
                  isScanning={isScanning}
                />
                <ResultCard result={currentResult} isScanning={isScanning} />
              </div>
            </div>
            <PredictionHistory history={history} />
          </>
        )}

        {/* Tab 2: 14 Breeds Encyclopedia */}
        {activeTab === 'catalog' && (
          <BreedCatalog onSelectBreedForTest={handleSelectBreedForTest} />
        )}

        {/* Tab 3: Breed Comparison Tool */}
        {activeTab === 'comparison' && (
          <BreedComparison />
        )}
      </main>
      <Footer />
    </div>
  )
}
