import { useState, useEffect } from 'react';
import { Route, createBrowserRouter, createRoutesFromElements, RouterProvider } from 'react-router-dom';
import './App.css'
import './index.css';
import Home from './pages/Home';
import League from './pages/League';
import Team from './pages/Team';
import Player from './pages/Player';
import Header from './components/nav/Header';



const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<Header />}>
      <Route index element={<Home />} />
      <Route path="league/:id" element={<League />} />
      <Route path="player/:id" element={<Player />} />
      <Route path="team/:id" element={<Team />} />
    </Route>
  )
)

function App() {

  return (
    <>
      <RouterProvider router={router}/>
    </>
  );
}

export default App;
