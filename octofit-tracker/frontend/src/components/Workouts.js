import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWorkouts = async () => {
      try {
        const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;
        console.log('Fetching workouts from:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Workouts data received:', data);
        
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        console.log('Processed workouts data:', workoutsData);
        
        setWorkouts(workoutsData);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching workouts:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchWorkouts();
  }, []);

  if (loading) {
    return (
      <div className="container mt-5">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3 text-muted">Loading workouts...</p>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="container mt-5">
        <div className="alert alert-danger error-alert" role="alert">
          <h4 className="alert-heading">Error!</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-5">
      <div className="page-header">
        <h2 className="text-primary">
          <i className="bi bi-lightning"></i> Workout Suggestions
        </h2>
        <p className="text-muted">Personalized workout recommendations for your fitness journey</p>
      </div>
      <div className="row">
        {workouts.length === 0 ? (
          <div className="col-12">
            <div className="alert alert-info text-center" role="alert">
              No workout suggestions available at the moment
            </div>
          </div>
        ) : (
          workouts.map((workout) => (
            <div key={workout.id} className="col-md-4 mb-4">
              <div className="card h-100">
                <div className="card-body d-flex flex-column">
                  <h5 className="card-title">{workout.name}</h5>
                  <p className="card-text flex-grow-1">{workout.description}</p>
                  <div className="mt-3">
                    <div className="d-flex justify-content-between mb-2">
                      <span className="badge bg-primary">Duration: {workout.duration} min</span>
                      <span className="badge bg-warning text-dark">Difficulty: {workout.difficulty}</span>
                    </div>
                    <div className="d-flex justify-content-between">
                      <span className="badge bg-success">Calories: {workout.calories}</span>
                      <span className="badge bg-info">{workout.workout_type}</span>
                    </div>
                  </div>
                  <button className="btn btn-primary btn-sm mt-3">Start Workout</button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Workouts;
