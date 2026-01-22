# OctoFit Tracker Frontend - React Setup

## Overview
This React frontend connects to the Django REST API backend to display fitness tracking data.

## Environment Configuration

The `.env` file has been automatically configured with your codespace name:
- `REACT_APP_CODESPACE_NAME`: Set to your GitHub Codespace name

## API Endpoints

All components fetch data from the Django backend at:
`https://${REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/`

### Available Endpoints:
- `/api/users/` - User profiles
- `/api/activities/` - Activity logs
- `/api/teams/` - Team information
- `/api/leaderboard/` - Competitive rankings
- `/api/workouts/` - Workout suggestions

## Components

### Navigation
The app includes a Bootstrap navbar with links to all sections:
- Users
- Activities
- Teams
- Leaderboard
- Workouts

### Component Features
All components include:
- Loading states
- Error handling
- Console logging for debugging
- Support for both paginated (`.results`) and plain array API responses
- REST API endpoint logging

## Running the Application

1. Make sure the backend is running on port 8000
2. Install dependencies (already done):
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start --prefix /workspaces/flai-workshop-github-copilot-800/octofit-tracker/frontend
   ```

4. The app will open at `http://localhost:3000`

## Debugging

Check the browser console for:
- API endpoint URLs being called
- Response data from each endpoint
- Any fetch errors

## Dependencies
- react-router-dom: For navigation and routing
- bootstrap: For styling and UI components
