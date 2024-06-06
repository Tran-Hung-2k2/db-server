import { toast } from 'react-toastify';

const notify = (text, type, containerId = 'main', duration = 1500, position = 'top-right') => {
    toast[type](text, {
        position: position,
        autoClose: duration,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: 'light',
        containerId: containerId,
    });
};

export default notify;
