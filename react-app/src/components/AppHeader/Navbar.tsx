import { restElement } from '@babel/types';
import { async, longStackSupport } from 'q';
import React from 'react';
import { pages, server_url } from '../../app-constants';
import '../../App.css';

export interface NavbarProps {
    changePage(newPage: number): void;
    isLoggedIn: boolean;
    setIsLoggedIn: React.Dispatch<React.SetStateAction<boolean>>;
}

export const Navbar: React.FC<NavbarProps> = ({
    changePage,
    isLoggedIn,
    setIsLoggedIn
}) => {

    const handlePageChange = (page: string) => {
        // Think about a better way to do that:
        switch(page) {
            case 'Polls':
                if(isLoggedIn) {
                    changePage(0);
                } else {
                    alert("You need to sign in first");
                }
                break;
            case 'About':
                changePage(1);
                break;
            case 'FAQ':
                changePage(2);
                break;
            case 'Create Admin':
                if(isLoggedIn) {
                    changePage(3);
                } else {
                    alert("You need to sign in first");
                }
                break;
            default:
                break;
        }   
    }

    const handleLogout = async () => {
        await fetch(`${server_url}/logout`)
        .then(resp => {
            if(resp.status === 200) {
                changePage(4);
                setIsLoggedIn(false);
            } else {
                alert("A problem occured");
            }
        });
        
    }
    const handleLogin = () => {
        changePage(4);
    }

    return (
        <div className='nav-tab'>
            {
                pages.map(page => 
                    <button key={page} className='nav-button' onClick={() => handlePageChange(page)}>
                        {page}
                    </button>)
            }
            {
                isLoggedIn ?
                <button className='nav-button-logout' onClick={() => handleLogout()}>
                    Logout    
                </button>
                :
                <button className='nav-button-login' onClick={() => handleLogin()}>
                    Login    
                </button>
            }
        </div>
    )
}