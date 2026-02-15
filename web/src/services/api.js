import axios from 'axios';

const api = axios.create({
    baseURL: 'https://quick-tt-1.onrender.com'
});

export const getTimetables = () => api.get('/timetables');
export const getTimetable = (name) => api.get(`/timetables/${name}`);
export const deleteTimetable = (name) => api.delete(`/timetables/${name}`);
export const generateTimetable = (data) => api.post('/generate', data);
export const saveTimetable = (data) => api.post('/timetables', data);

export default api;
