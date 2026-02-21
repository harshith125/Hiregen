import pandas as pd
import numpy as np
from models.placement import PlacementRecord

async def get_placement_dataframe() -> pd.DataFrame:
    """Helper function to fetch all records and return a Pandas DataFrame."""
    records = await PlacementRecord.find(fetch_links=True).to_list()
    data = []
    for r in records:
        data.append({
            "id": str(r.id),
            "student_branch": r.student_id.branch if r.student_id and hasattr(r.student_id, 'branch') else None,
            "company_name": r.company_id.name if r.company_id and hasattr(r.company_id, 'name') else None,
            "job_role": r.job_role,
            "package_ctc": r.package_ctc,
            "base_pay": r.base_pay,
            "skills_required": r.skills_required,
            "placement_type": r.placement_type.value if r.placement_type else None,
            "year": r.year
        })
    return pd.DataFrame(data)

async def calculate_avg_package_per_branch(year: int) -> dict:
    """Calculate average package per branch for a given year."""
    df = await get_placement_dataframe()
    if df.empty:
        return {}
    
    # Filter by selected year
    df = df[df['year'] == year]
    if df.empty:
        return {}
        
    # Group by branch and calculate mean CTC
    avg_per_branch = df.groupby('student_branch')['package_ctc'].mean().to_dict()
    
    # Replace NaN with None for JSON serialization
    return {k: (None if pd.isna(v) else v) for k, v in avg_per_branch.items()}

async def calculate_skill_roi() -> list:
    """Skill vs. Salary correlation (skills sorted by average CTC)."""
    df = await get_placement_dataframe()
    if df.empty:
        return []
        
    # Explode the skills list to have one row per skill
    df_exploded = df.explode('skills_required')
    if df_exploded.empty:
        return []
        
    # Group by skill and calculate mean CTC
    skill_stats = df_exploded.groupby('skills_required')['package_ctc'].mean().reset_index()
    # Sort descending based on CTC
    skill_stats = skill_stats.sort_values(by='package_ctc', ascending=False)
    
    result = []
    for _, row in skill_stats.iterrows():
        result.append({
            "skill": row['skills_required'],
            "avg_ctc": None if pd.isna(row['package_ctc']) else row['package_ctc']
        })
    return result

async def get_hiring_trends() -> dict:
    """Hiring trends: time-series data showing hiring volume over the last 5 years."""
    df = await get_placement_dataframe()
    if df.empty:
        return {}
        
    current_year = df['year'].max()
    if pd.isna(current_year):
        return {}
        
    start_year = max(int(current_year) - 4, int(df['year'].min()))
    
    # Filter dataframe to last 5 years including the current year
    df_recent = df[df['year'] >= start_year]
    
    # Size returns the count of rows per year
    trends = df_recent.groupby('year').size().to_dict()
    return trends
