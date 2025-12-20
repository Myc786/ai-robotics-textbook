import React, { useState, useEffect, useRef } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import ChatApiService from '../services/chat-api';
import ChatMessage from './ChatMessage';
import './BookChatbot.module.css';

const BookChatbot = ({ backendUrl }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [showSelectionButton, setShowSelectionButton] = useState(false);
  const [selectionButtonPosition, setSelectionButtonPosition] = useState({ x: 0, y: 0 });

  const messagesEndRef = useRef(null);
  const selectionButtonRef = useRef(null);
  const { siteConfig = {} } = useDocusaurusContext();

  // Determine backend URL with fallbacks
  const resolvedBackendUrl = backendUrl ||
    siteConfig?.customFields?.NEXT_PUBLIC_RAG_BACKEND_URL ||
    (typeof window !== 'undefined' && window?.env?.NEXT_PUBLIC_RAG_BACKEND_URL) ||
    (typeof window !== 'undefined' && window?.NEXT_PUBLIC_RAG_BACKEND_URL) ||
    document?.documentElement?.getAttribute('data-rag-backend-url') ||
    '/api';

  const chatApiService = new ChatApiService(resolvedBackendUrl);

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle text selection
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const selectedText = selection.toString().trim();

      if (selectedText.length > 0) {
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();

        setSelectionButtonPosition({
          x: rect.left + window.scrollX,
          y: rect.top + window.scrollY - 40 // Position above the selection
        });

        setSelectedText(selectedText);
        setShowSelectionButton(true);
      } else {
        setShowSelectionButton(false);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('touchend', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('touchend', handleSelection);
    };
  }, []);

  // Hide selection button when clicking elsewhere
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (selectionButtonRef.current && !selectionButtonRef.current.contains(event.target)) {
        setShowSelectionButton(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('touchstart', handleClickOutside);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('touchstart', handleClickOutside);
    };
  }, []);

  const sendMessage = async (question) => {
    if (!question.trim() || isLoading) return;

    const userMessage = { id: Date.now(), text: question, sender: 'user', timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const data = await chatApiService.sendQuestion(question);

      const botMessage = {
        id: Date.now() + 1,
        text: data.answer,
        sender: 'bot',
        timestamp: new Date(),
        sources: data.sources || [],
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error processing your request. Please try again.',
        sender: 'bot',
        timestamp: new Date(),
        sources: [],
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAskAboutSelection = () => {
    const question = `Explain this selection: ${selectedText}`;
    sendMessage(question);
    setShowSelectionButton(false);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(inputValue);
  };

  return (
    <>
      {/* Text selection button */}
      {showSelectionButton && (
        <div
          ref={selectionButtonRef}
          className="book-chatbot-selection-button"
          style={{
            position: 'absolute',
            left: `${selectionButtonPosition.x}px`,
            top: `${selectionButtonPosition.y}px`,
            zIndex: 10000,
          }}
        >
          <button
            onClick={handleAskAboutSelection}
            className="book-chatbot-selection-btn"
          >
            Ask about this
          </button>
        </div>
      )}

      {/* Floating chat button */}
      <button
        className={`book-chatbot-button ${isOpen ? 'open' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
      >
        {isOpen ? '✕' : '💬'}
      </button>

      {/* Chat window */}
      {isOpen && (
        <div className="book-chatbot-window">
          <div className="book-chatbot-header">
            <h3>Book Assistant</h3>
          </div>

          <div className="book-chatbot-messages">
            {messages.length === 0 ? (
              <div className="book-chatbot-welcome">
                <p>Ask me anything about the book content!</p>
                <p>I can answer questions and cite sources from the textbook.</p>
              </div>
            ) : (
              messages.map((message) => (
                <ChatMessage key={message.id} message={message} />
              ))
            )}
            {isLoading && (
              <div className="book-chatbot-message bot">
                <div className="book-chatbot-typing">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSubmit} className="book-chatbot-input-form">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask a question about the book..."
              disabled={isLoading}
              className="book-chatbot-input"
            />
            <button
              type="submit"
              disabled={isLoading || !inputValue.trim()}
              className="book-chatbot-send-btn"
            >
              Send
            </button>
          </form>
        </div>
      )}
    </>
  );
};

export default BookChatbot;