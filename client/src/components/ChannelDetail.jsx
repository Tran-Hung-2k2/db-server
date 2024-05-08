import { IoClose } from 'react-icons/io5';
import FormEdit from './FormEdit';
import fields from '@/constants/form/channels';
import api from '@/api/channels';

export default function Component({ reload, setReload, id }) {
    const handleSubmit = async (e, data) => {
        e.preventDefault();
        const { name, type, description, ...config } = data;

        const newData = {
            name,
            description,
            config,
        };

        console.log(newData);
        await api.updateChannel(newData, id);
        setReload(!reload);
        document.getElementById('channel_detail').close();
    };

    const getData = async () => {
        const res = await api.getChannel({ id });
        const data = res.data?.data[0];
        return {
            name: data.name,
            description: data.description,
            type: data.type,
            ...data.config,
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
                    title="Sửa thông tin nguồn dữ liệu"
                    onSubmit={handleSubmit}
                />
            </div>
            <form method="dialog" className="modal-backdrop">
                <button></button>
            </form>
        </>
    );
}
