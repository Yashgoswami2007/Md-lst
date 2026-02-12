import json
import boto3
from typing import List, Optional, Dict, Any
from botocore.exceptions import ClientError
from app.core.config import get_settings
from app.schemas.mood import MoodState, SupportMode

settings = get_settings()

class BedrockClient:
    def __init__(self):
        self.client = boto3.client(
            service_name='bedrock-runtime',
            region_name=settings.AWS_REGION or 'us-east-1',
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY
        )
        self.model_id = settings.BEDROCK_MODEL_ID or 'anthropic.claude-3-sonnet-20240229-v1:0'

    async def generate_response(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> str:
        """
        Generate a text response using Amazon Bedrock.
        """
        try:
            # Format for Claude 3
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "system": system_prompt,
                "messages": messages,
                "temperature": temperature,
            })

            response = self.client.invoke_model(
                body=body,
                modelId=self.model_id
            )

            response_body = json.loads(response.get('body').read())
            return response_body.get('content')[0].get('text')

        except ClientError as e:
            print(f"Bedrock Client Error: {e}")
            return "I'm having trouble connecting to my AI core right now. Please try again in a moment."
        except Exception as e:
            print(f"Bedrock Unexpected Error: {e}")
            return "An unexpected error occurred while generating a response."

    async def analyze_multimodal(
        self,
        prompt: str,
        image_bytes: Optional[bytes] = None,
        audio_bytes: Optional[bytes] = None
    ) -> Dict[str, Any]:
        """
        Perform multimodal analysis using Bedrock.
        Note: Current Bedrock multimodal models (like Claude 3) support image + text.
        Voice analysis might require Amazon Transcribe or separate processing if not directly supported by the model ID.
        """
        try:
            content = []
            
            if image_bytes:
                import base64
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_base64
                    }
                })
            
            content.append({
                "type": "text",
                "text": prompt
            })

            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                "temperature": 0
            })

            response = self.client.invoke_model(
                body=body,
                modelId=self.model_id
            )

            response_body = json.loads(response.get('body').read())
            result_text = response_body.get('content')[0].get('text')
            
            # Attempt to parse JSON from response
            try:
                start = result_text.find('{')
                end = result_text.rfind('}') + 1
                if start != -1 and end != 0:
                    return json.loads(result_text[start:end])
            except:
                pass
                
            return {"raw_response": result_text}

        except Exception as e:
            print(f"Bedrock Multimodal Error: {e}")
            return {}

bedrock_client = BedrockClient()
