from typing import Optional

from fastapi import UploadFile

from app.schemas.mood import (
    TextMoodRequest,
    MoodResponse,
    MultimodalMoodResponse,
    SupportMode,
)
from app.services.bedrock_client import bedrock_client
from app.services.memory import memory_store
from app.services.admin_storage import admin_storage
from app.core.config import get_settings


async def _select_mode(risk_score: float, dominant_mood: str) -> SupportMode:
    if risk_score >= 0.6:
        return SupportMode.CRISIS_AWARE
    if dominant_mood in {"sad", "anxious", "overwhelmed"}:
        return SupportMode.CALMING
    if dominant_mood in {"tired", "exhausted"}:
        return SupportMode.STABILITY
    if dominant_mood in {"neutral"}:
        return SupportMode.LISTENING
    return SupportMode.MOTIVATION


async def analyze_text_mood(request: TextMoodRequest, admin_password: Optional[str] = None) -> MoodResponse:
    # Use Bedrock for mood analysis
    prompt = f"Analyze the mood of this text: \"{request.text}\". Return JSON with: dominant_mood, energy_level, stability, risk_score (0-1)."
    mood_data = await bedrock_client.analyze_multimodal(prompt)
    
    mood_state = MoodState(
        dominant_mood=mood_data.get("dominant_mood", "neutral"),
        energy_level=mood_data.get("energy_level", "medium"),
        stability=mood_data.get("stability", "stable"),
        risk_score=mood_data.get("risk_score", 0.1)
    )
    
    # Simple keyword check for crisis (can be moved to Bedrock prompt)
    from app.services.text_emotion import CRISIS_KEYWORDS
    crisis_hits = [w for w in CRISIS_KEYWORDS if w in request.text.lower()]
    
    from app.services.safety import compute_risk_flags
    risk = compute_risk_flags(mood_state, crisis_hits)
    mode = await _select_mode(risk.risk_score, mood_state.dominant_mood)

    # Get conversation history
    conversation_id = request.conversation_id or "default"
    history = await memory_store.get_conversation_history(conversation_id, max_messages=10)

    # Generate response
    from app.services.llm_client import SYSTEM_PROMPT_BASE, _mode_instructions, _summarize_mood
    system_prompt = SYSTEM_PROMPT_BASE + "\n\n" + _mode_instructions(mode, risk.is_crisis)
    system_prompt += f"\n\nContext: {_summarize_mood(mood_state)}"
    
    formatted_history = []
    if history:
        for msg in history:
            formatted_history.append({"role": msg["role"], "content": [{"type": "text", "text": msg["content"]}]})
            
    messages = formatted_history + [{"role": "user", "content": [{"type": "text", "text": request.text}]}]

    response_text = await bedrock_client.generate_response(system_prompt, messages)

    # Check if admin
    settings = get_settings()
    is_admin = (admin_password or request.admin_password) == settings.ADMIN_PASSWORD if settings.ADMIN_PASSWORD else False
    
    mood_dict = mood_state.model_dump()
    mode_str = mode.value
    
    if is_admin:
        admin_storage.save_admin_conversation(request.text, response_text)
    else:
        await memory_store.save_message(conversation_id, "user", request.text, mood_dict, mode_str)
        await memory_store.save_message(conversation_id, "assistant", response_text, mood_dict, mode_str)

    return MoodResponse(response_text=response_text, mood_state=mood_state, mode=mode, risk=risk)


async def analyze_multimodal_mood(
    text: Optional[str],
    face_image: Optional[UploadFile],
    voice_audio: Optional[UploadFile],
    conversation_id: Optional[str],
    admin_password: Optional[str] = None,
) -> MultimodalMoodResponse:
    text_content = text.strip() if text and text.strip() else ""
    image_bytes = await face_image.read() if face_image else None
    
    # Use Bedrock for multimodal analysis
    prompt = "Analyze this user's state. "
    if text_content:
        prompt += f"User said: \"{text_content}\". "
    prompt += "Analyze facial expression if image provided. Return JSON with: dominant_mood, energy_level, stability, risk_score (0-1)."
    
    mood_data = await bedrock_client.analyze_multimodal(prompt, image_bytes)
    
    mood_state = MoodState(
        dominant_mood=mood_data.get("dominant_mood", "neutral"),
        energy_level=mood_data.get("energy_level", "medium"),
        stability=mood_data.get("stability", "stable"),
        risk_score=mood_data.get("risk_score", 0.1)
    )

    from app.services.text_emotion import CRISIS_KEYWORDS
    crisis_hits = [w for w in CRISIS_KEYWORDS if w in text_content.lower()]
    
    from app.services.safety import compute_risk_flags
    risk = compute_risk_flags(mood_state, crisis_hits)
    mode = await _select_mode(risk.risk_score, mood_state.dominant_mood)

    # Get conversation history
    conv_id = conversation_id or "default"
    history = await memory_store.get_conversation_history(conv_id, max_messages=10)

    # Generate response
    from app.services.llm_client import SYSTEM_PROMPT_BASE, _mode_instructions, _summarize_mood
    system_prompt = SYSTEM_PROMPT_BASE + "\n\n" + _mode_instructions(mode, risk.is_crisis)
    system_prompt += f"\n\nContext: {_summarize_mood(mood_state)}"
    
    formatted_history = []
    if history:
        for msg in history:
            formatted_history.append({"role": msg["role"], "content": [{"type": "text", "text": msg["content"]}]})
            
    messages = formatted_history + [{"role": "user", "content": [{"type": "text", "text": text_content if text_content else "User shared nonverbal signals."}]}]

    response_text = await bedrock_client.generate_response(system_prompt, messages)

    # Check if admin
    settings = get_settings()
    is_admin = admin_password == settings.ADMIN_PASSWORD if settings.ADMIN_PASSWORD else False
    
    mood_dict = mood_state.model_dump()
    mode_str = mode.value
    
    if is_admin and text_content:
        admin_storage.save_admin_conversation(text_content, response_text)
    elif text_content:
        await memory_store.save_message(conv_id, "user", text_content, mood_dict, mode_str)
        await memory_store.save_message(conv_id, "assistant", response_text, mood_dict, mode_str)

    return MultimodalMoodResponse(
        response_text=response_text,
        mood_state=mood_state,
        mode=mode,
        risk=risk,
        has_text=bool(text_content),
        has_face=image_bytes is not None,
        has_voice=voice_audio is not None,
    )


