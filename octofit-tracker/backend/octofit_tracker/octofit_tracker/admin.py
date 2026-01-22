from django.contrib import admin
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'team_id', 'created_at')
    list_filter = ('team_id', 'created_at')
    search_fields = ('name', 'email')
    readonly_fields = ('created_at',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'activity_type', 'duration', 'calories', 'date', 'created_at')
    list_filter = ('activity_type', 'date', 'created_at')
    search_fields = ('user_id', 'activity_type')
    readonly_fields = ('created_at',)


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('rank', 'user_name', 'team_name', 'total_calories', 'total_activities', 'updated_at')
    list_filter = ('team_name', 'updated_at')
    search_fields = ('user_name', 'team_name')
    readonly_fields = ('updated_at',)
    ordering = ('rank',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'activity_type', 'duration', 'difficulty', 'calories_estimate', 'created_at')
    list_filter = ('activity_type', 'difficulty', 'created_at')
    search_fields = ('name', 'description', 'activity_type')
    readonly_fields = ('created_at',)
