import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
//import {BrowserRouter} from 'react-router-dom';
//import App from './components/App';
import Upload from './components/Upload';
import Upload2 from './components/Upload2';

//when client.js is served, the below render method is called
//which selects the root element from client.php
document.addEventListener("DOMContentLoaded", function(event) {
    ReactDOM.render(<Upload2/>, document.getElementById('index'));
	//ReactDOM.render(<DevDash />, document.getElementById('root'));
  });