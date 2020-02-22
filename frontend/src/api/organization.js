import request from '@/utils/request'

export function org_list(data) {
  return request({
    url: '/org/list',
    method: 'post',
    data
  })
}

export function org_list_name(data) {
  return request({
    url: '/org/list/name',
    method: 'post',
    data
  })
}

export function org_add(data) {
  return request({
    url: '/org/add',
    method: 'post',
    data
  })
}

export function org_set(data) {
  return request({
    url: '/org/set',
    method: 'post',
    data
  })
}

export function org_del(data) {
  return request({
    url: '/org/del',
    method: 'post',
    data
  })
}

export function getSubOrgs(data) {
  return request({
    url: '/org/getSubOrgs',
    method: 'post',
    data
  })
}
