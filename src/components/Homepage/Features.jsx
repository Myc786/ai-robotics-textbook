import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';

const FeatureList = [
  {
    title: 'Physical AI Concepts',
    description: (
      <>
        <p>Physical AI refers to intelligent systems that interact with the physical world through sensors and actuators.</p>
        <p className="feature-preview">Key characteristics include perception using sensors to understand the environment, reasoning to process sensory information, action executing physical movements, and adaptation learning and adjusting to environmental changes.</p>
      </>
    ),
    buttonLabel: 'Explore Physical AI',
    to: '/docs/1-introduction-to-physical-ai',
  },
  {
    title: 'Humanoid Robotics',
    description: (
      <>
        <p>Humanoid robots are designed to resemble and mimic human appearance and behavior.</p>
        <p className="feature-preview">Key components include mechanical structure, actuation systems, sensor systems, control systems, and power systems. Actuators provide mechanical power for movement coordinated by control systems.</p>
      </>
    ),
    buttonLabel: 'Learn Robotics',
    to: '/docs/2-basics-of-humanoid-robotics',
  },
  {
    title: 'ROS 2 Fundamentals',
    description: (
      <>
        <p>ROS 2 (Robot Operating System 2) provides tools, libraries, and conventions for building robot applications.</p>
        <p className="feature-preview">Core concepts include nodes as basic computational elements, topics for data streams between nodes, and services for request-response communication between nodes.</p>
      </>
    ),
    buttonLabel: 'Get Started',
    to: '/docs/3-ros2-fundamentals',
  },
  {
    title: 'Digital Twin Simulation',
    description: (
      <>
        <p>Gazebo is used for simulation of robotic systems in realistic environments enabling the creation of digital twins.</p>
        <p className="feature-preview">Digital twins are virtual replicas of physical systems serving development, validation, training, debugging, and optimization purposes with accurate physics simulation and sensor modeling.</p>
      </>
    ),
    buttonLabel: 'Try Simulation',
    to: '/docs/4-digital-twin-simulation',
  },
  {
    title: 'Vision-Language-Action',
    description: (
      <>
        <p>Vision-Language-Action (VLA) systems integrate computer vision, language understanding, and action planning.</p>
        <p className="feature-preview">These systems combine computer vision for perceiving the environment, language understanding for processing commands, and action planning for executing physical responses in complex physical environments.</p>
      </>
    ),
    buttonLabel: 'Discover VLA',
    to: '/docs/5-vision-language-action-systems',
  },
  {
    title: 'Capstone Projects',
    description: (
      <>
        <p>Capstone project demonstrates integration of all concepts learned throughout the textbook.</p>
        <p className="feature-preview">The integrated AI-robot pipeline includes perception module for vision processing, understanding module for command interpretation, action module for execution, and multi-agent considerations for collaboration.</p>
      </>
    ),
    buttonLabel: 'View Projects',
    to: '/docs/6-capstone-simple-ai-robot-pipeline',
  },
];

function Feature({ title, description, buttonLabel, to }) {
  return (
    <div className={clsx('col col--4 margin-bottom--lg')}>
      <div className="card">
        <div className="card__body text--left padding--lg">
          <h3>{title}</h3>
          <div className="margin-top--sm">{description}</div>
        </div>
        <div className="card__footer text--center">
          <Link to={to} className="button button--lg">
            {buttonLabel}
          </Link>
        </div>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className="padding-vert--xl">
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}