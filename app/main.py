from fastapi import FastAPI

from app.routers import students

app = FastAPI(
    title="Student Management API",
    description="A small REST API for managing students.",
    version="1.0.0",
)

app.include_router(students.router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Student Management API is running."}
