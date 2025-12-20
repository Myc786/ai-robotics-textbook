# Feature Specification: RAG Chatbot Widget for Docusaurus Book

**Feature Branch**: `006-rag-chatbot-docusaurus`
**Created**: 2025-12-19
**Status**: Draft
**Input**: User description: "Spec 4 - Embed RAG chatbot widget in Docusaurus book

- In Docusaurus project, create src/components/BookChatbot.js (or custom HTML/JS file)
- Build simple floating chat widget (bottom-right button → opens chat window)
- Add input field and message display area
- Implement send function: on submit, fetch POST to backend /chat with question
- Display streamed or final answer + clickable source links
- Add selected-text feature: detect text selection → show "Ask about this" button → send "Explain this selection: [selected text]" as question
- Include script in Docusaurus layout (e.g., via Custom.js in theme or plugin)
- Ensure backend URL is configurable (use relative or env-based)
- Update and deploy book to GitHub Pages
- Test live: ask general questions, selected-text questions, verify answers and sources on multiple pages
- Confirm widget works on desktop and mobile"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Access Chatbot Widget (Priority: P1)

A user browsing the Docusaurus book wants to ask questions about the content they're reading. They see a floating chat button in the bottom-right corner, click it to open the chat window, type their question, and receive an answer with source citations.

**Why this priority**: This is the core functionality that enables users to interact with the RAG system directly from the book pages.

**Independent Test**: Can be fully tested by opening the chat widget, submitting a question, and verifying the response with source links.

**Acceptance Scenarios**:

1. **Given** the user is on any book page, **When** they see the floating chat button and click it, **Then** a chat window opens with an input field and message display area
2. **Given** the chat window is open, **When** the user submits a question, **Then** the system sends the question to the backend and displays the response with source links
3. **Given** the user receives an answer, **When** they see the source links, **Then** they can click on them to navigate to the referenced content

---

### User Story 2 - Use Selected Text Feature (Priority: P2)

A user selects text on a book page and wants to get an explanation of that specific content. A "Ask about this" button appears near the selection, and clicking it sends the selected text as a question to the chatbot.

**Why this priority**: This enhances user experience by providing context-aware assistance based on the exact content they're reading.

**Independent Test**: Can be tested by selecting text on a page, verifying the "Ask about this" button appears, clicking it, and confirming the question is sent with the selected text.

**Acceptance Scenarios**:

1. **Given** the user selects text on a book page, **When** they see the "Ask about this" button appear, **Then** clicking it sends "Explain this selection: [selected text]" to the chatbot
2. **Given** the user has selected text, **When** they click the "Ask about this" button, **Then** the chat window opens (if not already open) and shows the generated question

---

### User Story 3 - Cross-Device Experience (Priority: P3)

A user accesses the book from different devices and expects the chatbot widget to work consistently across desktop and mobile platforms.

**Why this priority**: Ensures accessibility and usability across different user contexts and devices.

**Independent Test**: Can be tested by accessing the book on different devices and verifying the widget functions properly on each.

**Acceptance Scenarios**:

1. **Given** the user is on a desktop device, **When** they interact with the chat widget, **Then** it functions properly with appropriate positioning and sizing
2. **Given** the user is on a mobile device, **When** they interact with the chat widget, **Then** it functions properly with touch-friendly interface elements

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display a floating chat button in the bottom-right corner of book pages
- **FR-002**: System MUST open a chat window when the floating button is clicked
- **FR-003**: System MUST provide an input field for users to enter questions
- **FR-004**: System MUST provide a message display area to show conversation history
- **FR-005**: System MUST send questions to the backend /chat endpoint via POST request
- **FR-006**: System MUST display answers from the backend with clickable source links
- **FR-007**: System MUST detect text selection on book pages
- **FR-008**: System MUST display an "Ask about this" button when text is selected
- **FR-009**: System MUST send "Explain this selection: [selected text]" as a question when the "Ask about this" button is clicked
- **FR-010**: System MUST have a configurable backend URL that can be set via environment or relative path
- **FR-011**: System MUST be integrated into the Docusaurus layout to appear on all book pages
- **FR-012**: System MUST be responsive and work on both desktop and mobile devices

### Key Entities

- **Chat Message**: A message in the conversation, either from the user (question) or the system (answer with sources)
- **Floating Widget**: The UI component that contains the chat button and window
- **Text Selection**: The portion of text selected by the user on a book page
- **Backend URL**: The configurable endpoint for the RAG backend API

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can open the chat widget and submit questions within 2 seconds of page load
- **SC-002**: 95% of questions result in successful responses with source citations within 10 seconds
- **SC-003**: Text selection detection works on 90% of different browsers and devices
- **SC-004**: The "Ask about this" button appears within 0.5 seconds of text selection
- **SC-005**: The widget is accessible and functional on both desktop and mobile devices
- **SC-006**: Backend URL can be configured without code changes
- **SC-007**: Widget does not interfere with page readability or performance