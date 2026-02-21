from fastapi import APIRouter, HTTPException, status
from typing import List
from models.community import (
    InterviewExperience,
    ReferralOpportunity,
    ReferralRequest
)
from models.user import User, RoleEnum

router = APIRouter()

@router.post("/experiences", response_model=InterviewExperience)
async def create_interview_experience(experience: InterviewExperience):
    await experience.insert()
    return experience

@router.get("/experiences", response_model=List[InterviewExperience])
async def get_interview_experiences():
    return await InterviewExperience.find(fetch_links=True).to_list()


@router.post("/referrals/opportunities", response_model=ReferralOpportunity)
async def create_referral_opportunity(opportunity: ReferralOpportunity):
    """
    Alumni POST referral opportunities
    """
    # Fetch the linked User document to ensure the role is Alumni
    alumni = await User.get(opportunity.alumni_id.ref.id)
    if not alumni or alumni.role != RoleEnum.Alumni:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Only users with Alumni role can post referral opportunities."
        )
    
    await opportunity.insert()
    return opportunity

@router.get("/referrals/opportunities", response_model=List[ReferralOpportunity])
async def get_referral_opportunities():
    return await ReferralOpportunity.find(fetch_links=True).to_list()


@router.post("/referrals/requests", response_model=ReferralRequest)
async def create_referral_request(request: ReferralRequest):
    """
    Students POST a referral request
    """
    student = await User.get(request.student_id.ref.id)
    if not student or student.role != RoleEnum.Student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Only users with Student role can request referrals."
        )

    await request.insert()
    return request

@router.get("/referrals/requests", response_model=List[ReferralRequest])
async def get_referral_requests():
    return await ReferralRequest.find(fetch_links=True).to_list()
