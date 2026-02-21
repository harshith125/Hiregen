from fastapi import APIRouter, Query
from typing import Optional, List
from models.placement import PlacementRecord
from models.user import User

router = APIRouter()

@router.post("/", response_model=PlacementRecord)
async def create_placement_record(record: PlacementRecord):
    """Log a new placement record."""
    await record.insert()
    return record

@router.get("/", response_model=List[PlacementRecord])
async def get_placement_records(
    year: Optional[int] = Query(None, description="Filter by year"),
    branch: Optional[str] = Query(None, description="Filter by branch")
):
    """Fetch records with optional query parameters to filter by year and branch."""
    query = {}
    if year is not None:
        query["year"] = year
        
    # Fetch records with linked fields to easily filter by branch natively in python
    records = await PlacementRecord.find(query, fetch_links=True).to_list()
    
    if branch:
        # Filter in memory using the linked student_id (User document)
        filtered_records = [
            r for r in records 
            if r.student_id and hasattr(r.student_id, 'branch') and r.student_id.branch == branch
        ]
        return filtered_records
        
    return records
