from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Clearing existing data...'))
        
        # Delete existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Existing data cleared!'))
        
        # Create Teams
        self.stdout.write(self.style.WARNING('Creating teams...'))
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Earth\'s Mightiest Heroes unite for fitness excellence!'
        )
        
        team_dc = Team.objects.create(
            name='Team DC',
            description='The Justice League of fitness champions!'
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created teams: {team_marvel.name}, {team_dc.name}'))
        
        # Create Users - Marvel Heroes
        self.stdout.write(self.style.WARNING('Creating Marvel heroes...'))
        marvel_users = [
            {'name': 'Tony Stark', 'email': 'ironman@avengers.com'},
            {'name': 'Steve Rogers', 'email': 'captainamerica@avengers.com'},
            {'name': 'Thor Odinson', 'email': 'thor@asgard.com'},
            {'name': 'Natasha Romanoff', 'email': 'blackwidow@avengers.com'},
            {'name': 'Bruce Banner', 'email': 'hulk@avengers.com'},
            {'name': 'Peter Parker', 'email': 'spiderman@avengers.com'},
        ]
        
        created_marvel_users = []
        for user_data in marvel_users:
            user = User.objects.create(
                name=user_data['name'],
                email=user_data['email'],
                password='marvel123',
                team_id=str(team_marvel._id)
            )
            created_marvel_users.append(user)
            self.stdout.write(f'  Created: {user.name}')
        
        # Create Users - DC Heroes
        self.stdout.write(self.style.WARNING('Creating DC heroes...'))
        dc_users = [
            {'name': 'Clark Kent', 'email': 'superman@justiceleague.com'},
            {'name': 'Bruce Wayne', 'email': 'batman@justiceleague.com'},
            {'name': 'Diana Prince', 'email': 'wonderwoman@justiceleague.com'},
            {'name': 'Barry Allen', 'email': 'flash@justiceleague.com'},
            {'name': 'Arthur Curry', 'email': 'aquaman@justiceleague.com'},
            {'name': 'Hal Jordan', 'email': 'greenlantern@justiceleague.com'},
        ]
        
        created_dc_users = []
        for user_data in dc_users:
            user = User.objects.create(
                name=user_data['name'],
                email=user_data['email'],
                password='dc123',
                team_id=str(team_dc._id)
            )
            created_dc_users.append(user)
            self.stdout.write(f'  Created: {user.name}')
        
        # Create Activities
        self.stdout.write(self.style.WARNING('Creating activities...'))
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weight Training', 'Yoga', 'Boxing']
        all_users = created_marvel_users + created_dc_users
        
        activity_count = 0
        for user in all_users:
            # Create 5-10 activities per user
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 90)
                calories = duration * random.randint(8, 12)
                date = datetime.now() - timedelta(days=random.randint(0, 30))
                
                Activity.objects.create(
                    user_id=str(user._id),
                    activity_type=activity_type,
                    duration=duration,
                    calories=calories,
                    date=date
                )
                activity_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {activity_count} activities'))
        
        # Create Leaderboard entries
        self.stdout.write(self.style.WARNING('Creating leaderboard...'))
        leaderboard_data = []
        
        for user in all_users:
            user_activities = Activity.objects.filter(user_id=str(user._id))
            total_calories = sum(activity.calories for activity in user_activities)
            total_activities = user_activities.count()
            
            team_name = team_marvel.name if user.team_id == str(team_marvel._id) else team_dc.name
            
            leaderboard_data.append({
                'user': user,
                'team_name': team_name,
                'total_calories': total_calories,
                'total_activities': total_activities
            })
        
        # Sort by calories and assign ranks
        leaderboard_data.sort(key=lambda x: x['total_calories'], reverse=True)
        
        for rank, data in enumerate(leaderboard_data, start=1):
            Leaderboard.objects.create(
                user_id=str(data['user']._id),
                user_name=data['user'].name,
                team_id=data['user'].team_id,
                team_name=data['team_name'],
                total_calories=data['total_calories'],
                total_activities=data['total_activities'],
                rank=rank
            )
            self.stdout.write(f'  Rank {rank}: {data["user"].name} - {data["total_calories"]} calories')
        
        # Create Workouts
        self.stdout.write(self.style.WARNING('Creating workout suggestions...'))
        workouts = [
            {
                'name': 'Superhero Strength Training',
                'description': 'Build strength like a superhero with compound exercises',
                'activity_type': 'Weight Training',
                'duration': 45,
                'difficulty': 'Advanced',
                'calories_estimate': 400
            },
            {
                'name': 'Speed Force Cardio',
                'description': 'High-intensity interval training for speed and endurance',
                'activity_type': 'Running',
                'duration': 30,
                'difficulty': 'Intermediate',
                'calories_estimate': 350
            },
            {
                'name': 'Asgardian Warrior Workout',
                'description': 'Full-body circuit training fit for a god',
                'activity_type': 'Weight Training',
                'duration': 60,
                'difficulty': 'Advanced',
                'calories_estimate': 500
            },
            {
                'name': 'Web-Slinger Flexibility',
                'description': 'Yoga and stretching for enhanced flexibility and balance',
                'activity_type': 'Yoga',
                'duration': 40,
                'difficulty': 'Beginner',
                'calories_estimate': 200
            },
            {
                'name': 'Atlantean Swimming',
                'description': 'Endurance swimming workout for aquatic fitness',
                'activity_type': 'Swimming',
                'duration': 45,
                'difficulty': 'Intermediate',
                'calories_estimate': 400
            },
            {
                'name': 'Gotham Night Patrol',
                'description': 'Evening cycling routine for stamina building',
                'activity_type': 'Cycling',
                'duration': 50,
                'difficulty': 'Intermediate',
                'calories_estimate': 450
            },
            {
                'name': 'Amazon Warrior Training',
                'description': 'Combat-focused boxing and martial arts',
                'activity_type': 'Boxing',
                'duration': 35,
                'difficulty': 'Advanced',
                'calories_estimate': 380
            },
            {
                'name': 'Beginner Hero Boot Camp',
                'description': 'Start your fitness journey with basic exercises',
                'activity_type': 'Weight Training',
                'duration': 30,
                'difficulty': 'Beginner',
                'calories_estimate': 250
            }
        ]
        
        for workout_data in workouts:
            workout = Workout.objects.create(**workout_data)
            self.stdout.write(f'  Created: {workout.name}')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Database populated successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Teams: {Team.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Users: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Activities: {Activity.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Leaderboard entries: {Leaderboard.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Workouts: {Workout.objects.count()}'))
