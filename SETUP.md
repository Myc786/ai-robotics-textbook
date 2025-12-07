# Quick Setup Guide

This guide will help you get the Physical AI & Humanoid Robotics textbook project up and running quickly.

## Prerequisites

- Node.js (version 18 or higher)
- npm or yarn
- Python 3.8+
- pip (Python package manager)

## Frontend Setup (Docusaurus Documentation)

1. **Clone the repository**
   ```bash
   git clone https://github.com/Myc786/ai-robotics-textbook.git
   cd ai-robotics-textbook
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```

   The documentation website will be available at http://localhost:3000

## Backend Setup (RAG Chatbot)

1. **Navigate to the RAG backend directory**
   ```bash
   cd RAG-backend
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the RAG server**
   ```bash
   python main.py
   ```

   The RAG backend will be available at http://localhost:8000

## Running Both Together

For the complete experience with the chatbot functionality:

1. In one terminal, start the frontend:
   ```bash
   npm start
   ```

2. In another terminal, navigate to the RAG-backend directory and start the server:
   ```bash
   cd RAG-backend && python main.py
   ```

3. Access the frontend at http://localhost:3000 and use the RAG chatbot at the `/rag-chat` route.

## Common Commands

- `npm start` - Start the development server
- `npm run build` - Build the static website
- `npm run serve` - Serve the built website locally
- `npm run deploy` - Deploy to GitHub Pages

## Troubleshooting

### Frontend Issues
- If you get dependency errors, try running `npm install` again
- If the site doesn't load properly, try clearing the Docusaurus cache: `npm run clear`

### Backend Issues
- Make sure you're using Python 3.8+
- If dependencies fail to install, ensure you have the required system packages for psycopg2

## Next Steps

- Check out the [Textbook Content](./docs/) to understand the structure
- Review the [Contributing Guidelines](./CONTRIBUTING.md)
- Look at the [Architecture](#) section in the main README