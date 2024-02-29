import requests
import os
from typing import Optional, Dict

from django.core.files import File

CMA_API_TOKEN_HEADER= None
CMA_API_ENDPOINT= None

def extract_info_via_api(file_obj: File=None, local: bool = False, chunk_size: int = 1000, sentence_cut_percentage: float = 25):
    if local:
        CMA_API_TOKEN_HEADER= os.environ.get("CMA_API_TOKEN_HEADER_LOCAL")
        CMA_API_ENDPOINT= os.environ.get("CMA_API_ENDPOINT_LOCAL")
    else:
        CMA_API_TOKEN_HEADER= os.environ.get("CMA_API_TOKEN_HEADER")
        CMA_API_ENDPOINT= os.environ.get("CMA_API_ENDPOINT")

    data = {}

    if CMA_API_TOKEN_HEADER is None:
        return data

    if CMA_API_ENDPOINT is None:
        return data

    if file_obj is None:
        return data
    
    # Check file extension
    allowed_extensions = ('.txt', '.pdf', '.doc', '.docx')
    file_extension = os.path.splitext(file_obj.name)[1].lower()

    if file_extension not in allowed_extensions:
        return data

    headers = {
        "Authorization": f"Bearer {CMA_API_TOKEN_HEADER}",
        "Chunk-Size": str(chunk_size),
        "Sentence-Cut-Percentage": str(sentence_cut_percentage)
    }

    with file_obj.open('rb') as f:
        r = requests.post(CMA_API_ENDPOINT, files={"file": f}, headers=headers)
        if r.status_code in range(200, 299):
            if r.headers.get("content-type") == 'application/json':
                data = r.json()
    return data

def ask_chat_via_api(question: str = None, chat_data: Optional[Dict] = None, local: bool = False, modelChoice: str = ""):
    if local:
        CMA_API_TOKEN_HEADER= os.environ.get("CMA_API_TOKEN_HEADER_LOCAL")
        CMA_API_ENDPOINT= os.environ.get("CMA_API_ENDPOINT_LOCAL")
    else:
        CMA_API_TOKEN_HEADER= os.environ.get("CMA_API_TOKEN_HEADER")
        CMA_API_ENDPOINT= os.environ.get("CMA_API_ENDPOINT")

    CMA_API_ENDPOINT = ''.join([CMA_API_ENDPOINT,"chat/"])

    data = {}

    if CMA_API_TOKEN_HEADER is None:
        return data

    if CMA_API_ENDPOINT is None:
        return data

    if chat_data is None:
        return data

    headers = {
        "Authorization": f"Bearer {CMA_API_TOKEN_HEADER}",
        "modelChoice": modelChoice,
    }

    history = chat_data.get('history')
    chatContext = chat_data.get('context')

    context = '\n'.join([history, chatContext])

    requestData = {
        "question":question,
        "context":context,
    }

    try:
        r = requests.post(CMA_API_ENDPOINT, json=requestData, headers=headers)

        if r.status_code in range(200, 299):
            if r.headers.get("content-type") == 'application/json':
                data = r.json()

        return data
        
    except requests.exceptions.RequestException as e:
        return data
