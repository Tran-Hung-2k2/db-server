import axios from './axios';

const api = {
    signin: async (data) => (await axios.post('/api/auth/signin', data, { withCredentials: true })).data,

    signup: async (data) => (await axios.post('/api/auth/signup', data)).data,

    logout: async () => await axios.post('/api/auth/logout'),
};

export default api;
