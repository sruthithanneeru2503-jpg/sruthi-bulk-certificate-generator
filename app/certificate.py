from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os


def generate_certificate(
    recipient_name: str,
    event_name: str,
    event_date: str,
    certificate_id: int
):
    os.makedirs("generated_certificates", exist_ok=True)

    file_path = (
        f"generated_certificates/certificate_{certificate_id}.pdf"
    )

    pdf = canvas.Canvas(file_path, pagesize=A4)

    width, height = A4

    # Border
    pdf.rect(
        20 * mm,
        20 * mm,
        width - 40 * mm,
        height - 40 * mm
    )

    # Title
    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(
        width / 2,
        height - 60 * mm,
        "CERTIFICATE OF COMPLETION"
    )

    # Main text
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        width / 2,
        height - 90 * mm,
        "This certificate is proudly presented to"
    )

    # Recipient name
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(
        width / 2,
        height - 110 * mm,
        recipient_name
    )

    # Event
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        width / 2,
        height - 140 * mm,
        f"for successfully completing {event_name}"
    )

    # Date
    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(
        width / 2,
        height - 165 * mm,
        f"Date: {event_date}"
    )

    pdf.save()

    return file_path