import React from 'react';
import Layout from '@theme/Layout';
import Chatbot from '../components/Chatbot';

function RagChat() {
  return (
    <Layout title="RAG Chatbot" description="Chat with the Physical AI & Humanoid Robotics textbook">
      <main className="container margin-vert--lg">
        <div className="text--center">
          <h1 className="hero__title">Textbook RAG Chatbot</h1>
        </div>
        <div className="card">
          <Chatbot />
        </div>
      </main>
    </Layout>
  );
}

export default RagChat;
