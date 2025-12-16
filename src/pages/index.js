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

// Chapter data
const chapters = [
  {
    id: 1,
    title: "Introduction to Physical AI",
    description: "Understanding intelligent systems that interact with the physical world through sensors and actuators",
    icon: "🤖",
    link: "/docs/introduction-to-physical-ai"
  },
  {
    id: 2,
    title: "Basics of Humanoid Robotics",
    description: "How humanoid robots achieve coordinated movement and control systems",
    icon: "🦾",
    link: "/docs/basics-of-humanoid-robotics"
  },
  {
    id: 3,
    title: "ROS2 Fundamentals",
    description: "Robot communication and control using ROS 2 nodes, topics, and services",
    icon: "📡",
    link: "/docs/ros2-fundamentals"
  },
  {
    id: 4,
    title: "Digital Twin Simulation",
    description: "Gazebo simulation and digital twin technologies for robot development",
    icon: "🎮",
    link: "/docs/digital-twin-simulation"
  },
  {
    id: 5,
    title: "Vision-Language-Action Systems",
    description: "Integration of perception, language processing, and action execution",
    icon: "👁️",
    link: "/docs/vision-language-action-systems"
  },
  {
    id: 6,
    title: "Capstone: Simple AI Robot Pipeline",
    description: "Bringing all concepts together in a comprehensive project",
    icon: "🏁",
    link: "/docs/capstone-simple-ai-robot-pipeline"
  },
  {
    id: 7,
    title: "Advanced Control Systems",
    description: "Modern control methodologies for precise and adaptive robot behavior",
    icon: "⚙️",
    link: "/docs/advanced-control-systems"
  },
  {
    id: 8,
    title: "Machine Learning for Robotics",
    description: "AI techniques applied to perception, control, planning, and decision-making",
    icon: "🧠",
    link: "/docs/machine-learning-for-robotics"
  },
  {
    id: 9,
    title: "Sensor Fusion and Perception",
    description: "Combining multiple sensors to create coherent environmental understanding",
    icon: "📡",
    link: "/docs/sensor-fusion-and-perception"
  },
  {
    id: 10,
    title: "Human-Robot Interaction",
    description: "Designing effective and intuitive human-robot collaboration systems",
    icon: "🤝",
    link: "/docs/human-robot-interaction"
  },
  {
    id: 11,
    title: "Robot Ethics and Safety",
    description: "Ethical considerations and safety measures in robotic systems",
    icon: "⚖️",
    link: "/docs/robot-ethics-and-safety"
  },
  {
    id: 12,
    title: "Cloud Robotics and Edge Computing",
    description: "Leveraging cloud and edge computing for enhanced robotic capabilities",
    icon: "☁️",
    link: "/docs/cloud-robotics-and-edge-computing"
  },
  {
    id: 13,
    title: "Robotic Simulation and Digital Twins",
    description: "Advanced simulation and digital twin technologies for robot development",
    icon: "🔮",
    link: "/docs/robotic-simulation-and-digital-twins"
  }
];

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
                  <h2 className="hero__title">13</h2>
                  <p className="text-lg">Comprehensive Chapters</p>
                </div>
              </div>
              <div className="col col--3">
                <div className="text--center padding-horiz--md">
                  <h2 className="hero__title">30+</h2>
                  <p className="text-lg">Code Examples</p>
                </div>
              </div>
              <div className="col col--3">
                <div className="text--center padding-horiz--md">
                  <h2 className="hero__title">75+</h2>
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

        <section className="padding-vert--lg">
          <div className="container">
            <div className="text--center margin-bottom--xl">
              <h2>Explore All Chapters</h2>
              <p className="text-lg max-w-3xl mx-auto">
                Dive deep into each topic with comprehensive learning modules
              </p>
            </div>
            <div className="row">
              {chapters.map((chapter) => (
                <div className="col col--4 margin-bottom--lg" key={chapter.id}>
                  <Link to={chapter.link} className="card">
                    <div className="card__header">
                      <h3 className="text--center">{chapter.icon} {chapter.title}</h3>
                    </div>
                    <div className="card__body">
                      <p>{chapter.description}</p>
                    </div>
                    <div className="card__footer text--center">
                      <span className="button button--secondary button--sm" style={{ pointerEvents: 'none' }}>
                        Explore Chapter
                      </span>
                    </div>
                  </Link>
                </div>
              ))}
            </div>
          </div>
        </section>

        <HomepageFeatures />

        <div className="container margin-vert--xl">
          <div className="row">
            <div className="col col--4 col--offset-2">
              <Link to="/rag-chat" className="card">
                <div className="card__body text--center padding--lg">
                  <h3>Interactive Learning</h3>
                  <p>
                    Engage with the RAG Chatbot to ask questions and get personalized responses based on the textbook content.
                  </p>
                </div>
              </Link>
            </div>

            <div className="col col--4">
              <Link to="/docs/capstone-simple-ai-robot-pipeline" className="card">
                <div className="card__body text--center padding--lg">
                  <h3>Practical Applications</h3>
                  <p>
                    Apply concepts through hands-on exercises and capstone projects that integrate multiple AI and robotics concepts.
                  </p>
                </div>
              </Link>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}