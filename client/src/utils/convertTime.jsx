import { format } from 'date-fns';

const convertTime = (utcTime) => {
    const date = new Date(utcTime);
    return format(date, 'dd-MM-yyyy HH:mm:ss');
};

export default convertTime;
