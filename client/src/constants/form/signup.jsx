const fields = [
    {
        label: 'Tên người dùng',
        id: 'Name',
        type: 'text',
        required: true,
        placeholder: 'Tên người dùng',
    },
    {
        label: 'Email',
        id: 'Email',
        type: 'email',
        required: true,
        placeholder: 'Địa chỉ Email',
    },
    {
        label: 'Mật khẩu',
        id: 'Password',
        type: 'password',
        required: true,
        placeholder: 'Mật khẩu',
    },
    {
        label: 'Nhập lại mật khẩu',
        id: 'Confirm_Password',
        type: 'password',
        required: true,
        placeholder: 'Nhập lại mật khẩu',
    },
];

export default fields;
