import React, { useState, useRef } from 'react'

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
  const fileInputRef = useRef(null)

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
    const mockFile = new File([sampleName], `${sampleName.toLowerCase()}_sample.jpg`, { type: 'image/jpeg' })
    onImageSelected(mockFile, SAMPLE_PREVIEWS[sampleName], sampleName)
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <div className="panel-step">01</div>
        <div>
          <h2 className="panel-title">Upload Livestock Photo</h2>
          <p className="panel-subtitle">Select or drop an indigenous cattle or buffalo image</p>
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

      {/* Dropzone or Preview */}
      {previewUrl ? (
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
      )}

      {/* Validation alert */}
      {validationError && (
        <div className="error-banner">
          <span>⚠️</span>
          <span>{validationError}</span>
        </div>
      )}

      {/* Quick samples */}
      <div className="quick-samples">
        <div className="quick-samples-label">Or test with verified sample:</div>
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
            <span className="pulse-dot"></span> Analyzing with EfficientNet-B0...
          </>
        ) : (
          <>Identify Breed →</>
        )}
      </button>
    </div>
  )
}
