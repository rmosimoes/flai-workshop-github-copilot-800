from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            name="Test User",
            email="test@example.com",
            password="testpass123"
        )

    def test_user_creation(self):
        """Test that a user is created correctly"""
        self.assertEqual(self.user.name, "Test User")
        self.assertEqual(self.user.email, "test@example.com")

    def test_user_str(self):
        """Test the string representation of user"""
        self.assertEqual(str(self.user), "Test User")


class TeamModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            name="Test Team",
            description="A test team for testing"
        )

    def test_team_creation(self):
        """Test that a team is created correctly"""
        self.assertEqual(self.team.name, "Test Team")
        self.assertEqual(self.team.description, "A test team for testing")

    def test_team_str(self):
        """Test the string representation of team"""
        self.assertEqual(str(self.team), "Test Team")


class ActivityModelTest(TestCase):
    def setUp(self):
        self.activity = Activity.objects.create(
            user_id="test_user_id",
            activity_type="Running",
            duration=30,
            calories=250,
            date=datetime.now()
        )

    def test_activity_creation(self):
        """Test that an activity is created correctly"""
        self.assertEqual(self.activity.activity_type, "Running")
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.calories, 250)


class UserAPITest(APITestCase):
    def test_api_root(self):
        """Test that API root endpoint returns links"""
        url = reverse('api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)

    def test_create_user(self):
        """Test creating a new user via API"""
        url = reverse('user-list')
        data = {
            'name': 'API Test User',
            'email': 'apitest@example.com',
            'password': 'apipass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'API Test User')

    def test_get_users(self):
        """Test retrieving users via API"""
        User.objects.create(name="User 1", email="user1@example.com", password="pass1")
        User.objects.create(name="User 2", email="user2@example.com", password="pass2")
        
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class TeamAPITest(APITestCase):
    def test_create_team(self):
        """Test creating a new team via API"""
        url = reverse('team-list')
        data = {
            'name': 'API Test Team',
            'description': 'A team created via API'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)

    def test_get_teams(self):
        """Test retrieving teams via API"""
        Team.objects.create(name="Team 1", description="Description 1")
        Team.objects.create(name="Team 2", description="Description 2")
        
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class ActivityAPITest(APITestCase):
    def test_create_activity(self):
        """Test creating a new activity via API"""
        url = reverse('activity-list')
        data = {
            'user_id': 'test_user_123',
            'activity_type': 'Cycling',
            'duration': 45,
            'calories': 350,
            'date': datetime.now().isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)


class WorkoutAPITest(APITestCase):
    def test_create_workout(self):
        """Test creating a new workout via API"""
        url = reverse('workout-list')
        data = {
            'name': 'Morning Run',
            'description': 'A refreshing morning run',
            'activity_type': 'Running',
            'duration': 30,
            'difficulty': 'Medium',
            'calories_estimate': 300
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 1)

    def test_get_workouts(self):
        """Test retrieving workouts via API"""
        Workout.objects.create(
            name="Workout 1",
            description="Description 1",
            activity_type="Running",
            duration=30,
            difficulty="Easy",
            calories_estimate=200
        )
        
        url = reverse('workout-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
