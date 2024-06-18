from rest_framework.views import APIView, Response
from django.forms.models import model_to_dict
from .models import Team
from utils import data_processing
from exceptions import NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError


class TeamView(APIView):
    
    def post(self, request):
        data = request.data        

        try:
            data_processing(data)
            team = Team.objects.create(**data)
            return Response(model_to_dict(team), status=201)
        except (NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError) as e:
            return Response({"error": str(e)}, status=400)      

    
    def get(self, request, team_id=None):

        if team_id == None: 
            all_teams = Team.objects.all()
            teams_data = [model_to_dict(team) for team in all_teams]
            return Response(teams_data, status=200)
        
        found_team = Team.objects.filter(id=team_id)
        if not found_team.exists():
            return Response({"message": "Team not found"}, status=404)
        
        team = Team.objects.get(id=team_id)
        return Response(model_to_dict(team), status=200)
    
    
    def patch(self, request, team_id):

        found_team = Team.objects.filter(id=team_id)
        if not found_team.exists():
            return Response({"message": "Team not found"}, status=404)
        
        team = Team.objects.get(id=team_id)

        data = request.data
        if 'name' in data:
            team.name = data['name']
        if 'titles' in data:
            team.titles = data['titles']
        if 'top_scorer' in data:
            team.top_scorer = data['top_scorer']
        if 'fifa_code' in data:
            team.fifa_code = data['fifa_code']
        if 'first_cup' in data:
            team.first_cup = data['first_cup']
            
        team.save()

        return Response(model_to_dict(team), status=200)
    
    def delete(self, request, team_id):

        found_team = Team.objects.filter(id=team_id)
        if not found_team.exists():
            return Response({"message": "Team not found"}, 404)
        
        team = Team.objects.get(id=team_id)
        team.delete()

        return Response(status=204)