import React from 'react';
import '../../App.css';
import { Navbar } from './Navbar';
import logo from '../../logo.jpg';

export interface HeaderProps {
    changePage(newPage: number): void;
    isLoggedIn: boolean;
    setIsLoggedIn: React.Dispatch<React.SetStateAction<boolean>>;
}

export const Header: React.FC<HeaderProps> = ({
    changePage,
    isLoggedIn,
    setIsLoggedIn
}) => {

    return (
        <div className='header-container'>
            <img src={logo} className="App-logo" alt="logo" />
            <Navbar 
                changePage={changePage}
                isLoggedIn={isLoggedIn}
                setIsLoggedIn={setIsLoggedIn}
            />
        </div>
    )
}