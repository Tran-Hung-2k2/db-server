import axios from './axios';

const api = {
    getDataset: async (params) => {
        const queryParams = ['id', 'user_id', 'limit', 'skip', 'sort_by', 'sort_dim', 'name'];
        const paramsObject = {};

        if (params) {
            queryParams.forEach((param) => {
                if (params[param]) {
                    paramsObject[param] = params[param];
                }
            });
        }

        const response = await axios.get('/api/datasets/', { withCredentials: true, params: paramsObject });

        return response.data;
    },

    createDataset: async (data) => {
        const fileField = data.get('file');
        const response = await axios.post(`/api/datasets/`, data, {
            withCredentials: true,
            headers: {
                Filename: fileField ? fileField.name : '',
            },
        });

        return response.data;
    },

    updateDataset: async (data, id) => {
        const response = await axios.patch(`/api/datasets/${id}`, data, {
            withCredentials: true,
        });

        return response.data;
    },

    deleteDataset: async (id) => {
        const response = await axios.delete(`/api/datasets/${id}`, {
            withCredentials: true,
        });

        return response.data;
    },
};

export default api;
