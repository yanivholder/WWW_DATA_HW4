import React, { useState } from 'react';
import '../../App.css';
import { About } from './AboutPage/About';
import { Polls } from './PollsPage/Polls';
import { FAQ } from './FAQPage/FAQ';
import { Login } from './LoginPage/Login'

export interface PageLayoutProps {
    page: number;
    failedLogin: boolean;
    setFailedLogin: React.Dispatch<React.SetStateAction<boolean>>;
}
export const PageLayout: React.FC<PageLayoutProps> = ({
    page,
    failedLogin,
    setFailedLogin
}) => {

    const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);

    if(isLoggedIn) {
        // TODO: Maybe switch to Router
        switch(page) {
            case 0:
                return <Polls />            
            case 1:
                return <About />
            case 2:
                return <FAQ />
            default:
                return null;            
    
        }
    }

    else { // No admin is logged in

        return <Login 
                    isLoggedIn={isLoggedIn}
                    setIsLoggedIn={setIsLoggedIn}
                    failedLogin={failedLogin}
                    setFailedLogin={setFailedLogin}
                />
    }
    
}