import { IoClose } from 'react-icons/io5';
import FormEdit from './FormEdit';
import fields from '@/constants/form/datasets';
import api from '@/api/datasets';

export default function Component({ reload, setReload, id }) {
    const handleSubmit = async (e, data) => {
        e.preventDefault();
        const { name, description } = data;

        const newData = {
            name,
            description,
        };

        await api.updateDataset(newData, id);
        setReload(!reload);
        document.getElementById('dataset_detail').close();
    };

    const getData = async () => {
        const res = await api.getDataset({ id });
        const data = res.data[0];
        return {
            name: data.name,
            description: data.description,
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
                    title="Sửa thông tin tập dữ liệu"
                    onSubmit={handleSubmit}
                />
            </div>
            <form method="dialog" className="modal-backdrop">
                <button></button>
            </form>
        </>
    );
}
