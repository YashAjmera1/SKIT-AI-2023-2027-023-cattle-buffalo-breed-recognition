import React, { useState } from 'react'
import { BREED_METADATA } from '../services/api'

export default function BreedCatalog({ onSelectBreedForTest }) {
  const [filterSpecies, setFilterSpecies] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [expandedBreed, setExpandedBreed] = useState(null)

  const breeds = Object.entries(BREED_METADATA).map(([name, data]) => ({
    name,
    ...data,
    isCattle: data.species.toLowerCase().includes('cattle')
  }))

  const filteredBreeds = breeds.filter((b) => {
    const matchesSpecies =
      filterSpecies === 'all' ||
      (filterSpecies === 'cattle' && b.isCattle) ||
      (filterSpecies === 'buffalo' && !b.isCattle)

    const matchesSearch =
      b.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      b.origin.toLowerCase().includes(searchQuery.toLowerCase()) ||
      b.description.toLowerCase().includes(searchQuery.toLowerCase())

    return matchesSpecies && matchesSearch
  })

  return (
    <section className="catalog-section" style={{ marginTop: '2.5rem', marginBottom: '2.5rem' }}>
      <div className="container">
        <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
          <div style={{
            display: 'inline-block',
            padding: '0.25rem 0.75rem',
            backgroundColor: '#EFF6FF',
            color: 'var(--primary)',
            fontSize: '0.75rem',
            fontWeight: 700,
            borderRadius: '999px',
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
            marginBottom: '0.5rem'
          }}>
            ICAR-NBAGR National Repository
          </div>
          <h2 style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--slate-900)' }}>
            Indian Bovine Breed Encyclopedia (14 Breeds)
          </h2>
          <p style={{ fontSize: '0.9rem', color: 'var(--slate-500)', maxWidth: '600px', margin: '0.35rem auto 0' }}>
            Comprehensive anatomical profiles, geographic distribution, and dairy productivity metrics for recognized indigenous livestock.
          </p>
        </div>

        {/* Filter & Search Bar */}
        <div style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: '1rem',
          justifyContent: 'space-between',
          alignItems: 'center',
          backgroundColor: '#fff',
          padding: '1rem',
          borderRadius: '12px',
          boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
          marginBottom: '1.5rem',
          border: '1px solid var(--slate-200)'
        }}>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button
              type="button"
              className={`toggle-btn ${filterSpecies === 'all' ? 'active' : ''}`}
              onClick={() => setFilterSpecies('all')}
              style={{ fontSize: '0.85rem' }}
            >
              All Breeds (14)
            </button>
            <button
              type="button"
              className={`toggle-btn ${filterSpecies === 'cattle' ? 'active' : ''}`}
              onClick={() => setFilterSpecies('cattle')}
              style={{ fontSize: '0.85rem' }}
            >
              🐄 Cattle (8)
            </button>
            <button
              type="button"
              className={`toggle-btn ${filterSpecies === 'buffalo' ? 'active' : ''}`}
              onClick={() => setFilterSpecies('buffalo')}
              style={{ fontSize: '0.85rem' }}
            >
              🐃 Buffalo (6)
            </button>
          </div>

          <div style={{ position: 'relative', minWidth: '260px' }}>
            <input
              type="text"
              placeholder="Search by breed name, state, or trait..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{
                width: '100%',
                padding: '0.55rem 1rem 0.55rem 2.2rem',
                borderRadius: '8px',
                border: '1px solid var(--slate-300)',
                fontSize: '0.85rem',
                outline: 'none'
              }}
            />
            <span style={{ position: 'absolute', left: '0.75rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--slate-400)' }}>
              🔍
            </span>
          </div>
        </div>

        {/* Breed Cards Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
          gap: '1.25rem'
        }}>
          {filteredBreeds.map((breed) => {
            const isExpanded = expandedBreed === breed.name
            return (
              <div
                key={breed.name}
                style={{
                  backgroundColor: '#fff',
                  borderRadius: '12px',
                  border: '1px solid var(--slate-200)',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.04)',
                  padding: '1.25rem',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                  transition: 'transform 0.2s, box-shadow 0.2s'
                }}
              >
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                    <div>
                      <span style={{
                        display: 'inline-block',
                        fontSize: '0.7rem',
                        fontWeight: 700,
                        padding: '0.2rem 0.5rem',
                        borderRadius: '4px',
                        backgroundColor: breed.isCattle ? '#FEF3C7' : '#F1F5F9',
                        color: breed.isCattle ? '#92400E' : '#334155',
                        marginBottom: '0.25rem'
                      }}>
                        {breed.isCattle ? '🐄 Cattle (Bos indicus)' : '🐃 Buffalo (Bubalus bubalis)'}
                      </span>
                      <h3 style={{ fontSize: '1.2rem', fontWeight: 800, color: 'var(--slate-900)' }}>
                        {breed.name}
                      </h3>
                    </div>
                    <span style={{
                      fontSize: '0.75rem',
                      fontWeight: 700,
                      color: 'var(--primary)',
                      backgroundColor: '#EFF6FF',
                      padding: '0.25rem 0.5rem',
                      borderRadius: '6px'
                    }}>
                      {breed.primary_use.split(' ')[0]}
                    </span>
                  </div>

                  <p style={{
                    fontSize: '0.83rem',
                    color: 'var(--slate-600)',
                    lineHeight: 1.45,
                    marginBottom: '0.75rem',
                    display: '-webkit-box',
                    WebkitLineClamp: isExpanded ? 'unset' : 3,
                    WebkitBoxOrient: 'vertical',
                    overflow: 'hidden'
                  }}>
                    {breed.description}
                  </p>

                  <div style={{
                    backgroundColor: '#F8FAFC',
                    borderRadius: '8px',
                    padding: '0.65rem 0.75rem',
                    fontSize: '0.78rem',
                    marginBottom: '0.75rem',
                    border: '1px solid #E2E8F0'
                  }}>
                    <div style={{ marginBottom: '0.35rem' }}>
                      <strong style={{ color: 'var(--slate-700)' }}>📍 Native Tract: </strong>
                      <span style={{ color: 'var(--slate-600)' }}>{breed.origin}</span>
                    </div>
                    <div>
                      <strong style={{ color: 'var(--slate-700)' }}>🥛 Milk Yield: </strong>
                      <span style={{ color: '#047857', fontWeight: 700 }}>{breed.milk_yield}</span>
                    </div>
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem' }}>
                  <button
                    type="button"
                    onClick={() => setExpandedBreed(isExpanded ? null : breed.name)}
                    style={{
                      flex: 1,
                      padding: '0.45rem',
                      fontSize: '0.78rem',
                      fontWeight: 600,
                      borderRadius: '6px',
                      border: '1px solid var(--slate-300)',
                      backgroundColor: '#fff',
                      color: 'var(--slate-700)',
                      cursor: 'pointer'
                    }}
                  >
                    {isExpanded ? 'Show Less ▲' : 'Read Profile ▼'}
                  </button>
                  {onSelectBreedForTest && (
                    <button
                      type="button"
                      onClick={() => onSelectBreedForTest(breed.name)}
                      style={{
                        padding: '0.45rem 0.75rem',
                        fontSize: '0.78rem',
                        fontWeight: 700,
                        borderRadius: '6px',
                        border: 'none',
                        backgroundColor: 'var(--primary)',
                        color: '#fff',
                        cursor: 'pointer'
                      }}
                    >
                      Test Breed 🔬
                    </button>
                  )}
                </div>
              </div>
            )
          })}
        </div>

        {filteredBreeds.length === 0 && (
          <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--slate-400)' }}>
            <p>No breeds match your search query "{searchQuery}".</p>
          </div>
        )}
      </div>
    </section>
  )
}

