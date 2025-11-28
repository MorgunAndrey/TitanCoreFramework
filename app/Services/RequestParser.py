from fastapi import Request, Form
from typing import Dict, Any
import urllib.parse
import json

class RequestParser:
    @staticmethod
    async def parse_request(request: Request) -> Dict[str, Any]:
        content_type = request.headers.get("content-type", "").lower()
        
        if "application/x-www-form-urlencoded" in content_type:
            body = await request.body()
            decoded_body = body.decode('utf-8')
            return dict(urllib.parse.parse_qsl(decoded_body))
            
        elif "multipart/form-data" in content_type:
            form_data = await request.form()
            return dict(form_data)
            
        elif "application/json" in content_type:
            return await request.json()
            
        else:
            try:
                form_data = await request.form()
                return dict(form_data)
            except:
                try:
                    return await request.json()
                except:
                    return {}