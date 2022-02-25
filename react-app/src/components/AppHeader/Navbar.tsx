import { longStackSupport } from 'q';
import React from 'react';
import { pages } from '../../app-constants';
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
        if(isLoggedIn){
            switch(page) {
                case 'Polls':
                    changePage(0);
                    break;
                case 'About':
                    changePage(1);
                    break;
                case 'FAQ':
                    changePage(2);
                    break;
                case 'Create Admin':
                    changePage(3);
                    break;
                default:
                    break;
            }   
        }
        else {
            alert("You need to sign in first")
        }
    }

    const handleLogout = () => {
        fetch('/test/logout');
        setIsLoggedIn(false);
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
                ""
            }
        </div>
    )
}