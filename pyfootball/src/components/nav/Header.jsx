
import { useState, useEffect } from 'react';
import { Outlet,Link } from 'react-router-dom';


const Header = () => {

  const [leagues, setLeagues] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/league/')
      .then(response => response.json())
      .then(data => setLeagues(data));
  }, []);

  return (
    <>
    
    <header className="bg-gray-800 text-white flex items-center justify-between px-6 ">
      <div className="flex items-center">
        <img src="/logo.png" alt="Logo" className="h-8 w-8 mr-4" />
        <Link to="/" className="font-bold text-xl">
          My App
        </Link>
      </div>
      <nav>
        <ul className="flex items-center menu">
          <li className="ml-6 menu-item py-4">
            <Link to="/">Home</Link>
          </li>
          <li className="ml-6 menu-item py-4">
            <a href="#">Leagues</a>
            {leagues.length !== 0 ? (
              <ul className="absolute bg-gray-800 text-white py-2 rounded-md mt-1 sub-menu menu-leagues">
                {leagues.map((league) => (
                  <li className="px-4 py-2 hover:bg-gray-700" key={league.id_league}>
                    <Link to={`/league/${league.id_league}`}>{league.league_name}</Link>
                  </li>
                ))}
              </ul>
            ) : null}
          </li>
          <li className="ml-6 menu-item py-4">
            <Link to="/about">About</Link>
          </li>
        </ul>
      </nav>
    </header>
    <div className='py-10'>
        <Outlet/>
    </div>
    </>
  )
};
export default Header;