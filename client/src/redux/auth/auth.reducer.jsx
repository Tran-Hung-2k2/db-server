import type from './auth.type';

const initialState = {
    user: null,
};

const reducer = (state = initialState, action) => {
    switch (action.type) {
        case type.LOGIN:
            return {
                ...state,
                user: action.payload,
            };

        case type.LOGOUT:
            return {
                ...initialState,
            };

        default:
            return state;
    }
};

export default reducer;
