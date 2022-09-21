import logo from './logo.svg';
// import './App.css';
import GetUser from './GetUser';
import Bienvenida from './Bienvenida';
import NavbarUp from './NavbarUp';
import NavbarEmpt from './NavbarEmpt';
import Button from 'react-bootstrap/Button';
import { useGlobalState } from 'state-pool';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';

function App() {

  return (
    <Router>
      <div className="App">

        <NavbarUp/>
        <NavbarEmpt/>

        <Routes>

          <Route path="/" element={<GetUser/>}/>

          <Route path="/userDetails/:userId" element={<Bienvenida/>}/>

        </Routes>
      
      </div>
    </Router>
  );
}

export default App;
