import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

const Team = () => {
  const [teamData, setTeamData] = useState([]);
  const { id } = useParams();

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/team/${id}`)
      .then(response => response.json())
      .then(data => setTeamData(data));
  }, [id]);

  return (
    <div className="container mx-auto px-4">
      <div className="flex flex-wrap mx-2">
        {teamData.map(item => (
          <div className="w-full md:w-1/2 lg:w-1/4 px-2 py-2" key={item.id_player}>
            <Link to={`/player/${item.id_player}`} className="bg-gray-100 rounded-lg overflow-hidden shadow-lg">
              <img src={item.player_img} alt={item.player_name} className="mx-auto" />
              <div className="p-4">
                <h2 className="font-bold text-lg mb-2 text-center">{item.player_name}</h2>
              </div>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Team;