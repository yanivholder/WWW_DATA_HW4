import React, { useState } from 'react';
import '../../App.css';
import { About } from './AboutPage/About';
import { Polls } from './PollsPage/PollsPart/Polls';
import { FAQ } from './FAQPage/FAQ';
import { Login } from './LoginPage/Login'
import { CreateAdmin } from './CreateAdminPage/CreateAdmin'
import { Filter } from '../../types';

export interface PageLayoutProps {
    page: number;
    isLoggedIn: boolean;
    setIsLoggedIn: React.Dispatch<React.SetStateAction<boolean>>;
}
export const PageLayout: React.FC<PageLayoutProps> = ({
    page,
    isLoggedIn,
    setIsLoggedIn
}) => {

    const [filters, setFilters] = React.useState<Filter[]>([]);


    if(isLoggedIn) {
        // TODO: Maybe switch to Router
        switch(page) {
            case 0:
                return <Polls 
                        filters={filters}
                        setFilters={setFilters}
                        />            
            case 1:
                return <About />
            case 2:
                return <FAQ />
            case 3:
                return <CreateAdmin />
            default:
                return null;            
    
        }
    }

    else { // No admin is logged in

        return <Login 
                    isLoggedIn={isLoggedIn}
                    setIsLoggedIn={setIsLoggedIn}
                />
    }
    
}