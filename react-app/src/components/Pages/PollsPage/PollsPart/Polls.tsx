import React from 'react';
import '../../../../App.css';
import { useEffect, useState } from 'react';
import { Question, Filter } from '../../../../types';
import { PollButton } from './PollButton';
import { Filters } from '../FiltersPart/Filters'
import { server_url } from '../../../../app-constants';
import { async } from 'q';

export interface PollsProps {
    filters: Filter[];
    setFilters: React.Dispatch<React.SetStateAction<Filter[]>>;
}
export const Polls: React.FC<PollsProps> = ({
    filters,
    setFilters
}) => {

   const [questions, setQuestions] = useState<Question[]>([]);

   const getPolls = async () => {
        await fetch(`${server_url}/get_polls`)
        .then(data => data.json())
        .then(data => { 
            let typeQuestions: Question[] = [];
            data.questions.forEach((element: any) => {
                    const newQuestion: Question = {
                        pollID: (element[0] as number),
                        content: (element[1] as string)
                    }
                    typeQuestions.push(newQuestion);
            });
            setQuestions(typeQuestions);
        })
        .catch(e => {
            alert("A problem occured");
        });
    }

   useEffect(() => {
    getPolls();
   }, []);

    return (
        <div className='polls-page-container'>
            <Filters
                filters={filters}
                setFilters={setFilters}
                getPolls={getPolls}
            />
            <h2 style={{fontSize: 'xx-large'}}> Polls </h2>
            <div className='polls-buttons-tab'> 
            {
                questions.length > 0 ?
                    questions.map(question =>
                        <PollButton
                            key={question.pollID}
                            question={question}
                            filters={filters}
                            setFilters={setFilters}
                            getPolls={getPolls}
                        />)
                :
                <h2 style={{color: "#999", marginTop: '10%'}}> No Polls Created Yet </h2>
            }
            </div>        
        </div>
    );
}