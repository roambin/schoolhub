import request from '@/utils/request'

export function backup_list(data) {
  return request({
    url: '/system/backup/list',
    method: 'post',
    data
  })
}

export function backup_delete(data) {
  return request({
    url: '/system/backup/delete',
    method: 'post',
    data
  })
}

export function backup_dump(data) {
  return request({
    url: '/system/backup/dump',
    method: 'post',
    data
  })
}

export function backup_restore(data) {
  return request({
    url: '/system/backup/restore',
    method: 'post',
    data
  })
}
