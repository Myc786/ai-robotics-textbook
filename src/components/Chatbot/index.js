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
        (typeof window !== 'undefined' && window?.env?.NEXT_PUBLIC_RAG_BACKEND_URL) ||
        (typeof window !== 'undefined' && window?.NEXT_PUBLIC_RAG_BACKEND_URL) ||
        document?.documentElement?.getAttribute('data-rag-backend-url') ||
        'https://muhammadyounis-rag.hf.space/';
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
      console.log('Chat response:', data); // Debug logging
      setResponse(data);
    } catch (err) {
      console.error('Chat error:', err); // Debug logging
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
      } else if (err.message.includes('404') || err.message.includes('not found')) {
        setError(
          'Chat API endpoint not found. The backend might not be properly deployed or the API endpoint may have changed.\n\n' +
          'Current backend URL: ' + backendBaseUrl + '\n' +
          'Expected endpoint: ' + RAG_BACKEND_URL + '\n\n' +
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

      {!response && !error && (
        <div className={styles.info}>
          <p style={{color: '#64748b', fontStyle: 'italic', textAlign: 'center', padding: '1rem', marginTop: '1rem', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0'}}>
            Note: This chatbot connects to a RAG (Retrieval-Augmented Generation) backend that answers questions based on the textbook content.
            The backend requires proper configuration with API keys and indexed content to function.
            If you see error messages, please check the backend setup instructions.
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
              <div className={styles.responseText}>
                <pre style={{whiteSpace: 'pre-wrap', wordWrap: 'break-word', fontFamily: 'inherit', margin: 0, color: 'black', backgroundColor: 'white', padding: '15px', borderRadius: '8px', border: '1px solid #e2e8f0', lineHeight: '1.6'}}>{response.response}</pre>
              </div>
            ) : (
              <div className={styles.responseText}>
                <pre style={{whiteSpace: 'pre-wrap', wordWrap: 'break-word', fontFamily: 'inherit', margin: 0, color: 'black', backgroundColor: 'white', padding: '15px', borderRadius: '8px', border: '1px solid #e2e8f0', lineHeight: '1.6'}}>No response content received from backend. Backend may not be properly configured or have indexed data.</pre>
              </div>
            )}
            {response.retrieved_chunks && response.retrieved_chunks.length > 0 && (
              <div className={styles.sourcesSection}>
                <h4>Sources:</h4>
                <div className={styles.sourcesList}>
                  {response.retrieved_chunks.slice(0, 3).map((chunk, index) => (
                    <div key={index} className={styles.sourceItem}>
                      <span className={styles.sourceFile}>{chunk.chapter || chunk.url || `Source ${index + 1}`}</span>
                      <span className={styles.sourceScore}>{chunk.score?.toFixed(3) || 'N/A'}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
            {response.execution_time_ms && (
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
