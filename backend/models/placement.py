from enum import Enum
from pydantic import Field
from beanie import Document, Link
from models.user import User
from models.company import Company

class PlacementTypeEnum(str, Enum):
    Internship = "Internship"
    Full_time = "Full-time"

class PlacementRecord(Document):
    student_id: Link[User]
    company_id: Link[Company]
    job_role: str
    package_ctc: float = Field(gt=0, description="Package CTC must be a positive number")
    base_pay: float = Field(gt=0, description="Base pay must be a positive number")
    skills_required: list[str]
    placement_type: PlacementTypeEnum
    year: int

    class Settings:
        name = "placement_records"
