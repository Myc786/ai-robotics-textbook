# Quickstart: RAG Chatbot Frontend Integration

## Setup

### Frontend Integration
1. **Add the Chatbot Script**
   Copy the `book-chatbot.js` file to your Docusaurus project's `static/js/` directory.

2. **Include in Docusaurus Configuration**
   Add the script to your `docusaurus.config.js`:
   ```js
   module.exports = {
     // ... other config
     scripts: [
       '/js/book-chatbot.js',
     ],
     // ... rest of config
   };
   ```

3. **Configure Backend URL**
   Update the backend API URL in the chatbot script to point to your running FastAPI server.

### Backend Setup
1. **Enable CORS in FastAPI**
   In your `main.py`, add the CORSMiddleware:
   ```python
   from fastapi.middleware.cors import CORSMiddleware

   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://your-github-pages-url.github.io"],  # Update with your URL
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Run the Backend Server**
   ```bash
   uvicorn main:app --reload
   ```

## Usage

### Chat Widget
- The floating chat button appears in the bottom-right corner of every page
- Click the button to open the chat interface
- Type your question in the input field and press Enter or click Send
- Answers appear with clickable source links

### Selected Text Feature
- Highlight any text on the page
- A floating "Ask about this" button will appear near your selection
- Click the button to pre-fill the question field with the selected text
- Modify the question if needed and submit

## Testing

Test the integration with these scenarios:
1. Basic question: Ask a simple question about book content
2. Selected text: Highlight text and ask about it
3. Source links: Click on source links to verify they work
4. Mobile: Test on different screen sizes
5. Error handling: Test with offline backend to verify error messages

## Validation

The system validates functionality by ensuring:
- Chat widget appears on all pages
- Questions are sent to backend and answers received
- Source links are clickable and point to correct locations
- Selected text feature works properly
- Responsive design works on mobile and desktop