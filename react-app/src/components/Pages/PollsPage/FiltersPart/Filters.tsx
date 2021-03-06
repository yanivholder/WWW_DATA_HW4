import React from 'react';
import '../../../../App.css';
import { useEffect, useState } from 'react';
import { Question, Filter } from '../../../../types';
import { PollButton } from '../PollsPart/PollButton';
import { CreatePollPopup } from './CreatePollPopup'

export interface FiltersProps {
    filters: Filter[];
    setFilters: React.Dispatch<React.SetStateAction<Filter[]>>;
    getPolls: any;
}
export const Filters: React.FC<FiltersProps> = ({
    filters,
    setFilters,
    getPolls
}) => {

    const [isCreatePollOpen, setIsCreatePollOpen] = useState<boolean>(false);
    const handleCreatePoll = () => {
        setIsCreatePollOpen(!isCreatePollOpen);
    }

    return (
        <div className='polls-filters-container'>
            <div className='filter-button-tab'>
                <button className='filter-button' onClick={() => { setFilters([]) }}>
                    Reset Filters
                </button>
                <button className='filter-button' onClick={() => handleCreatePoll()}>
                    Create Poll
                </button>
            </div>
            <div>
                <h2 style={{float: 'left', marginLeft: '10px', marginBottom: '0', textDecoration: 'underline'}}>
                    Filters:
                </h2>
            </div>
            <div className='row'>
                {
                    filters.length > 0 ?
                        filters.map(filter => 
                            <p 
                                key={
                                    filters.findIndex((element) => 
                                    element.pollID === filter.pollID)
                                }
                                className='filter'
                            >
                                {filter.question} = {filter.answer}
                            </p>)
                    :
                    <p style={{float: 'left', marginLeft: '10px', marginBottom: '0'}}>No filters yet</p>
                }
            </div>
            {isCreatePollOpen && 
                <CreatePollPopup
                    handleClose={handleCreatePoll}
                    filters={filters}
                    setFilters={setFilters}
                    getPolls={getPolls}
                />
            }
        </div>
    );
}