/**
 * API service for chatbot communication
 */

class ChatApiService {
  constructor(backendUrl) {
    this.backendUrl = backendUrl;
  }

  /**
   * Send a question to the backend and get a response
   * @param {string} question - The question to send
   * @returns {Promise<{answer: string, sources: string[]}>} The response from the backend
   */
  async sendQuestion(question) {
    try {
      const response = await fetch(`${this.backendUrl}/api/v1/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error sending question to backend:', error);
      throw error;
    }
  }

  /**
   * Test the connection to the backend
   * @returns {Promise<boolean>} Whether the connection is successful
   */
  async testConnection() {
    try {
      // Try to access the health endpoint or just make a simple request
      const response = await fetch(`${this.backendUrl}/api/v1/health`);
      return response.ok;
    } catch (error) {
      console.error('Error testing backend connection:', error);
      return false;
    }
  }
}

export default ChatApiService;