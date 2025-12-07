import React, { useState } from 'react';
import styles from './styles.module.css';

function Chatbot() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponse(null);
    setError(null);

    try {
      // Use base URL that works for both development and GitHub Pages
      let RAG_BACKEND_URL;

      // Check if we're in development or production
      if (typeof window !== 'undefined') {
        // Client-side: check current URL to determine backend URL
        const currentHost = window.location.hostname;

        if (currentHost === 'localhost' || currentHost === '127.0.0.1') {
          // Local development
          RAG_BACKEND_URL = 'http://localhost:8000/api/v1/query';
        } else {
          // Production (GitHub Pages) - you'll need to have your RAG backend deployed separately
          // For now, using a placeholder - in real deployment, you'd use your actual backend URL
          RAG_BACKEND_URL = 'https://your-production-rag-backend.com/api/v1/query';

          // If you're running the backend locally while accessing the frontend from GitHub Pages,
          // you might need to temporarily use your local IP, e.g.:
          // RAG_BACKEND_URL = 'http://YOUR_IP_ADDRESS:8000/api/v1/query';
        }
      } else {
        // Server-side rendering fallback
        RAG_BACKEND_URL = process.env.NODE_ENV === 'production'
          ? 'https://your-production-rag-backend.com/api/v1/query'
          : 'http://localhost:8000/api/v1/query';
      }

      // Note: For GitHub Pages deployment, you'll need to host the RAG backend separately
      // CORS policy might block requests from GitHub Pages to localhost, so for full functionality
      // you'll need to deploy the backend to a cloud service (like Heroku, Vercel, etc.)

      const res = await fetch(RAG_BACKEND_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || `HTTP error! status: ${res.status}`);
      }

      const data = await res.json();
      setResponse(data);
    } catch (err) {
      // Provide a more informative message about deployment configuration
      if (err.message.includes('CORS') || err.message.includes('Failed to fetch')) {
        setError(
          'The RAG backend is not accessible. When deployed to GitHub Pages, ' +
          'the backend needs to be hosted separately and configured to allow cross-origin requests. ' +
          'For local development, ensure the FastAPI server is running on port 8000.'
        );
      } else {
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.chatbotContainer}>
      <h2>Ask the Textbook AI</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question about Physical AI and Robotics..."
          disabled={loading}
        />
        <button type="submit" disabled={loading} className="button">
          {loading ? 'Thinking...' : 'Ask'}
        </button>
      </form>

      {error && <p className={styles.error}>Error: {error}</p>}

      {response && (
        <div className={styles.responseContainer}>
          <h3>Answer:</h3>
          <p>{response.answer}</p>
          {response.sources && response.sources.length > 0 && (
            <div className={styles.sources}>
              <h4>Sources:</h4>
              <ul>
                {response.sources.map((source, index) => (
                  <li key={index}>
                    <a href={source.url} target="_blank" rel="noopener noreferrer">
                      {source.title}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Chatbot;
