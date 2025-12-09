from fastapi import Request, Form
from typing import Dict, Any
import urllib.parse
import json
import logging

logger = logging.getLogger(__name__)

class RequestParser:
    @staticmethod
    async def parse_request(request: Request) -> Dict[str, Any]:
        content_type = request.headers.get("content-type", "").lower()
        
        if "application/x-www-form-urlencoded" in content_type:
            try:
                body = await request.body()
                decoded_body = body.decode('utf-8')
                return dict(urllib.parse.parse_qsl(decoded_body))
            except (UnicodeDecodeError, ValueError) as e:
                logger.warning(f"Failed to decode form-urlencoded body: {e}")
                return {}
            
        elif "multipart/form-data" in content_type:
            try:
                form_data = await request.form()
                return dict(form_data)
            except Exception as e:
                logger.warning(f"Failed to parse multipart form data: {e}")
                return {}
            
        elif "application/json" in content_type:
            try:
                return await request.json()
            except Exception as e:
                logger.warning(f"Failed to parse JSON: {e}")
                return {}
            
        else:
            try:
                form_data = await request.form()
                return dict(form_data)
            except Exception as e:
                try:
                    return await request.json()
                except Exception as json_error:
                    logger.warning(f"Failed to parse request body: form={e}, json={json_error}")
                    return {}