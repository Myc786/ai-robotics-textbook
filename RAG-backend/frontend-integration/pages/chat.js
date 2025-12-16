// pages/chat.js
// Example Next.js page integrating the RAG chat
import React, { useState } from 'react';
import RAGChat from '../components/RAGChat';
import DocumentUpload from '../components/DocumentUpload';
import '../styles/rag-chat.css';

const ChatPage = () => {
  const [activeTab, setActiveTab] = useState('chat'); // 'chat' or 'upload'
  const [documents, setDocuments] = useState([]);

  const handleDocumentUpload = (result) => {
    console.log('Document uploaded:', result);
    setDocuments(prev => [...prev, result]);

    // Optionally switch to chat view after upload
    setActiveTab('chat');
  };

  return (
    <div className="container">
      <header>
        <h1>AI Book Assistant</h1>
        <p>Powered by Retrieval-Augmented Generation (RAG)</p>
      </header>

      <main>
        <div className="tabs">
          <button
            className={activeTab === 'chat' ? 'active' : ''}
            onClick={() => setActiveTab('chat')}
          >
            Chat
          </button>
          <button
            className={activeTab === 'upload' ? 'active' : ''}
            onClick={() => setActiveTab('upload')}
          >
            Upload Document
          </button>
        </div>

        <div className="tab-content">
          {activeTab === 'chat' ? (
            <RAGChat />
          ) : (
            <DocumentUpload onUploadSuccess={handleDocumentUpload} />
          )}
        </div>
      </main>

      <footer>
        <p>Powered by RAG Technology • Answers sourced from book content</p>
      </footer>
    </div>
  );
};

export default ChatPage;