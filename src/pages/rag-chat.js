import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import Chatbot from '../components/Chatbot';

// Robot icon component
const RobotIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 100 100"
    width="120"
    height="120"
    className="margin-bottom--sm"
    style={{
      filter: 'drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2))'
    }}
  >
    <defs>
      <linearGradient id="robotBody" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#667eea" />
        <stop offset="100%" stopColor="#764ba2" />
      </linearGradient>
      <linearGradient id="robotHead" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#764ba2" />
        <stop offset="100%" stopColor="#667eea" />
      </linearGradient>
    </defs>
    <circle cx="50" cy="35" r="15" fill="url(#robotHead)" />
    <rect x="35" y="25" width="30" height="5" fill="#00f5ff" />
    <circle cx="42" cy="32" r="2" fill="#ffffff" />
    <circle cx="58" cy="32" r="2" fill="#ffffff" />
    <rect x="40" y="38" width="20" height="3" fill="#ffffff" />
    <rect x="30" y="50" width="40" height="35" fill="url(#robotBody)" rx="10" />
    <rect x="35" y="55" width="30" height="15" fill="#00f5ff" rx="5" />
    <rect x="25" y="65" width="10" height="15" fill="url(#robotBody)" rx="3" />
    <rect x="65" y="65" width="10" height="15" fill="url(#robotBody)" rx="3" />
    <rect x="40" y="90" width="8" height="15" fill="url(#robotBody)" rx="3" />
    <rect x="52" y="90" width="8" height="15" fill="url(#robotBody)" rx="3" />
  </svg>
);

function RagChat() {
  return (
    <Layout title="Textbook AI Assistant" description="Chat with the Physical AI & Humanoid Robotics textbook">
      <main className="container margin-vert--lg">
        {/* Hero Section */}
        <section className="margin-bottom--xl"
          style={{
            borderRadius: '12px',
            background: '#ffffff',
            padding: '3rem 2rem',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
            border: '1px solid #e2e8f0'
          }}>
          <div className="text--center padding-horiz--md">
            <div className="margin-bottom--lg">
              <RobotIcon />
            </div>
            <h1 className="hero__title" style={{
              fontSize: '2.5rem',
              marginBottom: '1rem',
              color: '#1e293b',
              fontWeight: '600'
            }}>
              Textbook AI Assistant
            </h1>
            <p className="hero__subtitle" style={{
              fontSize: '1.2rem',
              maxWidth: '700px',
              margin: '0 auto 1.5rem',
              color: '#334155',
              lineHeight: '1.6'
            }}>
              Interact with the Physical AI & Humanoid Robotics textbook using our AI-powered assistant. Ask questions and get personalized answers based on textbook content.
            </p>
            <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', flexWrap: 'wrap' }}>
              <div className="badge badge--success margin-horiz--sm" style={{
                fontSize: '0.9rem',
                backgroundColor: '#dcfce7',
                color: '#166534',
                border: '1px solid #bbf7d0',
                padding: '0.5rem 1rem',
                borderRadius: '6px'
              }}>
                Powered by RAG Technology
              </div>
              <div className="badge badge--primary margin-horiz--sm" style={{
                fontSize: '0.9rem',
                backgroundColor: '#dbeafe',
                color: '#1e40af',
                border: '1px solid #bfdbfe',
                padding: '0.5rem 1rem',
                borderRadius: '6px'
              }}>
                AI-Powered Responses
              </div>
              <div className="badge badge--secondary margin-horiz--sm" style={{
                fontSize: '0.9rem',
                backgroundColor: '#e9d5ff',
                color: '#5b21b6',
                border: '1px solid #d8b4fe',
                padding: '0.5rem 1rem',
                borderRadius: '6px'
              }}>
                Knowledge Extraction
              </div>
            </div>
          </div>
        </section>

        {/* Chatbot Section */}
        <section>
          <div className="row">
            <div className="col col--10 col--offset-1">
              <div className="card">
                <div className="card__header text--center">
                  <h2 style={{
                    marginBottom: 0,
                    fontSize: '1.5rem',
                    color: '#1e293b',
                    fontWeight: '600'
                  }}>
                    Start Conversing with AI
                  </h2>
                </div>
                <div className="card__body">
                  <Chatbot />
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Chapter Navigation Section */}
        <section className="margin-top--xl">
          <div className="text--center margin-bottom--lg">
            <h2 style={{
              fontSize: '1.75rem',
              color: '#1e293b',
              fontWeight: '600',
              marginBottom: '0.5rem'
            }}>
              Explore Textbook Chapters
            </h2>
            <p className="hero__subtitle" style={{
              maxWidth: '600px',
              margin: '0.5rem auto 0',
              color: '#64748b'
            }}>
              Dive deeper into specific topics covered in the Physical AI & Humanoid Robotics textbook
            </p>
          </div>

          <div className="row">
            <div className="col col--3">
              <Link to="/docs/1-introduction-to-physical-ai" className="card" style={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                padding: '1.5rem',
                textAlign: 'center',
                border: '1px solid #e2e8f0',
                borderRadius: '8px',
                backgroundColor: '#ffffff',
                transition: 'box-shadow 0.2s ease',
                textDecoration: 'none'
              }}>
                <div className="card__body" style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                  <h3 style={{ color: '#1e293b', marginBottom: '0.5rem' }}>Physical AI</h3>
                  <p style={{ color: '#64748b', margin: 0 }}>Introduction to intelligent systems in physical environments</p>
                </div>
              </Link>
            </div>
            <div className="col col--3">
              <Link to="/docs/2-basics-of-humanoid-robotics" className="card" style={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                padding: '1.5rem',
                textAlign: 'center',
                border: '1px solid #e2e8f0',
                borderRadius: '8px',
                backgroundColor: '#ffffff',
                transition: 'box-shadow 0.2s ease',
                textDecoration: 'none'
              }}>
                <div className="card__body" style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                  <h3 style={{ color: '#1e293b', marginBottom: '0.5rem' }}>Humanoid Robotics</h3>
                  <p style={{ color: '#64748b', margin: 0 }}>Principles of humanoid robot movement and control</p>
                </div>
              </Link>
            </div>
            <div className="col col--3">
              <Link to="/docs/5-vision-language-action-systems" className="card" style={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                padding: '1.5rem',
                textAlign: 'center',
                border: '1px solid #e2e8f0',
                borderRadius: '8px',
                backgroundColor: '#ffffff',
                transition: 'box-shadow 0.2s ease',
                textDecoration: 'none'
              }}>
                <div className="card__body" style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                  <h3 style={{ color: '#1e293b', marginBottom: '0.5rem' }}>Vision-Action Systems</h3>
                  <p style={{ color: '#64748b', margin: 0 }}>Integration of perception, language, and action</p>
                </div>
              </Link>
            </div>
            <div className="col col--3">
              <Link to="/docs/7-advanced-control-systems" className="card" style={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                padding: '1.5rem',
                textAlign: 'center',
                border: '1px solid #e2e8f0',
                borderRadius: '8px',
                backgroundColor: '#ffffff',
                transition: 'box-shadow 0.2s ease',
                textDecoration: 'none'
              }}>
                <div className="card__body" style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                  <h3 style={{ color: '#1e293b', marginBottom: '0.5rem' }}>Control Systems</h3>
                  <p style={{ color: '#64748b', margin: 0 }}>Advanced control methodologies for robotics</p>
                </div>
              </Link>
            </div>
          </div>

          <div className="text--center margin-top--lg">
            <Link to="/docs/intro" className="button button--primary button--lg">
              Browse All Chapters
            </Link>
          </div>
        </section>
      </main>
    </Layout>
  );
}

export default RagChat;
