import request from "../utils/request";
//回复复位标识
export function resetUpdateRequest() {
    return request({
        url: `/other/update_reset`,
        method: "post",
    });
}
//验证超级密码
export function checkPasswordRequest(message) {
    return request({
        url: `/check_super_password`,
        method: "post",
        data: message
    });
}
//下载 控制器 设备模板
export function getHelpRequest(template_type) {
    return request({
        url: `/other/template?template_type=${template_type}`,
        method: "get",
    });
}

//新增用户
export function addUserRequest(message) {
    return request({
        url: `/update_user`,
        method: "post",
        data: message
    });
}
//删除用户
export function deleteUserRequest(user_id) {
    return request({
        url: `/update_user/?user_id=${user_id}`,
        method: "DELETE",
    });
}
// 修改用户
export function revampUserRequest(message) {
    return request({
        url: `/update_user`,
        method: "put",
        data: message
    });
}
//新增项目
export function addObjectRequest(message) {
    return request({
        url: `/build_drawing/projects`,
        method: "post",
        data: message
    });
}
//删除项目
export function deleteObjectRequest(project_id) {
    return request({
        url: `/build_drawing/projects/?project_id=${project_id}`,
        method: "DELETE",
    });
}
//删除项目图
export function deleteImgRequest(project_picture_id) {
    return request({
        url: `/build_drawing/project_pictures/?project_picture_id=${project_picture_id}`,
        method: "DELETE",
    });
}
//删除控制器
export function deleteControllersRequest(controller_id) {
    return request({
        url: `/build_drawing/controllers/?controller_id=${controller_id}`,
        method: "DELETE",
    });
}
//修改项目
export function revampObjectRequest(message) {
    return request({
        url: `/build_drawing/projects`,
        method: "put",
        data: message
    });
}
//修改设备
export function revampDevicesRequest(message) {
    return request({
        url: `/build_drawing/devices`,
        method: "put",
        data: message
    });
}
//删除设备
export function deleteDevicesRequest(message) {
    return request({
        url: `/build_drawing/devices`,
        method: "DELETE",
        data: message
    });
}
//新增小区
export function newAreaRequest(message) {
    return request({
        url: `/build_drawing/areas`,
        method: "post",
        data: message
    });
}
//删除小区
export function deleteAreaRequest(area_id) {
    return request({
        url: `/build_drawing/areas/?area_id=${area_id}`,
        method: "DELETE",
    });
}
//修改小区
export function revampAreaRequest(message) {
    return request({
        url: `/build_drawing/areas`,
        method: "put",
        data: message
    });
}
//新增楼宇
export function newBuildsRequest(message) {
    return request({
        url: `/build_drawing/builds`,
        method: "post",
        data: message
    });
}
//删除楼宇
export function deteleBuildsRequest(build_id) {
    return request({
        url: `/build_drawing/builds/?build_id=${build_id}`,
        method: "DELETE",
    });
}
//修改楼宇
export function revampBuildsRequest(message) {
    return request({
        url: `/build_drawing/builds`,
        method: "put",
        data: message
    });
}
//删除楼层
export function deteleFloorsRequest(floor_ids) {
    return request({
        url: `/build_drawing/floors/?floor_ids=${floor_ids}`,
        method: "DELETE",
    });
}
// 新增控制器
export function addControllersRequest(params) {
    return request({
        url: `/build_drawing/controllers`,
        method: "post",
        data: params
    });
}
//修改控制器
export function revampControllersRequest(message) {
    return request({
        url: `/build_drawing/controllers`,
        method: "put",
        data: message
    });
}
//新增布点
export function addStationRequest(params) {
    return request({
        url: `/build_drawing/assign_devices`,
        method: "post",
        data: params
    });
}
//布点列表
export function stationListRequest(params) {
    return request({
        url: `/build_drawing/assign_devices`,
        method: "get",
        params: params
    });
}
// 首页布点列表
export function indexStationListRequest(params) {
    return request({
        url: `/other/drawing_assign`,
        method: "get",
        params: params
    });
}
//删除布点
export function deleteStationRequest(assign_id) {
    return request({
        url: `/build_drawing/assign_devices/?assign_id=${assign_id}`,
        // url: `/user/?user_id=${user_id}`,
        method: "DELETE",
        // data: params
    });
}
//删除布点
export function deletedevice_idStationRequest(device_id) {
    return request({
        url: `/build_drawing/assign_devices/?device_id=${device_id}`,
        method: "DELETE",
    });
}
//继承布点
export function inheritStationRequest(params) {
    return request({
        url: `/build_drawing/assign_inheritance`,
        method: "post",
        data: params
    });
}
// 模拟测试
export function testRequest(params) {
    return request({
        url: `/other/mock_test`,
        method: "POST",
        data: params
    });
}
// 复位
export function resetRequest() {
    return request({
        url: `/other/reset`,
        method: "post"
    });
}
// 生成SVG
export function saveSVG(message) {
    return request({
        url: `/build_drawing/quick_svg`,
        method: "post",
        data: message
    });
}
// 导出
export function deriveMsg(params) {
    return request({
        url: `/other/smart_iot_data`,
        method: "get",
        params: params
    });
}
// 备份
export function backupsMsg(params) {
    return request({
        url: `/other/backups`,
        method: "get",
        params: params
    });
}
// 升级
export function upgradeObject(params) {
    return request({
        url: `/other/upgrade`,
        method: "post",
        data: params
    });
}
// 重置
export function resetObject(params) {
    return request({
        url: `/other/factory_reset`,
        method: "post",
        data: params
    });
}

// 测试监管中心
export function testCenterRequest(message) {
    return request({
        url: `/other/test_center`,
        method: "get",
        data: message
    });
}
// 查询监管中心
export function getCenterRequest(message) {
    return request({
        url: `/other/center`,
        method: "get",
        data: message
    });
}
// 修改监管中心
export function revampCenterRequest(message) {
    return request({
        url: `/other/center`,
        method: "put",
        data: message
    });
}
// 清除监管中心信息
export function clearCenterFun() {
    return request({
        url: `/other/center`,
        method: "DELETE",
    });
}
// 查询版本号
export function getversionFun(message) {
    return request({
        url: `/other/last_version`,
        method: "get",
        data: message
    });
}