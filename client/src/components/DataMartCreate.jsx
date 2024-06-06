import { IoClose } from 'react-icons/io5';
import FormCreate from './FormCreate';
import fields from '@/constants/form/data_marts';
import notify from '@/utils/notify';
import api from '@/api/data_marts';

export default function Component({ reload, setReload }) {
    const handleSubmit = async (e, data) => {
        e.preventDefault();
        const { name, description, schema } = data;

        let jsonSchema;
        const validKeys = ['string', 'integer', 'double', 'datetime'];

        try {
            if (!isNaN(Number(schema))) {
                throw new Error('');
            }
            jsonSchema = JSON.parse(schema);

            const values = Object.values(jsonSchema);

            if (!values.every((value) => validKeys.includes(value))) {
                throw new Error('1');
            }
        } catch (error) {
            if (error.message == '1')
                notify(
                    'Lược đồ chỉ có các kiểu dữ liệu "string", "integer", "double" và "datetime"',
                    'error',
                    'data_mart_create',
                );
            else notify('Lược đồ dữ liệu phải có dạng JSON!', 'error', 'data_mart_create');
            return;
        }

        const newData = {
            name,
            description,
            schema: jsonSchema,
        };

        await api.createDataMart(newData);
        setReload(!reload);
        document.getElementById('data_mart_create').close();
    };

    return (
        <>
            <div className="w-11/12 max-w-2xl modal-box">
                <form method="dialog" className="mb-4">
                    {/* if there is a button in form, it will close the modal */}
                    <button className="absolute text-2xl font-black btn btn-base btn-circle btn-ghost right-2 top-2">
                        <IoClose />
                    </button>
                </form>
                <FormCreate fields={fields} title="Tạo kho dữ liệu mới" onSubmit={handleSubmit} />
            </div>
            <form method="dialog" className="modal-backdrop">
                <button></button>
            </form>
        </>
    );
}
