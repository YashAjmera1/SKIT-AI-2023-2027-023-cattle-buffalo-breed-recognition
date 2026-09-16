import { useState } from 'react'
import './App.css'

function App() {
  const [image, setImage] = useState(null)
  const [animal, setAnimal] = useState('Cattle')

  const handleImage = (event) => {
    const file = event.target.files?.[0]
    if (file && file.type.startsWith('image/')) {
      setImage(URL.createObjectURL(file))
    }
  }

  return (
    <main className="app">
      <header className="topbar">
        <div className="logo">CB</div>
        <div>
          <h2>BreedWise</h2>
          <p>Indian Livestock Recognition</p>
        </div>
        <span className="status">PROJECT PROTOTYPE</span>
      </header>

      <section className="hero">
        <span className="eyebrow">AI-POWERED LIVESTOCK IDENTIFICATION</span>
        <h1>Recognise the breed.<br /><span>Preserve our heritage.</span></h1>
        <p>Explore India's indigenous cattle and buffalo breeds with our image-based recognition system.</p>
      </section>

      <section className="workspace">
        <div className="panel">
          <div className="section-heading">
            <span>01</span>
            <div>
              <h3>Upload animal image</h3>
              <p>Select a clear photo to begin.</p>
            </div>
          </div>

          <div className="animal-options">
            {['Cattle', 'Buffalo'].map((item) => (
              <button
                key={item}
                className={animal === item ? 'animal active' : 'animal'}
                onClick={() => setAnimal(item)}
              >
                {item === 'Cattle' ? '🐄' : '🐃'} {item}
              </button>
            ))}
          </div>

          <label className="dropzone">
            {image ? (
              <img src={image} alt="Selected livestock" className="preview" />
            ) : (
              <>
                <span className="upload-icon">↑</span>
                <strong>Choose an animal photo</strong>
                <span>Click to browse your computer</span>
                <small>JPG, PNG or WEBP</small>
              </>
            )}
            <input type="file" accept="image/*" onChange={handleImage} />
          </label>

          {image && (
            <button className="remove" onClick={() => setImage(null)}>
              Remove image
            </button>
          )}

          <button
            className="primary"
            disabled={!image}
            onClick={() => alert('Image selected successfully. AI prediction will be enabled after model and backend integration.')}
          >
            Prepare for recognition →
          </button>

          <p className="note">
            Prototype mode: breed prediction is not connected yet.
          </p>
        </div>

        <div className="panel">
          <div className="section-heading">
            <span>02</span>
            <div>
              <h3>Recognition results</h3>
              <p>Breed information will appear here.</p>
            </div>
          </div>

          <div className="animal-preview">
            {image ? (
              <img src={image} alt="Uploaded livestock preview" className="preview" />
            ) : (
              <span>{animal === 'Cattle' ? '🐄' : '🐃'}</span>
            )}
          </div>

          <h3 className="result-title">Awaiting AI analysis</h3>
          <p className="result-description">
            The trained model will identify the breed after AI and backend integration.
          </p>

          <div className="result-row">
            <span>Animal category</span><strong>{animal}</strong>
          </div>
          <div className="result-row">
            <span>Predicted breed</span><strong>Not available</strong>
          </div>
          <div className="result-row">
            <span>Confidence score</span><strong>—</strong>
          </div>

          <div className="info-banner">
            Supporting the identification of Indian cattle and buffalo breeds.
          </div>
        </div>
      </section>

      <footer>
        Image-Based Breed Recognition System for Cattle and Buffalo in India
        <br />Academic Project · SKIT Jaipur
      </footer>
    </main>
  )
}

export default App