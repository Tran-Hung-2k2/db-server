import { MdOutlineEmail } from 'react-icons/md';
import { FaRegUser } from 'react-icons/fa';
import { LuKeyRound } from 'react-icons/lu';

const fields = [
    {
        label: 'Tên người dùng',
        id: 'Name',
        type: 'text',
        icon: <FaRegUser size={20} />,
        required: true,
        placeholder: 'Tên người dùng',
    },
    {
        label: 'Email',
        id: 'Email',
        type: 'email',
        icon: <MdOutlineEmail size={20} />,
        required: true,
        placeholder: 'Địa chỉ Email',
    },
    {
        label: 'Mật khẩu',
        id: 'Password',
        type: 'password',
        icon: <LuKeyRound size={20} />,
        required: true,
        placeholder: 'Mật khẩu',
    },
    {
        label: 'Nhập lại mật khẩu',
        id: 'Confirm_Password',
        type: 'password',
        required: true,
        icon: <LuKeyRound size={20} />,
        placeholder: 'Nhập lại mật khẩu',
    },
];

export default fields;
