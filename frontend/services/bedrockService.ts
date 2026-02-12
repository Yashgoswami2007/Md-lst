import { MoodState, SupportMode } from "../types";

const BASE_URL = (import.meta as any).env?.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export const analyzeMultimodalMood = async (
    text?: string,
    imageBuffer?: string,
    audioBuffer?: string,
    history: { role: 'user' | 'assistant'; content: string }[] = []
): Promise<{ mood_state: MoodState; mode: SupportMode; response: string }> => {
    try {
        const formData = new FormData();
        if (text) formData.append('text', text);

        if (imageBuffer) {
            // Convert base64 to blob
            const byteCharacters = atob(imageBuffer);
            const byteNumbers = new Array(byteCharacters.length);
            for (let i = 0; i < byteCharacters.length; i++) {
                byteNumbers[i] = byteCharacters.charCodeAt(i);
            }
            const byteArray = new Uint8Array(byteNumbers);
            const blob = new Blob([byteArray], { type: 'image/jpeg' });
            formData.append('face_image', blob, 'face.jpg');
        }

        if (audioBuffer) {
            const byteCharacters = atob(audioBuffer);
            const byteNumbers = new Array(byteCharacters.length);
            for (let i = 0; i < byteCharacters.length; i++) {
                byteNumbers[i] = byteCharacters.charCodeAt(i);
            }
            const byteArray = new Uint8Array(byteNumbers);
            const blob = new Blob([byteArray], { type: 'audio/webm' });
            formData.append('voice_audio', blob, 'voice.webm');
        }

        const response = await fetch(`${BASE_URL}/mood/multimodal`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Failed to analyze multimodal mood via backend");
        }

        const data = await response.json();

        return {
            mood_state: data.mood_state,
            mode: data.mode.toUpperCase() as SupportMode,
            response: data.response_text
        };
    } catch (error) {
        console.error("Bedrock Multimodal Analysis Error:", error);
        throw new Error("I couldn't process the emotional data right now. Please try again.");
    }
};

export const analyzeVoiceOnly = async (
    audioBuffer: string
): Promise<{ mood: string; transcription: string; confidence: number }> => {
    // Route voice-only analysis through the same multimodal endpoint
    // but just for transcription and mood
    try {
        const result = await analyzeMultimodalMood(undefined, undefined, audioBuffer);
        return {
            mood: result.mood_state.dominant_mood,
            transcription: "Voice analyzed via Bedrock", // Backend would need to provide transcription specifically if needed
            confidence: result.mood_state.risk_score // Placeholder
        };
    } catch (error) {
        console.error("Bedrock Voice Analysis Error:", error);
        throw new Error("I couldn't analyze the voice recording. Please try again.");
    }
};
