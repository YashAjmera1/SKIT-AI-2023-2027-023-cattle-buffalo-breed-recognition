import React, { useState, useEffect } from 'react'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import ImageUpload from './components/ImageUpload'
import ResultCard from './components/ResultCard'
import PredictionHistory from './components/PredictionHistory'
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

  return (
    <div className="app">
      <Navbar isBackendOnline={isBackendOnline} />
      <main>
        <Hero />
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
      </main>
      <Footer />
    </div>
  )
}
