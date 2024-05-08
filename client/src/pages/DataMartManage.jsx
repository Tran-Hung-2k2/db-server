import { useEffect, useState } from 'react';
import { FaSortAmountDown } from 'react-icons/fa';
import { FaSortAmountDownAlt } from 'react-icons/fa';
import { MdOutlineRateReview } from 'react-icons/md';
import { MdOutlineDelete } from 'react-icons/md';
import { MdOutlinePlaylistRemove } from 'react-icons/md';
import { IoSearch } from 'react-icons/io5';
import { FiPlus } from 'react-icons/fi';
import { IoClose } from 'react-icons/io5';

import Loader from '@components/Loader';
import DataMartCreate from '@/components/DataMartCreate';
import DataMartDetail from '@/components/DataMartDetail';

import api from '@/api/data_marts';

import convertTime from '@/utils/convertTime';
import confirm from '@/utils/confirm';

import recordPerPage from '@/constants/record_per_page';
import Pagination from '@/components/Pagination';
import { ToastContainer } from 'react-toastify';

export default function Page() {
    const [loading, setLoading] = useState(false);
    const [reload, setReload] = useState(false);

    const [limit, setLimit] = useState(recordPerPage[0]);
    const [total, setTotal] = useState(0);
    const [skip, setSkip] = useState(0);

    const [sortBy, setSortBy] = useState('');
    const [sortDim, setSortDim] = useState('');

    const [searchText, setSearchText] = useState('');

    const [id, setID] = useState('');
    const [dataList, setDataList] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            const res = await api.getDataMart({
                limit,
                skip,
                sort_by: sortBy,
                sort_dim: sortDim,
                name: searchText,
            });
            setTotal(res.total);
            setDataList(res.data);
            setLoading(false);
        };

        fetchData();
    }, [reload, limit, skip, sortBy, sortDim, searchText]);

    function deleteObj(id) {
        confirm({
            title: 'Xóa kho dữ liệu',
            message: `Xác nhận xóa vĩnh viễn kho dữ liệu.`,
            onConfirm: async () => {
                await api.deleteDataMart(id);
                setReload(!reload);
            },
        });
    }

    function SortableColumn({ name, label, className }) {
        return (
            <th
                onClick={() => {
                    setSortBy(name);
                    setSortDim(sortDim === 'asc' ? 'desc' : 'asc');
                }}
                className={`cursor-pointer font-normal ${className}`}
            >
                <div className="tooltip tooltip-accent tooltip-top " data-tip="Sắp xếp">
                    <div className={`text-base font-bold ${sortBy === name ? 'text-primary' : ''}`}>
                        <p className="inline-block !opacity-100">{label}</p>
                        <div
                            className={`inline-block ml-2 translate-y-0.5 ${
                                sortBy === name ? 'opacity-100' : 'opacity-0'
                            }`}
                        >
                            {sortDim == 'asc' ? <FaSortAmountDownAlt /> : <FaSortAmountDown />}
                        </div>
                    </div>
                </div>
            </th>
        );
    }

    return (
        <>
            <div className="flex-grow px-8 py-2">
                <dialog id="data_mart_create" className="modal">
                    <ToastContainer containerId="data_mart_create" style={{ zIndex: 9999 }} position="top-right" />
                    <DataMartCreate reload={reload} setReload={setReload} />
                </dialog>
                <dialog id="data_mart_detail" className="modal">
                    <ToastContainer containerId="data_mart_detail" style={{ zIndex: 9999 }} position="top-right" />
                    <DataMartDetail id={id} reload={reload} setReload={setReload} />
                </dialog>
                {/* Title */}
                <h3 className="pb-4 text-xl font-bold text-neutral">Quản lý kho dữ liệu</h3>

                {/* Action bar*/}
                <div className="flex justify-between">
                    <div className="flex flex-row gap-2 pb-4">
                        <button
                            className="h-10 py-2 font-bold text-white btn-sm btn btn-primary"
                            onClick={() => document.getElementById('data_mart_create').showModal()}
                        >
                            <FiPlus className="text-xl" />
                            Tạo mới
                        </button>

                        <label className="flex items-center h-10 gap-2 py-2 pl-2 w-fit input input-primary focus-within:outline-none focus-within:ring-primary focus-within:ring-1">
                            <IoSearch className="opacity-70" size={20} />
                            <input
                                type="text"
                                value={searchText}
                                onChange={(e) => setSearchText(e.target.value)}
                                className="grow max-w-40"
                                placeholder="Search"
                            />
                            <IoClose
                                size={20}
                                className={`cursor-pointer ${searchText ? 'opacity-100' : 'opacity-0'}`}
                                onClick={() => setSearchText('')}
                            />
                        </label>
                        {sortBy && (
                            <button
                                className="h-10 py-2 font-bold bg-white border btn-sm btn border-primary text-primary hover:bg-white hover:border-primary hover:opacity-75"
                                onClick={() => {
                                    setSortBy('');
                                    setSortDim('');
                                }}
                            >
                                <MdOutlinePlaylistRemove className="text-xl" />
                                Bỏ sắp xếp
                            </button>
                        )}
                    </div>

                    <div className="grid content-center grid-cols-2">
                        <select
                            className="inline-block h-6 font-semibold border-none focus:outline-none w-fit input"
                            value={limit}
                            onChange={(e) => {
                                setSkip(0);
                                setLimit(e.target.value);
                            }}
                        >
                            {recordPerPage.map((value, index) => (
                                <option key={index}>{value}</option>
                            ))}
                        </select>
                        <span className="inline -translate-x-3">/ trang</span>
                    </div>
                </div>

                {/* Table */}
                {loading ? (
                    <Loader />
                ) : (
                    <div className="flex flex-col items-center">
                        <table className="table border">
                            {/* head */}
                            <thead className="bg-zinc-100">
                                <tr>
                                    <th className="py-2 text-base text-center"></th>
                                    <SortableColumn className="py-2" name="name" label="Tên" />
                                    <SortableColumn className="py-2" name="description" label="Mô tả" />
                                    <SortableColumn className="py-2" name="created_at" label="Thời gian tạo" />
                                    <SortableColumn className="py-2" name="updated_at" label="Lần sửa đổi cuối" />
                                    <th className="py-2 text-base"></th>
                                </tr>
                            </thead>
                            <tbody>
                                {dataList?.map((data, index) => (
                                    <tr key={index}>
                                        <td className="py-2 text-center">
                                            <div className="text-base font-semibold">
                                                {parseInt(index) + parseInt(skip) + 1}
                                            </div>
                                        </td>
                                        <td className="p-0">
                                            <div>
                                                <div className="text-base font-semibold">{data?.name}</div>
                                            </div>
                                        </td>
                                        <td className="py-2 text-justify min-w-60">{data?.description}</td>
                                        <td className="py-2 font-mono">{convertTime(data?.created_at)}</td>
                                        <td className="py-2 font-mono">{convertTime(data?.updated_at)}</td>

                                        <td className="py-2 ">
                                            <div className="tooltip tooltip-accent tooltip-bottom" data-tip="Chi tiết">
                                                <button
                                                    className="text-xl bg-white border-none btn btn-xs btn-ghost text-success hover:bg-success hover:text-white"
                                                    onClick={() => {
                                                        setID(data?.id);
                                                        document.getElementById('data_mart_detail').showModal();
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

                        <Pagination skip={skip} setSkip={setSkip} limit={limit} total={total} />
                    </div>
                )}
            </div>
        </>
    );
}
