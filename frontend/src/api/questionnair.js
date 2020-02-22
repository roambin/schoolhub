import request from '@/utils/request'

export function getQuList(data) {
  return request({
    url: '/qu/list',
    method: 'post',
    data
  })
}

export function getQuInfo(data) {
  return request({
    url: '/qu/getQuInfo',
    method: 'post',
    data
  })
}

export function setQuData(data) {
  return request({
    url: '/qu/setQuData',
    method: 'post',
    data
  })
}

export function getQuData(data) {
  return request({
    url: '/qu/getQuData',
    method: 'post',
    data
  })
}

export function delQu(data) {
  return request({
    url: '/qu/delQu',
    method: 'post',
    data
  })
}

export function setQuInfo(data) {
  return request({
    url: '/qu/setQuInfo',
    method: 'post',
    data
  })
}

export function uploadQuData(data) {
  return request({
    url: '/qu/uploadData',
    method: 'post',
    data
  })
}

export function quSet(data) {
  return request({
    url: '/qu/set',
    method: 'post',
    data
  })
}

export function quGet(data) {
  return request({
    url: '/qu/get',
    method: 'post',
    data
  })
}
