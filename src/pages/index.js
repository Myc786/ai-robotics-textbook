import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '../components/Homepage/Features';

import { useColorMode } from '@docusaurus/theme-common';

import Heading from '@theme/Heading';

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  const { colorMode } = useColorMode();
  const isDarkMode = colorMode === 'dark';

  return (
    <header className={clsx('hero', { 'hero--dark': isDarkMode })}>
      <div className="container text--center padding-horiz--md">
        <div className="margin-bottom--lg">
          <div className="avatar avatar--lg">
            <img src="/img/logo.svg" alt="AI/Robotics Logo" className="w-16 h-16 mx-auto" />
          </div>
        </div>

        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>

        <p className="hero__subtitle margin-top--md">
          {siteConfig.tagline}
        </p>

        <div className="margin-top--lg">
          <Link
            className="button button--lg button--primary"
            to="/docs/intro">
            Get Started with Textbook
          </Link>

          <Link
            className="button button--lg button--secondary margin-left--md"
            to="/rag-chat">
            Try RAG Chatbot
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const { siteConfig } = useDocusaurusContext();
  React.useEffect(() => {
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = (y - centerY) / 20; 
        const rotateY = (x - centerX) / -20; 

        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
      });
    });
  }, []);

  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="AI-Native Textbook for Physical AI and Robotics">

      <HomepageHeader />

      <main>
        <div className="container margin-vert--xl">
          <div className="text--center padding-horiz--md">
            <h2>Comprehensive Learning Modules</h2>
            <p className="text-lg max-w-3xl mx-auto mt-4">
              Master the fundamentals of Physical AI, Humanoid Robotics, ROS 2, Digital Twin Simulation,
              Vision-Language-Action systems, and complete capstone projects.
            </p>
          </div>
        </div>

        <section className="padding-vert--lg">
          <div className="container">
            <div className="row">
              <div className="col col--3">
                <div className="text--center padding-horiz--md">
                  <h2 className="hero__title">6</h2>
                  <p className="text-lg">Comprehensive Chapters</p>
                </div>
              </div>
              <div className="col col--3">
                <div className="text--center padding-horiz--md">
                  <h2 className="hero__title">20+</h2>
                  <p className="text-lg">Code Examples</p>
                </div>
              </div>
              <div className="col col--3">
                <div className="text--center padding-horiz--md">
                  <h2 className="hero__title">50+</h2>
                  <p className="text-lg">Exercises & Projects</p>
                </div>
              </div>
              <div className="col col--3">
                <div className="text--center padding-horiz--md">
                  <h2 className="hero__title">AI</h2>
                  <p className="text-lg">Powered Q&A System</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <HomepageFeatures />

        <div className="container margin-vert--xl">
          <div className="row">
            <div className="col col--4 col--offset-2">
              <div className="card">
                <h3>Interactive Learning</h3>
                <p>
                  Engage with the RAG Chatbot to ask questions and get personalized responses based on the textbook content.
                </p>
              </div>
            </div>

            <div className="col col--4">
              <div className="card">
                <h3>Practical Applications</h3>
                <p>
                  Apply concepts through hands-on exercises and capstone projects that integrate multiple AI and robotics concepts.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}