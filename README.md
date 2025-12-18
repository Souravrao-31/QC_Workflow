# QC Workflow System

A role-based Quality Control (QC) workflow system for managing the lifecycle of drawings across drafting, review, and approval stages.  
Built to provide **clear ownership, traceability, and accountability** across teams.

---

##  Problem Statement

- Drawings pass through multiple roles (Drafter → QC → Final Approval)
- Ownership is unclear during transitions
- Status changes are not traceable
- No audit trail exists for compliance or reviews
- Manual coordination leads to delays and errors

This system solves those problems by enforcing a **strict workflow**, **role-based actions**, and **complete audit logging**.

---

##  Design Principles

- Clear separation of concerns
- Repository + Service pattern
- Defensive backend validation
- Minimal, readable UI
- Easy to extend workflow states and roles

---


## Workflow Overview

UNASSIGNED
↓ CLAIM (Drafter)
DRAFTING
↓ SUBMIT (Drafter)
FIRST_QC
↓ APPROVE (Shift Lead)
FINAL_QC
↓ APPROVE (Final QC)
APPROVED

---


## What This System Does

- Manages drawings through a defined QC lifecycle
- Enforces role-based actions at each stage
- Allows users to claim, submit, approve, or release drawings
- Provides full audit logs for every state transition
- Separates **Available Work** and **My Work**
- Designed for future real-time updates (polling / WebSockets)
- Only allowed actions are exposed in the UI
- Invalid actions are blocked at the API level
- Ownership is enforced for submit/approve actions

---

## Roles & Permissions

| Role        | Responsibilities |
|-------------|------------------|
| ADMIN       | View all drawings, view audit logs |
| DRAFTER     | Claim unassigned drawings, submit for QC |
| SHIFT_LEAD  | Perform First QC approval |
| FINAL_QC    | Perform Final QC approval |

---

## Tech Stack

### Backend
- **FastAPI** – API framework
- **SQLAlchemy** – ORM
- **PostgreSQL** – Database
- **Alembic** – Database migrations
- **JWT (python-jose)** – Authentication
- **Passlib (bcrypt)** – Password hashing

### Frontend
- **React + TypeScript**
- **Chakra UI** – Component library
- **React Router** – Routing
- **Axios** – API calls

### Infrastructure
- **Railway** – Backend deployment
- **Monorepo** – Client + Server in a single repository

## Backend Setup
~~~
cd server
python -m venv venv
source venv/bin/activate   
venv\Scripts\activate    

pip install -r requirements.txt

alembic upgrade head

uvicorn app.main:app --reload
~~~

## Frontend Setup
~~~
cd client
npm install
npm run dev
~~~


## Authentication Flow
**User logs in via /login**
**JWT token is stored in localStorage**
**Token is decoded on the frontend to drive role-based UI**
**Token is validated on the backend for every protected request**



