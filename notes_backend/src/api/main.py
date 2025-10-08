from datetime import datetime
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# PUBLIC_INTERFACE
class Note(BaseModel):
    """A note object returned by the API."""
    id: int = Field(..., description="Unique identifier for the note")
    title: str = Field(..., description="Title of the note")
    content: str = Field("", description="Content/body of the note")
    updated_at: datetime = Field(..., description="Last updated timestamp in ISO format")

# PUBLIC_INTERFACE
class NoteCreate(BaseModel):
    """Payload for creating a new note."""
    title: str = Field(..., description="Title of the note")
    content: Optional[str] = Field("", description="Content/body of the note")

# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Payload for updating an existing note."""
    title: Optional[str] = Field(None, description="Title of the note")
    content: Optional[str] = Field(None, description="Content/body of the note")


def _now() -> datetime:
    return datetime.utcnow()


# In-memory store for MVP. Structured to allow easy swap later.
NOTES: Dict[int, Note] = {}
NEXT_ID: int = 1

def _get_next_id() -> int:
    global NEXT_ID
    nid = NEXT_ID
    NEXT_ID += 1
    return nid


app = FastAPI(
    title="Simple Notes API",
    description="FastAPI backend for a simple notes application. Provides CRUD endpoints for notes.",
    version="0.1.0",
    openapi_tags=[
        {"name": "health", "description": "Health check endpoints"},
        {"name": "notes", "description": "CRUD operations for notes"},
    ],
)

# CORS - restrict to local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# PUBLIC_INTERFACE
@app.get("/", tags=["health"], summary="Health Check", description="Basic health check for the Notes API.")
def health_check():
    """Entrypoint for health check."""
    return {"message": "Healthy"}


# PUBLIC_INTERFACE
@app.get(
    "/notes",
    response_model=List[Note],
    tags=["notes"],
    summary="List notes",
    description="Return all notes sorted by updated_at descending.",
)
def list_notes() -> List[Note]:
    """List all notes."""
    return sorted(NOTES.values(), key=lambda n: n.updated_at, reverse=True)


# PUBLIC_INTERFACE
@app.get(
    "/notes/{note_id}",
    response_model=Note,
    tags=["notes"],
    summary="Get note by ID",
    description="Return a single note specified by its ID.",
    responses={
        404: {"description": "Note not found"},
    },
)
def get_note(note_id: int) -> Note:
    """Get a single note by ID."""
    note = NOTES.get(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


# PUBLIC_INTERFACE
@app.post(
    "/notes",
    response_model=Note,
    status_code=status.HTTP_201_CREATED,
    tags=["notes"],
    summary="Create note",
    description="Create a new note with title and content.",
)
def create_note(payload: NoteCreate) -> Note:
    """Create a new note."""
    note_id = _get_next_id()
    note = Note(
        id=note_id,
        title=payload.title.strip() if payload.title else "",
        content=(payload.content or ""),
        updated_at=_now(),
    )
    NOTES[note_id] = note
    return note


# PUBLIC_INTERFACE
@app.put(
    "/notes/{note_id}",
    response_model=Note,
    tags=["notes"],
    summary="Update note",
    description="Update an existing note with new title and/or content.",
    responses={
        404: {"description": "Note not found"},
    },
)
def update_note(note_id: int, payload: NoteUpdate) -> Note:
    """Update an existing note."""
    note = NOTES.get(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    new_title = note.title if payload.title is None else payload.title.strip()
    new_content = note.content if payload.content is None else payload.content
    updated = note.model_copy(update={"title": new_title, "content": new_content, "updated_at": _now()})
    NOTES[note_id] = updated
    return updated


# PUBLIC_INTERFACE
@app.delete(
    "/notes/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["notes"],
    summary="Delete note",
    description="Delete a note by ID.",
    responses={
        204: {"description": "Note deleted"},
        404: {"description": "Note not found"},
    },
)
def delete_note(note_id: int):
    """Delete a note by ID."""
    if note_id not in NOTES:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    del NOTES[note_id]
    return
