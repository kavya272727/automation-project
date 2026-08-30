from app.schemas import Student, StudentCreate, StudentUpdate

# Simple in-memory store suitable for a small academic project.
students: dict[int, Student] = {}
next_id: int = 1


def list_students() -> list[Student]:
    return list(students.values())


def get_student(student_id: int) -> Student | None:
    if student_id not in students:
        return None
    return students[student_id]


def create_student(payload: StudentCreate) -> Student:
    global next_id
    student = Student(id=next_id, **payload.model_dump())
    students[next_id] = student
    next_id += 1
    return student


def update_student(student_id: int, payload: StudentUpdate) -> Student | None:
    existing = students.get(student_id)
    if existing is None:
        return None

    updated_data = existing.model_dump()
    updates = payload.model_dump(exclude_unset=True)
    updated_data.update(updates)

    student = Student(**updated_data)
    students[student_id] = student
    return student


def delete_student(student_id: int) -> bool:
    if student_id not in students:
        return False
    del students[student_id]
    return True
