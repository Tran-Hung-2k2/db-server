import axios from './axios';

const api = {
    getPipeline: async (params) => {
        const queryParams = ['id', 'user_id', 'type', 'limit', 'skip', 'sort_by', 'sort_dim', 'name'];
        const paramsObject = {};

        if (params) {
            queryParams.forEach((param) => {
                if (params[param]) {
                    paramsObject[param] = params[param];
                }
            });
        }

        const response = await axios.get('/api/pipelines/', { withCredentials: true, params: paramsObject });

        return response.data;
    },

    createPipeline: async (data) => {
        const response = await axios.post(`/api/pipelines/`, data, {
            withCredentials: true,
        });

        return response.data;
    },

    updatePipeline: async (data, id) => {
        const response = await axios.patch(`/api/pipelines/${id}`, data, {
            withCredentials: true,
        });

        return response.data;
    },

    deletePipeline: async (id) => {
        const response = await axios.delete(`/api/pipelines/${id}`, {
            withCredentials: true,
        });

        return response.data;
    },
};

export default api;
