import _, { constant } from 'lodash';
import { useEffect, useState } from 'react';

import Loader from '@components/Loader';
import api from '@api/mlops';
import convertTime from '@/utils/convertTime';
import avatars from '@/constants/channel_type_image';

export default function Page() {
    const [loading, setLoading] = useState(false);
    const [dataList, setDataList] = useState([]);
    // const dispatch = useDispatch();

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            const res = await api.getExperiments();
            const sortedList = _.orderBy(res.experiments, ['name'], 'asc');
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
                                <th className="text-center">Tên</th>
                                <th className="text-center">Artifact Location</th>
                                <th className="text-center">Lifecycle Stage</th>
                                <th className="text-center">Thời gian tạo</th>
                                <th className="text-center">Lần cuối sửa đổi</th>
                                <th className="text-center"></th>
                            </tr>
                        </thead>
                        <tbody>
                            {dataList?.map((data, index) => (
                                <tr key={index}>
                                    <td className="text-center">
                                        <div className="flex items-center gap-3">
                                            <div>
                                                <div className="font-bold">{data.name}</div>
                                            </div>
                                        </div>
                                    </td>
                                    <td className="text-center">{data.artifact_location}</td>
                                    <td className="text-center">
                                        <span className="badge badge-ghost badge-sm">{data.lifecycle_stage}</span>
                                    </td>
                                    <td className="text-center">{convertTime(data.creation_time)}</td>
                                    <td className="text-center">{convertTime(data.last_update_time)}</td>
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
