from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import ScoreboardV2
from nba_api.stats.endpoints import leaguestandings
from nba_api.stats.static import teams

from django.templatetags.static import static

from datetime import datetime, timedelta, date
import pytz
from django.utils.timezone import make_aware, is_naive
import json
import requests

from apps.nba.proxy_management import call_function_with_proxy

eastern = pytz.timezone('US/Eastern')
all_games_api = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2.json"

def utc_to_local(date):
    if is_naive(date):
        date = make_aware(date, pytz.utc)
    return date.astimezone(eastern)
def utc_to_et(date):
    if is_naive(date):
        date = make_aware(date, pytz.utc)
    return date.astimezone(eastern)
def et_to_utc(date):
    if is_naive(date):
        date = make_aware(date, eastern)
    return date.astimezone(pytz.utc)

def get_team_information():
    team_info = {}
    for team in teams.get_teams():
        logo_filename = team["full_name"].replace(" ", "")
        logo = static(f"assets/svg/nba_team_logo/{logo_filename}.svg")
        team_info[team["id"]] = {
            "full_name": team["full_name"],
            "abbreviation": team["abbreviation"],
            "logo": logo
        }
    return team_info


def process_game_information(raw_games):
    games = []
    team_info = get_team_information()
    for game_data in raw_games:

        game_date = game_data["gameDateTimeUTC"]
        parsed_game_date = datetime.strptime(game_date, "%Y-%m-%dT%H:%M:%SZ")
        formatted_game_date = parsed_game_date.strftime("%d/%m/%Y")

        game_info = {
            "game_id": game_data["gameId"],
            "game_date": formatted_game_date,
            "game_status": game_data["gameStatusText"],
            "is_future_game": game_data["gameStatus"] == 1,
        }

        for key, home_or_away in zip(["home_team_info", "away_team_info"], ["homeTeam", "awayTeam"]):
            game_info[key] = {}
            team_id = game_data[home_or_away]["teamId"]
            game_info[key]["team_id"] = team_id
            game_info[key]["team_full_name"] = team_info[team_id]["full_name"]
            game_info[key]["team_abbr_name"] = team_info[team_id]["abbreviation"]
            game_info[key]["logo"] = team_info[team_id]['logo']
            game_info[key]["team_name"] = game_data[home_or_away]["teamName"]
            wins = game_data[home_or_away]["wins"]
            losses = game_data[home_or_away]["losses"]
            game_info[key]["team_wins_losses"] = f"{wins}-{losses}"
            game_info[key]["qtr_points"] = []
            game_info[key]["point"] = game_data[home_or_away]["score"]
        games.append(game_info)
    return games
        
def get_all_games_given_date(date):
    if not date:
        raise Exception("date must be given")
    if not isinstance(date, datetime):
        raise Exception("date must be a datetime or date")
    
    response = requests.get(all_games_api)
    if response.status_code != 200:
        return []
    data = response.json()
    for games_by_date in data["leagueSchedule"]["gameDates"]:
        game_date = datetime.strptime(games_by_date["gameDate"], "%m/%d/%Y %H:%M:%S")
        if date.date() == game_date.date():
            return process_game_information(games_by_date["games"])
    return []

def get_first_1_day_of_past_given_date_games(date):
    
    for day_delta in range(1, 8):
        current_date = date + timedelta(days=-day_delta)
        return get_all_games_given_date(current_date), current_date
    
def get_first_1_day_of_future_given_date_games(date):
    for day_delta in range(1, 8):
        current_date = date + timedelta(days=day_delta)
        return get_all_games_given_date(current_date), current_date
      

def get_today_games():

    current_date = utc_to_et(datetime.today())
    return get_all_games_given_date(current_date), current_date
    

def get_live_games():
    score_board = scoreboard.ScoreBoard()

    data = score_board.get_dict()
    team_info = get_team_information()
    games = {}
    for game in data["scoreboard"]["games"]:
        game_info = {}
        game_info["game_id"] = game["gameId"]
        game_info["is_future_game"] = game["gameStatus"] == 1
        game_info["game_status"] = game["gameStatusText"]
        game_date = game["gameTimeUTC"]
        parsed_game_date = utc_to_et(datetime.strptime(game_date, "%Y-%m-%dT%H:%M:%SZ"))
        formatted_game_date = parsed_game_date.strftime("%d/%m/%Y")
        game_info["game_date"] = formatted_game_date

        game_info["home_team_info"] = {}
        team_id = game["homeTeam"]["teamId"]
        game_info["home_team_info"]["team_id"] = team_id
        game_info["home_team_info"]["team_full_name"] = team_info[team_id]["full_name"]
        game_info["home_team_info"]["team_abbr_name"] = team_info[team_id]["abbreviation"]
        game_info["home_team_info"]["logo"] = team_info[team_id]['logo']
        game_info["home_team_info"]["team_name"] = game["homeTeam"]['teamName']
        game_info["home_team_info"]["team_wins_losses"] = f"{game['homeTeam']['wins']}-{game['homeTeam']['losses']}"
        qtr_points = []
        for period in game['homeTeam']['periods']:
            qtr_points.append(period["score"])
        game_info["home_team_info"]["qtr_points"] = qtr_points
        game_info["home_team_info"]["point"] = game["homeTeam"]['score']

        game_info["away_team_info"] = {}
        team_id = game["awayTeam"]["teamId"]
        game_info["away_team_info"]["team_id"] = team_id
        game_info["away_team_info"]["team_full_name"] = team_info[team_id]["full_name"]
        game_info["away_team_info"]["team_abbr_name"] = team_info[team_id]["abbreviation"]
        game_info["away_team_info"]["logo"] = team_info[team_id]['logo']
        game_info["away_team_info"]["team_name"] = game["awayTeam"]['teamName']
        game_info["away_team_info"]["team_wins_losses"] = f"{game['awayTeam']['wins']}-{game['awayTeam']['losses']}"
        qtr_points = []
        for period in game['awayTeam']['periods']:
            qtr_points.append(period["score"])
        game_info["away_team_info"]["qtr_points"] = qtr_points
        game_info["away_team_info"]["point"] = game["awayTeam"]['score']
        
        games[game_info["game_id"]] = game_info
    return games
        
def get_current_season() -> str:
    today = datetime.today()
    current_year = today.year
    current_month = today.month
    
    # If it's October or later, the season starts this year.
    # Otherwise, it started last year.
    if current_month >= 10:
        season_start = current_year
    else:
        season_start = current_year - 1
    
    # The second half of the season format is just the last two digits
    # of the following year:
    season_end_yy = str(season_start + 1)[-2:]
    
    return f"{season_start}-{season_end_yy}"

def get_current_standing():
    standings_endpoint = call_function_with_proxy(
            lambda proxy: leaguestandings.LeagueStandings(
                league_id='00',
                season=get_current_season(),
                season_type='Regular Season',
                proxy=proxy,
                timeout=5
            )
        )
    
    if not standings_endpoint:
        return {}
    
    team_info = get_team_information()

    teams = []
    raw_data = standings_endpoint.get_dict()
    headers = raw_data["resultSets"][0]["headers"]
    rowset = raw_data["resultSets"][0]["rowSet"]
    for row in rowset:
        data = {}
        for header, info in zip(headers, row):
            data[header] = info
        teams.append(data)

    standings = {}
    for team in teams:
        conference = team["Conference"].lower()
        standings[conference] = standings.get(conference, [])
        team_standing = {}
        team_standing["team_id"] = team["TeamID"]
        team_standing["team_name"] = team["TeamName"]
        team_standing["team_logo"] = team_info[team["TeamID"]]["logo"]
        team_standing["rank"] = team["PlayoffRank"]
        team_standing["pct"] = team["WinPCT"]
        team_standing["wins"] = team["WINS"]
        team_standing["losses"] = team["LOSSES"]
        team_standing["home"] = team["HOME"]
        team_standing["away"] = team["ROAD"]
        team_standing["ll10"] = team["L10"]
        standings[conference].append(team_standing)
    return standings

