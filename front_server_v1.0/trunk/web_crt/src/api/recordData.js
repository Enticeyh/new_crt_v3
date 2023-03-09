import request from "../utils/request";

//查询设备报警记录列表
export function alarmsRequest(params) {
  return request({
    url: `/records/alarm_logs`,
    method: "get",
    params: params,
  });
}
//查询设备单条报警记录列表
export function alarmsOnlyRequest(alarm_log_id) {
  return request({
    url: `/records/alarm_log/${alarm_log_id}`,
    method: "get",
  });
}
// 查询报警记录图纸
export function alarmsImgRequest(params) {
  return request({
    url: `/records/build_drawings`,
    method: "GET",
    params: params,
  });
}
//查询设备报警记录列表
// export function onlyAlarmsRequest() {
//     return request({
//         url: `/records/alarm_logs`,
//         method: "get",
//     });
// }

//图纸
export function drawingRequest() {
  return request({
    url: `/records/build_drawings`,
    method: "get",
  });
}

//布点记录
export function stationingRequest(params) {
  return request({
    url: `/records/device_assign_logs`,
    method: "get",
    params: params,
  });
}

//控制器操作记录
export function controllerOperationRequest(params) {
  return request({
    url: `/records/controller_op_logs`,
    method: "get",
    params: params,
  });
}

//维保记录
export function maintenanceRequest(params) {
  return request({
    url: `/records/maintenance_logs`,
    method: "get",
    params: params,
  });
}

//换班记录
export function changeShiftRequest(params) {
  return request({
    url: `/records/shift_records`,
    method: "get",
    params: params,
  });
}
//用户操作记录
export function operationRequest(params) {
  return request({
    url: `/records/system_logs`,
    method: "get",
    params: params,
  });
}
//布点图查询
export function drawingsRequest(params) {
  return request({
    url: `/records/build_drawings`,
    method: "get",
    params: params,
  });
}
//布点列表
export function stationingListRequest(params) {
  return request({
    url: `/build_drawing/current_relationship`,
    method: "get",
    params: params,
  });
}
// 文件列表
export function filesListRequest(params) {
  return request({
    url: `/records/files`,
    method: "get",
    params: params,
  });
}
// 项目图片列表
export function imgTypeListRequest(params) {
  return request({
    url: `/build_drawing/project_pictures`,
    method: "get",
    params: params,
  });
}
// 根据图纸id查图纸
export function imgIdRequest(alarm_log_id) {
  return request({
    url: `/build_drawing/floor/${alarm_log_id}`,
    method: "get",
  });
}
