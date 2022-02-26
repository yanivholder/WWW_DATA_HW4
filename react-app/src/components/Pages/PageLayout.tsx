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
    setPage: React.Dispatch<React.SetStateAction<number>>;
    isLoggedIn: boolean;
    setIsLoggedIn: React.Dispatch<React.SetStateAction<boolean>>;
}
export const PageLayout: React.FC<PageLayoutProps> = ({
    page,
    setPage,
    isLoggedIn,
    setIsLoggedIn
}) => {

    const [filters, setFilters] = React.useState<Filter[]>([]);

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
        case 4:
            return <Login
                        page={page}
                        setPage={setPage}
                        isLoggedIn={isLoggedIn}
                        setIsLoggedIn={setIsLoggedIn}
                    />
        default:
            return null;            

    }
}