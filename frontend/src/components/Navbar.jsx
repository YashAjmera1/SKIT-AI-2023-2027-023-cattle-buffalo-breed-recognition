import React from 'react'

export default function Navbar({ isBackendOnline = false }) {
  return (
    <header className="navbar">
      <div className="container navbar-inner">
        <div className="brand">
          <div className="brand-icon">CB</div>
          <div>
            <div className="brand-title">BreedWise</div>
            <div className="brand-subtitle">Indian Livestock Recognition · SKIT Jaipur</div>
          </div>
        </div>

        <div className="nav-badges">
          <span className={`status-badge ${isBackendOnline ? 'online' : 'offline'}`}>
            <span className="pulse-dot"></span>
            {isBackendOnline ? 'FastAPI Connected' : 'Demo / Standalone Mode'}
          </span>
          <span className="status-badge online" style={{ background: '#fef3c7', color: '#92400e', borderColor: '#fde68a' }}>
            CSE (AI) 2026-27
          </span>
        </div>
      </div>
    </header>
  )
}
