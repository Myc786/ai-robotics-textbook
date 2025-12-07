# Feature Tasks: Textbook Generation Project

## Objective
Generate atomic, traceable, and testable tasks for the Physical AI & Humanoid Robotics textbook project, ensuring clear dependencies, acceptance criteria, and verifiable outputs for each phase.

## Phase 1: Core Book Structure
*   **[X] 1.1 Initialize Docusaurus project**
    *   Duration: 15–20 min
    *   Dependencies: None
    *   Acceptance Criterion: Docusaurus project successfully initialized, `docusaurus.config.js` is configured, Initial Docusaurus site runs without errors.
    *   Output: Docusaurus project files (e.g., `docusaurus.config.js`, `package.json`, `src/`)
    *   Spec Link: `specs/textbook-generation/spec.md`

*   **[X] 1.2 Create Docusaurus config files**
    *   Duration: 10-15 min
    *   Dependencies: 1.1
    *   Acceptance Criterion: `docusaurus.config.js`, `sidebars.js`, and `package.json` are created and correctly configured for basic Docusaurus operation.
    *   Output: `docusaurus.config.js`, `sidebars.js`, `package.json`
    *   Spec Link: `specs/textbook-generation/spec.md`

*   **[X] 1.3 Create empty chapter markdown files**
    *   Duration: 5-10 min
    *   Dependencies: 1.1
    *   Acceptance Criterion: All 6 chapter markdown files (e.g., `docs/1-introduction-to-physical-ai.md`) are created with placeholder content.
    *   Output: Chapter markdown files in `docs/`
    *   Spec Link: `specs/textbook-generation/spec.md`

*   **[X] 1.4 Create deployment workflow (.github/workflows/deploy.yml)**
    *   Duration: 10-15 min
    *   Dependencies: None
    *   Acceptance Criterion: GitHub Actions workflow for GitHub Pages deployment is created and correctly configured.
    *   Output: `.github/workflows/deploy.yml`
    *   Spec Link: `specs/textbook-generation/spec.md`

*   **[X] 1.5 Create `README.md` and `.gitignore`**
    *   Duration: 5-10 min
    *   Dependencies: None
    *   Acceptance Criterion: `README.md` and `.gitignore` files are created with basic content.
    *   Output: `README.md`, `.gitignore`
    *   Spec Link: `specs/textbook-generation/spec.md`

*   **[X] 1.6 Create placeholder bonus feature files**
    *   Duration: 5-10 min
    *   Dependencies: None
    *   Acceptance Criterion: Placeholder files for auth, personalization, and Urdu translation are created in `src/`.
    *   Output: `src/_bonus_auth.js`, `src/_bonus_personalization.js`, `src/_bonus_urdu.js`
    *   Spec Link: `specs/textbook-generation/spec.md`

*   **[X] 1.7 Add 3-5 runnable Python code snippets per chapter**
    *   Duration: Varies per chapter (placeholder)
    *   Dependencies: Chapter content available
    *   Acceptance Criterion: Each chapter contains 3-5 verified runnable Python code snippets.
    *   Output: Updated chapter markdown files
    *   Spec Link: `specs/textbook-generation/spec.md`

*   **[X] 1.8 Add 1-2 small programming exercises per chapter**
    *   Duration: Varies per chapter (placeholder)
    *   Dependencies: Chapter content available
    *   Acceptance Criterion: Each chapter contains 1-2 small programming exercises.
    *   Output: Updated chapter markdown files
    *   Spec Link: `specs/textbook-generation/spec.md

**Checkpoint:** Human review of core book structure and initial content.

## Phase 2: RAG Integration
*   **2.1 Set up Qdrant instance and collection**
    *   Duration: 15-20 min
    *   Dependencies: None
    *   Acceptance Criterion: Qdrant instance is running, and a collection for textbook embeddings is created.
    *   Output: Qdrant connection details, collection name
    *   Spec Link: `specs/textbook-generation/plan.md`

*   **2.2 Set up Neon (Postgres) instance and schema**
    *   Duration: 15-20 min
    *   Dependencies: None
    *   Acceptance Criterion: Neon Postgres instance is running, and a schema for textbook metadata is defined.
    *   Output: Neon connection string, database schema
    *   Spec Link: `specs/textbook-generation/plan.md`

*   **2.3 Develop FastAPI RAG backend (initial skeleton)**
    *   Duration: 30-45 min
    *   Dependencies: 2.1, 2.2
    *   Acceptance Criterion: A basic FastAPI application is set up with a `/query` endpoint.
    *   Output: `RAG-backend/main.py`, `RAG-backend/requirements.txt`
    *   Spec Link: `specs/textbook-generation/plan.md`

*   **2.4 Implement text chunking and embedding generation**
    *   Duration: 45-60 min
    *   Dependencies: 2.3, Embedding Provider API access
    *   Acceptance Criterion: A script can chunk markdown files and generate embeddings using a free-tier provider.
    *   Output: Embedding generation script
    *   Spec Link: `specs/textbook-generation/plan.md`

*   **2.5 Implement initial data ingestion script (to Qdrant and Neon)**
    *   Duration: 45-60 min
    *   Dependencies: 2.1, 2.2, 2.4
    *   Acceptance Criterion: The script successfully ingests chunked textbook content and embeddings into Qdrant and metadata into Neon.
    *   Output: Data ingestion script
    *   Spec Link: `specs/textbook-generation/plan.md`

*   **2.6 Integrate RAG chatbot frontend into Docusaurus**
    *   Duration: 60-90 min
    *   Dependencies: 2.3 (working `/query` endpoint), Docusaurus frontend
    *   Acceptance Criterion: A chatbot UI component is integrated into Docusaurus, sending queries to the FastAPI backend and displaying responses/sources.
    *   Output: Docusaurus React component for chatbot
    *   Spec Link: `specs/textbook-generation/plan.md`

**Checkpoint:** Human review of RAG integration and initial chatbot functionality.

## Phase 3: Bonuses (Placeholders)
*   **3.1 Conceptualize Authentication Layer**
    *   Duration: 15-20 min
    *   Dependencies: N/A (conceptual)
    *   Acceptance Criterion: A high-level design for a future authentication layer is outlined.
    *   Output: Design document (internal)
    *   Spec Link: `specs/textbook-generation/spec.md`

*   **3.2 Conceptualize Personalization Module**
    *   Duration: 15-20 min
    *   Dependencies: N/A (conceptual)
    *   Acceptance Criterion: A high-level design for a future personalization module is outlined.
    *   Output: Design document (internal)
    *   Spec Link: `specs/textbook-generation/spec.md`

*   **3.3 Conceptualize Urdu Translation Module**
    *   Duration: 15-20 min
    *   Dependencies: N/A (conceptual)
    *   Acceptance Criterion: A high-level design for a future Urdu translation module is outlined, specifically addressing code block handling.
    *   Output: Design document (internal)
    *   Spec Link: `specs/textbook-generation/spec.md`

**Checkpoint:** Human review of RAG and bonuses.

## Phase 4: Testing & Deploy
*   **4.1 Validate RAG accuracy (≥90% on 20 queries)**
    *   Duration: 15–20 min
    *   Dependencies: Phase 2 complete, RAG backend operational
    *   Acceptance Criterion: Accuracy ≥90% on a predefined set of 20 test queries. Responses are strictly grounded.
    *   Output: Test report
    *   Spec Link: `specs/textbook-generation/plan.md`

*   **4.2 Accessibility check & GitHub Pages deploy**
    *   Duration: 15–20 min
    *   Dependencies: 4.1 complete, Docusaurus build successful
    *   Acceptance Criterion: Docusaurus site builds successfully, is deployed to GitHub Pages, and passes basic accessibility checks (e.g., Lighthouse audit).
    *   Output: Live GitHub Pages URL
    *   Spec Link: `specs/textbook-generation/spec.md`

**Checkpoint:** Final review, commit, and project ready for release.
