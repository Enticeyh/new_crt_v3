import request from "../utils/request";

//用户类型列表
export function userTypeRequest(params) {
  return request({
    url: `/basic_data/roles`,
    method: "get",
    params: params,
  });
}
//设备类型列表
export function deviceTypeRequest(params) {
  return request({
    url: `/basic_data/device_type`,
    method: "get",
    params: params,
  });
}
//图片类型列表
export function imgTypeRequest(params) {
  return request({
    url: `/basic_data/picture_type`,
    method: "get",
    params: params,
  });
}
//图片类型列表
export function deviceIconRequest(params) {
  return request({
    url: `/basic_data/device_icons`,
    method: "get",
    params: params,
  });
}
//报警类型列表
export function alarmsTypeRequest(params) {
  return request({
    url: `/basic_data/alarm_type`,
    method: "get",
    params: params,
  });
}
//国标事件类型列表
export function gbEventTypeRequest(params) {
  return request({
    url: `/basic_data/gb_evt_type`,
    method: "get",
    params: params,
  });
}
//设备图标列表
export function deviceIconsRequest(params) {
  return request({
    url: `/basic_data/device_icons`,
    method: "get",
    params: params,
  });
}
//新增设备图标
export function addDeviceIconsRequest() {
  return request({
    url: `/basic_data/device_icons`,
    method: "post",
  });
}
// 修改设备图标
export function revampDeviceIconsRequest(params, icon_id) {
  return request({
    url: `/basic_data/device_icons/${icon_id}`,
    method: "put",
    params: params,
  });
}
// 删除设备图标
export function deleteDeviceIconsRequest(params, icon_id) {
  return request({
    url: `/basic_data/device_icons/${icon_id}`,
    method: "delete",
    params: params,
  });
}
// 用户列表
export function userListRequest(params) {
  return request({
    url: `/user`,
    method: "get",
    params: params,
  });
}
// 项目列表
export function projectListRequest(params) {
  return request({
    url: `/build_drawing/projects`,
    method: "get",
    params: params,
  });
}
// 首页项目列表
export function projectIndexRequest() {
  return request({
    url: `/other/projects`,
    method: "get",
  });
}
// 小区列表
export function areaListRequest(params) {
  return request({
    url: `/build_drawing/areas`,
    method: "get",
    params: params,
  });
}
// 楼宇列表
export function buildingListRequest(params) {
  return request({
    url: `/build_drawing/builds`,
    method: "get",
    params: params,
  });
}
// 楼层列表
export function floorsListRequest(params) {
  return request({
    url: `/build_drawing/floors`,
    method: "get",
    params: params,
  });
}
// 控制器列表
export function controllersListRequest(params) {
  return request({
    url: `/build_drawing/controllers`,
    method: "get",
    params: params,
  });
}
// 根据控制器号 查询回路号
export function inquireLoopRequest(params) {
  return request({
    url: `/build_drawing/loops`,
    method: "get",
    params: params,
  });
}
// 设备列表
export function deviceListRequest(params) {
  return request({
    url: `/build_drawing/devices`,
    method: "get",
    params: params,
  });
}
// 项目图片
export function objectImgRequest(params) {
  return request({
    url: `/build_drawing/project_pictures`,
    method: "get",
    params: params,
  });
}
// 楼层关系
export function areaBuildsRequest(params) {
  return request({
    url: `/build_drawing/address_relationship`,
    method: "get",
    params: params,
  });
}
// 控制器回路关系
export function controllerLoopRequest(params) {
  return request({
    url: `/build_drawing/current_relationship`,
    method: "get",
    params: params,
  });
}
// 首页报警列表
export function alarmsNumListRequest(params) {
  return request({
    url: `/other/alarm_info`,
    method: "get",
    params: params,
  });
}
// 首页报警列表
export function alarmsListRequest(params) {
  return request({
    url: `/other/alarm_logs`,
    method: "get",
    params: params,
  });
}
// 首页报警列表
export function helpRequest(params) {
  return request({
    url: `/other/help`,
    method: "get",
  });
}
