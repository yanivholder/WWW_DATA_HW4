import React from 'react';
import '../../App.css';
import { About } from './AboutPage/About';
import { Polls } from './PollsPage/Polls';
import { FAQ } from './FAQPage/FAQ';

export interface PageLayoutProps {
    page: number;
}
export const PageLayout: React.FC<PageLayoutProps> = ({
    page
}) => {

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