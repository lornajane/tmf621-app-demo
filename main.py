from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from sqlalchemy import create_engine, Column, String, DateTime, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import uuid
import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./trouble_tickets.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model
class TroubleTicketDB(Base):
    __tablename__ = "trouble_tickets"
    
    id = Column(String, primary_key=True, index=True)
    href = Column(String)
    description = Column(Text, nullable=False)
    severity = Column(String)
    priority = Column(Integer)
    type = Column(String)
    status = Column(String)
    creationDate = Column(DateTime)
    expectedResolutionDate = Column(DateTime, nullable=True)
    resolutionDate = Column(DateTime, nullable=True)
    lastUpdate = Column(DateTime)
    channel = Column(String, nullable=True)
    externalId = Column(String, nullable=True)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Models
class TroubleTicketCreate(BaseModel):
    description: str = Field(..., description="Description of the trouble or issue")
    severity: Optional[str] = Field("minor", description="Severity: critical, major, minor")
    priority: Optional[int] = Field(3, description="Priority from 1 (highest) to 5 (lowest)")
    type: Optional[str] = Field("trouble", description="Type of ticket")
    channel: Optional[str] = None
    externalId: Optional[str] = None
    expectedResolutionDate: Optional[datetime] = None

class TroubleTicketUpdate(BaseModel):
    description: Optional[str] = None
    severity: Optional[str] = None
    priority: Optional[int] = None
    status: Optional[str] = None
    resolutionDate: Optional[datetime] = None
    expectedResolutionDate: Optional[datetime] = None

class TroubleTicket(BaseModel):
    id: str
    href: str
    description: str
    severity: str
    priority: int
    type: str
    status: str
    creationDate: datetime
    expectedResolutionDate: Optional[datetime] = None
    resolutionDate: Optional[datetime] = None
    lastUpdate: datetime
    channel: Optional[str] = None
    externalId: Optional[str] = None
    
    class Config:
        from_attributes = True

# FastAPI app
app = FastAPI(
    title="TMF621 Trouble Ticket API",
    description="Workshop implementation of TM Forum TMF621 Trouble Ticket Management API",
    version="5.0.1",
    docs_url=None,  # Disable default Swagger UI
    redoc_url=None  # Disable ReDoc
)

# Add Scalar API documentation
@app.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )

# CORS for Postman
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["info"])
async def root():
    return {
        "message": "TMF621 Trouble Ticket API - Workshop Edition",
        "version": "5.0.1",
        "documentation": "/docs (Scalar API Reference)",
        "endpoints": {
            "List tickets": "GET /tmf-api/troubleTicket/v5/troubleTicket",
            "Create ticket": "POST /tmf-api/troubleTicket/v5/troubleTicket",
            "Get ticket": "GET /tmf-api/troubleTicket/v5/troubleTicket/{id}",
            "Update ticket": "PATCH /tmf-api/troubleTicket/v5/troubleTicket/{id}",
            "Delete ticket": "DELETE /tmf-api/troubleTicket/v5/troubleTicket/{id}"
        }
    }

@app.get("/tmf-api/troubleTicket/v5/troubleTicket", response_model=List[TroubleTicket], tags=["troubleTicket"])
async def list_trouble_tickets(
    severity: Optional[str] = Query(None, description="Filter by severity"),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(100, description="Maximum number of results")
):
    """List all trouble tickets with optional filters"""
    db = next(get_db())
    query = db.query(TroubleTicketDB)
    
    if severity:
        query = query.filter(TroubleTicketDB.severity == severity)
    if status:
        query = query.filter(TroubleTicketDB.status == status)
    
    tickets = query.limit(limit).all()
    return tickets

@app.post("/tmf-api/troubleTicket/v5/troubleTicket", response_model=TroubleTicket, status_code=201, tags=["troubleTicket"])
async def create_trouble_ticket(ticket: TroubleTicketCreate):
    """Create a new trouble ticket"""
    db = next(get_db())
    
    ticket_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    db_ticket = TroubleTicketDB(
        id=ticket_id,
        href=f"/tmf-api/troubleTicket/v5/troubleTicket/{ticket_id}",
        description=ticket.description,
        severity=ticket.severity,
        priority=ticket.priority,
        type=ticket.type,
        status="acknowledged",
        creationDate=now,
        lastUpdate=now,
        channel=ticket.channel,
        externalId=ticket.externalId,
        expectedResolutionDate=ticket.expectedResolutionDate
    )
    
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    
    return db_ticket

@app.get("/tmf-api/troubleTicket/v5/troubleTicket/{id}", response_model=TroubleTicket, tags=["troubleTicket"])
async def get_trouble_ticket(id: str):
    """Get a specific trouble ticket by ID"""
    db = next(get_db())
    ticket = db.query(TroubleTicketDB).filter(TroubleTicketDB.id == id).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Trouble ticket not found")
    
    return ticket

@app.patch("/tmf-api/troubleTicket/v5/troubleTicket/{id}", response_model=TroubleTicket, tags=["troubleTicket"])
async def update_trouble_ticket(id: str, updates: TroubleTicketUpdate):
    """Update a trouble ticket (partial update)"""
    db = next(get_db())
    ticket = db.query(TroubleTicketDB).filter(TroubleTicketDB.id == id).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Trouble ticket not found")
    
    update_data = updates.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ticket, field, value)
    
    ticket.lastUpdate = datetime.utcnow()
    
    # Auto-update resolutionDate if status changes to resolved/closed
    if updates.status in ["resolved", "closed"] and not ticket.resolutionDate:
        ticket.resolutionDate = datetime.utcnow()
    
    db.commit()
    db.refresh(ticket)
    
    return ticket

@app.delete("/tmf-api/troubleTicket/v5/troubleTicket/{id}", status_code=204, tags=["troubleTicket"])
async def delete_trouble_ticket(id: str):
    """Delete a trouble ticket"""
    db = next(get_db())
    ticket = db.query(TroubleTicketDB).filter(TroubleTicketDB.id == id).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Trouble ticket not found")
    
    db.delete(ticket)
    db.commit()
    
    return None

# Health check for Railway
@app.get("/health", tags=["info"])
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
