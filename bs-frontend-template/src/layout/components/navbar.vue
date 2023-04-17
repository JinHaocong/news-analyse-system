<template>
    <div
        v-if='getSetting.mode === &apos;vertical&apos; || getMenubar.isPhone'
        class='flex items-center px-4 flex-wrap h-12 leading-12'
    >
        <span
            class='text-2xl cursor-pointer h-12 leading-12'
            :class='{
                &apos;el-icon-s-fold&apos;: !getMenubar.status,
                &apos;el-icon-s-unfold&apos;: getMenubar.status,
            }'
            @click='changeCollapsed'
        />
        <!-- 面包屑导航 -->
        <div class='px-4'>
            <el-breadcrumb separator='/'>
                <transition-group name='breadcrumb'>
                    <el-breadcrumb-item
                        key='/'
                        :to='{ path: &apos;/&apos; }'
                    >主页</el-breadcrumb-item>
                    <el-breadcrumb-item
                        v-for='v in data.breadcrumbList'
                        :key='v.path'
                        :to='v.path'
                    >{{ v.title }}</el-breadcrumb-item>
                </transition-group>
            </el-breadcrumb>
        </div>
    </div>
    <div v-else class='flex items-center px-4 flex-wrap h-12 flex-1'>
        <div
            class='
        layout-sidebar-logo
        flex
        relative
        shadow-lg
        w-60
        leading-12
        items-center
      '
        >
            <!-- <img class="w-12 h-8" :src="icon" /> -->
            <span
                v-if='getMenubar.status === 0 || getMenubar.status === 2'
                class='pl-2'
            >{{ ImportMetaEnv.VITE_APP_TITLE }}</span>
        </div>
        <div class='layout-sidebar-menubar flex flex-1 overflow-hidden'>
            <layout-menubar />
        </div>
    </div>
    <div class='flex items-center flex-row-reverse px-4 min-width-32'>
        <!-- 用户下拉 -->
        <el-dropdown>
            <span class='el-dropdown-link flex flex-center px-2'>
                <!-- <el-avatar
          :size="30"
          src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
        /> -->
                <span class='ml-2'>{{ loginRequired ? userInfo.name : "选项" }}</span>
                <i class='el-icon-arrow-down el-icon--right' />
            </span>
            <template #dropdown>
                <el-dropdown-menu>
                    <el-dropdown-item>
                        <el-link
                            target='_blank'
                            :underline='false'
                            href='/admin'
                        >前往后台</el-link>
                    </el-dropdown-item>
                    <el-dropdown-item
                        v-if='loginRequired'
                        divided
                        @click='logout'
                    >退出登录</el-dropdown-item>
                </el-dropdown-menu>
            </template>
        </el-dropdown>

        <Screenfull />
        <Search />
    </div>
</template>

<script lang='ts'>
import { defineComponent, reactive, watch } from 'vue'
import { useLayoutStore } from '/@/store/modules/layout'
import { useRoute, RouteLocationNormalizedLoaded } from 'vue-router'
import Screenfull from '/@/layout/components/screenfull.vue'
import Search from '/@/layout/components/search.vue'
import LayoutMenubar from '/@/layout/components/menubar.vue'
import icon from '/@/assets/img/icon.png'

interface IBreadcrumbList {
  path: string;
  title: string | symbol;
}
// 面包屑导航
const breadcrumb = (route: RouteLocationNormalizedLoaded) => {
    const fn = () => {
        const breadcrumbList: Array<IBreadcrumbList> = []
        const notShowBreadcrumbList = ['Dashboard', 'RedirectPage'] // 不显示面包屑的导航
        if (
            route.matched[0] &&
            notShowBreadcrumbList.includes(route.matched[0].name as string)
        )
            return breadcrumbList
        route.matched.forEach((v) => {
            const obj: IBreadcrumbList = {
                title: v.meta.title as string,
                path: v.path
            }
            breadcrumbList.push(obj)
        })
        return breadcrumbList
    }
    let data = reactive({
        breadcrumbList: fn()
    })
    watch(
        () => route.path,
        () => (data.breadcrumbList = fn())
    )
    return { data }
}

export default defineComponent({
    name: 'LayoutNavbar',
    components: {
        Search,
        Screenfull,
        LayoutMenubar
    },
    setup() {
        const {
            getMenubar,
            getUserInfo,
            changeCollapsed,
            logout,
            getSetting,
            loginRequired
        } = useLayoutStore()
        const route = useRoute()
        return {
            loginRequired,
            getMenubar,
            userInfo: getUserInfo,
            changeCollapsed,
            logout,
            ...breadcrumb(route),
            getSetting,
            icon
        }
    }
})
</script>

<style lang='postcss' scoped>
.breadcrumb-enter-active,
.breadcrumb-leave-active {
  transition: all 0.5s;
}

.breadcrumb-enter-from,
.breadcrumb-leave-active {
  opacity: 0;
  transform: translateX(20px);
}

.breadcrumb-move {
  transition: all 0.5s;
}

.breadcrumb-leave-active {
  position: absolute;
}
</style>
