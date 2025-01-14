# rl_agent/views.py

from apps.nba.serializers import GameSerializer, StandingTeamSerializer
from apps.nba.utils import (get_live_games, get_current_season)
from apps.nba.proxy_management import valid_proxies
from apps.nba.models import Game, StandingTeam, Conference

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Max, Min
from datetime import datetime
import pytz
from urllib.parse import urlencode

eastern = pytz.timezone('US/Eastern')


class GetGameList(APIView):
    def get(self, request):
        date = request.GET.get("date")
        try:
            if date:
                date = datetime.strptime(date, '%Y-%m-%d')
            else: date = datetime.today()
        except:
            return Response({"error": "date must be in following format: yyyy-mm-dd"},
                            status=status.HTTP_400_BAD_REQUEST)


        query_params = request.GET.copy()

        games = Game.objects.select_related('home_team', 'away_team') \
            .filter(game_date__date=date.date()).order_by("game_date")
        
        prev_game_datetime = Game.objects\
                .filter(game_date__date__lt=date.date())\
                .aggregate(Max('game_date'))['game_date__max']
        next_game_datetime = Game.objects\
                .filter(game_date__date__gt=date.date())\
                .aggregate(Min('game_date'))['game_date__min']
        
        prev_link = None
        if prev_game_datetime:
            query_params['date'] = prev_game_datetime.strftime("%Y-%m-%d")
            prev_link = request.build_absolute_uri(f"{request.path}?{urlencode(query_params)}")
        next_link = None
        if next_game_datetime:
            query_params['date'] = next_game_datetime.strftime("%Y-%m-%d")
            next_link = request.build_absolute_uri(f"{request.path}?{urlencode(query_params)}")
        
        live_games = get_live_games()
        serializer = GameSerializer(games, many=True, context={'live_games': live_games})
        data = serializer.data
        return Response({
            "prev_link": prev_link,
            "next_link": next_link,
            "data": data
        }, status=status.HTTP_200_OK)
    
class GetStanding(APIView):
    def get(self, request):
        current_season = get_current_season()
        
        east_standings = StandingTeam.objects.\
            filter(year=current_season, conference=Conference.EAST).order_by('rank')
        west_standings = StandingTeam.objects \
            .filter(year=current_season, conference=Conference.WEST).order_by('rank')

        # Serialize the data
        serializer_east = StandingTeamSerializer(east_standings, many=True)
        serializer_west = StandingTeamSerializer(west_standings, many=True)

        # Structure the response
        response_data = {
            'east': serializer_east.data,
            'west': serializer_west.data
        }
        return Response(response_data)
    
class TEST(APIView):
    def get(self, request):
        return Response(valid_proxies)
    

class LiveGameInformationSSE(APIView):
    def get(self, request):
        live_games = get_live_games()
        return Response(live_games)