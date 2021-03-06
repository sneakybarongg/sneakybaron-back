import json
import urllib
import os

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Summoner
from riotwatcher import RiotWatcher, ApiError
from .helpers.ApiConnector import ApiConnector
from .helpers.PlayerBehavior import PlayerBehavior
from .helpers.PlayerData import *


# Create your views here.
def get_stream_widget(request, code):
    summoner = get_object_or_404(Summoner, url=code)

    region = summoner.region_value
    summoner_name = summoner.summoner_name

    connector  = ApiConnector(region, os.getenv('RIOT_API_KEY'))
    behavior_helper = PlayerBehavior()

    rank_to_number = {
        'I':'1',
        'II':'2',
        'III':'3',
        'IV':'4',
    }

    summoner_obj = connector.get_summoner_by_name(summoner_name)
    league = connector.get_league_by_account_id(summoner_obj['id'])

    total_games = league['wins'] + league['losses']
    win_rate = round(league['wins']*100/total_games)

    #TODO: Traer la matchlist de la base o de la api dependiendo si existe. INEFICIENTE. para implementar kda
    #matchlist =  connector.get_last_games_by_account_id(summoner['accountId'], 5)
    #stats = behavior_helper.get_stats_for_matchlist(connector, summoner, matchlist)

    summoner_info = {
        'tier':league['tier'].lower(),
        'rank':league['rank'],
        'rank_number':rank_to_number[league['rank']],
        'league_points':league['leaguePoints'],
        'wins':league['wins'],
        'losses':league['losses'],
        'win_rate': win_rate,
        'wins': league['wins'],
        'losses': league['losses'],
        'hot_streak': league['hotStreak'],
        }

    if 'miniSeries' in league:
        summoner_info['mini_series'] = league['miniSeries']['progress']
    else:
        summoner_info['mini_series'] = False

    return render(request, 'widget.html', context={'summoner_info':summoner_info,})

def get_patch_info(request, patch, language):
    with urllib.request.urlopen("https://sneaky-static-data.s3.us-east-2.amazonaws.com/parches/{}/{}.json".format(language, patch)) as patch_file:
        patch_json = json.loads(patch_file.read())
        return JsonResponse(patch_json)

def get_new_widget(request):
    if request.method == 'POST':
        summoner_name = request.POST.get('summoner-name')
        region = request.POST.get('region')
        try:
            summoner = get_object_or_404(Summoner, summoner_name = summoner_name, region_value = region)
            return HttpResponse(summoner.url_pretty())
        except:
            summoner = Summoner(summoner_name = summoner_name, region_value = region)
            return JsonResponse({'widget-url': summoner.url_pretty()})
