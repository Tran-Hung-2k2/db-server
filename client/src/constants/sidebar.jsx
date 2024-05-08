import { GrUserManager } from 'react-icons/gr';
import { LuBrainCircuit } from 'react-icons/lu';
import { FiDatabase } from 'react-icons/fi';
import { LuWorkflow } from 'react-icons/lu';
import { MdOutlineDataExploration } from 'react-icons/md';
import { TbClipboardData } from 'react-icons/tb';

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
        bigIcon: <GrUserManager size={30} />,
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
        icon: <MdOutlineDataExploration size={23} />,
        bigIcon: <MdOutlineDataExploration size={30} />,
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
        icon: <FiDatabase size={21} />,
        bigIcon: <FiDatabase size={28} />,
    },
    {
        title: 'Tập dữ liệu',
        role: [...Object.values(label.role)],
        child: [
            {
                path: '/datasets/manage',
                title: 'Quản lý tập dữ liệu',
                role: [label.role.USER],
            },
        ],
        icon: <TbClipboardData size={23} />,
        bigIcon: <TbClipboardData size={30} />,
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
        icon: <LuWorkflow size={23} />,
        bigIcon: <LuWorkflow size={30} />,
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
        icon: <LuBrainCircuit size={23} />,
        bigIcon: <LuBrainCircuit size={30} />,
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
