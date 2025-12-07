---
id: 0001
title: Initial Constitution for Physical AI & Humanoid Robotics
stage: constitution
date: 2025-12-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: system
command: /sp.constitution
labels: ["project-setup", "constitution"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - D:\myapp\CLAUDE.md
tests:
null
---

## Prompt

Project Name: Physical AI & Humanoid Robotics — Essentials

Purpose

Create a short, clean, professional AI-Native textbook based on the Physical AI & Humanoid Robotics course.
The textbook must be easy to read, fast to build, and supported by a free-tier RAG chatbot.
The goal is to deliver a modern Docusaurus-based learning resource that teaches Physical AI, humanoid systems, ROS 2, simulation, VLA, and safe robotics fundamentals.

Scope

The book includes 6 short, focused chapters:

Introduction to Physical AI

Basics of Humanoid Robotics

ROS 2 Fundamentals

Digital Twin Simulation (Gazebo + Isaac)

Vision-Language-Action Systems

Capstone: Simple AI-Robot Pipeline

Additional scope:

Clean, minimal Docusaurus UI

Free-tier-friendly RAG system

Lightweight embeddings

Only book text used for retrieval

Optional Urdu translation module

Optional Personalization chapter

Core Principles

Simplicity — Everything explained in clear, beginner-friendly language.

Accuracy — Content validated against real robotics workflows (ROS 2, Gazebo, Isaac).

Minimalism — Only essential concepts; no unnecessary complexity.

Fast Builds — Works with GitHub Pages and small compute.

Free-Tier Architecture — Neon + Qdrant + FastAPI, no GPUs required.

RAG Discipline — Chatbot must answer ONLY from book content.

Interdisciplinary Balance — Combine AI, robotics, biomechanics, simulation, cognitive science.

Ethical AI Development — Safety, transparency, fairness, human-centered design.

Robustness & Safety — Simulation-first, risk-aware, failure-safe principles.

Human-Robot Interaction — Natural, intuitive, culturally-aware robot behavior.

Continuous Learning — Systems designed to adapt, improve, and iterate.

Key Features

Docusaurus textbook

RAG chatbot (Qdrant + Neon + FastAPI)

Select-text → Ask AI integration

Lightweight embeddings

Simple digital-twin examples

Beginner-friendly ROS 2 samples

Optional Urdu translation UI

Optional personalization module

Technical Standards

ROS 2 (Humble/Iron) fundamentals only

Gazebo & Isaac simulation used in simplified form

Hardware-Software co-design kept minimal

No heavy GPU workloads

All examples runnable on low-cost hardware

Embedding + RAG pipeline optimized for minimal tokens

Free-tier vector DB + SQL DB architecture only

Avoid large models or server-heavy pipelines

R&D Workflow

Iterative writing → testing → refinement

All chapters must end with small experiments or micro-simulations

Peer review encouraged for clarity & accuracy

Controlled updates to specification and implementation

Knowledge transfer prioritized: real-world examples > theory

Constraints

No heavy GPU usage

Minimal embeddings

No RL-heavy, large Isaac pipelines

No full humanoid hardware requirement

Textbook must work offline (optional)

Governance

Updates follow /sp.constitution → /sp.specify → /sp.plan → /sp.tasks → /sp.implement flow

All changes must follow core principles: simplicity, safety, accuracy

RAG must remain grounded in textbook content

Version control through SpecifyPlus branch workflow

Success Criteria

Textbook builds successfully with GitHub Pages

RAG chatbot answers 100% grounded and accurate

UI remains clean and fast

Architecture stays free-tier compatible

Students can understand all chapters without prior robotics background

Content remains safe, ethical, and technically correct

## Response snapshot

Created Prompt History Record for the project constitution.

## Outcome

- ✅ Impact: null
- 🧪 Tests: null
- 📁 Files: null
- 🔁 Next prompts: null
- 🧠 Reflection: null

## Evaluation notes (flywheel)

- Failure modes observed: null
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
