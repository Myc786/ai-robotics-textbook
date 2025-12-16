import React, { useState } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './styles.module.css';

function Chatbot() {
  const { siteConfig = {} } = useDocusaurusContext();
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
      // Use environment variable for backend URL
      // This allows configuration via NEXT_PUBLIC_RAG_BACKEND_URL
      // Use multiple fallbacks to ensure availability in different environments
      const backendBaseUrl =
        siteConfig?.customFields?.NEXT_PUBLIC_RAG_BACKEND_URL ||
        (typeof process !== 'undefined' && process.env?.NEXT_PUBLIC_RAG_BACKEND_URL) ||
        window?.env?.NEXT_PUBLIC_RAG_BACKEND_URL ||
        window?.NEXT_PUBLIC_RAG_BACKEND_URL ||
        document?.documentElement?.getAttribute('data-rag-backend-url') ||
        'http://localhost:8080';
      const RAG_BACKEND_URL = `${backendBaseUrl}/api/v1/chat`;

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
          'The RAG backend is not accessible. This is typically caused by one of the following:\n\n' +
          '1. The backend server is not running. To start it, run in a separate terminal:\n' +
          '   cd RAG-backend\n' +
          '   poetry run uvicorn main:app --host 0.0.0.0 --port 8000\n\n' +
          '2. CORS restrictions between frontend and backend. Make sure the backend allows requests ' +
          'from the frontend origin.\n\n' +
          '3. The backend is running but on a different port. Verify it\'s on port 8000.\n\n' +
          'For local development, ensure the FastAPI server is running on port 8000 before testing.'
        );
      } else {
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  // Check if we're on localhost to provide setup instructions
  const isLocalhost = typeof window !== 'undefined' &&
    (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');

  return (
    <div className={styles.chatbotContainer}>
      <h2>Textbook AI Assistant</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question about Physical AI and Robotics..."
          disabled={loading}
        />
        <button type="submit" disabled={loading} className="button">
          {loading ? 'Processing...' : 'Ask'}
        </button>
      </form>

      {error && (
        <div className={styles.error}>
          <pre className={styles.errorText}>{error}</pre>
        </div>
      )}

      {response && (
        <div className={styles.responseContainer}>
          <div className={styles.responseContent}>
            <div className={styles.responseText} style={{color: 'black', backgroundColor: 'white', padding: '10px', borderRadius: '4px'}}>
              <pre style={{whiteSpace: 'pre-wrap', wordWrap: 'break-word', fontFamily: 'inherit', margin: 0, color: 'black', backgroundColor: 'white'}}>{response.response}</pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Chatbot;
