from beanie import Document
from pydantic import HttpUrl
from models.user import BranchEnum

class Roadmap(Document):
    target_role: str
    target_branch: BranchEnum
    steps: list[str]
    video_recommendations: list[HttpUrl]

    class Settings:
        name = "roadmaps"
