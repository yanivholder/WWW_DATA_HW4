import React, { useEffect, useState } from "react";
import { string } from "yargs";
import { AnswerInfo } from "../../../../types";
 
export interface CreatePollPopupProps {
    handleClose: any;
}

export const CreatePollPopup: React.FC<CreatePollPopupProps> = ({
    handleClose
}) => {

    //const [questionInfo, setQuestionInfo] = useState<AnswerInfo[]>([]);
    

    return (
    <div className="popup-box">
      <div className="box">
        <span className="close-icon" onClick={handleClose}>x</span>
        <div>
        {
            
        }
        </div>
      </div>
    </div>
  );
};
 
export default CreatePollPopup;