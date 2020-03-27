import React from 'react';
import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Login from './screens/login'
import Register from './screens/register'
import { Form, Button } from 'react-bootstrap';
import { BrowserRouter as Router, Link, Switch, Route } from 'react-router-dom'

function App() {
  return (
    <div className="container m-auto">
      <Router>
        <Switch>
          <Route exact path="/register">
            <Register />
          </Route>
          <Route exact path="/login">
            <Login />
          </Route>
        </Switch>
      </Router>

    </div>
  );
}

export default App;
