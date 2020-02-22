import request from '@/utils/request'
import { encrypt } from '@/utils/rsa'

export function login(data) {
  data.password = encrypt(data.password)
  return request({
    url: '/login',
    method: 'post',
    data
  })
}

export function register(data) {
  data.password = encrypt(data.password)
  return request({
    url: '/register',
    method: 'post',
    data
  })
}

export function getInfo() {
  return request({
    url: '/user/getUserInfo',
    method: 'post'
  })
}

export function getUserInfo(data) {
  return request({
    url: '/user/getUserInfo',
    method: 'post',
    data
  })
}

export function resetPwd(data) {
  return request({
    url: '/user/resetPwd',
    method: 'post',
    data
  })
}

export function setUserInfo(data) {
  return request({
    url: '/user/setUserInfo',
    method: 'post',
    data
  })
}

export function setSubOrgs(data) {
  return request({
    url: '/user/setSubOrgs',
    method: 'post',
    data
  })
}

export function getUserList(data) {
  return request({
    url: '/user/list',
    method: 'post',
    data
  })
}

export function delUser(data) {
  return request({
    url: '/user/delUser',
    method: 'post',
    data
  })
}

export function setQuAuth(data) {
  return request({
    url: '/user/auth/qu',
    method: 'post',
    data
  })
}

export function addUser(data) {
  return request({
    url: '/user/add',
    method: 'post',
    data
  })
}

export function getUserQu(data) {
  return request({
    url: '/user/getQu',
    method: 'post',
    data
  })
}

export function setUserQuInfo(data) {
  return request({
    url: '/user/setUserQuInfo',
    method: 'post',
    data
  })
}

export function downloadReport(data) {
  return request({
    responseType: 'arraybuffer',
    url: '/user/downloadReport',
    method: 'post',
    data
  })
}

export function getReportText(data) {
  return request({
    url: '/user/getReportText',
    method: 'post',
    data
  })
}

export function userListSel(data) {
  return request({
    url: '/user/listSel',
    method: 'post',
    data
  })
}

export function userGetSel(data) {
  return request({
    url: '/user/getSel',
    method: 'post',
    data
  })
}

export function userSetSel(data) {
  return request({
    url: '/user/setSel',
    method: 'post',
    data
  })
}
