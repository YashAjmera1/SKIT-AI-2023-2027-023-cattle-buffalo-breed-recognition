import React, { useState, useRef, useEffect } from 'react'

const MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024 // 5 MB
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp']

// Sample SVG placeholder data URIs for quick testing without needing external image files
const SAMPLE_PREVIEWS = {
  Gir: 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300"><rect fill="%23f59e0b" width="400" height="300"/><circle cx="200" cy="150" r="80" fill="%23d97706"/><text x="50%25" y="50%25" text-anchor="middle" dy=".3em" fill="%23ffffff" font-size="24" font-family="sans-serif" font-weight="bold">Gir Cattle Sample</text></svg>',
  Sahiwal: 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300"><rect fill="%23b45309" width="400" height="300"/><circle cx="200" cy="150" r="80" fill="%2392400e"/><text x="50%25" y="50%25" text-anchor="middle" dy=".3em" fill="%23ffffff" font-size="24" font-family="sans-serif" font-weight="bold">Sahiwal Cattle Sample</text></svg>',
  Murrah: 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300"><rect fill="%231e293b" width="400" height="300"/><circle cx="200" cy="150" r="80" fill="%23334155"/><text x="50%25" y="50%25" text-anchor="middle" dy=".3em" fill="%23ffffff" font-size="24" font-family="sans-serif" font-weight="bold">Murrah Buffalo Sample</text></svg>',
  Jaffrabadi: 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300"><rect fill="%230f172a" width="400" height="300"/><circle cx="200" cy="150" r="80" fill="%231e293b"/><text x="50%25" y="50%25" text-anchor="middle" dy=".3em" fill="%23ffffff" font-size="24" font-family="sans-serif" font-weight="bold">Jaffrabadi Buffalo Sample</text></svg>'
}

export default function ImageUpload({
  selectedFile,
  previewUrl,
  category,
  onCategoryChange,
  onImageSelected,
  onImageRemoved,
  onScan,
  isScanning
}) {
  const [dragOver, setDragOver] = useState(false)
  const [validationError, setValidationError] = useState('')
  const [isCameraActive, setIsCameraActive] = useState(false)
  const [cameraError, setCameraError] = useState('')

  const fileInputRef = useRef(null)
  const videoRef = useRef(null)
  const streamRef = useRef(null)

  // Cleanup video stream on unmount
  useEffect(() => {
    return () => {
      stopCamera()
    }
  }, [])

  const startCamera = async () => {
    setCameraError('')
    setValidationError('')
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } }
      })
      streamRef.current = stream
      setIsCameraActive(true)
      setTimeout(() => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream
        }
      }, 100)
    } catch (err) {
      console.error('Camera access error:', err)
      setCameraError('Unable to access camera. Please check camera permissions or upload an image.')
    }
  }

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop())
      streamRef.current = null
    }
    setIsCameraActive(false)
  }

  const capturePhoto = () => {
    if (!videoRef.current) return
    const video = videoRef.current
    const canvas = document.createElement('canvas')
    canvas.width = video.videoWidth || 640
    canvas.height = video.videoHeight || 480
    const ctx = canvas.getContext('2d')
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)

    canvas.toBlob((blob) => {
      if (blob) {
        const liveFile = new File([blob], `live_capture_${Date.now()}.jpg`, { type: 'image/jpeg' })
        const dataUrl = canvas.toDataURL('image/jpeg', 0.92)
        stopCamera()
        onImageSelected(liveFile, dataUrl, 'Live Camera Capture')
      }
    }, 'image/jpeg', 0.92)
  }

  const validateAndProcessFile = (file) => {
    setValidationError('')

    if (!file) return

    if (!ALLOWED_TYPES.includes(file.type)) {
      setValidationError('Invalid file format. Please upload a JPEG, PNG, or WEBP image.')
      return
    }

    if (file.size > MAX_FILE_SIZE_BYTES) {
      const sizeMB = (file.size / (1024 * 1024)).toFixed(1)
      setValidationError(`File size (${sizeMB} MB) exceeds maximum allowed limit of 5.0 MB.`)
      return
    }

    onImageSelected(file)
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setDragOver(true)
  }

  const handleDragLeave = () => {
    setDragOver(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragOver(false)
    const file = e.dataTransfer.files?.[0]
    validateAndProcessFile(file)
  }

  const handleFileChange = (e) => {
    const file = e.target.files?.[0]
    validateAndProcessFile(file)
  }

  const handleSampleClick = (sampleName) => {
    setValidationError('')
    stopCamera()
    const mockFile = new File([sampleName], `${sampleName.toLowerCase()}_sample.jpg`, { type: 'image/jpeg' })
    onImageSelected(mockFile, SAMPLE_PREVIEWS[sampleName], sampleName)
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <div className="panel-step">01</div>
        <div>
          <h2 className="panel-title">Upload Livestock Photo</h2>
          <p className="panel-subtitle">Select, capture, or drop an indigenous cattle or buffalo image</p>
        </div>
      </div>

      {/* Category selector */}
      <div className="category-toggle">
        <button
          type="button"
          className={`toggle-btn ${category === 'cattle' ? 'active' : ''}`}
          onClick={() => onCategoryChange('cattle')}
        >
          <span>🐄</span> Indigenous Cattle
        </button>
        <button
          type="button"
          className={`toggle-btn ${category === 'buffalo' ? 'active' : ''}`}
          onClick={() => onCategoryChange('buffalo')}
        >
          <span>🐃</span> Indigenous Buffalo
        </button>
      </div>

      {/* Live Camera Viewfinder Modal or Dropzone */}
      {isCameraActive ? (
        <div className="camera-viewfinder" style={{ position: 'relative', borderRadius: '12px', overflow: 'hidden', backgroundColor: '#000', marginBottom: '1rem' }}>
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            style={{ width: '100%', height: '280px', objectFit: 'cover' }}
          />
          <div style={{
            position: 'absolute',
            inset: '20px',
            border: '2px dashed rgba(255, 255, 255, 0.65)',
            borderRadius: '8px',
            pointerEvents: 'none',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'rgba(255, 255, 255, 0.75)',
            fontSize: '0.8rem',
            fontWeight: 600
          }}>
            [ Align cow or buffalo within frame ]
          </div>
          <div style={{ padding: '0.75rem', backgroundColor: '#0f172a', display: 'flex', gap: '0.5rem', justifyContent: 'center' }}>
            <button
              type="button"
              className="toggle-btn"
              onClick={capturePhoto}
              style={{ backgroundColor: 'var(--primary)', color: '#fff', fontWeight: 700 }}
            >
              📸 Snap Photo
            </button>
            <button
              type="button"
              className="toggle-btn"
              onClick={stopCamera}
              style={{ backgroundColor: '#334155', color: '#fff' }}
            >
              ✕ Cancel
            </button>
          </div>
        </div>
      ) : previewUrl ? (
        <div className="preview-container">
          <img src={previewUrl} alt="Livestock Preview" className="preview-image" />
          <button
            type="button"
            className="remove-image-btn"
            onClick={onImageRemoved}
            title="Remove image"
          >
            ✕
          </button>
        </div>
      ) : (
        <div>
          <div
            className={`dropzone ${dragOver ? 'dragover' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept="image/jpeg,image/png,image/webp"
              onChange={handleFileChange}
            />
            <div className="dropzone-icon">📷</div>
            <div className="dropzone-text">Click to browse or drag & drop</div>
            <div className="dropzone-subtext">Supports JPG, PNG, WEBP (Max 5 MB)</div>
          </div>

          <div style={{ marginTop: '0.75rem', textAlign: 'center' }}>
            <button
              type="button"
              onClick={startCamera}
              className="toggle-btn"
              style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.82rem', padding: '0.4rem 0.85rem' }}
            >
              <span>📹</span> Open Live Camera / Webcam
            </button>
          </div>
        </div>
      )}

      {/* Camera / Validation alert */}
      {cameraError && (
        <div className="error-banner" style={{ marginTop: '0.5rem' }}>
          <span>⚠️</span>
          <span>{cameraError}</span>
        </div>
      )}

      {validationError && (
        <div className="error-banner" style={{ marginTop: '0.5rem' }}>
          <span>⚠️</span>
          <span>{validationError}</span>
        </div>
      )}

      {/* Quick samples */}
      <div className="quick-samples">
        <div className="quick-samples-label">Or test with verified reference sample:</div>
        <div className="samples-row">
          {category === 'cattle' ? (
            <>
              <button type="button" className="sample-chip" onClick={() => handleSampleClick('Gir')}>
                Gir (Gujarat)
              </button>
              <button type="button" className="sample-chip" onClick={() => handleSampleClick('Sahiwal')}>
                Sahiwal (Punjab)
              </button>
            </>
          ) : (
            <>
              <button type="button" className="sample-chip" onClick={() => handleSampleClick('Murrah')}>
                Murrah (Haryana)
              </button>
              <button type="button" className="sample-chip" onClick={() => handleSampleClick('Jaffrabadi')}>
                Jaffrabadi (Gujarat)
              </button>
            </>
          )}
        </div>
      </div>

      {/* Primary Action Button */}
      <button
        type="button"
        className="btn-primary"
        disabled={!selectedFile || isScanning}
        onClick={onScan}
      >
        {isScanning ? (
          <>
            <span className="pulse-dot"></span> Analyzing with Vision Engine...
          </>
        ) : (
          <>Identify Breed →</>
        )}
      </button>
    </div>
  )
}
