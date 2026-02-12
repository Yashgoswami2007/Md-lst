# AI for Bharat Hackathon: Requirements & Submission

## 1. Problem Statement
Mental health issues are often undetected due to social stigma and lack of accessible, real-time emotional support. Traditional therapy can be expensive and intimidating. There is a need for a "Private Sanctuary" where users can express themselves freely and receive immediate, AI-guided support that understands their emotions through text, voice, and facial expressions.

## 2. Proposed Solution: MoodDoctor
MoodDoctor is an AI-powered emotional support companion built for the Indian community. It uses **Amazon Bedrock** to perform multi-modal sentiment analysis, providing a safe space for users to manage their mental well-being.

### Key Capabilities:
- **Multi-modal Detection**: Analyzes text, voice tone, and facial expressions to get a holistic view of the user's mood.
- **Adaptive Support**: Switches between listening, calming, and motivational modes based on real-time emotional biometric data.
- **Crisis Prevention**: Integrates safety protocols for high-risk emotional states.

## 3. Tech Stack & AWS Services
- **AI Core**: **Amazon Bedrock** (using Claude 3 Sonnet and Llama 3 models for high-accuracy sentiment analysis).
- **Frontend**: React 19, Vite, TypeScript, Recharts.
- **Backend**: FastAPI (Python), Boto3 (AWS SDK).
- **Database**: MongoDB for session management and user progress tracking.

## 4. Unique Selling Proposition (USP)
Unlike standard chatbots, MoodDoctor is **multi-modal first**. It doesn't just read what you type; it "sees" your expression and "hears" your tone, allowing for a much deeper and more empathetic support experience that aligns with the "AI for Bharat" vision of building impactful, real-world solutions.

## 5. Process Flow
1. **Input**: User interacts via chat, camera, or microphone.
2. **Analysis**: Data is sent to the FastAPI backend.
3. **Inference**: Backend invokes **Amazon Bedrock** multimodal models.
4. **Response**: AI provides empathetic feedback and suggests wellness actions.
5. **Tracking**: User progress is stored and visualized in the personal dashboard.




# MoodDoctor Design Document

MoodDoctor is an emotionally intelligent support companion that uses multi-modal sentiment analysis to provide wellness guidance and emotional support.

## Architecture Overview

The system follows a modern client-server architecture:

- **Frontend**: A React-based SPA (Single Page Application) that handles the user interface, real-time audio/video capture, and interactive chat.
- **Backend**: A FastAPI server that provides RESTful endpoints, manages authentication, integrates with AI services, and handles data persistence.
- **Database**: MongoDB for storing user data, session archives, and safety plans. Supabase is also used for specific cloud-related features or as an alternative auth/data layer.
- **AI Integration**:
    - **Google Gemini**: Primary driver for multi-modal emotion detection (text, image, audio) and conversational intelligence.
    - **Groq/OpenRouter**: Fallback or specialized LLMs for faster or alternative response generation.

## Technology Stack

### Frontend
- **Framework**: React 19 (Vite)
- **Language**: TypeScript
- **Styling**: Vanilla CSS (based on modular structure) / Tailwind-like utilities
- **Icons**: Lucide React
- **Visuals**: Recharts (for mood tracking analytics)
- **Networking**: native Fetch API with modular service wrappers

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.12+
- **Database Driver**: Motor (Asynchronous MongoDB)
- **Security**: JWT (Python-Jose), Passlib (Bcrypt)
- **AI SDKs**: `google-generativeai`, `groq`

## Key Features

### 1. Multi-modal Sentiment Analysis
Detects emotional states by combining inputs from:
- **Text Analysis**: Natural language understanding of user messages.
- **Facial Expression Analysis**: Processing image frames captured via webcam.
- **Voice Tone Analysis**: Analyzing audio recordings for pitch and energy.

### 2. Emotionally Adaptive Support
MoodDoctor adjusts its "Support Mode" based on the detected mood:
- **LISTENING**: Reflective and empathetic.
- **CALMING**: Grounding exercises for anxiety.
- **MOTIVATION**: Encouraging small, achievable actions.
- **STABILITY**: Focus on routines to reduce overwhelm.
- **CRISIS_AWARE**: Essential safety protocols for high-risk situations.

### 3. Therapy Sanctuary (Chat)
A secure environment for real-time interaction with the AI, featuring:
- **Session Archiving**: Encrypted storage of past conversations.
- **Biometric Sync**: Visual feedback of detected emotional states during chat.
- **Streaming Responses**: Real-time response generation for a fluid experience.

### 4. Safety Planning
Built-in features for users to document and access their personal safety plans during periods of high distress.

## Data Flow

1.  **Capture**: User provides text, records audio, or scans their face in the `MultimodalCapture` component.
2.  **Processing**: The `geminiService` (or backend pipeline) sends the data to Gemini 1.5 Flash.
3.  **Synthesis**: The model returns the `mood_state`, recommended `support_mode`, and a therapeutic response.
4.  **Action**: The UI updates the background/mood indicator and the AI responds in the `ChatWindow`.
5.  **Persistence**: Messages and mood data are saved to MongoDB for future reference and dashboard analytics.

## Security & Privacy
- **Authentication**: JWT-based secure login.
- **Data Privacy**: Conversations are stored securely; AI prompts focus on wellness without clinical diagnosis.
- **Guest Access**: Option to use core features without full registration.
