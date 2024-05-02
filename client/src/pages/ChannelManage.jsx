import _, { constant } from 'lodash';
import { useEffect, useState } from 'react';

import Loader from '@components/Loader';
import api from '@api/channels';
import convertTime from '@/utils/convertTime';
import avatars from '@/constants/channel_type_image';

export default function Page() {
    const [loading, setLoading] = useState(false);
    const [dataList, setDataList] = useState([]);
    // const dispatch = useDispatch();

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            const res = await api.getChannel();
            console.log(res.data?.data);
            const sortedList = _.orderBy(res.data?.data, ['created_at', 'name'], 'asc');
            setDataList(sortedList);
            setLoading(false);
        };
        fetchData();
    }, []);

    // const removeDevice = (id) => {
    //     setDevices((prev) => {
    //         return prev.filter((item) => item.Device_ID !== id);
    //     });
    // };

    // function deleteDevice(object) {
    //     confirm({
    //         title: 'Xóa thiết bị',
    //         message: `Khi bạn xác nhận thiết bị "${object.Name}" sẽ bị xóa vĩnh viễn và không thể khôi phục. Bạn vẫn muốn xóa?`,
    //         onConfirm: async () => {
    //             await service.deleteDevice(object.Device_ID);
    //             removeDevice(object.Device_ID);
    //         },
    //     });
    // }

    return (
        <>
            {loading ? (
                <Loader />
            ) : (
                <div className="m-8 overflow-x-auto w-fit">
                    <table className="table">
                        {/* head */}
                        <thead>
                            <tr>
                                <th className="text-center"></th>
                                <th className="text-center">Tên</th>
                                <th className="text-center">Loại</th>
                                <th className="text-center">Thời gian tạo</th>
                                <th className="text-center">Thời gian cập nhật</th>
                                <th className="text-center"></th>
                            </tr>
                        </thead>
                        <tbody>
                            {dataList?.map((data, index) => (
                                <tr key={index}>
                                    <td className="text-center">
                                        <div className="avatar">
                                            <div className="w-12 h-12 mask mask-squircle">
                                                <img src={avatars[data.type]} alt="Channel" />
                                            </div>
                                        </div>
                                    </td>
                                    <td className="text-center">
                                        <div className="flex items-center gap-3">
                                            <div>
                                                <div className="font-bold">{data.name}</div>
                                            </div>
                                        </div>
                                    </td>
                                    <td className="text-center">
                                        <span className="badge badge-ghost badge-sm">{data.type}</span>
                                    </td>
                                    <td className="text-center">{convertTime(data.created_at)}</td>
                                    <td className="text-center">{convertTime(data.updated_at)}</td>
                                    <td className="text-center">
                                        <button className="btn btn-ghost btn-xs">Chi tiết</button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </>
    );
}
