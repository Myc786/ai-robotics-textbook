# Feature Tasks: Textbook Generation Project - Production Deployment

## Objective
Prepare full production deployment for frontend (Docusaurus) and backend (RAG chatbot).

## Phase 8: Full Production Deployment

*   **8.1 Configure Docusaurus build for production:**
    *   Duration: 20-30 min
    *   Dependencies: Phase 1 tasks complete
    *   Acceptance Criterion: Docusaurus project builds successfully in production mode (`npm run build`).
    *   Output: `build/` directory with static assets.
    *   Spec Link: `specs/textbook-generation/plan.md` (Deployment and Rollback strategies)

*   **8.2 Enhance GitHub Pages workflow for production deployment:**
    *   Duration: 30-45 min
    *   Dependencies: 8.1
    *   Acceptance Criterion: GitHub Actions workflow successfully deploys the production-built Docusaurus site to GitHub Pages.
    *   Output: Updated `.github/workflows/deploy.yml`, live GitHub Pages URL.
    *   Spec Link: `specs/textbook-generation/plan.md` (Deployment and Rollback strategies)

*   **8.3 Prepare RAG backend for deployment (Railway/Render):**
    *   Duration: 45-60 min
    *   Dependencies: Phase 2 tasks complete
    *   Acceptance Criterion: FastAPI application is containerized (e.g., Dockerfile) and configured for deployment to Railway/Render.
    *   Output: Dockerfile, deployment configuration files.
    *   Spec Link: `specs/textbook-generation/plan.md` (Deployment and Rollback strategies)

*   **8.4 Configure environment variables for RAG backend:**
    *   Duration: 30-45 min
    *   Dependencies: 8.3
    *   Acceptance Criterion: All necessary environment variables (e.g., Qdrant API key, Neon connection string, embedding provider API key) are securely configured for the chosen deployment platform.
    *   Output: Deployment platform environment variable settings.
    *   Spec Link: `specs/textbook-generation/plan.md` (Security - Secrets)

*   **8.5 Implement health checks for RAG backend:**
    *   Duration: 30-45 min
    *   Dependencies: 8.3
    *   Acceptance Criterion: A `/health` or similar endpoint is added to the FastAPI application, returning `200 OK` if the RAG components (Qdrant, Neon, embedding provider) are reachable.
    *   Output: Updated `RAG-backend/main.py`.
    *   Spec Link: `specs/textbook-generation/plan.md` (Operational Readiness - Health checks)

*   **8.6 Create a launch checklist for production:**
    *   Duration: 20-30 min
    *   Dependencies: All other Phase 8 tasks complete.
    *   Acceptance Criterion: A comprehensive markdown checklist for production launch is created, covering all pre-launch validations.
    *   Output: `specs/textbook-generation/launch-checklist.md`.
    *   Spec Link: `specs/textbook-generation/plan.md` (Operational Readiness - Runbooks)
