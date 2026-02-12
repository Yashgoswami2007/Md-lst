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
