# MoodDoctor Design Document

MoodDoctor is an emotionally intelligent support companion that uses multi-modal sentiment analysis to provide wellness guidance and emotional support, built for the **AI for Bharat** hackathon.

## Architecture Overview

The system follows a modern client-server architecture optimized for AWS:

- **Frontend**: A React-based SPA (Single Page Application) that handles the user interface, real-time audio/video capture, and interactive chat.
- **Backend**: A FastAPI server that provides RESTful endpoints, manages authentication, and orchestrates AWS services.
- **Database**: MongoDB for storing user data, session archives, and safety plans.
- **AI Integration**:
    - **Amazon Bedrock**: The core AI engine providing multi-modal emotion detection (via models like Claude 3 / Llama 3) and conversational intelligence.
    - **AWS SDK (Boto3)**: Used for seamless integration with Bedrock and other AWS services.

## Technology Stack

### Frontend
- **Framework**: React 19 (Vite)
- **Language**: TypeScript
- **Styling**: Vanilla CSS / Tailwind-like utilities
- **Icons**: Lucide React
- **Visuals**: Recharts
- **Networking**: native Fetch API and AWS SDK (where applicable)

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.12+
- **Security**: JWT (Python-Jose), Passlib (Bcrypt)
- **AI Layer**: **Amazon Bedrock** (Amazon Web Services)
- **SDK**: `boto3` (AWS SDK for Python)

## Key Features

### 1. Multi-modal Sentiment Analysis
Detects emotional states by combining inputs from:
- **Text Analysis**: Natural language understanding using Amazon Bedrock.
- **Facial Expression Analysis**: Processing image frames via Bedrock multimodal models.
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
- **Streaming Responses**: Real-time response generation powered by Amazon Bedrock.

### 4. Safety Planning
Built-in features for users to document and access their personal safety plans during periods of high distress.

## Data Flow

1.  **Capture**: User provides text, records audio, or scans their face in the `MultimodalCapture` component.
2.  **Processing**: Data is sent to the backend, which invokes the **Amazon Bedrock** API.
3.  **Synthesis**: Bedrock models (Claude 3 / Llama 3) return the `mood_state`, recommended `support_mode`, and a therapeutic response.
4.  **Action**: The UI updates the background/mood indicator and the AI responds in the `ChatWindow`.
5.  **Persistence**: Messages and mood data are saved to MongoDB for future reference and dashboard analytics.

## Security & Privacy
- **Authentication**: JWT-based secure login.
- **Infrastructure**: Powered by AWS secure cloud infrastructure.
- **Data Privacy**: Conversations are stored securely; AI prompts focus on wellness without clinical diagnosis.
