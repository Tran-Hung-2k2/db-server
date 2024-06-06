import { FiFolder } from 'react-icons/fi';
import { GrUserManager } from 'react-icons/gr';
import { LuBrainCircuit } from 'react-icons/lu';
import { FiDatabase } from 'react-icons/fi';
import { LuWorkflow } from 'react-icons/lu';
import { MdOutlineDataExploration } from 'react-icons/md';
import { TbClipboardData } from 'react-icons/tb';
import { MdOutlineWbCloudy } from 'react-icons/md';
import { SiJupyter } from 'react-icons/si';

import label from './label';

const menuItem = [
    { label: 'DataOps' },
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
        title: 'Notebooks',
        role: [label.role.ADMIN, label.role.USER],
        child: [
            {
                path: '/notebooks/manage',
                title: 'Quản lý notebooks',
                role: [label.role.USER],
            },
        ],
        icon: <SiJupyter size={23} />,
        bigIcon: <SiJupyter size={30} />,
    },
    { label: 'MLOps' },
    {
        title: 'Dự án',
        role: [label.role.USER],
        child: [
            {
                path: '/mlops/experiments/manage',
                title: 'Quản lý dự án',
                role: [label.role.USER],
            },
        ],
        icon: <FiFolder size={21} />,
        bigIcon: <FiFolder size={30} />,
    },
    {
        title: 'Mô hình',
        role: [label.role.USER],
        child: [
            {
                path: '/mlops/models/manage',
                title: 'Quản lý mô hình',
                role: [label.role.USER],
            },
        ],
        icon: <LuBrainCircuit size={23} />,
        bigIcon: <LuBrainCircuit size={30} />,
    },
    {
        title: 'Triển khai',
        role: [label.role.USER],
        child: [
            {
                path: '/mlops/enpoints/manage',
                title: 'Triển khai mô hình',
                role: [label.role.USER],
            },
        ],
        icon: <MdOutlineWbCloudy size={21} />,
        bigIcon: <MdOutlineWbCloudy size={30} />,
    },
    {
        label: 'Other',
    },
    {
        path: '/signin',
        title: 'Đăng xuất',
        role: [...Object.values(label.role)],
    },
];

export default menuItem;
