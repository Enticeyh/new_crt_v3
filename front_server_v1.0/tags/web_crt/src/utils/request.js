import axios from "axios";
import {
    ElMessage
} from "element-plus";
import config from "./config";
import JSON_BIG from 'json-bigint'
let messageBox = null;
const service = axios.create({
    baseURL: config.baseUrl, // process.env.VUE_APP_BASE_API,
    withCredentials: false,
    timeout: 600000,
    // // 处理雪花id精度丢失的问题
    transformResponse: data => {
        try {
            if (typeof (data) == 'string') {
                return JSON_BIG.parse(data);
            } else {
                return data
            }
        } catch (err) {
            return data
        }
    }
});
const interfaceList = {}; // 记录已请求接口，防止多次触发
const prohibitLoginURL = ["selectRecommendCourse", "judgeBuyAndAttention"];

function down(data, filename) {

    let link = document.createElement('a');
    link.href = window.URL.createObjectURL(new Blob([data], {
        type: 'application/pdf;charset=utf-8'
    }))
    link.download = filename;
    link.click();

}

function downLoadXls(data, filename) {

    // var blob = new Blob([data], {type: 'application/vnd.ms-excel'}) //接收的是blob，若接收的是文件流，需要转化一下
    // var blob = new Blob([data], {type: 'application/octet-stream'}) //接收的是blob，若接收的是文件流，需要转化一下
    if (typeof window.chrome !== 'undefined') {
        // Chrome version
        let link = document.createElement('a');
        // let pdfUrl = window.URL.createObjectURL(new Blob(binaryData, { type: "application/pdf" }));
        //    let pdfUrl= window.URL.createObjectURL(new Blob([data], { type: "application/pdf" }))
        // window.print(pdfUrl);
        link.href = window.URL.createObjectURL(data);
        link.download = filename;
        link.click();
    } else if (typeof window.navigator.msSaveBlob !== 'undefined') {
        //     // IE version
        let blob = new Blob([data], {
            type: 'application/force-download'
        });
        window.navigator.msSaveBlob(blob, filename);
    } else {
        // Firefox version
        let file = new File([data], filename, {
            type: 'application/force-download'
        });
        window.open(URL.createObjectURL(file));
    }                                                                    
}

service.interceptors.request.use(
    config => {
        if (sessionStorage.getItem('userInfo')) {
            config.headers.Authorization = 'Bearer' + ' ' + JSON.parse(sessionStorage.getItem('userInfo'))['token'];
        }
        if (config.params && config.params.export_flag == 1) {
            config['responseType'] = 'blob'
        }
        return config;
    },
    error => {
        // do something with request error
        console.log(error); // for debug
        ElMessage({
            message: error.response.data.msg,
            type: "error",
            duration: 3 * 1000
        });
        return Promise.reject(error);
    }
);
service.interceptors.response.use(
    response => {
        // interfaceList[response.request.responseURL] = false;
        const res = response.data;
        
        if (response.headers.hasOwnProperty('filename')) {
            if (decodeURI(response.headers.filename).substr(decodeURI(response.headers.filename).length - 3, 3) == "pdf") {
                down(res, decodeURI(response.headers.filename))
            } else {
                downLoadXls(res, decodeURI(response.headers.filename) + '.xlsx')
            }
            return res
        }
        // if the custom code is not 20000, it is judged as an error.
        if (res.code === 0 || res.code === undefined) {
            
            return res;
        } else if (res.code === 1103 || res.code === 1301) { // 未登录或者登录失效  未授权
            if (messageBox) messageBox.close();
            messageBox = ElMessage({
                // message: res.msg,
                message: "登录失效,请重新登录",
                type: "error",
                duration: 3 * 1000
            });
            console.log(response)
            console.log(res);
            if (response.config.url !== '/') {
                window.location.href = '/'
            }
            return Promise.reject(new Error(res.msg || "Error"));
        } else if(res.code === 1101){
            ElMessage({
                message:"超级密码已过期!",
                type: "error",
                duration: 10 * 1000
            });
            window.location.href = '/'
        }else if(res.code === 1201){
            ElMessage({
                message:"系统升级包版本过低，请联系管理员确认！!",
                type: "error",
                duration: 10 * 1000
            });
            
        }else {
            if (messageBox) messageBox.close();
            messageBox = ElMessage({
                message: res.msg || "服务错误，请重试",
                type: "error",
                duration: 3 * 1000
            });
            return Promise.reject(new Error(res.msg || "Error"));
        }
    },
    error => {
        let errorList = [];
        const res = error.response.data;
        if (res.code == 1103 || res.code == 1301) { // 未登录或者登录失效  未授权
            if (messageBox) messageBox.close();
            messageBox = ElMessage({
                // message: res.msg,
                message: "登录失效,请重新登录",
                type: "error",
                duration: 10 * 1000
            });
            if (error.response.config.url !== '/') {
                window.location.href = '/'
            }
            sessionStorage.clear();
            return Promise.reject(new Error(res.msg || "Error"));
        }else if(res.code === 0 || res.code === undefined){
            return res
        }
        if (error.message) errorList = error.message.split("|");
        switch (errorList[0]) {
            case "1001":
                console.error("重复请求了");
                break;
            default:
                if (messageBox) messageBox.close();
                messageBox = ElMessage({
                    message: error.response.data.msg || "服务错误",
                    type: "error",
                    duration: 3 * 1000
                });
                return res
                break;
        }
        if (errorList[1]) interfaceList[errorList[1]] = false;
        return Promise.reject(error);
    }
);

export default service;