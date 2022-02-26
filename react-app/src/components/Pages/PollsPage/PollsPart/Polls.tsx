import React from 'react';
import '../../../../App.css';
import { useEffect, useState } from 'react';
import { Question, Filter } from '../../../../types';
import { PollButton } from './PollButton';
import { Filters } from '../FiltersPart/Filters'

export interface PollsProps {
    filters: Filter[];
    setFilters: React.Dispatch<React.SetStateAction<Filter[]>>;
}
export const Polls: React.FC<PollsProps> = ({
    filters,
    setFilters
}) => {

   const [questions, setQuestions] = useState<Question[]>([]);

   useEffect(() => {
       fetch('/test/get_polls')
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
        });
   }, []);

    return (
        <div className='polls-page-container'>
            <Filters
                filters={filters}
                setFilters={setFilters}
            />
            <h2> Polls Page </h2>
            <div> 
            {
                // TODO: Fix the race between rendering and useEffect
                questions.length > 0 ?
                    questions.map(question =>
                        <PollButton
                            key={question.pollID}
                            question={question}
                            filters={filters}
                            setFilters={setFilters}
                        />)
                :
                <h2> No Polls Created Yet </h2>
            }
            </div>        
        </div>
    );
}