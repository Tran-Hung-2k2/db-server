import axios from './axios';

const api = {
    getDataMart: async (params) => {
        const queryParams = ['id', 'user_id', 'type', 'limit', 'skip', 'sort_by', 'sort_dim', 'name'];
        const paramsObject = {};

        if (params) {
            queryParams.forEach((param) => {
                if (params[param]) {
                    paramsObject[param] = params[param];
                }
            });
        }

        const response = await axios.get('/api/data_marts/', { withCredentials: true, params: paramsObject });

        return response.data;
    },

    createDataMart: async (data) => {
        const response = await axios.post(`/api/data_marts/`, data, {
            withCredentials: true,
        });

        return response.data;
    },

    updateDataMart: async (data, id) => {
        const response = await axios.patch(`/api/data_marts/${id}`, data, {
            withCredentials: true,
        });

        return response.data;
    },

    deleteDataMart: async (id) => {
        const response = await axios.delete(`/api/data_marts/${id}`, {
            withCredentials: true,
        });

        return response.data;
    },
};

export default api;
