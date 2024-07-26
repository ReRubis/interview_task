from pydantic import BaseModel, field_validator

from src.zypl_interview.auth.utils import hash_password


class UserInAuth(BaseModel):
    """User model for authentication."""

    password: str
    email: str


class UserInRegistration(BaseModel):
    """User model for registration."""

    username: str
    password: str
    email: str

    @field_validator("password")
    @classmethod
    def hash_password(cls, value):
        return hash_password(value)


class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class AuthUser(BaseModel):
    """Represents a user model that we get when user is authenticated."""

    id: int
    username: str
    email: str

    class Config:
        from_attributes = True
