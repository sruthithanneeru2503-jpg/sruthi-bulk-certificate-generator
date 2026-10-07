from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, nullable=False)
    event_date = Column(String, nullable=False)
    status = Column(String, default="pending")
    total = Column(Integer, default=0)
    successful = Column(Integer, default=0)
    failed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    recipients = relationship(
        "Recipient",
        back_populates="job",
        cascade="all, delete-orphan"
    )


class Recipient(Base):
    __tablename__ = "recipients"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    status = Column(String, default="pending")
    error_message = Column(String, nullable=True)

    job = relationship("Job", back_populates="recipients")

    certificate = relationship(
        "Certificate",
        back_populates="recipient",
        uselist=False,
        cascade="all, delete-orphan"
    )


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    recipient_id = Column(
        Integer,
        ForeignKey("recipients.id"),
        nullable=False
    )
    file_path = Column(String, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    recipient = relationship("Recipient", back_populates="certificate")