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
      // Use environment variable for backend URL with fallback chain
      // Priority: 1. Docusaurus customFields, 2. window.env, 3. data attribute, 4. default
      const backendBaseUrl =
        siteConfig?.customFields?.NEXT_PUBLIC_RAG_BACKEND_URL ||
        (typeof window !== 'undefined' && window?.env?.NEXT_PUBLIC_RAG_BACKEND_URL) ||
        (typeof window !== 'undefined' && window?.NEXT_PUBLIC_RAG_BACKEND_URL) ||
        document?.documentElement?.getAttribute('data-rag-backend-url') ||
        'http://localhost:8000';
      const RAG_BACKEND_URL = `${backendBaseUrl}/api/v1/chat`;

      // Note: For GitHub Pages deployment, you'll need to host the RAG backend separately
      // CORS policy might block requests from GitHub Pages to localhost, so for full functionality
      // you'll need to deploy the backend to a cloud service (like Heroku, Vercel, etc.)

      const res = await fetch(RAG_BACKEND_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query_text: query, mode: 'global' }),
      });

      if (!res.ok) {
        let errorMessage = `HTTP error! status: ${res.status}`;
        try {
          const errorData = await res.json();
          errorMessage = errorData.detail || errorMessage;
        } catch {
          // Response was not valid JSON, use default error message
        }
        throw new Error(errorMessage);
      }

      const data = await res.json();
      console.log('Chat response:', data); // Debug logging
      setResponse(data);
    } catch (err) {
      console.error('Chat error:', err); // Debug logging
      // Provide a more informative message about deployment configuration
      if (err.message.includes('CORS') || err.message.includes('Failed to fetch')) {
        setError(
          'The RAG backend is not accessible. This is typically caused by one of the following:\n\n' +
          '1. The backend server is not running. To start it, run in a separate terminal:\n' +
          '   cd rag-backend\n' +
          '   pip install -r requirements.txt\n' +
          '   python start_server.py\n\n' +
          '2. CORS restrictions between frontend and backend. Make sure the backend allows requests ' +
          'from the frontend origin.\n\n' +
          '3. The backend is running but on a different port. Verify it\'s on port 8000.\n\n' +
          'For local development, ensure the FastAPI server is running on port 8000 before testing.'
        );
      } else if (err.message.includes('404') || err.message.includes('not found')) {
        setError(
          'Chat API endpoint not found. The backend might not be properly deployed or the API endpoint may have changed.\n\n' +
          'Please verify that the backend service is properly deployed and accessible.'
        );
      } else if (err.message.includes('500') || err.message.includes('error')) {
        setError(
          'Backend server error. The RAG service may not be properly configured.\n\n' +
          'Error details: ' + err.message + '\n\n' +
          'This could be due to missing environment variables (API keys) or missing indexed data.\n' +
          'Check that the backend has proper API keys configured and that documents have been indexed.'
        );
      } else {
        setError('Error: ' + err.message);
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

      {!response && !error && !loading && (
        <div className={styles.info}>
          <p className={styles.welcomeMessage}>
            I'll answer your question based on the provided documents. Go ahead and ask your question about Physical AI.
          </p>
        </div>
      )}

      {error && (
        <div className={styles.error}>
          <pre className={styles.errorText}>{error}</pre>
        </div>
      )}

      {response && (
        <div className={styles.responseContainer}>
          <div className={styles.responseContent}>
            {response.response ? (
              <pre className={styles.responseText}>{response.response}</pre>
            ) : (
              <pre className={styles.responseText}>No response content received from backend. Backend may not be properly configured or have indexed data.</pre>
            )}
            {response.retrieved_chunks && response.retrieved_chunks.length > 0 && (
              <div className={styles.sourcesSection}>
                <h4>Sources:</h4>
                <div className={styles.sourcesList}>
                  {response.retrieved_chunks.slice(0, 3).map((chunk, index) => (
                    <div key={index} className={styles.sourceItem}>
                      <span className={styles.sourceFile}>{chunk.chapter_id || chunk.section_id || `Chunk ${index + 1}`}</span>
                      <span className={styles.sourceScore}>{chunk.similarity_score?.toFixed(3) || 'N/A'}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
            {(response.execution_time_ms !== undefined && response.execution_time_ms !== null) && (
              <div className={styles.performanceInfo}>
                <small>Response time: {response.execution_time_ms}ms</small>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default Chatbot;
