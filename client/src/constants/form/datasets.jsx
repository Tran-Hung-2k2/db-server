const fields = [
    {
        label: 'Tên tập dữ liệu',
        name: 'name',
        type: 'text',
        required: true,
        placeholder: 'Tên tập dữ liệu',
    },
    {
        label: 'Mô tả',
        name: 'description',
        type: 'textarea',
        placeholder: 'Mô tả tập dữ liệu',
    },
    {
        label: 'Tập dữ liệu (.csv hoặc .zip)',
        name: 'file',
        type: 'file',
        accept: '.csv, .zip',
        required: true,
    },
];

export default fields;
