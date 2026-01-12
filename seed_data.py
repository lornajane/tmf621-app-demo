"""
Seed data script to populate sample trouble tickets for workshop demos
Run this after deploying: python seed_data.py
"""
from datetime import datetime, timedelta
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import TroubleTicketDB, Base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./trouble_tickets.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_tickets():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if already seeded
    existing = db.query(TroubleTicketDB).first()
    if existing:
        print("Database already contains tickets. Skipping seed.")
        db.close()
        return
    
    now = datetime.utcnow()
    
    sample_tickets = [
        {
            "description": "URGENT: Toast stuck in toaster, smoke alarm singing solo concert in kitchen",
            "severity": "critical",
            "priority": 1,
            "type": "incident",
            "status": "inProgress",
            "channel": "phone",
            "externalId": "KITCHEN-911",
            "expectedResolutionDate": now + timedelta(hours=1)
        },
        {
            "description": "Spaghetti has achieved orbit and is now stuck to ceiling. Physics teacher would be proud.",
            "severity": "major",
            "priority": 2,
            "type": "trouble",
            "status": "acknowledged",
            "channel": "email",
            "expectedResolutionDate": now + timedelta(days=1)
        },
        {
            "description": "Request for anti-gravity device to prevent future cake-floor collision incidents",
            "severity": "minor",
            "priority": 4,
            "type": "request",
            "status": "pending",
            "channel": "web",
        },
        {
            "description": "Mixed up salt and sugar in cookie recipe. Created world's saltiest disappointment.",
            "severity": "major",
            "priority": 2,
            "type": "complaint",
            "status": "inProgress",
            "channel": "chat",
            "externalId": "BAKE-FAIL-2026",
            "expectedResolutionDate": now + timedelta(days=2)
        },
        {
            "description": "Flour explosion successfully contained. Kitchen now resembles winter wonderland.",
            "severity": "critical",
            "priority": 1,
            "type": "incident",
            "status": "resolved",
            "channel": "automated",
            "resolutionDate": now - timedelta(hours=2),
            "expectedResolutionDate": now - timedelta(hours=1)
        },
        {
            "description": "Positive feedback: Managed to make toast without incident for 3 consecutive days!",
            "severity": "minor",
            "priority": 5,
            "type": "feedback",
            "status": "closed",
            "channel": "email",
            "resolutionDate": now - timedelta(days=1)
        },
        {
            "description": "Microwave timer beeped 47 times before anyone noticed. Neighbors filed noise complaint.",
            "severity": "major",
            "priority": 2,
            "type": "trouble",
            "status": "acknowledged",
            "channel": "phone",
            "expectedResolutionDate": now + timedelta(days=3)
        },
        {
            "description": "EMERGENCY: Dog ate entire birthday cake. Dog now experiencing sugar-fueled zoomies.",
            "severity": "critical",
            "priority": 1,
            "type": "incident",
            "status": "inProgress",
            "channel": "automated",
            "externalId": "DOGGO-2026",
            "expectedResolutionDate": now + timedelta(hours=2)
        },
        {
            "description": "Suggest adding 'defrost' step to frozen pizza instructions. Current result: ice disk with toppings.",
            "severity": "minor",
            "priority": 4,
            "type": "request",
            "status": "pending",
            "channel": "web",
        },
        {
            "description": "Pancake attempted independence by flipping itself onto floor. Freedom was short-lived.",
            "severity": "major",
            "priority": 3,
            "type": "trouble",
            "status": "acknowledged",
            "channel": "email",
            "expectedResolutionDate": now + timedelta(days=1)
        }
    ]
    
    for ticket_data in sample_tickets:
        ticket_id = str(uuid.uuid4())
        creation_date = now - timedelta(hours=ticket_data.get("_hours_ago", 4))
        
        db_ticket = TroubleTicketDB(
            id=ticket_id,
            href=f"/tmf-api/troubleTicket/v5/troubleTicket/{ticket_id}",
            creationDate=creation_date,
            lastUpdate=creation_date,
            **{k: v for k, v in ticket_data.items() if not k.startswith("_")}
        )
        db.add(db_ticket)
    
    db.commit()
    print(f"✅ Successfully seeded {len(sample_tickets)} sample trouble tickets!")
    db.close()

if __name__ == "__main__":
    seed_tickets()
