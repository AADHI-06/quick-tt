from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.orm import Session
from typing import List
import os

from timetable_system.models import init_db, SessionLocal
from timetable_system.repositories.timetable_manager import TimetableManager
from timetable_system.services.scheduler import TimetableScheduler
from .models import TimetableCreate, TimetableResponse, GenerateRequest

app = FastAPI(title="Timetable Management API")

# Mount static files
if os.path.exists("web/dist/assets"):
    app.mount("/assets", StaticFiles(directory="web/dist/assets"), name="assets")
else:
    print("WARNING: web/dist/assets not found. Frontend assets will not be served.")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/generate")
def generate_timetable(request: GenerateRequest):
    """
    Generate a schedule based on provided constraints. 
    Does NOT save to DB automatically.
    """
    scheduler = TimetableScheduler(request.classes, request.periods)
    schedule = scheduler.solve()
    
    if not schedule:
        raise HTTPException(status_code=400, detail="Could not generate a conflict-free timetable.")
    
    return schedule

@app.post("/timetables", response_model=TimetableResponse)
def create_timetable(timetable: TimetableCreate, db: Session = Depends(get_db)):
    tm = TimetableManager(db)
    try:
        created = tm.create_timetable(timetable.name, timetable.entries, timetable.periods)
        return TimetableResponse(
            id=created.id,
            name=created.name,
            created_at=created.created_at.isoformat(),
            entries=[
                {"period_index": e.period_index, "class_name": e.class_name, "subject": e.subject}
                for e in created.entries
            ]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/timetables", response_model=List[TimetableResponse])
def list_timetables(db: Session = Depends(get_db)):
    tm = TimetableManager(db)
    timetables = tm.get_all_timetables()
    return [
        TimetableResponse(
            id=t.id,
            name=t.name,
            created_at=t.created_at.isoformat(),
            entries=[] # Omit entries for list view to save bandwidth
        )
        for t in timetables
    ]

@app.get("/timetables/{name}", response_model=TimetableResponse)
def get_timetable(name: str, db: Session = Depends(get_db)):
    tm = TimetableManager(db)
    t = tm.get_timetable_by_name(name)
    if not t:
        raise HTTPException(status_code=404, detail="Timetable not found")
        
    return TimetableResponse(
        id=t.id,
        name=t.name,
        created_at=t.created_at.isoformat(),
        entries=[
            {"period_index": e.period_index, "class_name": e.class_name, "subject": e.subject}
            for e in t.entries
        ]
    )

@app.delete("/timetables/{name}")
def delete_timetable(name: str, db: Session = Depends(get_db)):
    tm = TimetableManager(db)
    success = tm.delete_timetable(name)
    if not success:
        raise HTTPException(status_code=404, detail="Timetable not found")
    return {"message": "Deleted successfully"}

# Catch-all for SPA
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    possible_path = os.path.join("web/dist", full_path)
    if os.path.exists(possible_path) and os.path.isfile(possible_path):
        return FileResponse(possible_path)
    
    index_path = "web/dist/index.html"
    if os.path.exists(index_path):
        return FileResponse(index_path)
        
    return HTMLResponse(
        content=f"<h1>Deployment Error</h1><p>Frontend not found. Checked {os.path.abspath(index_path)}</p>", 
        status_code=404
    )

@app.on_event("startup")
async def startup_check():
    print("--- Startup Check ---")
    print(f"CWD: {os.getcwd()}")
    if os.path.exists("web/dist"):
        print("web/dist exists. Contents:")
        for root, dirs, files in os.walk("web/dist"):
            for name in files:
                print(os.path.join(root, name))
    else:
        print("web/dist does NOT exist.")
    print("---------------------")
