import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
//import {BrowserRouter} from 'react-router-dom';
//import App from './components/App';
import Project from './components/Project';

//when client.js is served, the below render method is called
//which selects the root element from client.php
document.addEventListener("DOMContentLoaded", function(event) {
    ReactDOM.render(<Project/>, document.getElementById('root'));
	//ReactDOM.render(<DevDash />, document.getElementById('root'));
  });