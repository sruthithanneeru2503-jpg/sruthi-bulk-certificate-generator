from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import models
from .schemas import JobCreate
from .certificate import generate_certificate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bulk Certificate Generator")


@app.get("/")
def home():
    return {"message": "Bulk Certificate Generator API is running!"}


@app.post("/jobs")
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db)
):
    # Create the job
    job = models.Job(
        event_name=job_data.event_name,
        event_date=job_data.event_date,
        total=len(job_data.recipients),
        status="processing"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    successful = 0
    failed = 0

    # Process every recipient separately
    for recipient_data in job_data.recipients:

        recipient = models.Recipient(
            job_id=job.id,
            name=recipient_data.name,
            email=recipient_data.email,
            status="pending"
        )

        db.add(recipient)
        db.commit()
        db.refresh(recipient)

        try:
            file_path = generate_certificate(
                recipient.name,
                job.event_name,
                job.event_date,
                recipient.id
            )

            certificate = models.Certificate(
                recipient_id=recipient.id,
                file_path=file_path,
                status="success"
            )

            recipient.status = "success"

            db.add(certificate)

            successful += 1

        except Exception as error:
            recipient.status = "failed"
            recipient.error_message = str(error)

            failed += 1

        db.commit()

    # Update final job status
    job.successful = successful
    job.failed = failed
    job.status = "completed"

    db.commit()

    return {
        "job_id": job.id,
        "status": job.status,
        "total": job.total,
        "successful": job.successful,
        "failed": job.failed
    }


@app.get("/jobs/{job_id}")
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(models.Job).filter(
        models.Job.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return {
        "job_id": job.id,
        "event_name": job.event_name,
        "event_date": job.event_date,
        "status": job.status,
        "total": job.total,
        "successful": job.successful,
        "failed": job.failed
    }


@app.get("/certificates/{certificate_id}")
def get_certificate(
    certificate_id: int,
    db: Session = Depends(get_db)
):
    certificate = db.query(models.Certificate).filter(
        models.Certificate.id == certificate_id
    ).first()

    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found"
        )

    return FileResponse(
        certificate.file_path,
        media_type="application/pdf",
        filename=f"certificate_{certificate.id}.pdf"
    )