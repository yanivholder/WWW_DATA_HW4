import React, { useEffect, useState } from "react";
import { server_url } from "../../../../app-constants";
import { AnswerInfo, Filter, Question } from "../../../../types";
import { Chart } from './Chart';

export interface PopupProps {
    handleClose: any;
    filters: Filter[];
    setFilters: React.Dispatch<React.SetStateAction<Filter[]>>;
    question: Question;
    getPolls: any;
}

export const Popup: React.FC<PopupProps> = ({
    handleClose,
    filters,
    setFilters,
    question,
    getPolls
}) => {

    const [questionInfo, setQuestionInfo] = useState<AnswerInfo[]>([]);
    
    useEffect(() => {
        fetch(`${server_url}/poll_info/${question.pollID}`)
        .then(data => data.json())
        .then(data => {
            let answerInfoList: AnswerInfo[] = [];
            data.data.forEach((element: any) => {
                 const newAnswerInfo: AnswerInfo = {
                     answer: (element[0] as string),
                     amount: (element[1] as number)
                 }
                 answerInfoList.push(newAnswerInfo);
            });
            setQuestionInfo(answerInfoList);
         })
        .catch(e => {
          alert("A problem occured");
        });
    }, []);

    const handleAnswerSelect = (answerInfo: AnswerInfo) => {
        const newFilter: Filter = {
          pollID: question.pollID,
          question: question.content,
          answer: answerInfo.answer
        }
        if(filters.filter(e => e.pollID === newFilter.pollID).length > 0) {
            alert("This poll is already filtered");
        }
        else {
            handleClose();
            const newFilterList = [...filters, newFilter];
            setFilters(newFilterList);
        }
    }

    const handleRemovePoll = () => {
      fetch(`${server_url}/remove_poll/${question.pollID}`)
      .then(resp => {
          if(resp.status === 200) {
              getPolls();
              handleClose();
          }
          else {
              alert("A problem occured");
          }    
      });
    }

    return (
    <div className="popup-box">
      <div className="box">
        <button style={{float: 'right', background: '#cc0c0c'}} onClick={() => handleRemovePoll()}>
          Remove Poll
        </button>
        <h2 style={{marginBottom: '20px', marginTop: '0', textDecoration: 'underline'}}>
          {question.content}
        </h2>
        <span className="close-icon" onClick={handleClose}>x</span>
        <div style={{position: 'relative', float: 'left', width: '50%', height: '30vh'}}>
          <Chart question={question} questionInfo={questionInfo}/>
        </div>
        <div style={{position: 'relative', float: 'right', width: '50%'}}>
          <h2>By which answer would you like to filter?</h2>
          {
              questionInfo.map(answerInfo => 
                  <div 
                    key={
                      questionInfo.findIndex((element) => 
                        element.answer === answerInfo.answer)
                      }
                    className="answers-row"
                  >
                    <button className="poll-button" onClick={() => handleAnswerSelect(answerInfo)}>
                      {answerInfo.answer}
                    </button>  
                  </div>)
          }
        </div>
      </div>
    </div>
  );
};
 
export default Popup;