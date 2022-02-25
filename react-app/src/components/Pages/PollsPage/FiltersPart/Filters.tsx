import React from 'react';
import '../../../../App.css';
import { useEffect, useState } from 'react';
import { Question, Filter } from '../../../../types';
import { PollButton } from '../PollsPart/PollButton';
import { CreatePollPopup } from './CreatePollPopup'

export interface FiltersProps {
    filters: Filter[];
    setFilters: React.Dispatch<React.SetStateAction<Filter[]>>;
}
export const Filters: React.FC<FiltersProps> = ({
    filters,
    setFilters
}) => {

    const [isCreatePollOpen, setIsCreatePollOpen] = useState<boolean>(false);
    const handleCreatePoll = () => {
        setIsCreatePollOpen(!setIsCreatePollOpen);
    }

    return (
        <div className='polls-filters-container'>
            <button className='filter-button' onClick={() => { setFilters([]) }}>
                Reset Filters
            </button>
            <button className='filter-button' onClick={() => handleCreatePoll()}>
                Create Poll
            </button>
            {
                filters.length > 0 ?
                    filters.map(filter => 
                        <p> {filter.question} </p>)
                :
                ""
            }
            {isCreatePollOpen && 
                <CreatePollPopup
                    handleClose={handleCreatePoll}
                />
            }
        </div>
    );
}