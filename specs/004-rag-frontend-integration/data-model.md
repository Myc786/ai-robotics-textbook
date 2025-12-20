# Data Model: RAG Chatbot Frontend Integration

## Entities

### ChatMessage
**Description**: Represents a message in the chat interface
- **id**: String (required) - Unique identifier for the message
- **content**: String (required) - The text content of the message
- **sender**: String (required) - Either "user" or "bot"
- **timestamp**: Date (required) - When the message was created
- **sources**: Array[String] (optional) - Source URLs for bot responses

### UserQuestion
**Description**: Represents a question submitted by the user
- **question**: String (required) - The user's question text
- **selectedText**: String (optional) - Text that was selected when question was asked
- **timestamp**: Date (required) - When the question was submitted

### BackendResponse
**Description**: Represents the response from the backend API
- **answer**: String (required) - The answer text from the backend
- **sources**: Array[String] (required) - List of source URLs for the information
- **timestamp**: Date (required) - When the response was received

### ChatState
**Description**: Represents the current state of the chat interface
- **isOpen**: Boolean (required) - Whether the chat window is open or closed
- **isLoading**: Boolean (required) - Whether a response is currently being loaded
- **messages**: Array[ChatMessage] (required) - List of messages in the current chat
- **inputText**: String (required) - Current text in the input field

### SelectionContext
**Description**: Represents the context when user selects text
- **selectedText**: String (required) - The text that was selected by the user
- **position**: Object (required) - Coordinates for positioning the "Ask" button
- **timestamp**: Date (required) - When the selection occurred

## Relationships

- One `ChatState` contains multiple `ChatMessage` items
- One `UserQuestion` generates one `BackendResponse`
- One `SelectionContext` may lead to one `UserQuestion`
- Multiple `ChatMessage` items form a conversation thread

## Validation Rules

- `question` in `UserQuestion` must not be empty (unless from selected text)
- `answer` in `BackendResponse` must not be empty
- `sources` in `BackendResponse` must be an array of valid URLs
- `sender` in `ChatMessage` must be either "user" or "bot"
- `position` in `SelectionContext` must have x, y coordinates