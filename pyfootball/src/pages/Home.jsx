import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

function Home() {
    const [leagues, setLeagues] = useState([]);

    useEffect(() => {
      fetch('http://127.0.0.1:5000/league/2')
        .then(response => response.json())
        .then(data => setLeagues(data));
    }, []);
  
    if (!leagues.length) {
      return <div>Cargando...</div>;
    }
  
    return (
      <div className="flex flex-wrap mx-2">
        {leagues.map(item => (
          <div className="w-full md:w-1/3 lg:w-1/6 px-2 py-2" key={item.id_team}>
            <Link to={`/team/${item.id_team}`} className="p-4 w-60 bg-gray-100 rounded-lg overflow-hidden shadow-lg">
              <img src={item.team_image} alt={item.team_name} className="mx-auto h-64 object-cover" />
              <div className="p-4">
                <h2 className="font-bold text-lg mb-2 text-center">{item.team_name}</h2>
              </div>
            </Link>
          </div>
        ))}
      </div>
    )
}

export default Home