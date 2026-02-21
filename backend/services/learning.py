import json
from pydantic import ValidationError
from typing import Dict, Any
from core.llm import groq_client
from models.learning import Roadmap

async def generate_dynamic_roadmap(target_role: str, target_branch: str, graduation_year: int) -> Roadmap:
    """
    Generate a dynamic learning roadmap using the Groq API's LLaMA 3 model.
    """
    
    system_prompt = f"""
    You are an expert career advisor and technical mentor for engineering students.
    The user is a B.Tech student studying {target_branch} who is targeting a role as a {target_role} and graduating in {graduation_year}.
    
    Your task is to generate a comprehensive, timeline-specific learning roadmap leading up to their campus placements.
    
    You MUST output ONLY a valid JSON object strictly matching this schema, with no additional text or formatting:
    {{
      "target_role": "{target_role}",
      "target_branch": "{target_branch}",
      "steps": [
        "String: Specific learning milestone or skill to acquire (e.g., 'Learn Python basics by Q1 2025')",
        "String: Another step..."
      ],
      "video_recommendations": [
        "https://www.youtube.com/watch?v=example1",
        "https://www.youtube.com/watch?v=example2"
      ]
    }}
    
    Ensure the `video_recommendations` are valid URLs (preferably YouTube crash courses or tutorials relevant to the role).
    """

    user_prompt = "Generate my personalized roadmap."

    try:
        response = await groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3, # Lower temperature for more consistent JSON output
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response
        content = response.choices[0].message.content
        roadmap_data = json.loads(content)
        
        # Create and validate the Beanie Document model instance
        roadmap = Roadmap(**roadmap_data)
        
        return roadmap

    except (json.JSONDecodeError, ValidationError) as e:
        print(f"Error generating roadmap: {e}")
        # Return a fallback roadmap in case of generation failure
        return Roadmap(
            target_role=target_role,
            target_branch=target_branch,
            steps=[
                "Master Data Structures and Algorithms",
                f"Learn core web development skills for {target_role}",
                "Build 2-3 impressive portfolio projects",
                "Practice mock interviews and soft skills"
            ],
            video_recommendations=[
                "https://www.youtube.com/watch?v=8hly31xKli0", # General SWE advice fallback
            ]
        )
