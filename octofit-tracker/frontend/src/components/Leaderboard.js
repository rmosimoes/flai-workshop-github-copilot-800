import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;
        console.log('Fetching leaderboard from:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Leaderboard data received:', data);
        
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        console.log('Processed leaderboard data:', leaderboardData);
        
        setLeaderboard(leaderboardData);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching leaderboard:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  if (loading) {
    return (
      <div className="container mt-5">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3 text-muted">Loading leaderboard...</p>
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
          <i className="bi bi-trophy"></i> Leaderboard
        </h2>
        <p className="text-muted">Top performers based on total calories burned</p>
      </div>
      <div className="table-responsive">
        <table className="table table-hover">
          <thead>
            <tr>
              <th scope="col">Rank</th>
              <th scope="col">User</th>
              <th scope="col">Total Calories</th>
              <th scope="col">Total Activities</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.length === 0 ? (
              <tr>
                <td colSpan="4" className="text-center text-muted py-4">
                  No leaderboard data available
                </td>
              </tr>
            ) : (
              leaderboard.map((entry, index) => {
                let rankBadge = 'bg-secondary';
                if (index === 0) rankBadge = 'bg-warning';
                else if (index === 1) rankBadge = 'bg-secondary';
                else if (index === 2) rankBadge = 'bg-danger';
                
                return (
                  <tr key={entry.id || index}>
                    <td><span className={`badge ${rankBadge}`}>{index + 1}</span></td>
                    <td><strong>{entry.user_name || entry.user}</strong></td>
                    <td><span className="badge bg-success">{entry.total_calories}</span></td>
                    <td><span className="badge bg-info">{entry.total_activities}</span></td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Leaderboard;
