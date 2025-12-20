# Quickstart Guide: RAG Chatbot Widget for Docusaurus Book

**Feature**: 006-rag-chatbot-docusaurus
**Created**: 2025-12-19
**Status**: Complete

## Prerequisites

- Docusaurus project already set up
- RAG backend API running and accessible
- Node.js and npm/yarn installed

## Installation Steps

### 1. Create the Component File
Create the chatbot component in the Docusaurus source directory:
```bash
mkdir -p src/components
touch src/components/BookChatbot.js
```

### 2. Component Implementation
Add the BookChatbot component code to src/components/BookChatbot.js with:
- Floating chat button in bottom-right corner
- Expandable chat window with message history
- Input field for questions
- Text selection detection functionality
- API communication with backend

### 3. Environment Configuration
Set the backend URL in your environment or configuration:
```bash
# In your .env file or environment
REACT_APP_BACKEND_URL=https://your-backend-url.com
```

### 4. Integrate into Layout
Add the component to your Docusaurus layout by including it in your theme or layout components.

## Usage Instructions

### Basic Usage
1. Visit any page in your Docusaurus book
2. Look for the floating chat button in the bottom-right corner
3. Click the button to open the chat window
4. Type your question in the input field and press Enter or click Send
5. View the response with source citations

### Text Selection Feature
1. Select any text on a book page
2. Look for the "Ask about this" button that appears near your selection
3. Click the button to send "Explain this selection: [selected text]" as a question
4. View the explanation with source citations

## Configuration Options

### Backend URL Configuration
The component supports multiple ways to configure the backend URL:

1. **Environment Variable**: Set `REACT_APP_BACKEND_URL` in your environment
2. **Props**: Pass `backendUrl` prop when using the component
3. **Relative Path**: Use a relative path if backend is hosted on the same domain

### Customization
- Adjust the widget's appearance by modifying the CSS styles
- Change the initial open state by setting `initialOpenState` prop
- Modify the text selection trigger delay if needed

## Testing

### Local Testing
1. Start your Docusaurus development server: `npm run start`
2. Navigate to any book page
3. Test the floating chat button functionality
4. Verify text selection detection works
5. Test sending questions and receiving responses
6. Verify source links are clickable and functional

### Cross-device Testing
1. Test on desktop browser (Chrome, Firefox, Safari)
2. Test on mobile devices (iOS Safari, Android Chrome)
3. Verify responsive design works properly
4. Test touch interactions on mobile devices

## Troubleshooting

### Common Issues

- **API requests failing**: Verify the backend URL is correctly configured and accessible
- **Text selection not working**: Check browser compatibility and any conflicting selection handlers
- **Widget not appearing**: Verify the component is properly included in the layout
- **Mobile responsiveness issues**: Check CSS media queries and viewport settings

### Debugging
- Check browser console for JavaScript errors
- Verify network requests to backend are successful
- Confirm the backend API is responding correctly
- Test the backend API independently with tools like Postman