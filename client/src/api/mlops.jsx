import axios from './axios';

const api = {
    getExperiments: async () => {
        const response = await axios.post('/api/ml/experiments/search', { max_results: 100 });

        return response.data;
    },
};

export default api;
