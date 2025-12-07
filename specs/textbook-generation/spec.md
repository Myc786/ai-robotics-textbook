# Feature Specification: Textbook Generation (Clarified)

## Objective
Define a complete, unambiguous specification for building the AI-native textbook with RAG chatbot that is interactive, deployable, and extensible.

## Book Structure
1.  **Introduction to Physical AI**
    *   Overview of Physical AI concepts
    *   Key applications and examples
    *   Historical perspective and emerging trends

2.  **Basics of Humanoid Robotics**
    *   Anatomy of humanoid robots
    *   Sensors and actuators
    *   Control systems overview

3.  **ROS 2 Fundamentals**
    *   ROS 2 installation and setup
    *   Nodes, topics, and services
    *   Basic robot control and simulation

4.  **Digital Twin Simulation (Gazebo + Isaac)**
    *   Gazebo environment setup
    *   Isaac Sim integration
    *   Building and testing digital twins

5.  **Vision-Language-Action Systems**
    *   Computer vision basics for robots
    *   Language understanding and command parsing
    *   Action planning and execution

6.  **Capstone: Simple AI-Robot Pipeline**
    *   Integrating learned concepts into a small project
    *   Multi-agent and physical AI demonstrations
    *   Evaluation and best practices

## Technical Requirements (Clarified)
*   Docusaurus v3 with auto-generated sidebar for chapters
*   RAG backend using Qdrant vector DB + Neon API
*   Free-tier embeddings (e.g., OpenAI/Claude embeddings)
*   Full GitHub Pages deployable configuration
*   Placeholder assets folder for images, diagrams, and media
*   Placeholder pages for bonus features: auth, personalization, Urdu translation

## Clarification Focus and Identified Issues

### 1. Ambiguous Terms: "interactive elements"
*   **Original:** "AI-native textbook with RAG chatbot that is interactive..."
*   **Clarification (CRITICAL):**
    *   **Code Snippets:** Each chapter will include 3-5 runnable Python code snippets, directly executable by the reader (e.g., using a local setup).
    *   **Quizzes:** No formal quiz system is required for the initial release. "Interactive" refers primarily to the RAG chatbot and runnable code.
    *   **Exercises:** Each chapter will include 1-2 small programming exercises. Solutions will not be provided directly in the text.

### 2. Missing Assumptions
*   **Target reader prerequisites (CRITICAL):**
    *   Readers are assumed to have basic programming knowledge (Python) and familiarity with command-line interfaces.
    *   No prior robotics, AI, or Docusaurus experience is assumed.
*   **Simulation hardware requirements (CRITICAL):**
    *   All simulations (Gazebo, Isaac Sim) must be runnable on a typical laptop (>=8GB RAM, ideally no dedicated GPU required).
    *   Environment setup instructions for Linux, Windows (via WSL2), and macOS will be provided.
*   **Deployment assumptions (CRITICAL):**
    *   GitHub Pages free tier implies no server-side computation or persistent storage for the Docusaurus site itself. The RAG backend will be hosted separately (e.g., on Neon/Qdrant free tiers).
    *   The deployment workflow will handle building the Docusaurus site and pushing it to `gh-pages`.
*   **Bonus feature integration (NICE-TO-HAVE for initial spec, CRITICAL for future planning):**
    *   If personalization is enabled, the RAG system *should* consider user interaction history or preferences. This is a future consideration, not part of the initial specification.

### 3. Incomplete Requirements
*   **RAG chatbot edge cases (CRITICAL):**
    *   **Off-topic queries:** The RAG chatbot must be strictly grounded in the textbook content. Off-topic queries will result in a response stating inability to answer based on provided content.
    *   **Urdu translation handling in code blocks:** If Urdu translation is enabled, code blocks must *not* be translated.
*   **Capstone project simulation tools for VLA module (CRITICAL):**
    *   The Capstone project will primarily utilize Gazebo for robot simulation, demonstrating integration with the VLA system. Isaac Sim will not be the primary tool for the Capstone to maintain simplicity.

### 4. Scope Conflicts
*   **Simulation-only vs. real hardware guidance (CRITICAL):**
    *   The textbook is "Simulation-first." All examples and exercises will be designed for simulation environments. Mentions of real hardware will be conceptual only.
*   **Optional bonuses should not overlap with base requirements causing delays (CRITICAL):**
    *   "Optional Features" (Urdu translation, personalization) are strictly out of scope for the *initial* specification. No implementation or integration work is planned for the first release.

## Output Artifacts Created (No Changes)
*   **Folder Structure:** `docs/`, `src/`, `assets/`, `RAG-backend/`, `specs/textbook-generation/`
*   **Chapter Files:** Empty markdown files for each of the 6 chapters in `docs/`.
*   **Config Files:** `docusaurus.config.js`, `sidebars.js`, `package.json`.
*   **Deployment Workflow:** `.github/workflows/deploy.yml` for GitHub Pages.
*   **Root Files:** `README.md`, `.gitignore`.
*   **Placeholder Bonus Files:** `src/_bonus_auth.js`, `src/_bonus_personalization.js`, `src/_bonus_urdu.js`.
