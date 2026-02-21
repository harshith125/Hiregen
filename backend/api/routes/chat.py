from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Optional
from core.llm import groq_client

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    reply: str

SYSTEM_PROMPT = """
You are the "HIREGEN Career Assistant", a highly specialized AI advisor designed to help B.Tech students navigate their careers.

Your expertise includes:
1. Placements and Internships
2. Interview Preparation (technical and HR)
3. Resume building and coding skills (DSA, Development, etc.)

Rules:
- Be encouraging, concise, and highly actionable.
- Do NOT answer questions that are completely unrelated to careers, academics, coding, or college success. If asked an off-topic question, politely steer the conversation back to career preparation.
- Keep your answers formatted nicely using markdown (bullet points, bold text).
"""

@router.post("/", response_model=ChatResponse)
async def chat_with_assistant(request: ChatRequest):
    """
    Conversational endpoint for the HIREGEN Career Assistant.
    """
    # Build the message array starting with the system prompt
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Append the history provided by the client
    if request.history:
         messages.extend([{"role": msg.role, "content": msg.content} for msg in request.history])
    
    # Append the current user message
    messages.append({"role": "user", "content": request.message})
    
    try:
        response = await groq_client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_completion_tokens=1024
        )
        
        reply_content = response.choices[0].message.content
        return ChatResponse(reply=reply_content)
        
    except Exception as e:
        print(f"Chat error: {e}")
        return ChatResponse(reply="I'm sorry, I am currently experiencing technical difficulties connecting to my servers. Please try again later.")
