#!/bin/bash

# OctoFit Tracker API Test Script
# This script tests all API endpoints on both localhost and codespace URL

echo "========================================"
echo "OctoFit Tracker API Test Script"
echo "========================================"
echo ""

# Determine the base URL
if [ -n "$CODESPACE_NAME" ]; then
    BASE_URL="https://${CODESPACE_NAME}-8000.app.github.dev"
    echo "Running in GitHub Codespace"
    echo "Codespace Name: $CODESPACE_NAME"
else
    BASE_URL="http://localhost:8000"
    echo "Running on localhost"
fi

echo "Base URL: $BASE_URL"
echo ""

# Test API Root
echo "========================================"
echo "1. Testing API Root"
echo "========================================"
curl -s "$BASE_URL/" | python3 -m json.tool
echo ""

# Test Users endpoint
echo "========================================"
echo "2. Testing /api/users/"
echo "========================================"
curl -s "$BASE_URL/api/users/" | python3 -m json.tool | head -30
echo ""

# Test Teams endpoint
echo "========================================"
echo "3. Testing /api/teams/"
echo "========================================"
curl -s "$BASE_URL/api/teams/" | python3 -m json.tool
echo ""

# Test Activities endpoint
echo "========================================"
echo "4. Testing /api/activities/"
echo "========================================"
curl -s "$BASE_URL/api/activities/" | python3 -m json.tool | head -30
echo ""

# Test Leaderboard endpoint
echo "========================================"
echo "5. Testing /api/leaderboard/"
echo "========================================"
curl -s "$BASE_URL/api/leaderboard/" | python3 -m json.tool | head -30
echo ""

# Test Workouts endpoint
echo "========================================"
echo "6. Testing /api/workouts/"
echo "========================================"
curl -s "$BASE_URL/api/workouts/" | python3 -m json.tool | head -30
echo ""

echo "========================================"
echo "All API tests completed!"
echo "========================================"
