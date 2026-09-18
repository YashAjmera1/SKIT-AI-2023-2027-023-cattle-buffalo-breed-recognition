import React from 'react'

export default function Hero() {
  return (
    <section className="hero">
      <div className="container">
        <div className="hero-card">
          <div className="hero-pill">
            <span>●</span> AI-POWERED LIVESTOCK RECOGNITION
          </div>
          <h1 className="hero-title">
            Recognise Indian Breeds. <span className="hero-highlight">Preserve Indigenous Heritage.</span>
          </h1>
          <p className="hero-desc">
            An automated, lightweight deep learning system utilizing EfficientNet-B0 transfer learning to identify 
            and catalog native Indian cattle and buffalo breeds in unconstrained farm environments.
          </p>

          <div className="hero-tags">
            <span className="hero-tag">🎯 UN SDG 2 (Zero Hunger)</span>
            <span className="hero-tag">🧠 EfficientNet-B0 CNN</span>
            <span className="hero-tag">⚡ FastAPI Backend</span>
            <span className="hero-tag">🐄 14 Indigenous Breeds</span>
            <span className="hero-tag">📍 SKIT Project ID: SKIT/AI/2023-2027/023</span>
          </div>
        </div>
      </div>
    </section>
  )
}
