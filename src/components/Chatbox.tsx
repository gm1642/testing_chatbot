"use client"

import React, { useState, FormEvent, ChangeEvent, useEffect, useRef } from 'react';
import axios from 'axios';

interface Message {
  type: 'user' | 'bot';
  text: string;
  responseId?: string;
  rating?: number;
}

interface Feedback {
  response_id: string;
  rating: number;
  comment?: string;
}

const ChatBox: React.FC = () => {
  const [input, setInput] = useState<string>('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [feedback, setFeedback] = useState<Feedback>({ response_id: '', rating: 0 });
  const [showFeedbackDialog, setShowFeedbackDialog] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (input.trim() === '') return;

    const userMessage: Message = { type: 'user', text: input };
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setIsLoading(true);

    const loadingMessage: Message = { type: 'bot', text: 'Loading...', responseId: 'loading' };
    setMessages(prevMessages => [...prevMessages, loadingMessage]);

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/get_response', { prompt: input },
        { headers: { 'Content-Type': 'application/json' }
       }
      );
      const botMessage: Message = { 
        type: 'bot', 
        text: response.data.response,
        responseId: response.data.response_id 
      };
      setMessages(prevMessages => [...prevMessages.slice(0, -1), botMessage]);
    } catch (error) {
      console.error('Error fetching response:', error);
      const errorMessage: Message = { type: 'bot', text: 'Sorry, something went wrong. Please try again later.' };
      setMessages(prevMessages => [...prevMessages.slice(0, -1), errorMessage]);
    } finally {
      setIsLoading(false);
    }

    setInput('');
  };

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  const handleRating = (responseId: string, rating: number) => {
    setMessages(prevMessages =>
      prevMessages.map(msg =>
        msg.responseId === responseId ? { ...msg, rating } : msg
      )
    );
    setFeedback({ response_id: responseId, rating });
    setShowFeedbackDialog(true);
  };

  const handleCommentChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setFeedback(prev => ({ ...prev, comment: e.target.value }));
  };

  const submitFeedback = async () => {
    try {
      console.log('Sending feedback:', feedback);
      await axios.post('http://127.0.0.1:8000/api/feedback', feedback);
      alert('Thank you for your feedback!');
      setShowFeedbackDialog(false);
      setFeedback({ response_id: '', rating: 0 });
    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert('Failed to submit feedback. Please try again.');
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      alert('Copied to clipboard!');
    }).catch(err => {
      console.error('Failed to copy: ', err);
    });
  };

  return (
    <div className="flex flex-col h-full p-4">
      <div className="flex-grow overflow-y-auto mb-4">
        {messages.map((msg, index) => (
          <div key={index} className="mb-4">
            <div className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div
                className={`max-w-[70%] p-3 rounded-lg ${
                  msg.type === 'user' ? 'bg-customlightblue text-customwhite' : 'bg-customgrey text-customwhite'
                }`}
              >
                {msg.text}
              </div>
            </div>
            {msg.type === 'bot' && msg.responseId && msg.responseId !== 'loading' && (
              <div className="flex items-center mt-2 space-x-2">
                <button 
                  className="text-gray-400 hover:text-white text-sm"
                  onClick={() => copyToClipboard(msg.text)}
                >
                  Copy
                </button>
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    onClick={() => handleRating(msg.responseId!, star)}
                    className={`text-sm ${
                      star <= (msg.rating || 0) ? 'text-yellow-500' : 'text-gray-400'
                    } hover:text-yellow-500 focus:outline-none`}
                  >
                    ★
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <form className="flex justify-center mb-10" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Ask your question..."
          className="w-[780px] h-[55px] p-2 rounded bg-customgrey text-customwhite font-montserrat px-5"
          value={input}
          onChange={handleInputChange}
        />
        <button 
          type="submit" 
          className="bg-customgrey p-2 rounded ml-2"
          disabled={isLoading}
        >
          {isLoading ? (
            <div className="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-customwhite"></div>
          ) : (
            <img src="/send.svg" className="w-6 h-6 text-customwhite" alt="Send" />
          )}
        </button>
      </form>

      {showFeedbackDialog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-customgrey p-4 rounded-lg">
            <h2 className="text-customwhite mb-2">Additional Feedback (Optional)</h2>
            <textarea
              value={feedback.comment || ''}
              onChange={handleCommentChange}
              placeholder="Your comments..."
              className="w-full p-2 rounded bg-gray-700 text-customwhite font-montserrat mb-2"
            />
            <div className="flex justify-end">
              <button
                onClick={() => setShowFeedbackDialog(false)}
                className="mr-2 bg-customlightblue text-customwhite p-2 rounded"
              >
                Cancel
              </button>
              <button
                onClick={submitFeedback}
                className="bg-customlightblue text-customwhite p-2 rounded"
              >
                Submit Feedback
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatBox;
