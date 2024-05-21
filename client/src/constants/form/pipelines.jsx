import label from '@constants/label';

const fields = [
    {
        label: 'Tên pipeline',
        name: 'name',
        type: 'text',
        required: true,
        placeholder: 'Tên pipeline',
    },
    {
        label: 'Loại',
        name: 'type',
        type: 'select',
        options: Object.values(label.pipeline_type).map((value) => ({ [value]: value })),
        required: true,
        placeholder: 'Loại',
    },
    {
        label: 'Mô tả',
        name: 'description',
        type: 'textarea',
        placeholder: 'Mô tả pipeline',
    },
];

export default fields;
