import { IoClose } from 'react-icons/io5';
import FormEdit from './FormEdit';
import fields from '@/constants/form/data_marts';
import api from '@/api/data_marts';
import notify from '@/utils/notify';

export default function Component({ reload, setReload, id }) {
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
                    'data_mart_detail',
                );
            else notify('Lược đồ dữ liệu phải có dạng JSON!', 'error', 'data_mart_detail');
            return;
        }

        const newData = {
            name,
            description,
            schema: jsonSchema,
        };

        await api.updateDataMart(newData, id);
        setReload(!reload);
        document.getElementById('data_mart_detail').close();
    };

    const getData = async () => {
        const res = await api.getDataMart({ id });
        const data = res.data[0];
        return {
            name: data.name,
            description: data.description,
            schema: JSON.stringify(data.schema),
        };
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
                <FormEdit
                    reload={id}
                    fields={fields}
                    getData={getData}
                    title="Sửa thông tin kho dữ liệu"
                    onSubmit={handleSubmit}
                />
            </div>
            <form method="dialog" className="modal-backdrop">
                <button></button>
            </form>
        </>
    );
}
