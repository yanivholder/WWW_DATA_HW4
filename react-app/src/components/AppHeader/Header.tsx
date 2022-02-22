import React from 'react';
import '../../App.css';
import { Navbar } from './Navbar';
import logo from '../../logo.jpg';

export interface HeaderProps {
    changePage(newPage: number): void;
}

export const Header: React.FC<HeaderProps> = ({
    changePage
}) => {

    return (
        <div className='header-container'>
            <img src={logo} className="App-logo" alt="logo" />
            <Navbar changePage={changePage}/>
        </div>
    )
}