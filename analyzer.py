import anthropic
import dotenv
import json
import base64
import re
import prompts

from typing import Dict, Any, Optional
from pydantic import BaseModel, ValidationError
from datetime import datetime
from receipt_objects import ReceiptItem, ReceiptData

class ReceiptAnalyzer: 
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.max_retries = 2
        self.model = "claude-sonnet-4-20250514"
    
    def encode_image(self, image_path: str) -> str:
        """Convert image to base64 for API"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def analyze_receipt(self, image_path:str) -> Optional[ReceiptData]:               
        try:
            image_data = self.encode_image(image_path)
        except Exception as e:
            print(f"Error encoding image: {e}")
            return None

        # Get image type
        image_type = "image/jpeg" if image_path.lower().endswith('.jpg') or image_path.lower().endswith('.jpeg') else "image/png"

        # Define the tool for structured output using Pydantic schema
        extract_receipt_tool = {
           
        }

        try:
            response = self.client.messages.create(
                model = self.model,
                max_tokens = 4000,
                tools = [
                    {
                        "name": "extract_receipt_data",
                        "description": "Extract structured receipt data from the receipt image",
                        "input_schema": ReceiptData.model_json_schema()
                    }
                ],
                tool_choice = {"type": "tool", "name": "extract_receipt_data"},
                messages= [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompts.receipt_analysis_prompt
                            },
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": image_type,
                                    "data": image_data
                                }
                            }
                        ]
                    }
                ]
            )

            # Extract tool use from response
            if response.content and len(response.content) > 0:
                for content_block in response.content:
                    if content_block.type == "tool_use":
                        receipt_dict = content_block.input
                        receipt_data = ReceiptData(**receipt_dict)
                        return receipt_data

        except ValidationError as e:
            print(f"Validation error: {e}")

        except Exception as e:
            print(f"Unexpected error: {e}")

        print("Failed to analyze the receipt")
        return None
    

