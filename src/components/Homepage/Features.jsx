import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';

const FeatureList = [
  {
    title: 'Physical AI Concepts',
    description: (
      <>
        Learn about intelligent systems that interact with the physical world through sensors and actuators.
      </>
    ),
    buttonLabel: 'Explore Physical AI',
    to: '/docs/1-introduction-to-physical-ai',
  },
  {
    title: 'Humanoid Robotics',
    description: (
      <>
        Understand how humanoid robots move using actuators and control systems for coordinated motions.
      </>
    ),
    buttonLabel: 'Learn Robotics',
    to: '/docs/2-basics-of-humanoid-robotics',
  },
  {
    title: 'ROS 2 Fundamentals',
    description: (
      <>
        Master ROS 2 nodes, topics, and services for effective robot communication and control.
      </>
    ),
    buttonLabel: 'Get Started',
    to: '/docs/3-ros2-fundamentals',
  },
  {
    title: 'Vision-Language-Action',
    description: (
      <>
        Explore how computer vision, language understanding, and action planning integrate for intelligent systems.
      </>
    ),
    buttonLabel: 'Discover VLA',
    to: '/docs/5-vision-language-action-systems',
  },
  {
    title: 'Digital Twin Simulation',
    description: (
      <>
        Experience Gazebo simulation for robotic systems and creating digital twins of physical environments.
      </>
    ),
    buttonLabel: 'Try Simulation',
    to: '/docs/4-digital-twin-simulation',
  },
  {
    title: 'Capstone Projects',
    description: (
      <>
        Integrate learned concepts into comprehensive systems with multi-agent demonstrations.
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
        <div className="card__body text--center padding--lg">
          <h3>{title}</h3>
          <p className="margin-top--sm">{description}</p>
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