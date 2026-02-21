import os
import json
from groq import Groq
from django.conf import settings

def generate_dynamic_roadmap(user, target_role):
    """
    Communicates with the Groq API to generate a JSON roadmap.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set.")

    client = Groq(api_key=api_key)

    # Safely extract user context
    skills = ", ".join(user.skills) if isinstance(user.skills, list) else str(user.skills)
    college = user.college if user.college else "Unknown University"

    system_prompt = f"""
    You are an expert career advisor and technical mentor for engineering students.
    The user is a B.Tech student studying at {college}. 
    They already know these skills: {skills}.
    They are targeting a role as a {target_role}.
    
    Your task is to generate a comprehensive, personalized timeline learning roadmap to help them reach their goal.
    
    You MUST output ONLY a valid JSON object strictly matching this schema, with no additional text, markdown backticks, or formatting:
    {{
      "target_role": "{target_role}",
      "steps": [
        "String: Specific learning milestone or skill to acquire (e.g., 'Learn advanced React patterns by Q2')",
        "String: Another step..."
      ],
      "video_recommendations": [
        "https://www.youtube.com/watch?v=example1",
        "https://www.youtube.com/watch?v=example2"
      ]
    }}
    
    Ensure the `video_recommendations` are valid URLs (preferably YouTube crash courses or tutorials relevant to the missing skills).
    """

    user_prompt = "Generate my personalized JSON roadmap."

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        print(f"Error generating roadmap via Groq: {e}")
        # Fallback payload in case of failure
        return {
            "target_role": target_role,
            "steps": [
                "Master Data Structures and Algorithms",
                f"Learn core skills for {target_role}",
                "Build 2-3 impressive portfolio projects"
            ],
            "video_recommendations": [
                "https://www.youtube.com/watch?v=8hly31xKli0"
            ]
        }
