import { GrUserManager } from 'react-icons/gr';
import { LuBrainCircuit } from 'react-icons/lu';
import { FiDatabase } from 'react-icons/fi';
import { LuWorkflow } from 'react-icons/lu';
import { MdOutlineDataExploration } from 'react-icons/md';

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
        title: 'Nguồn dữ liệu',
        role: [...Object.values(label.role)],
        child: [
            {
                path: '/channels/manage',
                title: 'Quản lý nguồn dữ liệu',
                role: [label.role.USER],
            },
        ],
        icon: <MdOutlineDataExploration />,
    },
    {
        title: 'Kho dữ liệu',
        role: [...Object.values(label.role)],
        child: [
            {
                path: '/datamarts/manage',
                title: 'Quản lý kho dữ liệu',
                role: [label.role.USER],
            },
        ],
        icon: <FiDatabase />,
    },
    {
        title: 'Pipelines',
        role: [label.role.ADMIN, label.role.USER],
        child: [
            {
                path: '/pipelines/manage',
                title: 'Quản lý pipelines',
                role: [label.role.USER],
            },
        ],
        icon: <LuWorkflow />,
    },
    {
        title: 'AI/ML',
        role: [label.role.USER],
        child: [
            {
                path: '/mlops/experiments/manage',
                title: 'Experiments',
                role: [label.role.USER],
            },
            {
                path: '/mlops/models/manage',
                title: 'Models',
                role: [label.role.USER],
            },
        ],
        icon: <LuBrainCircuit />,
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
