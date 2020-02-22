import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/',
    component: () => import('@/views/root'),
    hidden: true
  },

  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    hidden: true,
    path: '/dashboard',
    component: Layout,
    redirect: '/dashboard/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '面板', icon: 'dashboard' }
    }]
  },

  {
    path: '/questionnair',
    component: Layout,
    redirect: '/questionnair/questionnair_do',
    name: 'Questionnair',
    meta: {
      title: '问卷',
      icon: 'form',
      role: ['document', 'form']
    },
    children: [
      {
        path: 'questionnair_do',
        name: 'Questionnair_do',
        component: () => import('@/views/questionnair/questionnair_do/index'),
        meta: { title: '问卷', icon: 'form' }
      },
      {
        hidden: true,
        path: 'qu_do',
        name: 'qu_do',
        component: () => import('@/views/questionnair/questionnair_do/qu_do'),
        meta: { title: '填写', noCache: true, icon: 'form' }
      }
    ]
  },

  {
    hidden: true,
    path: '/report',
    component: Layout,
    redirect: '/report/generate_report',
    name: 'Report',
    meta: {
      title: '报告',
      icon: 'documentation',
      role: ['document', 'form']
    },
    children: [
      {
        path: 'generate_report',
        name: 'Generate_report',
        component: () => import('@/views/report/generate_report/index'),
        meta: { title: '报告', icon: 'documentation' }
      },
      {
        path: 'general_report',
        name: 'General_report',
        component: () => import('@/views/report/general_report'),
        meta: { title: '综合报告', icon: 'documentation' }
      }
    ]
  },

  {
    path: '/personal',
    component: Layout,
    redirect: '/personal/personal_info',
    name: 'Personal',
    meta: {
      title: '个人中心',
      icon: 'user',
      role: ['admin', 'editor']
    },
    children: [
      {
        path: 'personal_info',
        name: 'Personal_info',
        component: () => import('@/views/personal/personal_info/index'),
        meta: { title: '个人信息', icon: 'documentation' }
      },
      {
        path: 'change_password',
        name: 'Change_password',
        component: () => import('@/views/personal/change_password/index'),
        meta: { title: '修改密码', icon: 'edit' }
      }
    ]
  }
]

/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
  {
    path: '/manage',
    component: Layout,
    redirect: '/manage/manage_user',
    // hidden: true,
    // alwaysShow: true,
    name: 'Manage',
    meta: {
      title: '管理',
      icon: 'component',
      roles: 2
    },
    children: [
      {
        path: 'home',
        name: 'Home',
        component: () => import('@/views/manage/home/index'),
        meta: { title: '机构首页', icon: 'international' }
      },
      {
        path: 'user_data_hub',
        component: () => import('@/views/manage/user_data_hub/index'),
        redirect: '/manage/user_data_hub/user_data',
        name: 'UserDataHub',
        meta: { title: '用户数据', icon: 'chart' },
        children: [
          {
            path: 'user_data',
            name: 'UserData',
            component: () => import('@/views/manage/user_data_hub/user_data/index'),
            meta: { title: '用户数据', icon: 'table' }
          },
          {
            hidden: true,
            path: 'user_data_personal',
            name: 'UserDataPersona',
            component: () => import('@/views/manage/user_data_hub/user_data/user_data_personal'),
            meta: { title: '个人数据', icon: 'table' }
          }
        ]
      },
      {
        path: 'manage_user',
        name: 'Manage_user',
        component: () => import('@/views/manage/manage_user/index'),
        meta: { title: '用户管理', icon: 'user' }
      },
      {
        path: 'manage_qu',
        name: 'Manage_qu',
        component: () => import('@/views/manage/manage_qu/index'),
        meta: { title: '问卷管理', icon: 'form', roles: 100 }
      },
      {
        hidden: true,
        path: 'manage_qu/qu_edit',
        name: 'Qu_edit',
        component: () => import('@/views/manage/manage_qu/qu_edit'),
        meta: { title: '问卷编辑', noCache: true, icon: 'form' }
      },
      {
        hidden: true,
        path: 'manage_qu/qu_edit_report',
        name: 'Qu_edit_report',
        component: () => import('@/views/manage/manage_qu/qu_edit_report'),
        meta: { title: '报告编辑', noCache: true, icon: 'form' }
      },
      {
        hidden: true,
        path: 'manage_qu/qu_do',
        name: 'Qu_do',
        component: () => import('@/views/questionnair/questionnair_do/qu_do'),
        meta: { title: '浏览', noCache: true, icon: 'form' }
      },
      {
        path: 'upload_data',
        name: 'Upload_data',
        component: () => import('@/views/manage/upload_data/index'),
        meta: { title: '上传数据', icon: 'excel', roles: 4 }
      },
      {
        path: 'organization',
        name: 'organization',
        component: () => import('@/views/manage/organization/index'),
        meta: { title: '机构管理', icon: 'tree', roles: 4 }
      },
      {
        path: 'system',
        name: 'system',
        component: () => import('@/views/manage/system/index'),
        meta: { title: '系统管理', icon: 'example', roles: 100 }
      },
      {
        path: 'manage_user/set',
        name: 'Manage_user_set',
        component: () => import('@/views/manage/component/set'),
        meta: { title: '用户信息' },
        hidden: true
      }
    ]
  },
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
