import { useState } from "react";
import './CSS/App.css'
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout } from './Layout';
import Home from './Pages/Home';
import SongReview from './Pages/SongReview';
import Page2 from "./Pages/Page2";
import Profile from "./Pages/Profile";
import Login from "./Pages/Login";

import SongDetails from './Pages/SongDetails';
import AlbumDetails from './Pages/AlbumDetails';
import ArtistDetails from './Pages/ArtistDetails';
import TopRatedAlbums from './Pages/TopRatedAlbums';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route element={<Layout />}>
          <Route path="/home" element={<Home />} />
          <Route path="/SongReview" element={<SongReview />} />
          <Route path="/Page2" element={<Page2 />} />
          <Route path="/Profile" element={<Profile />} />
          <Route path="/song/:songId" element={<SongDetails />} />
          <Route path="/album/:albumId" element={<AlbumDetails />} />
          <Route path="/artist/:artistId" element={<ArtistDetails />} />
          <Route path="/top-rated-albums" element={<TopRatedAlbums />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;

