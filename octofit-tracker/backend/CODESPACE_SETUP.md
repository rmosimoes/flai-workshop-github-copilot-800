# OctoFit Tracker - Codespace Setup Guide

## Overview

This guide explains how the OctoFit Tracker Django backend is configured to work in GitHub Codespaces with HTTPS support.

## Configuration Changes

### 1. Settings Configuration (`settings.py`)

The Django settings have been updated to support both local development and GitHub Codespaces:

#### ALLOWED_HOSTS
```python
import os
CODESPACE_NAME = os.getenv('CODESPACE_NAME')
if CODESPACE_NAME:
    ALLOWED_HOSTS = [
        f'{CODESPACE_NAME}-8000.app.github.dev',
        'localhost',
        '127.0.0.1',
    ]
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

#### CORS Settings
```python
if CODESPACE_NAME:
    CORS_ALLOWED_ORIGINS = [
        f'https://{CODESPACE_NAME}-8000.app.github.dev',
        f'https://{CODESPACE_NAME}-3000.app.github.dev',
    ]
    CSRF_TRUSTED_ORIGINS = [
        f'https://{CODESPACE_NAME}-8000.app.github.dev',
        f'https://{CODESPACE_NAME}-3000.app.github.dev',
    ]
else:
    CORS_ALLOW_ALL_ORIGINS = True
```

### 2. URLs Configuration (`urls.py`)

Added `import os` to support environment variable access for future enhancements.

## Starting the Server

### Option 1: Using VS Code Launch Configuration (Recommended)

1. Open VS Code's Run and Debug panel (Ctrl+Shift+D / Cmd+Shift+D)
2. Select "Launch Django Backend" from the dropdown
3. Click the green play button or press F5

This will:
- Activate the virtual environment automatically
- Start the Django server on `0.0.0.0:8000`
- Enable Django debugging features
- Use the correct Python interpreter from the venv

### Option 2: Using Terminal

```bash
cd octofit-tracker/backend/octofit_tracker
source ../venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

## API Endpoints

The API is accessible at:

### Codespace URL Format
```
https://$CODESPACE_NAME-8000.app.github.dev/api/[endpoint]/
```

### Local Development
```
http://localhost:8000/api/[endpoint]/
```

### Available Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | API root - lists all available endpoints |
| `/api/users/` | User management |
| `/api/teams/` | Team management |
| `/api/activities/` | Activity tracking |
| `/api/leaderboard/` | Competition leaderboard |
| `/api/workouts/` | Workout suggestions |

## Testing the API

### Quick Test
Use the provided test script:
```bash
cd octofit-tracker/backend
./test_api.sh
```

### Manual Testing with curl

#### Test API Root
```bash
# Codespace
curl https://${CODESPACE_NAME}-8000.app.github.dev/

# Localhost
curl http://localhost:8000/
```

#### Test Users Endpoint
```bash
# Codespace
curl https://${CODESPACE_NAME}-8000.app.github.dev/api/users/

# Localhost
curl http://localhost:8000/api/users/
```

#### Test with Pretty Printing
```bash
curl -s https://${CODESPACE_NAME}-8000.app.github.dev/api/users/ | python3 -m json.tool
```

## Port Forwarding

GitHub Codespaces automatically forwards ports:
- **Port 8000**: Django Backend (Public)
- **Port 3000**: React Frontend (Public)
- **Port 27017**: MongoDB (Private)

You can view forwarded ports in the VS Code "Ports" tab.

## Environment Variables

The configuration automatically detects the `$CODESPACE_NAME` environment variable:
- **In Codespaces**: Uses HTTPS with the full codespace URL
- **Locally**: Uses HTTP with localhost

## Database

MongoDB is running on port 27017 with:
- Database name: `octofit_db`
- Pre-populated with sample data
- 12 users across 2 teams
- Activities, leaderboard, and workout data

## Troubleshooting

### Server Not Starting
1. Check if MongoDB is running: `ps aux | grep mongod`
2. Verify virtual environment: `which python` should show the venv path
3. Check for port conflicts: `lsof -i :8000`

### CORS Errors
- Ensure `CODESPACE_NAME` is set correctly
- Check that the frontend is using the correct backend URL
- Verify CORS settings in `settings.py`

### Certificate/HTTPS Issues
The configuration handles HTTPS automatically in Codespaces. The `CSRF_TRUSTED_ORIGINS` setting ensures HTTPS requests are accepted.

## Development Workflow

1. Make code changes
2. Django auto-reloads (no need to restart server)
3. Test API endpoints using curl or the test script
4. Check Django server logs in the terminal for any errors

## Next Steps

- Configure the React frontend to use the backend API
- Implement authentication
- Add more comprehensive tests
- Deploy to production
