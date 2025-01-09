# rl_agent/views.py

from apps.nba.utils import (get_first_1_day_of_past_given_date_games,
                            get_first_1_day_of_future_given_date_games,
                            get_today_games,
                            get_live_games,
                            get_current_standing,
                            utc_to_et,
                            et_to_utc)
from apps.nba.proxy_management import valid_proxies
from apps.restful_config.SSE_render import SSERenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime
import pytz
from django.utils.timezone import make_aware
from urllib.parse import urlencode

from django.http import StreamingHttpResponse
import time
import json

eastern = pytz.timezone('US/Eastern')


class GetGameList(APIView):
    def get(self, request):
        date = request.GET.get("date")
        timeline = request.GET.get("timeline", "today")
        
        if timeline not in ["past", "today", "future"]:
            return Response({"error": "timeline must be either past, today, or future"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        if timeline == "today":
            date = utc_to_et(datetime.today())
        else:
            try:
                date = utc_to_et(datetime.strptime(date, '%Y-%m-%d'))
            except:
                return Response({"error": "date must be in following format: yyyy-mm-dd"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        query_params = request.GET.copy()
        if timeline == "today":
            games = get_today_games()
            new_date = et_to_utc(date)
            query_params['date'] = new_date.strftime("%Y-%m-%d")
            
            query_params['timeline'] = 'past'
            prev_link = request.build_absolute_uri(f"{request.path}?{urlencode(query_params)}")
            
            query_params['timeline'] = 'future'
            next_link = request.build_absolute_uri(f"{request.path}?{urlencode(query_params)}")
        
        elif timeline == "past":
            games, new_date = get_first_1_day_of_past_given_date_games(date)
            new_date = et_to_utc(new_date)
            query_params['date'] = new_date.strftime("%Y-%m-%d")
            query_params['timeline'] = 'past'
            prev_link = request.build_absolute_uri(f"{request.path}?{urlencode(query_params)}")
            next_link = None
        
        else:  # timeline == "future"
            games, new_date = get_first_1_day_of_future_given_date_games(date)
            new_date = et_to_utc(new_date)
            query_params['date'] = new_date.strftime("%Y-%m-%d")
            query_params['timeline'] = 'future'
            prev_link = None
            next_link = request.build_absolute_uri(f"{request.path}?{urlencode(query_params)}")
        
        return Response({
            "prev_link": prev_link,
            "next_link": next_link,
            "data": games,
        })
    
class GetStanding(APIView):
    def get(self, request):
        standing = get_current_standing()
        return Response(standing)
    
class TEST(APIView):
    def get(self, request):
        return Response(valid_proxies)
    

class LiveGameInformationSSE(APIView):
    renderer_classes = [SSERenderer]
    
    def get(self, request):
        # Generator function for streaming data
        def event_stream():
            while True:
                live_games = get_live_games()
                yield f"data: {json.dumps(live_games)}\n\n"
                time.sleep(10)

        # Create and return a StreamingHttpResponse
        response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        return response