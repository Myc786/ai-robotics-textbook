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

The integrated RAG chatbot is accessible at `/rag-chat`. It uses a semantic search-based approach to find relevant content in the textbook and generate contextually appropriate responses with source citations.

For the chatbot to work locally, you need to run both the frontend and backend:

### Development Setup

1. **Start the RAG backend server:**
   ```bash
   cd RAG-backend
   pip install -r requirements.txt
   python main.py
   ```
   The backend will be available at http://localhost:8000

2. **In a separate terminal, start the Docusaurus frontend:**
   ```bash
   npm start
   ```
   The frontend will be available at http://localhost:3000

3. **Access the chatbot:**
   Visit http://localhost:3000/rag-chat to use the RAG chatbot

### Production Deployment

When deployed to GitHub Pages, the backend must be hosted separately. For full functionality in production:

1. Deploy the RAG backend to a cloud service (Heroku, Render, VPS, etc.)
2. Update the backend URL in `src/components/Chatbot/index.js` to point to your deployed backend
3. Configure CORS settings to allow requests from your GitHub Pages domain

### API Documentation

The backend provides the following endpoints:
- `POST /api/v1/query` - Process a query against the textbook content
- `GET /health` - Check backend health status

Example query:
```json
{
  "query": "What is Physical AI?"
}
```

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
