import React, { useState } from "react";
import '../../../../App.css';
import { Filter, Question } from "../../../../types";
import Popup from './Popup';

export interface PollButtonProps {
    question: Question;
    filters: Filter[];
    setFilters: React.Dispatch<React.SetStateAction<Filter[]>>;
    getPolls: any;
}

export const PollButton: React.FC<PollButtonProps> = ({
    question,
    filters,
    setFilters,
    getPolls
}) => {

    const [isOpen, setIsOpen] = useState<boolean>(false);

    const { pollID, content } = question;

    const handlePollButtonOpen = () => {
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
                    handleClose={handlePollButtonClose}
                    filters={filters}
                    setFilters={setFilters}
                    question={question}
                    getPolls={getPolls}
                />
            }
        </div>
    )
}