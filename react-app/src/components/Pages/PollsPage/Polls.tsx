import React from 'react';
import '../../../App.css';
import { useEffect, useState } from 'react';
import { Question } from '../../../types';
import { PollButton } from './PollButton';

export const Polls = () => {
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
            <h2> Polls Page </h2>
            <div> 
            {
                // TODO: Fix the race between rendering and useEffect
                questions.length > 0 ?
                    questions.map(question =>
                        <PollButton key={question.pollID} question={question}/>)
                :
                <h2> No Polls Created Yet </h2>
            }
            </div>        
        </div>
    );
}