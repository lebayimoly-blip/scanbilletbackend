from datetime import datetime
from io import StringIO

import csv
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse, FileResponse
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session

from app.models import Scan, User
from app.database import get_db

router = APIRouter()

# 🔹 Statistiques globales
@router.get("/global")
def get_scan_stats(
    period: str = Query("today", enum=["today", "month", "year"]),
    db: Session = Depends(get_db)
):
    now = datetime.now()
    if period == "today":
        start = datetime(now.year, now.month, now.day)
    elif period == "month":
        start = datetime(now.year, now.month, 1)
    elif period == "year":
        start = datetime(now.year, 1, 1)

    total = db.query(Scan.ticket_id).distinct().count()
    valides = db.query(Scan.ticket_id).filter(Scan.validated == True).distinct().count()
    scanned_today = db.query(Scan).filter(Scan.timestamp >= start).count()

    scans_by_user = (
        db.query(User.username, db.func.count(Scan.id))
        .join(Scan, Scan.user_id == User.id)
        .filter(Scan.timestamp >= start)
        .group_by(User.username)
        .all()
    )

    return {
        "total": total,
        "valides": valides,
        "scanned_today": scanned_today,
        "scans_by_user_today": [
            {"user": username, "count": count} for username, count in scans_by_user
        ]
    }


# 🔹 Statistiques d’un utilisateur
@router.get("/user/{username}")
def get_user_stats(
    username: str,
    period: str = Query("today", enum=["today", "month", "year"]),
    db: Session = Depends(get_db)
):
    now = datetime.now()
    if period == "today":
        start = datetime(now.year, now.month, now.day)
    elif period == "month":
        start = datetime(now.year, now.month, 1)
    elif period == "year":
        start = datetime(now.year, 1, 1)

    user = db.query(User).filter(User.username == username).first()
    if not user:
        return {"error": f"Utilisateur '{username}' introuvable"}

    scan_count = db.query(Scan).filter(
        Scan.user_id == user.id,
        Scan.timestamp >= start
    ).count()

    return {
        "user": username,
        "period": period,
        "scan_count": scan_count
    }


# 🔹 Export CSV utilisateur
@router.get("/user/{username}/export/csv")
def export_user_stats_csv(
    username: str,
    period: str = Query("today", enum=["today", "month", "year"]),
    db: Session = Depends(get_db)
):
    stats = get_user_stats(username, period, db)
    if "error" in stats:
        return stats

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Utilisateur", "Période", "Nombre de scans"])
    writer.writerow([stats["user"], stats["period"], stats["scan_count"]])
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={username}_{period}.csv"}
    )


# 🔹 Export PDF utilisateur
@router.get("/user/{username}/export/pdf")
def export_user_stats_pdf(
    username: str,
    period: str = Query("today", enum=["today", "month", "year"]),
    db: Session = Depends(get_db)
):
    stats = get_user_stats(username, period, db)
    if "error" in stats:
        return stats

    filename = f"{username}_{period}.pdf"
    c = canvas.Canvas(filename)
    c.drawString(100, 800, f"Statistiques de {username} - Période : {period.upper()}")
    c.drawString(100, 760, f"Nombre de scans : {stats['scan_count']}")
    c.save()

    return FileResponse(filename, media_type="application/pdf", filename=filename)
