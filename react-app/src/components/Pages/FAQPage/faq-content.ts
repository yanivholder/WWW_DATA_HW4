export type FaqContent = {
    qID: number,
    question: string,
    answer: string;
}

export const faqContent: FaqContent[] = [
    {
        qID: 1,
        question: 'How much does TelePoll Cost??',
        answer: 'It’s completely free!',
    },
    {
        qID: 2,
        question: 'What is a Restricted Poll?',
        answer: 'An admin can chose previous poll answers as filters on he’s new poll audience.' +
            ' For example: if we have previous polls such as “are you a student at the Technion?” ' +
            'and “what is your age?”\n We can choose to send the next poll only to those who answered' +
            ' “Yes” and “30-40”\n',
    },
    {
        qID: 3,
        question: 'How to Run/Send a Poll?',
        answer: 'Just enter the “Polls” section, chose filters (or don’t) and use the “new poll”' +
            ' interface to send your next poll to all your audience.',
    },
    {
        qID: 4,
        question: 'Comparison to Ordinary Surveys',
        answer: 'Our service runs via a telegram bot and as such, does not require your users to download a dedicated app',
    },
    {
        qID: 5,
        question: 'Security and reliability',
        answer: 'Admins are authenticated, none other can send polls.\n' +
            '+ We care about your password’s safety and will never save it as plain-text\n',
    },
    {
        qID: 6,
        question: 'Can I delte a Poll after I sent it?',
        answer: 'Polls cannot be deleted once sent'
    }

]