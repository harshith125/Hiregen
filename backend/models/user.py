from enum import Enum
from beanie import Document
from pydantic import EmailStr

class BranchEnum(str, Enum):
    CSE = "Computer Science (CSE)"
    ECE = "Electronics (ECE)"
    ME = "Mechanical (ME)"
    CE = "Civil (CE)"

class RoleEnum(str, Enum):
    Student = "Student"
    Alumni = "Alumni"

class User(Document):
    email: EmailStr
    hashed_password: str
    full_name: str
    branch: BranchEnum
    role: RoleEnum
    
    class Settings:
        name = "users"
