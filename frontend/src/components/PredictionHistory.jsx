import React from 'react'

export default function PredictionHistory({ history = [] }) {
  if (!history || history.length === 0) {
    return null
  }

  return (
    <section className="history-section">
      <div className="container">
        <div className="history-card">
          <div className="panel-header" style={{ marginBottom: '0.75rem', borderBottom: 'none' }}>
            <div className="panel-step" style={{ background: 'var(--accent-light)', color: 'var(--accent)' }}>03</div>
            <div>
              <h2 className="panel-title">Session Scan History</h2>
              <p className="panel-subtitle">Chronological record of processed livestock images</p>
            </div>
          </div>

          <div className="table-responsive">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Filename</th>
                  <th>Predicted Breed</th>
                  <th>Confidence</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {history.map((item, idx) => (
                  <tr key={idx}>
                    <td style={{ fontFamily: 'monospace', fontSize: '0.8rem', color: 'var(--slate-500)' }}>
                      {new Date(item.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                    </td>
                    <td style={{ fontWeight: 600 }}>{item.filename}</td>
                    <td>
                      <span style={{ fontWeight: 700, color: 'var(--primary)' }}>
                        {item.predicted_breed}
                      </span>
                    </td>
                    <td>
                      <span style={{ fontFamily: 'monospace', fontWeight: 700 }}>
                        {(item.confidence * 100).toFixed(1)}%
                      </span>
                    </td>
                    <td>
                      <span className="status-badge online" style={{ padding: '0.2rem 0.5rem', fontSize: '0.7rem' }}>
                        Verified
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  )
}
