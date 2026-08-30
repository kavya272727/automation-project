from email_validator import EmailNotValidError, validate_email
from pydantic import BaseModel, Field, field_validator


def _validate_name(value: str) -> str:
    if not value.strip():
        raise ValueError("the student name cannot be empty")
    return value.strip()


def _validate_email(value: str) -> str:
    try:
        result = validate_email(value, check_deliverability=False)
    except EmailNotValidError as exc:
        raise ValueError("the email must be a valid email address") from exc
    return result.normalized


def _validate_age(value: int) -> int:
    if value < 16:
        raise ValueError("the age must be at least 16")
    return value


class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, examples=["Kavya"])
    email: str = Field(..., examples=["kavya@example.com"])
    age: int = Field(..., examples=[19])
    course: str = Field(..., min_length=1, max_length=100, examples=["Computer Science"])

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        return _validate_name(value)

    @field_validator("email")
    @classmethod
    def email_must_be_valid(cls, value: str) -> str:
        return _validate_email(value)

    @field_validator("age")
    @classmethod
    def age_must_be_at_least_16(cls, value: int) -> int:
        return _validate_age(value)


class StudentCreate(StudentBase):
    """Payload used when creating a new student."""


class StudentUpdate(BaseModel):
    """Payload used when updating an existing student. All fields are optional."""

    name: str | None = Field(None, min_length=1, max_length=100)
    email: str | None = None
    age: int | None = None
    course: str | None = Field(None, min_length=1, max_length=100)

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return _validate_name(value)

    @field_validator("email")
    @classmethod
    def email_must_be_valid(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return _validate_email(value)

    @field_validator("age")
    @classmethod
    def age_must_be_at_least_16(cls, value: int | None) -> int | None:
        if value is None:
            return value
        return _validate_age(value)


class Student(StudentBase):
    id: int
