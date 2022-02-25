export interface Question {
    pollID: number;
    content: string;
}

export interface AnswerInfo {
    answer: string;
    amount: number;
}

export interface Filter {
    pollID: number;
    question: string;
    answer: string;
}