import React, { useState } from "react";
import '../../../App.css';
import { Question } from "../../../types";
import Popup from './Popup';

export interface PollButtonProps {
    question: Question,
}

export const PollButton: React.FC<PollButtonProps> = ({
    question,
}) => {

    const [isOpen, setIsOpen] = useState<boolean>(false);

    const { pollID, content } = question;

    const handlePollButton = () => {
        setIsOpen(!isOpen);
    }

    return (
        <div className="poll-button-tab">
            <button key={pollID} className='poll-button' onClick={() => handlePollButton()}>
                {content}
            </button>
            {isOpen && <Popup
                pollID={ pollID }
                handleClose={handlePollButton}
                />}
        </div>
    )
}