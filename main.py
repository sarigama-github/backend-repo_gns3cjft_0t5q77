import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from database import create_document, get_documents
from schemas import Booking

app = FastAPI(title="Reverb Music Academy API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Reverb Music Academy backend is running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from Reverb Music Academy API"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response

# Booking endpoints

@app.post("/api/bookings")
def create_booking(booking: Booking):
    try:
        inserted_id = create_document("booking", booking)
        return {"success": True, "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class BookingQuery(BaseModel):
    email: str | None = None
    instrument: str | None = None

@app.get("/api/bookings")
def list_bookings(email: str | None = None, instrument: str | None = None, limit: int = 50):
    try:
        filter_dict = {}
        if email:
            filter_dict["email"] = email
        if instrument:
            filter_dict["instrument"] = instrument
        docs = get_documents("booking", filter_dict, limit)
        # Convert ObjectId to string if present
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return {"success": True, "items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
