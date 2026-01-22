from rest_framework import serializers
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from bson import ObjectId
from django.db import connection


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='name', read_only=True)
    team_name = serializers.SerializerMethodField()
    id = serializers.CharField(source='_id', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'name', 'email', 'password', 'team_id', 'team_name', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}
    
    def get_team_name(self, obj):
        if not obj.team_id:
            return None
        
        try:
            # Get the team using MongoDB directly
            from pymongo import MongoClient
            
            # Create a direct MongoDB connection
            client = MongoClient('localhost', 27017)
            db = client['octofit_db']
            teams_collection = db['teams']
            
            # Convert team_id to ObjectId for lookup
            team_oid = ObjectId(obj.team_id)
            team_doc = teams_collection.find_one({'_id': team_oid})
            
            if team_doc:
                return team_doc.get('name')
            return None
        except Exception:
            # Fallback: try Django ORM
            try:
                team = Team.objects.filter(_id=obj.team_id).first()
                return team.name if team else None
            except Exception:
                return None


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['_id', 'name', 'description', 'created_at']


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['_id', 'user_id', 'activity_type', 'duration', 'calories', 'date', 'created_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = ['_id', 'user_id', 'user_name', 'team_id', 'team_name', 'total_calories', 'total_activities', 'rank', 'updated_at']


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['_id', 'name', 'description', 'activity_type', 'duration', 'difficulty', 'calories_estimate', 'created_at']
