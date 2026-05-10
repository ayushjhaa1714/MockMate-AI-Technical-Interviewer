// frontend/src/api/api.js
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export const startInterview = async (file, jobDescription) => {
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_description', jobDescription);

    const response = await axios.post(`${API_URL}/start-interview`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data; // Returns { session_id, message }
};

export const sendMessage = async (sessionId, answer) => {
    const response = await axios.post(`${API_URL}/chat`, {
        session_id: sessionId,
        answer: answer,
    });
    return response.data; // Returns { message, question_count }
};