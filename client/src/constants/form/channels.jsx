import label from '@constants/label';

const fields = [
    {
        label: 'Tên nguồn dữ liệu',
        name: 'name',
        type: 'text',
        required: true,
        placeholder: 'Tên nguồn dữ liệu',
    },
    {
        label: 'Loại nguồn dữ liệu',
        name: 'type',
        type: 'select',
        options: Object.values(label.channel_type).map((value) => ({ [value]: value })),
        required: true,
        disable: 1,
        placeholder: 'Loại nguồn dữ liệu',
    },
    {
        label: 'Mô tả',
        name: 'description',
        type: 'textarea',
        placeholder: 'Mô tả nguồn dữ liệu',
    },
    {
        label: 'Host',
        name: 'host',
        type: 'text',
        required: true,
        placeholder: '192.1689.1.1',
        col: 1,
        inline_label: 1,
    },
    {
        label: 'Port',
        name: 'port',
        type: 'text',
        required: true,
        placeholder: '80',
        col: 1,
        inline_label: 1,
    },
    {
        label: 'Database',
        name: 'db_name',
        type: 'text',
        required: true,
        placeholder: 'postgres',
        col: 1,
        inline_label: 1,
    },
    {
        label: 'Username',
        name: 'username',
        type: 'text',
        required: true,
        col: 1,
        placeholder: 'postgres',
        inline_label: 1,
    },
    {
        label: 'Password',
        name: 'password',
        type: 'password',
        required: true,
        placeholder: 'Mật khẩu truy cập database',
        inline_label: 1,
    },
];

export default fields;
