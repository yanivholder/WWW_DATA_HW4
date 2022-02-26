import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';

import React, { useEffect, useState } from "react";
import { AnswerInfo, Question } from "../../../../types";


export interface ChartProps {
    question: Question;
    questionInfo: AnswerInfo[];
}

export const Chart: React.FC<ChartProps> = ({
    question,
    questionInfo
}) => {

    ChartJS.register(ArcElement, Tooltip, Legend);

    let labels_list: string[] = [];
    let votes_list: number[] = [];

    questionInfo.forEach(answerInfo => {
        labels_list.push(answerInfo.answer);
        votes_list.push(answerInfo.amount);
    })

    const data = {
        labels: labels_list,
        datasets: [
          {
            label: '# of Votes',
            data: votes_list,
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(255, 159, 64, 0.2)',
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)',
            ],
            borderWidth: 1,
          },
        ],
        
    };


    return(
        <Pie data={data} />
    )
}