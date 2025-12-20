# Agent Context: RAG Chatbot Widget for Docusaurus Book

**Feature**: 006-rag-chatbot-docusaurus
**Created**: 2025-12-19
**Technologies Added**: React, Docusaurus, Text Selection API, Fetch API

## Technology Stack

### React
- Component-based architecture for the chatbot widget
- Hooks for state management (useState, useEffect, useRef)
- JSX for UI rendering
- Props for configuration and communication

### Docusaurus
- Static site generator for the book documentation
- Theme customization for integrating the chat widget
- Layout components for consistent placement across pages
- Plugin system for extending functionality

### Browser APIs
- Selection API for detecting text selection
- DOM manipulation for positioning the "Ask about this" button
- Fetch API for communication with the backend
- Event listeners for user interactions

### CSS
- Flexbox and Grid for responsive layout
- Media queries for mobile responsiveness
- CSS positioning for floating widget
- Custom properties for theming

## Integration Pattern

The system follows a client-side integration pattern:
1. User interacts with Docusaurus book page
2. Text selection is detected using browser Selection API
3. "Ask about this" button appears near selection
4. Question is sent to backend via fetch API
5. Response with sources is displayed in chat widget
6. Source links allow navigation to referenced content