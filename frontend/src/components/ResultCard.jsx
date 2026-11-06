import React from 'react'
import { BREED_METADATA } from '../services/api'

export default function ResultCard({ result, isScanning }) {
  if (isScanning) {
    return (
      <div className="panel">
        <div className="panel-header">
          <div className="panel-step">02</div>
          <div>
            <h2 className="panel-title">Recognition Results</h2>
            <p className="panel-subtitle">Analyzing image with EfficientNet-B0...</p>
          </div>
        </div>

        <div style={{ padding: '3rem 1.5rem', textAlign: 'center' }}>
          <div className="dropzone-icon" style={{ animation: 'pulse 1.2s infinite' }}>🔬</div>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginTop: '1rem', color: 'var(--slate-800)' }}>
            Extracting Deep Feature Representations
          </h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--slate-500)', marginTop: '0.25rem' }}>
            Evaluating morphological contours, horn structure, and coat patterns...
          </p>
        </div>
      </div>
    )
  }

  if (!result) {
    return (
      <div className="panel">
        <div className="panel-header">
          <div className="panel-step">02</div>
          <div>
            <h2 className="panel-title">Recognition Results</h2>
            <p className="panel-subtitle">Awaiting animal image submission</p>
          </div>
        </div>

        <div style={{ padding: '3.5rem 1.5rem', textAlign: 'center', color: 'var(--slate-400)' }}>
          <div style={{ fontSize: '3rem', marginBottom: '0.75rem' }}>📊</div>
          <h3 style={{ fontSize: '1.05rem', fontWeight: 600, color: 'var(--slate-700)' }}>
            No Analysis Yet
          </h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--slate-500)', maxWidth: '320px', margin: '0.5rem auto 0' }}>
            Upload or select an indigenous livestock photo on the left panel and click <strong>Identify Breed</strong>.
          </p>
        </div>
      </div>
    )
  }

  const { predicted_breed, confidence, top_predictions, breed_info } = result
  const percentage = (confidence * 100).toFixed(1)
  const meta = BREED_METADATA[predicted_breed] || breed_info || {}

  return (
    <div className="panel">
      <div className="panel-header">
        <div className="panel-step">02</div>
        <div>
          <h2 className="panel-title">Recognition Results</h2>
          <p className="panel-subtitle">Identification completed with {percentage}% confidence</p>
        </div>
      </div>

      <div className="result-box">
        {/* Main Breed Hero Card */}
        <div className="breed-hero-card">
          <div className="breed-name-row">
            <div>
              <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--primary)', textTransform: 'uppercase' }}>
                Top Match
              </div>
              <h3 className="breed-title">{predicted_breed}</h3>
            </div>
            <div className="confidence-badge">
              {percentage}% Match
            </div>
          </div>

          <div className="confidence-bar-bg">
            <div className="confidence-bar-fill" style={{ width: `${percentage}%` }}></div>
          </div>
        </div>

        {/* Top 3 Predictions Distribution */}
        {top_predictions && top_predictions.length > 0 && (
          <div className="top-candidates">
            <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--slate-500)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Candidate Probability Breakdown:
            </div>
            {top_predictions.slice(0, 3).map((item, idx) => (
              <div key={idx} className="candidate-row">
                <span className="candidate-name">
                  {idx + 1}. {item.breed}
                </span>
                <span className="candidate-score">
                  {(item.confidence * 100).toFixed(1)}%
                </span>
              </div>
            ))}
          </div>
        )}

        {/* Breed Details Matrix */}
        <div className="info-matrix">
          <div>
            <div className="info-item-label">Species</div>
            <div className="info-item-value">{meta.species || 'Indigenous Livestock'}</div>
          </div>
          <div>
            <div className="info-item-label">Primary Purpose</div>
            <div className="info-item-value">{meta.primary_use || 'Dairy'}</div>
          </div>
          <div>
            <div className="info-item-label">Origin / Tract</div>
            <div className="info-item-value">{meta.origin || 'India'}</div>
          </div>
          <div>
            <div className="info-item-label">Avg Daily Milk Yield</div>
            <div className="info-item-value">{meta.milk_yield || meta.milk_yield_litres_per_day ? `${meta.milk_yield || meta.milk_yield_litres_per_day + ' L/day'}` : 'N/A'}</div>
          </div>
        </div>

        {/* Breed Description Summary */}
        {meta.description && (
          <div className="breed-summary">
            <strong style={{ color: 'var(--slate-900)' }}>Morphological Profile: </strong>
            {meta.description}
          </div>
        )}
      </div>
    </div>
  )
}
