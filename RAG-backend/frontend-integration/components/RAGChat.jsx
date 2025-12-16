// components/RAGChat.jsx
// React component for the RAG Chat interface
import React, { useState, useRef, useEffect } from 'react';
import ragApiClient from '../api/rag-api';

const RAGChat = ({ documentId = null }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState(null);
  const [searchScope, setSearchScope] = useState('full_book'); // 'full_book' or 'selected_text_only'
  const messagesEndRef = useRef(null);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Handle text selection
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      if (selection.toString().trim() !== '') {
        setSelectedText(selection.toString().trim());
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to chat
    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Send query to backend
      const response = await ragApiClient.chat(inputValue, {
        selectedText: searchScope === 'selected_text_only' ? selectedText : null,
        searchScope: searchScope
      });

      // Add bot response to chat
      const botMessage = {
        id: Date.now() + 1,
        text: response.response,
        sender: 'bot',
        timestamp: new Date(),
        sources: response.retrieved_chunks || [],
        status: response.response_status
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Chat error:', error);

      // Add error message to chat
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error processing your request. Please try again.',
        sender: 'bot',
        timestamp: new Date(),
        isError: true
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleScopeChange = (scope) => {
    setSearchScope(scope);
  };

  return (
    <div className="rag-chat-container">
      <div className="rag-chat-header">
        <h2>RAG Chatbot</h2>
        <div className="search-scope-controls">
          <button
            className={`scope-btn ${searchScope === 'full_book' ? 'active' : ''}`}
            onClick={() => handleScopeChange('full_book')}
          >
            Full Book
          </button>
          <button
            className={`scope-btn ${searchScope === 'selected_text_only' ? 'active' : ''}`}
            onClick={() => handleScopeChange('selected_text_only')}
            disabled={!selectedText}
          >
            Selected Text Only
          </button>
        </div>
        {selectedText && (
          <div className="selected-text-preview">
            <small>Selected: "{selectedText.substring(0, 50)}{selectedText.length > 50 ? '...' : ''}"</small>
          </div>
        )}
      </div>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <p>Hello! I'm your RAG-powered assistant. I can answer questions based on the book content.</p>
            <p>Ask me anything about the book, or select text and ask questions about it specifically!</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
            >
              <div className="message-content">
                <p>{message.text}</p>
                {message.sources && message.sources.length > 0 && (
                  <div className="sources">
                    <small>Sources:</small>
                    <ul>
                      {message.sources.slice(0, 3).map((source, index) => (
                        <li key={index}>
                          {source.url ? (
                            <a href={source.url} target="_blank" rel="noopener noreferrer">
                              {source.chapter ? `${source.chapter}` : 'Source'}
                            </a>
                          ) : (
                            <span>{source.chapter || 'Source'}</span>
                          )}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {message.isError && (
                  <div className="error-message">
                    <small>Error: Could not process your request</small>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="message bot-message">
            <div className="message-content">
              <p>Thinking...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask a question about the book..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !inputValue.trim()}>
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default RAGChat;