import { defineConfig } from 'vite'
import { resolve } from 'path'

import vue from '@vitejs/plugin-vue'
import WindiCSS from 'vite-plugin-windicss'
import liveReload from 'vite-plugin-live-reload'
import Icons from 'unplugin-icons/vite'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig(({ command, mode }) => {
    return {
        publicDir: 'icm/public',
        base: command === 'serve'
          ? 'https://localhost:3001/'
          : '/static/',

        plugins: [
            vue(),
            VitePWA({
                registerType: 'autoUpdate'
            }),
            WindiCSS({
                transformCSS: 'pre',
                scan: {
                    include: ['icm/**/*.{vue,html,js}'],
                }
            }),
            liveReload('./**/*.py'),
            Icons({ compiler: 'vue3' })
        ],

        build: {
            manifest: true,
            rollupOptions: {
                input: [
                    resolve(__dirname, '/icm/assets/main.js'),
                ]
            },
            outDir:  'icm/static',
            assetsDir:  'icm',
        },

        server: {
            port: 3001,
            host: '0.0.0.0',
            open: false,
            cors: true,

            // hmr: {
            //     port: 3001,
            //     host: 'localhost'
            // }
        }
    }
})
