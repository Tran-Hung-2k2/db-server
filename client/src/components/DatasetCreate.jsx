import { IoClose } from 'react-icons/io5';
import FormCreate from './FormCreate';
import fields from '@/constants/form/datasets';
import api from '@/api/datasets';

export default function Component({ reload, setReload }) {
    const handleSubmit = async (e, data) => {
        e.preventDefault();

        const formData = new FormData();
        for (const key in data) {
            formData.append(key, data[key]);
        }

        await api.createDataset(formData);
        setReload(!reload);
        document.getElementById('dataset_create').close();
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
                <FormCreate fields={fields} title="Tạo tập dữ liệu mới" onSubmit={handleSubmit} />
            </div>
            <form method="dialog" className="modal-backdrop">
                <button></button>
            </form>
        </>
    );
}
