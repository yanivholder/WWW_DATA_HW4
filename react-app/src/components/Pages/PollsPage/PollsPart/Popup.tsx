import React, { useEffect, useState } from "react";
import { string } from "yargs";
import { AnswerInfo, Filter, Question } from "../../../../types";
 
export interface PopupProps {
    // TODO: change the type
    handleClose: any;
    filters: Filter[];
    setFilters: React.Dispatch<React.SetStateAction<Filter[]>>;
    question: Question;
}

export const Popup: React.FC<PopupProps> = ({
    handleClose,
    filters,
    setFilters,
    question
}) => {

    const [questionInfo, setQuestionInfo] = useState<AnswerInfo[]>([]);
    
    useEffect(() => {
        fetch(`/test/poll_info/${question.pollID}`)
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

    return (
    <div className="popup-box">
      <div className="box">
        <span className="close-icon" onClick={handleClose}>x</span>
        <div>
        {
            // TODO: add key
            questionInfo.map(answerInfo =>
                <>
                  <button onClick={() => handleAnswerSelect(answerInfo)}>
                    {answerInfo.answer}
                  </button>  
                  <p>{answerInfo.amount}</p>
                </>)
        }
        </div>
      </div>
    </div>
  );
};
 
export default Popup;