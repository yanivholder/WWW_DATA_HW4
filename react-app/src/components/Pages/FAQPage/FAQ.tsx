import React from 'react';
import '../../../App.css';
import { faqContent } from './faq-content';

export const FAQ = () => {

    return (
        <div className='faq-page-container'>
            <h2>  FAQ  </h2>
            { faqContent.map((faq) => 
                <details className='faq' key={faq.qID}>
                    <summary>{faq.question}</summary>
                    {faq.answer}
                </details>
            )}                        
        </div>
    )
}