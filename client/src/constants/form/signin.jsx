import { MdOutlineEmail } from 'react-icons/md';
import { LuKeyRound } from 'react-icons/lu';

const fields = [
    {
        label: 'Email',
        id: 'Email',
        type: 'email',
        required: true,
        icon: <MdOutlineEmail size={20} />,
        placeholder: 'Địa chỉ Email',
    },
    {
        label: 'Mật khẩu',
        id: 'Password',
        icon: <LuKeyRound size={20} />,
        type: 'password',
        required: true,
        placeholder: 'Mật khẩu',
    },
];

export default fields;
