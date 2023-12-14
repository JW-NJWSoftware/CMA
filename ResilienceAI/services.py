import requests
import os

from django.core.files import File

CMA_API_TOKEN_HEADER= None
CMA_API_ENDPOINT= None

def extract_info_via_api(file_obj: File=None, local = False):
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
    
    headers = {
        "Authorization": f"Bearer {CMA_API_TOKEN_HEADER}"
        }

    with file_obj.open('rb') as f:
        r = requests.post(CMA_API_ENDPOINT, files={"file": f}, headers=headers)
        if r.status_code in range(200, 299):
            if r.headers.get("content-type") == 'application/json':
                data = r.json()

    return data