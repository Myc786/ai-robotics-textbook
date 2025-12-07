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
      // Replace with your actual RAG backend URL
      const RAG_BACKEND_URL = process.env.NODE_ENV === 'production'
        ? 'https://your-production-rag-backend.com/api/v1/query'
        : 'http://localhost:8000/api/v1/query';

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
      setError(err.message);
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
