from fastapi import APIRouter, Query
from typing import List
from models.learning import Roadmap
from models.user import BranchEnum
from pydantic import BaseModel
from services.learning import generate_dynamic_roadmap

router = APIRouter()

@router.post("/", response_model=Roadmap)
async def create_roadmap(roadmap: Roadmap):
    await roadmap.insert()
    return roadmap

@router.get("/", response_model=List[Roadmap])
async def get_roadmaps():
    return await Roadmap.find().to_list()

@router.get("/recommend", response_model=List[Roadmap])
async def recommend_roadmaps(
    branch: BranchEnum = Query(..., description="User's registered branch")
):
    """
    Returns roadmaps filtered by the user's branch
    """
    roadmaps = await Roadmap.find(Roadmap.target_branch == branch).to_list()
    return roadmaps

class GenerateRoadmapRequest(BaseModel):
    graduation_year: int
    target_role: str
    target_branch: BranchEnum

@router.post("/generate", response_model=Roadmap)
async def generate_roadmap_with_ai(request: GenerateRoadmapRequest):
    """
    Use the Groq AI engine to dynamically generate a specific roadmap.
    Saves the generated roadmap to the database and returns it.
    """
    roadmap = await generate_dynamic_roadmap(
        target_role=request.target_role,
        target_branch=request.target_branch.value,
        graduation_year=request.graduation_year
    )
    
    # Save the dynamically generated roadmap to the database for future cache/recommendations
    await roadmap.insert()
    
    return roadmap
