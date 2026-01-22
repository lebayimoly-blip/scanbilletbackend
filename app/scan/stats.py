from datetime import datetime
from io import StringIO
from app.models import Scan, User, Ticket

import csv
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse, FileResponse
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db

router = APIRouter()

# 🔹 Statistiques globales
@router.get("/global")
def get_ticket_stats(
    period: str = Query("today", enum=["today", "month", "year", "all"]),
    db: Session = Depends(get_db)
):
    now = datetime.now()

    if period == "today":
        start = datetime(now.year, now.month, now.day)
    elif period == "month":
        start = datetime(now.year, now.month, 1)
    elif period == "year":
        start = datetime(now.year, 1, 1)
    else:
        start = None

    # 🎟️ Tickets
    ticket_query = db.query(Ticket)
    if start:
        ticket_query = ticket_query.filter(Ticket.created_at >= start)

    total = ticket_query.count()
    valides = ticket_query.filter(Ticket.validé == True).count()
    invalides = ticket_query.filter(Ticket.validé == False).count()

    # 📥 Scans
    scan_query = db.query(Scan)
    if start:
        scan_query = scan_query.filter(Scan.timestamp >= start)

    scanned = scan_query.count()

    # 👤 Répartition des scans par utilisateur (billets uniques scannés)
    stats_by_user = (
        db.query(User.username, func.count(func.distinct(Scan.ticket_id)))
        .join(Scan, Scan.user_id == User.id)
    )
    if start:
        stats_by_user = stats_by_user.filter(Scan.timestamp >= start)

    stats_by_user = stats_by_user.group_by(User.username).all()

    return {
        "period": period,
        "total": total,
        "valides": valides,
        "invalides": invalides,
        "scanned": scanned,
        "scans_by_user": [
            {"user": username, "count": count} for username, count in stats_by_user
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

    scan_count = db.query(func.count(func.distinct(Scan.ticket_id))).filter(
        Scan.user_id == user.id,
        Scan.timestamp >= start
    ).scalar()

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

# 🔹 Liste des utilisateurs (pour menu déroulant)
@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User.username).all()
    return [u.username for u in users]
