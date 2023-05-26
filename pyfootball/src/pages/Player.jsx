import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function Player() {
    const [playerData, setPlayerData] = useState([]);
    const [playerStatsData, setPlayerStatsData] = useState([]);
    const { id } = useParams();

    
    useEffect(() => {

            const fetchData = async () => {
              const response = await fetch(`http://127.0.0.1:5000/player/${id}`);
              const player = await response.json();
          
              setPlayerData(player[0]);
            };
          
            fetchData();
        
      }, [id]);


      useEffect(() => {
        if (playerData.id_team) {
            console.log(playerData);
          const fetchTeam = async () => {
            const response = await fetch(`http://127.0.0.1:5000/team/${playerData.id_team}`);
            const data = await response.json();
            setPlayerStatsData( data );
          };
      
          fetchTeam();
        }
      }, [playerData.id_team]);
    
      if (!playerData) {
        return <div>Loading...</div>;
      }

    if (!playerData) return 'loading...';

  return (

    <div className="container mx-auto px-4">
      <div className="flex flex-wrap mx-2">

          <div className="w-full md:w-1/2 lg:w-1/4 px-2 py-2">
            <figure className='mb-4'>
                <img src={playerData.player_img} alt={playerData.player_name} />
            </figure>
            <h1>{playerData.player_name}</h1>
          </div>
          <div className="w-full md:w-1/2 lg:w-3/4 px-2 py-2">
            {
              playerStatsData ?
              <div>
                {}
              </div>
              :
              <div>Loading</div>
            }
          </div>

      </div>
    </div>
  )
}

export default Player