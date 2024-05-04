import _ from 'lodash';
import { useEffect, useState } from 'react';
import { MdOutlineRateReview } from 'react-icons/md';
import { MdOutlineDelete } from 'react-icons/md';
import { VscFilter } from 'react-icons/vsc';
import { FiPlus } from 'react-icons/fi';

import Loader from '@components/Loader';
import ChannelDetail from '@/components/ChannelDetail';
import ChannelCreate from '@/components/ChannelCreate';

import api from '@api/channels';

import convertTime from '@/utils/convertTime';
import confirm from '@/utils/confirm';

import avatars from '@/constants/channel_type_image';

export default function Page() {
    const [loading, setLoading] = useState(false);
    const [reload, setReload] = useState(false);
    const [id, setID] = useState('');
    const [dataList, setDataList] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            const res = await api.getChannel();
            setDataList(res.data?.data);
            setLoading(false);
        };

        fetchData();
    }, [reload]);

    function deleteObj(id) {
        confirm({
            title: 'Xóa nguồn dữ liệu',
            message: `Xác nhận xóa vĩnh viễn nguồn dữ liệu.`,
            onConfirm: async () => {
                await api.deleteChannel(id);
                setReload(!reload);
            },
        });
    }

    return (
        <>
            <div className="flex-grow w-full px-8 py-2 ">
                <dialog id="channel_create" className="modal">
                    <ChannelCreate reload={reload} setReload={setReload} />
                </dialog>
                <dialog id="channel_detail" className="modal">
                    <ChannelDetail id={id} />
                    
                </dialog>
                {/* Title */}
                <h3 className="pb-4 text-xl font-bold text-neutral">Quản lý nguồn dữ liệu</h3>

                {/* Action bar*/}
                <div className="flex flex-row gap-2 pb-4">
                    <button
                        className="h-10 py-2 font-bold text-white btn-sm btn btn-primary"
                        onClick={() => document.getElementById('channel_create').showModal()}
                    >
                        <FiPlus className="text-xl" />
                        Tạo mới
                    </button>

                    <button className="h-10 py-2 font-bold bg-white border btn-sm btn border-primary text-primary hover:bg-white hover:border-primary hover:opacity-75">
                        <VscFilter className="text-xl" />
                        Lọc
                    </button>
                </div>

                {/* Table */}
                {loading ? (
                    <Loader />
                ) : (
                    <table className="table border">
                        {/* head */}
                        <thead className="bg-zinc-100">
                            <tr>
                                <th className="pr-0 text-sm text-center"></th>
                                <th className="text-sm text-center">Tên</th>
                                <th className="text-sm text-center w-52">Loại</th>
                                <th className="w-56 text-sm text-center">Mô tả</th>
                                <th className="text-sm text-center">Thời gian tạo</th>
                                <th className="text-sm text-center">Thời gian cập nhật</th>
                                <th className="text-sm text-center"></th>
                            </tr>
                        </thead>
                        <tbody>
                            {dataList?.map((data, index) => (
                                <tr key={index}>
                                    <td className="pr-0 text-center">
                                        <div className="avatar">
                                            <div className="w-10 h-10 mask mask-squircle">
                                                <img src={avatars[data?.type]} alt="Channel" />
                                            </div>
                                        </div>
                                    </td>
                                    <td className="text-center">
                                        <div>
                                            <div className="text-base font-semibold">{data?.name}</div>
                                        </div>
                                    </td>
                                    <td className="text-center">
                                        <span className="font-semibold badge badge-ghost badge-base h-fit">
                                            {data?.type}
                                        </span>
                                    </td>
                                    <td className="text-justify">{data?.description}</td>
                                    <td className="font-mono text-center">{convertTime(data?.created_at)}</td>
                                    <td className="font-mono text-center">{convertTime(data?.updated_at)}</td>

                                    <td className="text-center">
                                        <div className="tooltip tooltip-accent tooltip-bottom" data-tip="Chi tiết">
                                            <button
                                                className="text-xl bg-white border-none btn btn-xs btn-ghost text-success hover:bg-success hover:text-white"
                                                onClick={() => {
                                                    setID(data?.id);
                                                    document.getElementById('channel_detail').showModal();
                                                }}
                                            >
                                                <MdOutlineRateReview />
                                            </button>
                                        </div>
                                        <div className="tooltip tooltip-accent tooltip-bottom" data-tip="Xóa">
                                            <button
                                                className="text-xl bg-white border-none btn btn-xs text-error hover:bg-error hover:text-white"
                                                onClick={() => deleteObj(data?.id)}
                                            >
                                                <MdOutlineDelete />
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
        </>
    );
}
