from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import ScoreboardV2
from nba_api.stats.endpoints import leaguestandings
from nba_api.stats.static import teams

from django.templatetags.static import static

from datetime import datetime, timedelta
import pytz
from django.utils.timezone import make_aware, is_naive
import json

eastern = pytz.timezone('US/Eastern')


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

def process_scoreboard_game(data):
    '''
    process the data:
    scoreboard = ScoreboardV2(game_date=game_date_str, league_id='00', day_offset=0)
    data = scoreboard.get_normalized_dict()
    '''
    games = {}

    standing = {}
    for s in data["EastConfStandingsByDay"] + data["WestConfStandingsByDay"]:
        wins = s["W"]
        losses = s["L"]
        standing[s["TEAM_ID"]] = f"{wins}-{losses}"
    
    team_info = get_team_information()

    for game_header in data["GameHeader"]:
        game_id = game_header["GAME_ID"]
        home_team_id = game_header["HOME_TEAM_ID"]
        away_team_id = game_header["VISITOR_TEAM_ID"]
        game_date = game_header["GAME_DATE_EST"]
        parsed_game_date = datetime.strptime(game_date, "%Y-%m-%dT%H:%M:%S")
        formatted_game_date = parsed_game_date.strftime("%d/%m/%Y")
        game_status = game_header["GAME_STATUS_TEXT"]
        is_future_game = game_header["GAME_STATUS_ID"] == 1
        games[game_id] = games.get(game_id, {})
        games[game_id]["home_team_id"] = home_team_id
        games[game_id]["away_team_id"] = away_team_id
        games[game_id]["game_date"] = formatted_game_date
        games[game_id]["game_status"] = game_status
        games[game_id]["is_future_game"] = is_future_game
    
    for linescore in data["LineScore"]:
        game_id = linescore["GAME_ID"]
        is_game_ended = games[game_id]["game_status"] == "Final"
        team_id = linescore["TEAM_ID"]
        team_name = linescore["TEAM_NAME"]
        team_name = linescore["TEAM_NAME"]
        # team_wins_losses = linescore["TEAM_WINS_LOSSES"]
        team_wins_losses = standing[team_id] if is_game_ended else None
        qtr_points = []
        for qtr in [f"PTS_QTR{i}" for i in range(1, 5)] + [f"PTS_OT{i}" for i in range(1, 11)]:
            if linescore[qtr] is None or linescore[qtr] == 0: break
            qtr_points.append(linescore[qtr])
        point = linescore["PTS"]
        home_or_away = "home_team_info" if team_id == games[game_id]["home_team_id"] else "away_team_info"
        games[game_id][home_or_away] = {}
        games[game_id][home_or_away]["team_id"] = team_id
        games[game_id][home_or_away]["team_full_name"] = team_info[team_id]["full_name"]
        games[game_id][home_or_away]["team_abbr_name"] = team_info[team_id]["abbreviation"]
        games[game_id][home_or_away]["logo"] = team_info[team_id]['logo']
        games[game_id][home_or_away]["team_name"] = team_name
        games[game_id][home_or_away]["team_wins_losses"] = team_wins_losses
        games[game_id][home_or_away]["qtr_points"] = qtr_points
        games[game_id][home_or_away]["point"] = point
    
    result = []
    for game_id, game_info in games.items():
        game_data = {
            "game_id": game_id,
            "game_date": game_info["game_date"],
            "game_status": game_info["game_status"],
            "is_future_game": game_info["is_future_game"],
            "home_team_info": game_info["home_team_info"],
            "away_team_info": game_info["away_team_info"],
        }
        result.append(game_data)

    return result

        

def get_first_1_day_of_past_given_date_games(date):

    for day_delta in range(1, 8):
        current_date = date + timedelta(days=-day_delta)
        game_date_str = current_date.strftime('%m/%d/%Y')
        score_board = ScoreboardV2(game_date=game_date_str, league_id='00', day_offset=0)
        data = score_board.get_normalized_dict()
        return process_scoreboard_game(data), current_date
    
def get_first_1_day_of_future_given_date_games(date):
    for day_delta in range(1, 8):
        current_date = date + timedelta(days=day_delta)
        game_date_str = current_date.strftime('%m/%d/%Y')
        score_board = ScoreboardV2(game_date=game_date_str, league_id='00', day_offset=0)

        data = score_board.get_normalized_dict()
        return process_scoreboard_game(data), current_date

def get_today_games():

    current_date = utc_to_et(datetime.today())

        
    game_date_str = current_date.strftime('%m/%d/%Y')
    score_board = ScoreboardV2(game_date=game_date_str, league_id='00', day_offset=0)

    data = score_board.get_normalized_dict()
    data = process_scoreboard_game(data)
    live_games = get_live_games()
    for i in range(len(data)):
        if data[i]["game_id"] in live_games:
            data[i] = live_games[data[i]["game_id"]]
    return data

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

    standings_endpoint = leaguestandings.LeagueStandings(
        league_id='00',
        season=get_current_season(),
        season_type='Regular Season'  
    )

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