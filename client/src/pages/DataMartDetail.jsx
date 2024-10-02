import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { VscSend } from 'react-icons/vsc';
import { IoClose } from 'react-icons/io5';
import { TbFileTypeSql } from 'react-icons/tb';

import Loader from '@components/Loader';
import ButtonBack from '@components/ButtonBack';

import api from '@/api/datasets';
import apiDataMart from '@/api/data_marts';

import convertTime from '@/utils/convertTime';

import recordPerPage from '@/constants/record_per_page';
import Pagination from '@/components/Pagination';

export default function Page() {
    const { id } = useParams();

    const { user } = useSelector((state) => state.auth);
    const [loading, setLoading] = useState(true);

    const [limit, setLimit] = useState(recordPerPage[2]);
    const [total, setTotal] = useState(0);
    const [skip, setSkip] = useState(0);

    const [SQLCommand, setSQLCommand] = useState('SELECT * FROM dataset');
    const [SQL, setSQL] = useState('SELECT * FROM dataset');

    const [dataList, setDataList] = useState([]);
    const [dataset, setDataset] = useState();

    useEffect(() => {
        const fetchData = async () => {
            const res = await apiDataMart.getDataMart({
                id: id,
            });
            setDataset(res.data[0]);
        };

        fetchData();
        document.title = 'Dataset | DEP';
    }, []);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            const res = await api.queryDataset({
                limit,
                skip,
                dataset_id: id,
                sql_cmd: SQL,
            });
            setTotal(res.total);
            setDataList(res.data);
            console.log(res.data);
            setLoading(false);
        };

        fetchData();
        document.title = 'Dataset | DEP';
    }, [limit, skip, SQL]);

    return (
        <>
            <div className="flex-grow px-8 py-2max-w-screen">
                <ButtonBack className="my-2" />
                {/* Title */}
                <h3 className="pb-4 text-xl font-bold text-neutral">Thông tin chi tiết kho dữ liệu</h3>
                {dataset && (
                    <div className="flex flex-col gap-2 mb-4">
                        <p>
                            <span className="font-semibold">Tên kho dữ liệu:</span> {dataset.name}
                        </p>
                        <p>
                            <span className="font-semibold">Đường dẫn:</span> {'s3://' + user.id + '/' + dataset.id}
                        </p>
                        <p>
                            <span className="font-semibold">Thời gian tạo:</span> {convertTime(dataset.created_at)}
                        </p>
                        <p>
                            <span className="font-semibold">Lần cập nhật gần nhất:</span>{' '}
                            {convertTime(dataset.updated_at)}
                        </p>
                    </div>
                )}
                {/* Action bar*/}
                <div className="flex justify-between">
                    <div className="flex flex-row gap-2 pb-4">
                        <label className="flex items-center h-10 gap-2 py-2 pl-2 w-fit input input-primary focus-within:outline-none focus-within:ring-primary focus-within:ring-1">
                            <TbFileTypeSql className="opacity-70" size={23} />
                            <input
                                type="text"
                                value={SQLCommand}
                                onChange={(e) => setSQLCommand(e.target.value)}
                                className="grow min-w-60"
                                placeholder="SELECT * FROM dataset"
                            />
                            <IoClose
                                size={20}
                                className={`cursor-pointer ${SQLCommand ? 'opacity-100' : 'opacity-0'}`}
                                onClick={() => setSQLCommand('')}
                            />
                        </label>
                        <button
                            className="h-10 py-2 font-bold bg-white border btn-sm btn border-primary text-primary hover:bg-white hover:border-primary hover:opacity-75"
                            onClick={() => {
                                setSQL(SQLCommand);
                            }}
                        >
                            <VscSend className="text-xl" />
                            Áp dụng
                        </button>
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
                    <div className="flex flex-col items-center overflow-x-auto w-fit">
                        <table className="table overflow-x-auto border">
                            {/* head */}
                            <thead className="bg-zinc-100">
                                <tr>
                                    <th className="py-2 text-base"></th>
                                    {Object.keys(dataList?.schema).map((key, index) => (
                                        <th key={index} className="py-2 text-justify">
                                            {key}
                                        </th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {dataList?.result.map((data, index) => (
                                    <tr key={index}>
                                        <td className="py-2 text-center">
                                            <div className="text-base font-semibold">
                                                {parseInt(index) + parseInt(skip) + 1}
                                            </div>
                                        </td>
                                        {Object.keys(dataList.schema).map((key, idx) => (
                                            <td key={idx} className="py-2 text-justify">
                                                {data[key] !== null ? data[key].toString() : ''}
                                            </td>
                                        ))}
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
