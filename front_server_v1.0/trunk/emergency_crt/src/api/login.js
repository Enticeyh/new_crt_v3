import request from "../utils/request";

//登录
export function loginRequest(message) {
    return request({
        url: `/login`,
        method: "post",
        data: message
    });
}
//退出登录
export function logoutRequest(params) {
    return request({
        url: `/logout`,
        method: "post",
        data:params
    });
}
//换班
export function shiftUserRequest(params) {
    return request({
        url: `/shift_duty`,
        method: "post",
        data:params
    });
}
// 验证登录状态
export function verifyLoginStateRequest(params) {
    return request({
        url: `/other/test`,
        method: "get",
params: params
    });
}