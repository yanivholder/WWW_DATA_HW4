export type FaqContent = {
    qID: number,
    question: string,
    answer: string;
}

export const faqContent: FaqContent[] = [
    {
        qID: 1,
        question: 'Hello World?',
        answer: 'Yes, Hello World fo sure',
    }
]