import React, { useState } from 'react'
import { BREED_METADATA } from '../services/api'

export default function BreedComparison() {
  const breedNames = Object.keys(BREED_METADATA)
  const [breedA, setBreedA] = useState('Gir')
  const [breedB, setBreedB] = useState('Sahiwal')

  const dataA = BREED_METADATA[breedA]
  const dataB = BREED_METADATA[breedB]

  return (
    <section style={{ backgroundColor: '#fff', borderTop: '1px solid var(--slate-200)', borderBottom: '1px solid var(--slate-200)', padding: '2.5rem 0' }}>
      <div className="container">
        <div style={{ textAlign: 'center', marginBottom: '1.75rem' }}>
          <div style={{
            display: 'inline-block',
            padding: '0.25rem 0.75rem',
            backgroundColor: '#FEF3C7',
            color: '#B45309',
            fontSize: '0.75rem',
            fontWeight: 700,
            borderRadius: '999px',
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
            marginBottom: '0.5rem'
          }}>
            Comparative Morphological Analysis
          </div>
          <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--slate-900)' }}>
            Side-by-Side Breed Differential Matrix
          </h2>
          <p style={{ fontSize: '0.9rem', color: 'var(--slate-500)', maxWidth: '580px', margin: '0.35rem auto 0' }}>
            Compare anatomical characteristics, lactation persistence, and regional environmental adaptations between any two breeds.
          </p>
        </div>

        {/* Breed Selectors */}
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontWeight: 700, fontSize: '0.85rem', color: 'var(--slate-700)' }}>Breed A:</span>
            <select
              value={breedA}
              onChange={(e) => setBreedA(e.target.value)}
              style={{ padding: '0.45rem 0.85rem', borderRadius: '8px', border: '1px solid var(--slate-300)', fontWeight: 600, fontSize: '0.85rem' }}
            >
              {breedNames.map((name) => (
                <option key={name} value={name}>{name}</option>
              ))}
            </select>
          </div>

          <div style={{
            width: '32px',
            height: '32px',
            borderRadius: '50%',
            backgroundColor: 'var(--primary)',
            color: '#fff',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: 800,
            fontSize: '0.8rem'
          }}>
            VS
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontWeight: 700, fontSize: '0.85rem', color: 'var(--slate-700)' }}>Breed B:</span>
            <select
              value={breedB}
              onChange={(e) => setBreedB(e.target.value)}
              style={{ padding: '0.45rem 0.85rem', borderRadius: '8px', border: '1px solid var(--slate-300)', fontWeight: 600, fontSize: '0.85rem' }}
            >
              {breedNames.map((name) => (
                <option key={name} value={name}>{name}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Comparison Table */}
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', backgroundColor: '#fff', borderRadius: '12px', overflow: 'hidden', boxShadow: '0 1px 3px rgba(0,0,0,0.05)', border: '1px solid var(--slate-200)' }}>
            <thead>
              <tr style={{ backgroundColor: '#1E293B', color: '#fff', textAlign: 'left', fontSize: '0.85rem' }}>
                <th style={{ padding: '0.85rem 1rem', width: '22%' }}>Comparative Feature</th>
                <th style={{ padding: '0.85rem 1rem', width: '39%', borderRight: '1px solid #334155' }}>
                  {breedA} (Profile A)
                </th>
                <th style={{ padding: '0.85rem 1rem', width: '39%' }}>
                  {breedB} (Profile B)
                </th>
              </tr>
            </thead>
            <tbody style={{ fontSize: '0.82rem', color: 'var(--slate-700)' }}>
              <tr style={{ borderBottom: '1px solid #E2E8F0', backgroundColor: '#F8FAFC' }}>
                <td style={{ padding: '0.75rem 1rem', fontWeight: 700, color: 'var(--slate-900)' }}>Biological Species</td>
                <td style={{ padding: '0.75rem 1rem', borderRight: '1px solid #E2E8F0' }}>{dataA.species}</td>
                <td style={{ padding: '0.75rem 1rem' }}>{dataB.species}</td>
              </tr>
              <tr style={{ borderBottom: '1px solid #E2E8F0' }}>
                <td style={{ padding: '0.75rem 1rem', fontWeight: 700, color: 'var(--slate-900)' }}>Native Tract / State</td>
                <td style={{ padding: '0.75rem 1rem', borderRight: '1px solid #E2E8F0' }}>{dataA.origin}</td>
                <td style={{ padding: '0.75rem 1rem' }}>{dataB.origin}</td>
              </tr>
              <tr style={{ borderBottom: '1px solid #E2E8F0', backgroundColor: '#F8FAFC' }}>
                <td style={{ padding: '0.75rem 1rem', fontWeight: 700, color: 'var(--slate-900)' }}>Daily Milk Productivity</td>
                <td style={{ padding: '0.75rem 1rem', borderRight: '1px solid #E2E8F0', color: '#047857', fontWeight: 700 }}>{dataA.milk_yield}</td>
                <td style={{ padding: '0.75rem 1rem', color: '#047857', fontWeight: 700 }}>{dataB.milk_yield}</td>
              </tr>
              <tr style={{ borderBottom: '1px solid #E2E8F0' }}>
                <td style={{ padding: '0.75rem 1rem', fontWeight: 700, color: 'var(--slate-900)' }}>Primary Commercial Role</td>
                <td style={{ padding: '0.75rem 1rem', borderRight: '1px solid #E2E8F0' }}>{dataA.primary_use}</td>
                <td style={{ padding: '0.75rem 1rem' }}>{dataB.primary_use}</td>
              </tr>
              <tr style={{ backgroundColor: '#F8FAFC' }}>
                <td style={{ padding: '0.75rem 1rem', fontWeight: 700, color: 'var(--slate-900)' }}>Key Physical Identifiers</td>
                <td style={{ padding: '0.75rem 1rem', borderRight: '1px solid #E2E8F0', lineHeight: 1.45 }}>{dataA.description}</td>
                <td style={{ padding: '0.75rem 1rem', lineHeight: 1.45 }}>{dataB.description}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>
  )
}

