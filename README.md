# Physical AI & Humanoid Robotics — Essentials

[![Deploy to GitHub Pages](https://github.com/Myc786/ai-robotics-textbook/actions/workflows/deploy.yml/badge.svg)](https://github.com/Myc786/ai-robotics-textbook/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the AI-native textbook for Physical AI and Humanoid Robotics, built with Docusaurus. The project features an integrated RAG (Retrieval-Augmented Generation) chatbot that allows users to ask questions about the textbook content.

## 🚀 Features

- Interactive textbook with 6 comprehensive chapters
- Integrated RAG chatbot for Q&A functionality
- Modern documentation with code examples and exercises
- GitHub Pages deployment with automated builds

## 📚 Table of Contents

- [About](#about)
- [Development](#development)
- [Textbook Content](#textbook-content)
- [RAG Chatbot](#rag-chatbot)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## About

This AI-native textbook combines traditional educational content with modern AI capabilities. Students can read the textbook or interact with the RAG chatbot to get answers to their questions based on the textbook content.

## Development

To start the local development server:

```bash
npm install
npm start
```

To build the static website:

```bash
npm run build
```

To run the RAG backend server:

```bash
cd RAG-backend
pip install -r requirements.txt
python main.py
```

## Textbook Content

The textbook covers these key areas:

1. Introduction to Physical AI
2. Basics of Humanoid Robotics
3. ROS2 Fundamentals
4. Digital Twin Simulation
5. Vision-Language-Action Systems
6. Capstone: Simple AI Robot Pipeline

## RAG Chatbot

The integrated RAG chatbot is accessible at `/rag-chat`. It uses a simple search-based approach to find relevant content in the textbook and generate contextually appropriate responses.

For the chatbot to work locally, make sure to run both:
- Frontend: `npm start` (runs on http://localhost:3000)
- Backend: `cd RAG-backend && python main.py` (runs on http://localhost:8000)

## Deployment

This site is configured for deployment to GitHub Pages using GitHub Actions. On every push to the `main` branch, the site is automatically built and deployed.

The deployment URL follows this pattern: `https://Myc786.github.io/ai-robotics-textbook/`

To configure GitHub Pages for your repository:
1. Go to your repository Settings → Pages
2. Select source as "GitHub Actions"

## Contributing

We welcome contributions! Here are some ways you can contribute:

1. Report issues in the [Issues](https://github.com/Myc786/ai-robotics-textbook/issues) section
2. Fork the repository and submit pull requests
3. Improve textbook content or add new chapters
4. Enhance the RAG chatbot functionality
5. Suggest new features

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Maintainers

- [Myc786](https://github.com/Myc786) - Project Lead

## Acknowledgments

Built with [Docusaurus](https://docusaurus.io/), an excellent static site generator for documentation.
