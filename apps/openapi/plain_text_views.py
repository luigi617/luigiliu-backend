
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core.cache import cache
from rest_framework import renderers

from datetime import datetime, timedelta


def set_text_page_ids(ids):
    cache.set("text_page_ids", ids, timeout=None)

def get_available_text_page_ids():
    text_page_ids = cache.get("text_page_ids", [])
    text_page_available_ids = []
    for text_page_id in text_page_ids:
        if not cache.get(f"text_page_{text_page_id}", None): continue
        text_page_available_ids.append(text_page_id)
    set_text_page_ids(text_page_available_ids)
    return text_page_available_ids




class GetAllTextPageAPIView(APIView):

    def get(self, request):
        text_page_available_ids = get_available_text_page_ids()
        response = {
            "status": "success",
            "message": f"Current available text page ids are: {text_page_available_ids}",
            "text_page_available_ids": text_page_available_ids
        }
        return Response(response)
    
class CreateTextPageAPIView(APIView):

    def post(self, request):
        text = request.data.get("text")
        if not text:
            response = {
                "status": "error",
                "message": f"parameter 'text' cannot be empty"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        text_page_ids = get_available_text_page_ids()
        new_text_page_id = max(text_page_ids) + 1 if text_page_ids else 0
        text_page_ids.append(new_text_page_id)
        set_text_page_ids(text_page_ids)

        text_page_info = {
            "text_page_info": {
                "id": new_text_page_id,
                "time_created": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            },
            "text": text
        }
        cache.set(f"text_page_{new_text_page_id}", text_page_info, timeout=86400)
        text_page_info_url = request.build_absolute_uri(f"/openapi/text_page/{new_text_page_id}/")
        response = {
            "status": "success",
            "message": f"New text page has been created, use {text_page_info_url} to access information",
            "text_page_id": new_text_page_id
        }
        return Response(response)
    
class TextPageInfoAPIView(APIView):

    def get(self, request, text_page_id):
        text_page_info = cache.get(f"text_page_{text_page_id}")
        if text_page_info is None:
            text_page_creation_url = request.build_absolute_uri(f"/openai/text_page/create/")
            response = {
                "status": "error",
                "message": f"this text page id is not valid, please input a valid one or create a new one in {text_page_creation_url}"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        response = {
            "status": "success",
            "result": text_page_info
        }
        return Response(response)



class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        return data.encode(self.charset)
    
class TextPageAPIView(APIView):
    renderer_classes=[PlainTextRenderer]
    def get(self, request, text_page_id):
        text_page_info = cache.get(f"text_page_{text_page_id}")
        if text_page_info is None:
            text_page_creation_url = request.build_absolute_uri(f"/openai/text_page/create/")
            response = {
                "status": "error",
                "message": f"this text page id is not valid, please input a valid one or create a new one in {text_page_creation_url}"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        response = text_page_info["text"]
        return Response(response)