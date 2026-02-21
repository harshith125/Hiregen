from enum import Enum
from beanie import Document

class SectorEnum(str, Enum):
    IT = "IT"
    Core = "Core"
    Consulting = "Consulting"

class Company(Document):
    name: str
    sectors: list[SectorEnum]
    hiring_frequency: str
    
    class Settings:
        name = "companies"
