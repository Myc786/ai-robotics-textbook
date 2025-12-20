const express = require('express');
const cors = require('cors');
const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'Mock RAG Chatbot API' });
});

// Chat endpoint that mimics the real backend
app.post('/api/v1/chat', (req, res) => {
  try {
    const question = req.body.query || req.body.question || 'No question provided';

    // Simple mock response
    const mockResponse = {
      answer: `This is a mock response to your question: "${question}". In a fully configured system, this would connect to the RAG backend to provide answers based on the textbook content. The system would retrieve relevant textbook sections and generate AI-powered responses.`,
      sources: ['https://ai-robotics-textbook.vercel.app/docs/intro', 'https://ai-robotics-textbook.vercel.app/docs/introduction-to-physical-ai']
    };

    // Add a small delay to simulate processing
    setTimeout(() => {
      res.json(mockResponse);
    }, 300);
  } catch (error) {
    console.error('Error processing request:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Catch-all for debugging (only one catch-all route needed)
app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

const PORT = 8000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Mock RAG backend server running on port ${PORT}`);
  console.log(`Health endpoint: http://localhost:${PORT}/health`);
  console.log(`Chat endpoint: http://localhost:${PORT}/api/v1/chat`);
});