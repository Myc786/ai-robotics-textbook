# Frontend Integration Guide for RAG Chatbot

## Overview
This guide explains how to integrate the RAG Chatbot backend with your existing frontend application at https://myapp-beta-eight.vercel.app/.

## Prerequisites
- Your backend must be deployed and accessible via HTTPS
- CORS must be properly configured on the backend
- API keys must be properly set up on the backend

## Step 1: Environment Configuration

1. Create a `.env.local` file in your frontend project root (if using Next.js):
```env
NEXT_PUBLIC_RAG_BACKEND_URL=https://your-deployed-backend-url.com
```

2. Replace `https://your-deployed-backend-url.com` with the actual URL of your deployed backend.

## Step 2: Install Required Dependencies

If your frontend is a React/Next.js application, you likely already have the necessary dependencies. If not:

```bash
npm install
```

## Step 3: Add the API Client

Copy the `api/rag-api.js` file to your frontend project's API folder (e.g., `lib/api/` or `services/`).

Update the base URL in the client to use your environment variable:

```javascript
const ragApiClient = new RAGApiClient(process.env.NEXT_PUBLIC_RAG_BACKEND_URL || 'https://your-backend-url.com');
```

## Step 4: Add Components

1. Copy the components (`RAGChat.jsx`, `DocumentUpload.jsx`) to your components folder
2. Copy the CSS file (`rag-chat.css`) to your styles folder
3. Import and use the components in your pages

## Step 5: Basic Integration Example

Here's how to integrate the chat component into an existing page:

```jsx
import RAGChat from '../components/RAGChat';

function YourPage() {
  return (
    <div>
      <h1>Your Existing Content</h1>
      {/* Your existing content */}

      <div style={{ marginTop: '2rem' }}>
        <h2>Ask Questions About the Book</h2>
        <RAGChat />
      </div>
    </div>
  );
}

export default YourPage;
```

## Step 6: Advanced Integration Options

### With Document Context
If you want to provide document context:

```jsx
<RAGChat documentId="specific-document-id" />
```

### With Custom Styling
The components come with default styling, but you can override styles by targeting the CSS classes:
- `.rag-chat-container`
- `.message.user-message`
- `.message.bot-message`
- `.chat-input-form`

## Step 7: Testing the Integration

1. Make sure your backend is deployed and accessible
2. Verify the health endpoint: `GET /health`
3. Test the chat endpoint with a simple query
4. Check browser console for any CORS or network errors

## Common Issues and Solutions

### CORS Errors
- Ensure your backend has the correct `ALLOWED_ORIGINS` setting
- For development, you can temporarily set it to `["*"]`
- For production, specify your exact frontend domain

### Network Errors
- Verify the backend URL is correct
- Check that the backend is deployed and running
- Ensure your frontend and backend protocols match (both HTTP or both HTTPS)

### Authentication
The current implementation doesn't require authentication, but you can add it by:
1. Adding authentication headers in the API client
2. Implementing authentication middleware on the backend

## API Endpoints Used

The frontend integration uses these backend endpoints:
- `POST /api/v1/chat` - For chat queries
- `POST /api/v1/documents` - For text document uploads
- `POST /api/v1/documents/file` - For file uploads
- `GET /api/v1/health` - For health checks

## Deployment Notes

When deploying your frontend with the integration:
1. Ensure the `NEXT_PUBLIC_RAG_BACKEND_URL` environment variable is set correctly for each environment
2. Test the integration in your staging environment before production
3. Monitor API response times and implement loading states appropriately

## Security Considerations

1. Never expose backend API keys in frontend code
2. Use environment variables for backend URLs
3. Implement rate limiting on the backend to prevent abuse
4. Validate and sanitize all user inputs on the frontend

## Performance Optimization

1. Implement loading states for better UX
2. Consider implementing caching for frequently asked questions
3. Use virtualization for long message histories
4. Optimize API calls to reduce unnecessary requests

## Support and Troubleshooting

If you encounter issues:
1. Check browser developer tools for console errors
2. Verify the backend is accessible and responding
3. Confirm all environment variables are correctly set
4. Review the backend logs for any server-side errors

For further assistance, refer to the backend documentation at [DEPLOYMENT.md](../DEPLOYMENT.md).