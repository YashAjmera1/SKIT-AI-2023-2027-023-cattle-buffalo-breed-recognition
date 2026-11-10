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
            <p className="panel-subtitle">Executing Computer Vision & Morphological Engine...</p>
          </div>
        </div>

        <div style={{ padding: '3.5rem 1.5rem', textAlign: 'center' }}>
          <div className="dropzone-icon" style={{ animation: 'pulse 1.2s infinite' }}>🔬</div>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginTop: '1rem', color: 'var(--slate-800)' }}>
            Biometric Gatekeeper & Feature Analysis Active
          </h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--slate-500)', marginTop: '0.35rem', maxWidth: '380px', margin: '0.35rem auto 0' }}>
            Evaluating human/non-bovine discrimination shield, HSV color moments, horn contours, and ear droop curvature...
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
            Upload, snap a photo, or select an indigenous livestock sample on the left panel and click <strong>Identify Breed</strong>.
          </p>
        </div>
      </div>
    )
  }

  const {
    predicted_breed,
    confidence,
    top_predictions,
    breed_info,
    is_verified_bovine,
    verification_message,
    reasoning
  } = result

  const percentage = (confidence * 100).toFixed(1)
  const meta = BREED_METADATA[predicted_breed] || breed_info || {}

  // ---------------- CASE 1: NON-BOVINE / HUMAN REJECTION ----------------
  if (is_verified_bovine === false) {
    return (
      <div className="panel">
        <div className="panel-header">
          <div className="panel-step">02</div>
          <div>
            <h2 className="panel-title">Recognition Results</h2>
            <p className="panel-subtitle" style={{ color: '#DC2626', fontWeight: 600 }}>
              Domain Gatekeeper: Non-Bovine Subject Rejected
            </p>
          </div>
        </div>

        <div className="result-box">
          <div style={{
            padding: '1.75rem 1.25rem',
            backgroundColor: '#FEF2F2',
            border: '1.5px solid #F87171',
            borderRadius: '12px',
            textAlign: 'center',
            marginBottom: '1.25rem'
          }}>
            <div style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>🚫</div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 800, color: '#991B1B', marginBottom: '0.4rem' }}>
              Subject Rejected by Biometric Shield
            </h3>
            <p style={{ fontSize: '0.88rem', color: '#B91C1C', lineHeight: 1.5, maxWidth: '420px', margin: '0 auto' }}>
              {verification_message || 'Biometric security shield detected a human or non-bovine subject in the frame.'}
            </p>
          </div>

          <div style={{
            backgroundColor: '#F8FAFC',
            border: '1px solid #E2E8F0',
            borderRadius: '10px',
            padding: '1.1rem',
            fontSize: '0.82rem',
            color: '#334155'
          }}>
            <strong style={{ color: '#0F172A', display: 'block', marginBottom: '0.4rem', fontSize: '0.85rem' }}>
              🛡️ System Operating Parameters:
            </strong>
            <p style={{ margin: '0 0 0.5rem 0', lineHeight: 1.45 }}>
              This system uses deep learning biometric filters (YuNet + Color Moment Tensors) to prevent false classifications on human faces, domestic pets, or inanimate objects.
            </p>
            <div style={{ backgroundColor: '#fff', padding: '0.65rem', borderRadius: '6px', border: '1px solid #CBD5E1' }}>
              <span style={{ fontWeight: 700, color: 'var(--primary)' }}>Permitted Input Classes:</span>
              <ul style={{ margin: '0.35rem 0 0 1.25rem', padding: 0, lineHeight: 1.5 }}>
                <li><strong>Cattle (8 Breeds):</strong> Gir, Sahiwal, Red Sindhi, Tharparkar, Rathi, Kankrej, Hariana, Ongole</li>
                <li><strong>Buffalo (6 Breeds):</strong> Murrah, Jaffarabadi, Mehsana, Surti, Nili-Ravi, Banni</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    )
  }

  // ---------------- CASE 2: AUTHENTICATED BOVINE BREED MATCH ----------------
  return (
    <div className="panel">
      <div className="panel-header">
        <div className="panel-step">02</div>
        <div>
          <h2 className="panel-title">Recognition Results</h2>
          <p className="panel-subtitle">
            Authenticated Bovine Match • {percentage}% confidence
          </p>
        </div>
      </div>

      <div className="result-box">
        {/* Authenticated Bovine Badge */}
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.4rem',
          padding: '0.35rem 0.75rem',
          backgroundColor: '#ECFDF5',
          border: '1px solid #A7F3D0',
          borderRadius: '999px',
          fontSize: '0.75rem',
          fontWeight: 700,
          color: '#065F46',
          marginBottom: '0.75rem'
        }}>
          <span>🛡️</span> Authenticated Indian Bovine Subject
        </div>

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

        {/* Model Morphological Reasoning */}
        {reasoning && (
          <div style={{
            padding: '0.85rem',
            backgroundColor: '#F8FAFC',
            border: '1px solid #E2E8F0',
            borderRadius: '8px',
            fontSize: '0.82rem',
            color: '#334155',
            lineHeight: 1.45,
            marginBottom: '1rem'
          }}>
            <strong style={{ color: '#0F172A' }}>Visual Morphological Signature: </strong>
            {reasoning}
          </div>
        )}

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
            <div className="info-item-value">{meta.species || 'Indigenous Bovine'}</div>
          </div>
          <div>
            <div className="info-item-label">Primary Purpose</div>
            <div className="info-item-value">{meta.primary_use || 'Dairy & Draught'}</div>
          </div>
          <div>
            <div className="info-item-label">Origin / Tract</div>
            <div className="info-item-value">{meta.origin || 'India'}</div>
          </div>
          <div>
            <div className="info-item-label">Avg Daily Milk Yield</div>
            <div className="info-item-value">{meta.milk_yield || (meta.milk_yield_litres_per_day ? `${meta.milk_yield_litres_per_day} L/day` : '1,800 - 3,200 kg / lactation')}</div>
          </div>
        </div>

        {/* Breed Description Summary */}
        {meta.description && (
          <div className="breed-summary">
            <strong style={{ color: 'var(--slate-900)' }}>NBAGR Breed Profile: </strong>
            {meta.description}
          </div>
        )}

        {/* Diagnostic Actions */}
        <div style={{ marginTop: '1rem', display: 'flex', gap: '0.75rem', justifyContent: 'flex-end' }}>
          <button
            type="button"
            onClick={() => window.print()}
            style={{
              padding: '0.5rem 1rem',
              fontSize: '0.82rem',
              fontWeight: 700,
              backgroundColor: '#fff',
              border: '1px solid var(--slate-300)',
              borderRadius: '8px',
              color: 'var(--slate-700)',
              cursor: 'pointer',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.4rem'
            }}
          >
            <span>🖨️</span> Print / Export Diagnostic Slip
          </button>
        </div>
      </div>
    </div>
  )
}
