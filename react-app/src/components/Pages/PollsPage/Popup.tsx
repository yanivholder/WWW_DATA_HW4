import React, { useEffect, useState } from "react";
import { string } from "yargs";
import { AnswerInfo } from "../../../types";
 
export interface PopupProps {
    // TODO: change the type
    pollID: number;
    handleClose: any;
}

export const Popup: React.FC<PopupProps> = ({
    pollID,
    handleClose
}) => {

    const [questionInfo, setQuestionInfo] = useState<AnswerInfo[]>([]);
    
    useEffect(() => {
        fetch(`/test/poll_info/${pollID}`)
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

    return (
    <div className="popup-box">
      <div className="box">
        <span className="close-icon" onClick={handleClose}>x</span>
        <div>
        {
            // TODO: add key
            questionInfo.map(answerInfo =>
                <><p>{answerInfo.answer}</p><p>{answerInfo.amount}</p></>)
        }
        </div>
      </div>
    </div>
  );
};
 
export default Popup;