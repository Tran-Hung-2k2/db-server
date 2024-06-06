const fields = [
    {
        label: 'Tên kho dữ liệu',
        name: 'name',
        type: 'text',
        required: true,
        placeholder: 'Tên kho dữ liệu',
    },
    {
        label: 'Mô tả',
        name: 'description',
        type: 'textarea',
        placeholder: 'Mô tả kho dữ liệu',
    },
    {
        label: 'Lược đồ dữ liệu của kho',
        name: 'schema',
        type: 'textarea',
        className: 'h-44',
        required: true,
        placeholder:
            '{\n     "name": "string",\n     "age": "integer",\n     "balance": "double"\n     "timestamp": "datetime"\n}',
    },
];

export default fields;
