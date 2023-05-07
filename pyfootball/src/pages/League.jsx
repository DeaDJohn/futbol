import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

const League = () => {
  const [leagueData, setLeagueData] = useState([]);
  const { id } = useParams();

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/league/${id}`)
      .then(response => response.json())
      .then(data => setLeagueData(data));
  }, [id]);
  if (!leagueData) return 'loading...';
  
  return (
    <div className="container mx-auto px-4">
      <div className="flex flex-wrap -mx-2">
        {leagueData.map(item => (
          <div className="w-full md:w-1/2 lg:w-1/4 px-2 py-2" key={item.id_team}>
            <Link to={`/team/${item.id_team}`} className="bg-gray-100 rounded-lg overflow-hidden shadow-lg">
              <img src={item.team_image} alt={item.team_name} className="mx-auto h-64 object-cover" />
              <div className="p-4">
                <h2 className="font-bold text-lg mb-2 text-center">{item.team_name}</h2>
              </div>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default League;