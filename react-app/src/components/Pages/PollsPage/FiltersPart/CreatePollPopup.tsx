import { async } from "q";
import React, { useEffect, useState } from "react";
import { string } from "yargs";
import { server_url } from "../../../../app-constants";
import { AnswerInfo, Filter } from "../../../../types";
 
export interface CreatePollPopupProps {
    handleClose: any;
    filters: Filter[];
    setFilters: React.Dispatch<React.SetStateAction<Filter[]>>;
    getPolls: any;
}

export const CreatePollPopup: React.FC<CreatePollPopupProps> = ({
    handleClose,
    filters,
    setFilters,
    getPolls
}) => {

    const [question, setQuestion] = useState<string>("");
    const [answer1, setAnswer1] = useState<string>("");
    const [answer2, setAnswer2] = useState<string>("");
    const [answer3, setAnswer3] = useState<string>("");
    const [answer4, setAnswer4] = useState<string>("");

    let answerArray: string[] = [answer1, answer2];
    if(answer3 !== "") {
        answerArray.push(answer3);
    }
    if(answer4 !== "") {
        answerArray.push(answer4);
    }

    const createFiltersString = (): string => {
        let res: string = "";
        filters.forEach(filter => 
            res = res.concat(`${filter.pollID},${filter.answer}$`));
        return res;
    }

    const QuestionAndAnswerNotValid = (element: string) => {
        return ((element.length > 30) || (element !== "" && (!element.match("^[A-Za-z0-9\? -]+$"))));
    }

    const handleSubmit = async () => {
        if(question === "") {
            alert("Your Question is empty");
        } 
        else if(answer1 === "" || answer2 === "") {
            alert("You have to fill at least 2 answers");
        } else if(
                    (QuestionAndAnswerNotValid(question)) ||
                    (QuestionAndAnswerNotValid(answer1)) ||
                    (QuestionAndAnswerNotValid(answer2)) ||
                    (QuestionAndAnswerNotValid(answer3)) ||
                    (QuestionAndAnswerNotValid(answer4))
                ) {
            alert("The question and the answers should contain only letters and number, '-', and '?'. Also, is can be at max 30 characters");
        }
        else if(new Set(answerArray).size !== answerArray.length) {
            alert("All answers must be different");
        }
        else {
            await fetch(`${server_url}/add_poll`,
            {
                method: 'GET',
                headers: {
                    'question': question,
                    'answer1': answer1,
                    'answer2': answer2,
                    'answer3': answer3,
                    'answer4': answer4,
                    'filters': createFiltersString(),
                    'Content-Type': 'application/json'   
                }
            })
            .then(resp => {
                if(resp.status === 200) {
                    setFilters([]);
                    getPolls();
                    handleClose();
                } 
                else {
                    alert("A problem occured");
                }
            }); 
        }
    }


    return (
    <div className="popup-box">
      <div className="box">
        <span className="close-icon" onClick={handleClose}>x</span>
            <div className='container'>
                <label htmlFor="Question"><b>Question </b></label>
                <input id="Question"
                    type="text"
                    placeholder="Enter your question"
                    onChange={({ target }) => {setQuestion(target.value)}}
                />

                <label htmlFor="Possible Answers"><b>Possible Answers </b></label>
                <input id="Answer1"
                    type="text"
                    placeholder="First Answer - must"
                    onChange={({ target }) => {setAnswer1(target.value)}}
                />
                <input id="Answer2"
                    type="text"
                    placeholder="Second Answer - must"
                    onChange={({ target }) => {setAnswer2(target.value)}}
                />
                <input id="Answer3"
                    type="text"
                    placeholder="Third Answer - optional"
                    onChange={({ target }) => {setAnswer3(target.value)}}
                />
                <input id="Answer4"
                    type="text"
                    placeholder="Fourth Answer - optional"
                    onChange={({ target }) => {setAnswer4(target.value)}}
                />
            </div>

            <div id="button">
                <button className="nav-button" onClick={() => handleSubmit()}>Submit</button>
            </div>
      </div>
    </div>
  );
};
 
export default CreatePollPopup;