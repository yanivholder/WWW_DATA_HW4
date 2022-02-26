import React from 'react';
import '../../../App.css';
import communication from '../../../communication.jpg';



export const About = () => {
    
    return (
        <div className='about-page-container'>
            <h2> Hi, we're TelePolls </h2>
            <p> We help people like you conduct surveys so you can make smarter decisions based on easy to read graphs </p>
            <p> In today's digital arena, any product delivering company/ digital marketer must keep up with the audience's needs. This is where we come in handy</p>
            <img src={communication} className="App-logo" alt="logo" />
        </div>
    );
}