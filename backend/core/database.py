from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.user import User
from models.company import Company
from models.placement import PlacementRecord
from models.community import InterviewExperience, ReferralOpportunity, ReferralRequest
from models.learning import Roadmap
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/hiregen")

async def init_db():
    # Create Motor client
    client = AsyncIOMotorClient(MONGO_URI)
    
    # Initialize beanie with the User and Company document classes
    # client.get_database() gets the default database from the URI
    await init_beanie(
        database=client.get_database(), 
        document_models=[
            User, 
            Company, 
            PlacementRecord,
            InterviewExperience,
            ReferralOpportunity,
            ReferralRequest,
            Roadmap
        ]
    )
