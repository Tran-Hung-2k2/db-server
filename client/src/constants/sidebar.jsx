import { GrUserManager } from 'react-icons/gr';
import { GoArrowSwitch } from 'react-icons/go';
import { LuParkingCircle } from 'react-icons/lu';
import { CiCreditCard1 } from 'react-icons/ci';
import { BsFillDeviceSsdFill } from 'react-icons/bs';

import label from './label';

const menuItem = [
    { label: 'MENU' },
    {
        title: 'Người dùng',
        role: [label.role.ADMIN],
        child: [
            {
                path: '/users/manage',
                title: 'Quản lý người dùng',
                role: [label.role.ADMIN],
            },
        ],
        icon: <GrUserManager />,
    },
    {
        title: 'Channel',
        role: [...Object.values(label.role)],
        child: [
            {
                path: '/in-out/parking',
                title: 'Quản lý channel',
                role: [label.role.MANAGER],
            },
            {
                path: '/record/manager',
                title: 'Lịch sử ra vào',
                role: [label.role.USER, label.role.ADMIN],
            },
        ],
        icon: <GoArrowSwitch />,
    },
    {
        title: 'Bãi đỗ xe',
        role: [...Object.values(label.role)],
        child: [
            {
                path: '/parking/info',
                title: 'Thông tin các bãi đỗ xe',
                role: [label.role.USER, label.role.MANAGER],
            },
            {
                path: '/parking/manager',
                title: 'Quản lý bãi đỗ xe',
                role: [label.role.ADMIN],
            },
            {
                path: '/parking/add',
                title: 'Thêm bãi đỗ xe',
                role: [label.role.ADMIN],
            },
        ],
        icon: <LuParkingCircle />,
    },
    {
        title: 'Thẻ gửi xe',
        role: [label.role.ADMIN, label.role.USER],
        child: [
            {
                path: '/card/manager',
                title: 'Quản lý thẻ gửi xe',
                role: [label.role.ADMIN, label.role.USER],
            },
            {
                path: '/card/add',
                title: 'Thêm thẻ gửi xe',
                role: [label.role.ADMIN],
            },
        ],
        icon: <CiCreditCard1 />,
    },
    {
        title: 'Thiết bị',
        role: [label.role.ADMIN],
        child: [
            {
                path: '/device/manager',
                title: 'Quản lý thiết bị',
                role: [label.role.ADMIN],
            },
            {
                path: '/device/add',
                title: 'Thêm thiết bị',
                role: [label.role.ADMIN],
            },
        ],
        icon: <BsFillDeviceSsdFill />,
    },
    {
        label: 'OTHER',
    },
    {
        path: '/signin',
        title: 'Đăng xuất',
        role: [...Object.values(label.role)],
    },
];

export default menuItem;
