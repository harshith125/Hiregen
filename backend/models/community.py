from enum import Enum
from pydantic import Field
from beanie import Document, Link
from models.user import User
from models.company import Company

class ReferralStatusEnum(str, Enum):
    Pending = "Pending"
    Accepted = "Accepted"
    Rejected = "Rejected"

class InterviewExperience(Document):
    author_id: Link[User]
    company_id: Link[Company]
    rounds_details: list[str]
    questions_asked: list[str]
    difficulty_rating: int = Field(ge=1, le=5, description="Difficulty rating from 1 to 5")

    class Settings:
        name = "interview_experiences"

class ReferralOpportunity(Document):
    alumni_id: Link[User]
    company_id: Link[Company]
    job_role: str
    requirements: list[str]

    class Settings:
        name = "referral_opportunities"

class ReferralRequest(Document):
    student_id: Link[User]
    opportunity_id: Link[ReferralOpportunity]
    status: ReferralStatusEnum = ReferralStatusEnum.Pending

    class Settings:
        name = "referral_requests"
