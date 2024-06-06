import type from './auth.type';
import api from '@api/auth';

const action = {
    signin: (data, callback) => async (dispatch) => {
        const response = await api.signin(data);
        dispatch({
            type: type.LOGIN,
            payload: response.data,
        });
        if (callback) callback();
    },

    logout: () => async (dispatch) => {
        await api.logout();

        dispatch({
            type: type.LOGOUT,
        });
    },
};

export default action;
