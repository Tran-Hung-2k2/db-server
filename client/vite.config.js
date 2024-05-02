import path from 'path';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    resolve: {
        alias: [
            { find: '@', replacement: '/src' },
            { find: '@assets', replacement: '/src/assets' },
            { find: '@api', replacement: '/src/api' },
            { find: '@layouts', replacement: '/src/layouts' },
            { find: '@components', replacement: '/src/components' },
            { find: '@constants', replacement: '/src/constants' },
            { find: '@pages', replacement: '/src/pages' },
            { find: '@routes', replacement: '/src/routes' },
            { find: '@utils', replacement: '/src/utils' },
            { find: '@redux', replacement: '/src/redux' },
        ],
    },
});
