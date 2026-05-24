import axios from 'axios';

// Esta es la URL donde corre tu backend (FastAPI)
const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1',
});

export default api;