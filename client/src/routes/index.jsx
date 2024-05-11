import { lazy } from 'react';
import label from '@constants/label';

import MainLayout from '@layouts/MainLayout';
import AuthLayout from '@layouts/AuthLayout';

import SignIn from '@pages/SignIn';
import SignUp from '@pages/SignUp';
import NotFound from '@pages/NotFound';
import HomeNavigate from '@pages/HomeNavigate';

const ChannelManage = lazy(() => import('@pages/ChannelManage'));
const DataMartManage = lazy(() => import('@pages/DataMartManage'));
const DatasetManage = lazy(() => import('@/pages/DatasetManage'));
const MLOpsManage = lazy(() => import('@pages/MLOpsManage'));
const PipelineManage = lazy(() => import('@pages/PipelineManage'));
const PipelineEdit = lazy(() => import('@pages/PipelineEdit'));

const routes = [
    // Unauthorized routes
    {
        require: null,
        layouts: [
            {
                layout: AuthLayout,
                routes: [
                    {
                        path: '/signin',
                        component: SignIn,
                    },
                    {
                        path: '/signup',
                        component: SignUp,
                    },
                ],
            },
        ],
    },

    // User routes
    {
        require: [label.role.USER],
        layouts: [
            {
                layout: MainLayout,
                routes: [
                    {
                        path: '/channels/manage',
                        component: ChannelManage,
                    },
                    {
                        path: '/datamarts/manage',
                        component: DataMartManage,
                    },
                    {
                        path: '/datasets/manage',
                        component: DatasetManage,
                    },
                    {
                        path: '/pipelines/manage/edit',
                        component: PipelineEdit,
                    },
                    {
                        path: '/pipelines/manage',
                        component: PipelineManage,
                    },
                    {
                        path: '/mlops/experiments/manage',
                        component: MLOpsManage,
                    },
                    {
                        path: '/mlops/models/manage',
                        component: MLOpsManage,
                    },
                    {
                        path: '/mlops/enpoints/manage',
                        component: MLOpsManage,
                    },
                ],
            },
        ],
    },

    // Other routes
    {
        require: null,
        layouts: [
            {
                layout: null,
                routes: [
                    {
                        path: '/',
                        component: HomeNavigate,
                    },
                    {
                        path: '*',
                        component: NotFound,
                    },
                ],
            },
        ],
    },
];
export default routes;
