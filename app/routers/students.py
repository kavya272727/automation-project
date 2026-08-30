from fastapi import APIRouter, HTTPException, status

from app.schemas import Student, StudentCreate, StudentUpdate
from app import storage

router = APIRouter(prefix="/students", tags=["students"])


@router.post("/", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate) -> Student:
    return storage.create_student(payload)


@router.get("/", response_model=list[Student])
def read_students() -> list[Student]:
    return storage.list_students()


@router.get("/{student_id}", response_model=Student)
@router.get("/{student_id}/", response_model=Student, include_in_schema=False)
def read_student(student_id: int) -> Student:
    student = storage.get_student(student_id)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} was not found.",
        )
    return student


@router.put("/{student_id}", response_model=Student)
def update_student(student_id: int, payload: StudentUpdate) -> Student:
    student = storage.update_student(student_id, payload)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} was not found.",
        )
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int) -> None:
    deleted = storage.delete_student(student_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} was not found.",
        )
