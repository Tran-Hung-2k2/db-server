import axios from './axios';

const api = {
    getChannel: async (params) => {
        const queryParams = ['id', 'user_id', 'type', 'limit', 'skip'];
        const paramsObject = {};

        if (params) {
            queryParams.forEach((param) => {
                if (params[param]) {
                    paramsObject[param] = params[param];
                }
            });
        }

        const response = await axios.get('/api/channels/', { withCredentials: true, params: paramsObject });

        return response.data;
    },

    createChannel: async (data) => {
        const response = await axios.post(`/api/channels/`, data, {
            withCredentials: true,
        });

        return response.data;
    },

    updateChannel: async (data, id) => {
        const response = await axios.patch(`/api/channels/${id}`, data, {
            withCredentials: true,
        });

        return response.data;
    },

    deleteChannel: async (id) => {
        const response = await axios.delete(`/api/channels/${id}`, {
            withCredentials: true,
        });

        return response.data;
    },
};

export default api;
