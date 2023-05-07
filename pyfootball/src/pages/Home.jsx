import {useState, useEffect} from 'react'

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
      <div className='grid grid-cols-4 gap-8'>
        {leagues.map(league => (
          <div key={league.id_league}>
            <img className='mx-auto' src={league.team_image} />
            <h2>{league.team_name}</h2>
          </div>
        ))}
      </div>
    )
}

export default Home