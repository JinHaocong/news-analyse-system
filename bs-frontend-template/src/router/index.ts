import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import { IMenubarList } from '/@/type/store/layout'
import { components } from '/@/router/asyncRouter'

const Components: IObject<() => Promise<typeof import('*.vue')>> = Object.assign({}, components, {
    Layout: (() => import('/@/layout/index.vue')) as unknown as () => Promise<typeof import('*.vue')>,
    Redirect: (() => import('/@/layout/redirect.vue')) as unknown as () => Promise<typeof import('*.vue')>,
    LayoutBlank: (() => import('/@/layout/blank.vue')) as unknown as () => Promise<typeof import('*.vue')>
})

// 静态路由页面
export const allowRouter: Array<IMenubarList> = [
    {
        name: 'Data',
        path: '/',
        component: Components['Layout'],
        redirect: '/Data/List',
        meta: { title: '新闻数据', icon: 'el-icon-s-home' },
        children: [
            {
                name: 'DataList',
                path: '/Data/List',
                component: Components['Data'],
                meta: { title: '新闻数据', icon: 'el-icon-s-home' }
            }
        ]
    },
    {
        name: 'Detail_',
        path: '/Detail',
        component: Components['Layout'],
        meta: { title: '新闻详情', icon: 'el-icon-s-home', hidden: true },
        children: [
            {
                name: 'Detail',
                path: '/Detail/:id',
                props: true,
                component: Components['Detail'],
                meta: { title: '新闻详情', icon: 'el-icon-s-home' }
            }
        ]
    },
    {
        name: 'Analyse',
        path: '/Analyse',
        component: Components['Layout'],
        meta: { title: '内容分析', icon: 'el-icon-data-analysis', hidden: true },
        children: [
            {
                name: 'AnalyseList',
                path: '/Analyse/List/:subject',
                component: Components['Analyse'],
                props: true,
                meta: { title: '内容分析', icon: 'el-icon-data-analysis' }
            }
        ]
    },
    {
        name: 'ErrorPage',
        path: '/ErrorPage',
        meta: { title: '错误页面', icon: 'el-icon-eleme', hidden: true },
        component: Components.Layout,
        redirect: '/ErrorPage/404',
        children: [
            {
                name: '401',
                path: '/ErrorPage/401',
                component: Components['401'],
                meta: { title: '401', icon: 'el-icon-s-tools' }
            },
            {
                name: '404',
                path: '/ErrorPage/404',
                component: Components['404'],
                meta: { title: '404', icon: 'el-icon-s-tools' }
            }
        ]
    },
    {
        name: 'RedirectPage',
        path: '/redirect',
        component: Components['Layout'],
        meta: { title: '重定向页面', icon: 'el-icon-eleme', hidden: true },
        children: [
            {
                name: 'Redirect',
                path: '/redirect/:pathMatch(.*)*',
                meta: {
                    title: '重定向页面',
                    icon: ''
                },
                component: Components.Redirect
            }
        ]
    },
    {
        name: 'Login',
        path: '/Login',
        component: Components.Login,
        meta: { title: '登录', icon: 'el-icon-eleme', hidden: true }
    },
    {
        name: 'Register',
        path: '/Register',
        component: Components.Register,
        meta: { title: '注册', icon: 'el-icon-eleme', hidden: true }
    },
]

const router = createRouter({
    history: createWebHashHistory(), // createWebHistory
    routes: allowRouter as RouteRecordRaw[]
})

export default router