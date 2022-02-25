import React, { useState } from "react";
import '../../../../App.css';
import { Filter, Question } from "../../../../types";
import Popup from './Popup';

export interface PollButtonProps {
    question: Question;
    filters: Filter[];
    setFilters: React.Dispatch<React.SetStateAction<Filter[]>>;
}

export const PollButton: React.FC<PollButtonProps> = ({
    question,
    filters,
    setFilters
}) => {

    const [isOpen, setIsOpen] = useState<boolean>(false);

    const { pollID, content } = question;

    const handlePollButtonOpen = () => {
        const newFilter: Filter = {
            pollID: question.pollID,
            question: question.content,
            answer: ""
        }
        const newFilterList = [...filters, newFilter];
        setFilters(newFilterList);
        setIsOpen(true);
    }

    const handlePollButtonClose = () => {
        setIsOpen(false);
    }

    return (
        <div className="poll-button-tab">
            <button key={pollID} className='poll-button' onClick={() => handlePollButtonOpen()}>
                {content}
            </button>
            {isOpen && 
                <Popup
                    pollID={ pollID }
                    handleClose={handlePollButtonClose}
                />
            }
        </div>
    )
}