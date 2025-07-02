Medical Wallet Backend (CKD MVP)

A HIPAA-compliant, FHIR-native backend for patient-controlled health data, starting with Chronic Kidney Disease (CKD) management.
Built with Python, FastAPI, PostgreSQL, and a modular, secure architecture.

Project Overview

Medical Wallet empowers CKD patients to securely manage, share, and gain AI-powered insights from their health data.
Our mission: Give patients full control, cross-provider portability, and actionable health intelligence.

Core MVP Features:

    Secure patient authentication & role-based access

    FHIR-compliant storage and retrieval of labs, medications, and clinical notes

    AI-powered health summaries (integrated via cloud LLM)

    Secure data sharing with providers

    Full audit logging and HIPAA-grade security

Tech Stack

    Backend: Python 3.11+, FastAPI, Pydantic

    Database: PostgreSQL (with SQLAlchemy ORM)

    FHIR Server: HAPI FHIR (external integration)

    AI/ML: Azure OpenAI / Hugging Face

    Auth: Auth0 or FusionAuth (JWT, RBAC, MFA)

    DevOps: Docker, Alembic, GitHub Actions, Terraform (infra)

Security & Compliance

    HIPAA-ready: End-to-end encryption, audit logging, RBAC, secure secrets management

    FHIR-native: All patient data modeled as FHIR R4 resources

    Audit trails: Every access and modification is logged

Roadmap

    CKD MVP (labs, meds, notes, summaries, sharing)

    Provider dashboard & onboarding

    Diabetes & comorbidity support

    Wearable and remote monitoring integration

    Global health data interoperability
