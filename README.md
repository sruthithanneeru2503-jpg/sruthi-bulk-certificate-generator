# Bulk Certificate Generator API

A FastAPI backend API for generating certificates for multiple recipients.

## Features

- Create a certificate generation job
- Accept multiple recipients in one request
- Validate recipient email addresses
- Generate PDF certificates
- Track job status and progress
- Handle individual certificate failures without stopping the job
- Retrieve generated certificates
- Store job and certificate information in SQLite
- Automated tests with Pytest

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- ReportLab
- Pytest

## Setup

Create and activate a virtual environment:

```bash
python -m venv venv