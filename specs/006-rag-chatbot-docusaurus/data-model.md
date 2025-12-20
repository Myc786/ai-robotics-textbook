# Data Model: RAG Chatbot Widget for Docusaurus Book

**Feature**: 006-rag-chatbot-docusaurus
**Created**: 2025-12-19
**Status**: Complete

## Core Entities

### ChatMessage
- **Description**: Represents a single message in the chat conversation
- **Fields**:
  - `id` (string): Unique identifier for the message
  - `text` (string): The content of the message
  - `sender` (string): Either "user" or "bot"
  - `timestamp` (Date): When the message was created
  - `sources` (array of strings): Source URLs for bot responses (optional)
- **Validation**:
  - `id` is required and must be unique
  - `text` is required and must be non-empty
  - `sender` must be either "user" or "bot"
  - `timestamp` is required
  - `sources` is optional but if present must be an array of valid URLs

### ChatState
- **Description**: Represents the current state of the chat interface
- **Fields**:
  - `messages` (array of ChatMessage): The conversation history
  - `isLoading` (boolean): Whether the bot is processing a response
  - `isWidgetOpen` (boolean): Whether the chat widget is open
  - `backendUrl` (string): The URL of the backend API
- **Validation**:
  - `messages` is required and must be an array
  - `isLoading` is required and must be boolean
  - `isWidgetOpen` is required and must be boolean
  - `backendUrl` is required and must be a valid URL

### TextSelection
- **Description**: Represents a user's text selection on the page
- **Fields**:
  - `text` (string): The selected text content
  - `position` (object): Coordinates for positioning the "Ask about this" button
    - `x` (number): X coordinate
    - `y` (number): Y coordinate
  - `isVisible` (boolean): Whether the "Ask about this" button should be visible
- **Validation**:
  - `text` is required and must be non-empty
  - `position` is required with both `x` and `y` as numbers
  - `isVisible` is required and must be boolean

### APIRequest
- **Description**: Represents a request to the backend API
- **Fields**:
  - `question` (string): The question to be sent to the backend
- **Validation**:
  - `question` is required and must be non-empty

### APIResponse
- **Description**: Represents a response from the backend API
- **Fields**:
  - `answer` (string): The answer from the backend
  - `sources` (array of strings): Source URLs for the answer
- **Validation**:
  - `answer` is required and must be non-empty
  - `sources` is required and must be an array of valid URLs

## State Transitions

### Chat Widget Flow
1. **Closed**: Widget is hidden, only the floating button is visible
2. **Opening**: User clicks the floating button
3. **Open**: Chat window is displayed with input field and message area
4. **Sending**: User submits a question
5. **Processing**: Waiting for backend response
6. **Response**: Answer is displayed with sources
7. **Closed**: User closes the widget

### Text Selection Flow
1. **Idle**: No text is selected
2. **Selecting**: User is in the process of selecting text
3. **Selected**: Text is selected, "Ask about this" button appears
4. **Asking**: User clicks the "Ask about this" button
5. **Question Sent**: The selected text is sent as a question

## Relationships

- A `ChatState` contains multiple `ChatMessage` entities
- A `TextSelection` is independent but can trigger the creation of a `ChatMessage` when "Ask about this" is used
- An `APIRequest` is created from user input or selected text
- An `APIResponse` creates a bot `ChatMessage` with sources