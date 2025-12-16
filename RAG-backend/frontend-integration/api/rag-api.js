// api/rag-api.js
// API client for connecting to your RAG backend
class RAGApiClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
  }

  // Method to send a chat query to the backend
  async chat(query, options = {}) {
    const {
      selectedText = null,
      topK = 5,
      similarityThreshold = 0.5,
      searchScope = 'full_book' // 'full_book' or 'selected_text_only'
    } = options;

    try {
      const response = await fetch(`${this.baseURL}/api/v1/chat`, {
        method: 'POST',
        headers: this.defaultHeaders,
        body: JSON.stringify({
          query,
          selected_text: selectedText,
          top_k: topK,
          similarity_threshold: similarityThreshold,
          search_scope: searchScope
        })
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Chat API error:', error);
      throw error;
    }
  }

  // Method to upload and index a document
  async uploadDocument(title, content, options = {}) {
    const {
      url = null,
      author = null,
      sourceType = 'book'
    } = options;

    try {
      const response = await fetch(`${this.baseURL}/api/v1/documents`, {
        method: 'POST',
        headers: this.defaultHeaders,
        body: JSON.stringify({
          title,
          content,
          url,
          author,
          source_type: sourceType
        })
      });

      if (!response.ok) {
        throw new Error(`Document upload failed: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Document upload error:', error);
      throw error;
    }
  }

  // Method to upload a document file
  async uploadDocumentFile(file, options = {}) {
    const {
      title = null,
      url = null,
      author = null,
      sourceType = 'book'
    } = options;

    const formData = new FormData();
    formData.append('file', file);

    if (title) formData.append('title', title);
    if (url) formData.append('url', url);
    if (author) formData.append('author', author);
    if (sourceType) formData.append('source_type', sourceType);

    try {
      const response = await fetch(`${this.baseURL}/api/v1/documents/file`, {
        method: 'POST',
        body: formData,
        // Don't set Content-Type header, let the browser set it with boundary
      });

      if (!response.ok) {
        throw new Error(`File upload failed: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('File upload error:', error);
      throw error;
    }
  }

  // Method to check backend health
  async healthCheck() {
    try {
      const response = await fetch(`${this.baseURL}/health`);
      if (!response.ok) {
        throw new Error(`Health check failed: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Health check error:', error);
      throw error;
    }
  }
}

// Initialize the API client with your backend URL
// Replace 'YOUR_BACKEND_URL' with the actual URL of your deployed backend
const ragApiClient = new RAGApiClient(process.env.NEXT_PUBLIC_RAG_BACKEND_URL || 'https://your-backend-url.com');

export default ragApiClient;