<template>
    <div class="systemRecordBox">

        <div class="recordBox" v-if="recordData.propsRecordType == 24">
            <div class="demandBox">
                <div class="selectBox">

                </div>
                <div class="btnBox">
                    <div class="more" @click="openPopup(20)">新增</div>
                    <div class="derive" @click="refresh">刷新</div>
                </div>
            </div>
            <div class="tableBox">
                <el-table :data="recordData.tableData" class="alarmsTable"
                    :header-cell-style="{ color: '#000000', backgroundColor: '#F8F9FC' }">
                    <el-table-column type="index" label="序号" align="center">
                        <template #default="scope">
                            <div class="deviceState">
                                <div :class="scope.$index <= 2 ? 'highlight-index' : ''">{{ scope.$index +
                                        recordData.tableId
                                }}</div>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column prop="user_name" label="用户名" align="center" />
                    <el-table-column prop="role_name" label="角色" align="center" />
                    <el-table-column label="操作" align="center">
                        <template #default="scope">
                            <div class="objectList">
                                <div class="objectListBtn" @click="openPopup(22, scope.row)">
                                    <img class="examinObjectIcon" src="../../assets/img/comment/redactObjectIcon.svg"
                                        alt="" @dragstart.prevent>
                                </div>
                                <div class="objectListBtn" @click="openPopup(21, scope.row)">
                                    <img class="examinObjectIcon" src="../../assets/img/comment/deleteObjectIcon.svg"
                                        alt="" @dragstart.prevent>
                                </div>
                            </div>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <div class="pagingBigBox">
                <div class="pagingBox">
                    <el-pagination layout="total,prev, pager, next,jumper " :total="recordData.total"
                        :page-size="recordData.page_size" @current-change="handleCurrentChange"
                        :current-page="recordData.requestObject.page" />
                </div>
            </div>
        </div>
        <!-- 打印设置 -->
        <div class="recordBox" v-if="recordData.propsRecordType == 19">
            <div class="timeBox">
                <div class="timeSelect">
                    时间
                </div>

                <div class="timeMsg">间隔时间（分钟）<el-input v-model="recordData.loginAccount" placeholder="请输入内容">
                    </el-input>
                </div>
            </div>
            <div class="alarmsListBox">
                <div class="timeSelect">
                    报警条数
                </div>

                <div class="timeMsg">距上次提示的报警数（条）<el-input v-model="recordData.loginAccount" placeholder="请输入内容">
                    </el-input>
                </div>
            </div>
        </div>
        <!-- 参数设置 -->
        <div class="recordBox" v-if="recordData.propsRecordType == 20">
            <div class="parameterBox">
                <div class="inputBox">&nbsp;&nbsp;&nbsp;故障时长（秒）<el-input v-model="recordData.loginAccount"
                        placeholder="请输入内容">
                    </el-input>
                </div>
                <!-- carouselTime -->
                <div class="inputBox">&nbsp;&nbsp;
                    轮播时长（秒）<el-input v-model="recordData.carouselTime" placeholder="请输入内容">
                    </el-input>

                </div>
                <div class="loTime">轮播时长最低为10秒</div>
                <div class="inputBox">
                    屏保时间（分钟）<el-input v-model="recordData.loginAccount" placeholder="请输入内容">
                    </el-input>

                </div>
                <div class="btnBox">
                    <div class="btnBoxBtn" @click="save">保存</div>
                    <div class="btnBoxBtn" @click="restart">重启服务</div>
                    <div class="btnBoxBtn">关闭服务</div>
                    <div class="btnBoxBtn" @click="inspection">自检</div>
                </div>
            </div>
        </div>
        <!-- 数据导出 -->
        <div class="recordBox" v-if="recordData.propsRecordType == 21" v-loading="recordData.loading">
            <div class="deriveBigBox">
                <!-- 导出 -->
                <div class="dataBox">
                    <div class="trxtBox">
                        智慧消防数据导出
                    </div>
                    <div class="remindBox">
                        用于智慧消防云平台导入数据
                    </div>
                    <div class="deriveBox">
                        项目名称 &nbsp;<el-select v-model="recordData.projectSelect" placeholder="请选择项目" clearable
                            @change="selectFun(recordData.projectSelect)" @visible-change="visible">
                            <el-option v-for="item in recordData.projectList" :key="item.id" :label="item.name"
                                :value="item.id" />
                        </el-select>
                    </div>
                    <div class="deriveBox">
                        文件路径 &nbsp;<el-input @dblclick="fileCopy" v-model="recordData.objectInput" placeholder="请输入指定路径"
                            id="exportBlur" @change="exportBlurFun">

                        </el-input>
                    </div>

                    <div class="sureBox" @click="derive">
                        立即导出
                    </div>
                </div>
                <!-- 备份数据 -->
                <div class="dataBox">
                    <div class="trxtBox">
                        CRT系统数据备份
                    </div>
                    <div class="remindBox">

                    </div>

                    <div class="deriveBox">
                        备份路径 &nbsp;<el-input @dblclick="bCopy" v-model="recordData.backupInput" placeholder="请输入指定路径"
                            id="backupsFun" @change="backupsBlurFun">

                        </el-input>
                    </div>
                    <div class="deriveBox">

                    </div>
                    <div class="sureBox" @click="backups">
                        备份
                    </div>
                </div>
            </div>

        </div>
        <!-- 远程传输 -->
        <div class="recordBox" v-if="recordData.propsRecordType == 22">
            <div class="distanceBox">
                <div class="inputBox">网关名称&nbsp;<el-input v-model="recordData.name" placeholder="请输入内容">
                    </el-input>
                </div>
                <div class="inputBox">IP&nbsp;<el-input v-model="recordData.ip" placeholder="请输入内容">
                    </el-input>
                </div>
                <div class="inputBox">端口&nbsp;<el-input v-model="recordData.port" placeholder="请输入内容">
                    </el-input>
                </div>
                <div class="inputBox">协议&nbsp;<el-select v-model="recordData.protocol" placeholder="请选择">
                        <el-option v-for="item in recordData.protocolArr" :key="item.label" :label="item.label"
                            :value="item.label" />
                    </el-select>
                </div>
                <div class="inputBox">序列号&nbsp;<el-input v-model="recordData.code" placeholder="请输入内容">
                    </el-input>
                </div>
                <div class="distanceBtnBox">
                    <div class="distanceBtnBoxBtn" @click="testCenter">连接测试</div>
                    <div class="distanceBtnBoxBtn" @click="saveCenter">保存</div>
                    <div class="distanceBtnBoxBtn" @click="clearCenter">清除信息</div>
                </div>
            </div>

        </div>
        <!-- 升级 -->
        <div class="recordBox" v-if="recordData.propsRecordType == 23" v-loading="recordData.loading">
            <div class="upBox">
                <div class="updataBigBox">
                    <div class="upgradeBox">
                        <div class="updataBox">
                            选择方式:&nbsp;<el-select v-model="recordData.fileDataSelect" placeholder="数据导入" clearable
                                @change="FileselectFun(recordData.fileDataSelect)">
                                <el-option v-for="item in recordData.fileData" :key="item.value" :label="item.label"
                                    :value="item.value" />
                            </el-select>
                        </div>
                        <div class="updataBox">
                            <template v-if="recordData.fileDataSelect == 1">
                                升级文件
                            </template>
                            <template v-else>
                                导入文件
                            </template>
                            &nbsp;<el-input @dblclick="onCopy" v-model="recordData.updataInput"
                                placeholder="请输入升级文件指定路径" id="updata" @change="updataBlurFun">
                            </el-input>
                        </div>
                        <div class="updataBox">
                            备份路径 &nbsp;<el-input @dblclick="onCopyTwo" v-model="recordData.backupsInput"
                                placeholder="请输入备份文件指定路径" id="backupsPath" @change="backupsPathBlur">
                            </el-input>
                        </div>
                        <div class="sureBox" @click="up">
                            <template v-if="recordData.fileDataSelect == 1">
                                立即升级
                            </template>
                            <template v-else>
                                立即导入
                            </template>
                            
                        </div>
                        <div class="updataBox">版本号:{{recordData.VersionData.version_num}};版本信息:{{recordData.VersionData.notes[0]}}</div>
                    </div>
                </div>
                <div class="updataBigBox">
                    <div class="upgradeBox">

                        <div class="updataBox">
                            重置会清空系统下的所有数据
                        </div>
                        <div class="sureBox" @click="openResetShow">
                            重置
                        </div>
                    </div>
                </div>
            </div>
            <div class="UpBox" v-show="recordData.upShow">
                <el-progress type="circle" :percentage="recordData.fireTime"></el-progress>
            </div>
            
        </div>  
        <!-- 升级提示 -->
        <el-dialog v-model="recordData.updataShow" :show-close="false">
            <template #header>
                <div class="headerBox">提示</div>
            </template>
            <div class="logoutMsg">
                <div class="password">
                    <span style="color: red;">升级完成,请立即重启设备</span>
                </div>
            </div>
            <div class="sureBox">
                <button class="sureBtn" @click="offupdataShow">确定</button>
            </div>
        </el-dialog>
        <!-- 重置提示 -->
        <el-dialog v-model="recordData.resetShow" :show-close="false">
            <template #header>
                <div class="headerBox">提示</div>
            </template>
            <div class="logoutMsg">
                <div class="password">
                    <span style="color: red;">此操作会重置CRT数据,是否继续</span>
                </div>
            </div>
            <div class="sureBox">
                <button class="sureBtn" @click="offResetShow">取消</button>
                <button class="sureBtn" @click="reset">确定</button>
            </div>
        </el-dialog>

    </div>
    <popup :popupType="recordData.popupType" :popupData="recordData.popupData" @offPopup="offPopup" @sure="sure">
    </popup>

</template>
<script>
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessage } from "element-plus";
import { reactive, watch, onMounted } from 'vue'
import popup from "../popup/popup"
import md5 from 'js-md5' //引入
import {
    userListRequest,
    userTypeRequest,
    projectListRequest
} from "../../api/baseData";
import {
    addUserRequest,
    deleteUserRequest,
    revampUserRequest,
    deriveMsg,
    upgradeObject,
    backupsMsg,
    resetObject,
    revampCenterRequest,
    getCenterRequest,
    testCenterRequest,
    clearCenterFun,
    getversionFun
} from "../../api/operation";
import { truncate } from 'fs';
export default {
    components: {
        popup
    },
    props: {
        systemRecordState: Number
    },
    setup(props) {
        const store = useStore();
        const router = useRouter()
        let recordData = reactive({
            loading: false,
            tableData: [
            ],
            requestObject: {
                page: 1,
                per_page: 8,
            },//请求参数
            value1: "",
            propsRecordType: 24,
            popupType: 0,
            radio: 1,
            loginAccount: "",
            tableId: 1,//列表序号
            total: 0,//总条数
            page_size: 8,
            Request: {
                page: 0
            },
            popupData: {},
            filePath: "",
            fileName: "",
            imgSavePath: '',
            projectSelect: "",//
            projectList: [],//
            objectId: "",//项目id
            objectInput: "",
            updataInput: "",
            backupsInput: "",
            backupInput: "",//备份地址
            // 远程传输
            name: "",//监管中心名称
            ip: "",//监管中心ip
            port: "",//监管中心端口号
            protocol: "",//通讯协议类型
            protocolArr: [
                {
                    value: '0',
                    label: 'TCP/IP',
                },

            ],
            fileDataSelect: "",
            fileData: [{
                value: '0',
                label: '数据导入'
            }, {
                value: '1',
                label: "系统升级"
            }],
            code: "",//网关编号
            resetInput: "",//充值密码
            updataOk: 0,
            carouselTime: "",
            updataShow: false,
            fireTime: 0,
            upShow: false,
            VersionData:{},//版本号最新
        })
        onMounted(() => {
            firstRequest()
            console.log('当前版本为3.0.0');
        })
        const onCopy = () => {
            const TEXT = navigator.clipboard.readText();
            TEXT.then(text => {
                // navigator.clipboard.writeText('');
                // 操作完之后，可以写空值到剪切板，防止下次还是相同数据
                recordData.updataInput = text

            }).catch(err => {
                console.error('Failed to read clipboard contents: ', err);
            });


        }
        const onCopyTwo = () => {
            const TEXT = navigator.clipboard.readText();
            TEXT.then(text => {
                // navigator.clipboard.writeText('');
                // 操作完之后，可以写空值到剪切板，防止下次还是相同数据
                recordData.backupsInput = text

            }).catch(err => {
                console.error('Failed to read clipboard contents: ', err);
            });


        }
        const fileCopy = () => {
            const TEXT = navigator.clipboard.readText();
            TEXT.then(text => {
                // navigator.clipboard.writeText('');
                // 操作完之后，可以写空值到剪切板，防止下次还是相同数据
                recordData.objectInput = text

            }).catch(err => {
                console.error('Failed to read clipboard contents: ', err);
            });
        }
        const bCopy = () => {
            const TEXT = navigator.clipboard.readText();
            TEXT.then(text => {
                // navigator.clipboard.writeText('');
                // 操作完之后，可以写空值到剪切板，防止下次还是相同数据
                recordData.backupInput = text

            }).catch(err => {
                console.error('Failed to read clipboard contents: ', err);
            });
        }
        // 打开弹窗
        const openPopup = (type, item) => {
            recordData.popupData = item
            recordData.popupType = type
        }
        // 关闭弹窗
        const offPopup = () => {
            recordData.popupType = 0
        }
        // 第一次请求记录 计算总数
        const firstRequest = () => {
            userListRequest(recordData.requestObject).then((res) => {
                recordData.tableData = res.data.items
                recordData.total = res.data.record_size
            });
        }
        const Request = () => {
            userListRequest(recordData.requestObject).then((res) => {
                recordData.tableData = res.data.items
            });

        }
        const sure = (popupData, operationType, selectData) => {
            if (operationType == 20) {
                addUser(popupData)
            } else if (operationType == 21) {
                deteleUser(popupData)
            } else if (operationType == 22) {
                revampUser(popupData)
            }
        }
        // 新增用户
        const addUser = (popupData) => {
            addUserRequest(popupData).then((res) => {
                if (res.ok) {
                    ElMessage({
                        message: '添加用户成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    // 用户类型列表
                    userTypeRequest(recordData.Request).then((res) => {
                        store.commit('userTypeData', res.data.items)
                    });
                    firstRequest()
                    offPopup()
                }

            });
        }
        // 删除用户
        const deteleUser = (popupData) => {
            deleteUserRequest(popupData).then((res) => {
                if (res.ok) {
                    ElMessage({
                        message: '删除用户信息成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    // 用户类型列表
                    userTypeRequest(recordData.Request).then((res) => {
                        store.commit('userTypeData', res.data.items)
                    });
                    firstRequest()
                    offPopup()
                }

            });
        }
        // 修改用户
        const revampUser = (popupData) => {
            revampUserRequest(popupData).then((res) => {
                if (res.ok) {
                    ElMessage({
                        message: '修改成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    // 用户类型列表
                    userTypeRequest(recordData.Request).then((res) => {
                        store.commit('userTypeData', res.data.items)
                    });
                    firstRequest()
                    offPopup()
                }
            });
        }
        // 切换分页
        const handleCurrentChange = (val) => {
            recordData.requestObject.page = val;
            Request();
            // 序号
            recordData.tableId = (val - 1) * recordData.requestObject.per_page + 1;
        }
        const refresh = () => {
            recordData.requestObject.page = 1//页数为1
            recordData.tableId = 1//页数为1
            handleCurrentChange(1)
        }
        // 选择项目下拉
        const visible = () => {
            let Request = {
                page: 0,
            }
            projectListRequest(Request).then((res) => {
                recordData.projectList = res.data.items
            });
        }
        const FileselectFun = (val) => {
            recordData.fileDataSelect = val
        }
        const selectFun = (val) => {
            recordData.objectId = val
        }
        // 参数设置保存
        const save = () => {
            if (recordData.carouselTime < 10) {
                recordData.carouselTime = 10
            }
            store.state.carouselTime = recordData.carouselTime * 1000

            ElMessage({
                message: '修改成功',
                type: 'success',
                duration: 3 * 1000
            })

        }
        // 重启服务
        const restart = () => {
            router.push({ name: 'webCrtIndex' })
            store.commit('setSwitchRecord', 0)
            sessionStorage.setItem("setSwitchRecord", 0);
        }
        const inspection = () => {
            history.go(0)
        }
        // 导出
        const derive = () => {

            let data = {
                project_id: recordData.objectId,
                path: recordData.objectInput
            }
            if (recordData.objectId == "") return ElMessage({
                message: '请选择项目',
                type: 'error',
                duration: 3 * 1000
            })

            if (recordData.objectInput == "") return ElMessage({
                message: '请填写地址',
                type: 'error',
                duration: 3 * 1000
            })
            recordData.loading = true
            deriveMsg(data).then((res) => {
                if (res.ok) {
                    ElMessage({
                        message: '导出成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    recordData.loading = false
                    recordData.projectSelect = ""
                    recordData.objectId = ""
                    recordData.objectInput = ""
                }
            });
        }
        // 备份
        const backups = () => {
            let data = {
                path: recordData.backupInput
            }
            if (recordData.backupInput == "") return ElMessage({
                message: '请输入备份地址',
                type: 'error',
                duration: 3 * 1000
            })
            recordData.loading = true
            backupsMsg(data).then((res) => {
                if (res.ok) {
                    ElMessage({
                        message: '备份成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    recordData.loading = false
                    recordData.projectSelect = ""
                    recordData.objectId = ""
                    recordData.objectInput = ""
                    recordData.backupInput = ""
                }
            });
        }
        // 升级
        const up = () => {

            if (recordData.updataInput == "" || recordData.backupsInput == "") return ElMessage({
                message: '请填写地址',
                type: 'error',
                duration: 3 * 1000
            })
            recordData.loading = true
            recordData.upShow = true
            if (recordData.fileDataSelect == 1) {
                ElMessage({
                    message: '正在升级中,请勿进行任何操作',
                    type: 'info',
                    duration: 3 * 1000
                })
            } else {
                ElMessage({
                    message: '正在导入中,请勿进行任何操作',
                    type: 'info',
                    duration: 3 * 1000
                })
            }

            let data = {
                path: recordData.updataInput,
                backups_path: recordData.backupsInput
            }
            let timer = null
            recordData.fireTime = 0
            timer = setInterval(() => {
                if (recordData.fireTime < 99) {
                    recordData.fireTime += 1
                } else if (recordData.fireTime == 99) {
                    recordData.fireTime = 99
                }
            }, 3000);
            upgradeObject(data).then((res) => {
                if (res.ok) {
                    clearTimeout(timer)
                    let timerTwo = null
                    timer = setInterval(() => {
                        recordData.fireTime += Math.trunc(Math.random(5, 10) * 10)
                        if (recordData.fireTime >= 100) {
                            recordData.loading = false
                            recordData.upShow = false
                            recordData.updataShow = true
                            recordData.updataInput = ""
                            recordData.backupsInput = ""
                            recordData.fireTime = 0
                            clearTimeout(timerTwo)
                        }
                    }, 2000);

                } else {
                    clearTimeout(timer)
                    recordData.upShow = false
                    recordData.loading = false
                }
            });
        }
        // 关闭  升级成功提示
        const offupdataShow = () => {
            recordData.updataShow = false
        }
        // 打开 重置弹窗
        const openResetShow = () => {
            recordData.resetShow = true
        }
        const offResetShow = () => {
            recordData.resetShow = false
        }
        // 重置
        const reset = () => {
            resetObject().then((res) => {
                recordData.loading = true
                if (res.ok) {
                    ElMessage({
                        message: '重置成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    recordData.loading = false
                    recordData.resetShow = false
                }
            });
        }
        const saveCenter = () => {
            let data = {
                name: recordData.name,
                ip: recordData.ip,
                port: recordData.port,
                protocol: recordData.protocol,
                code: recordData.code
            }
            if (recordData.name == "" || recordData.ip == "" || recordData.port == "" || recordData.protocol == "" || recordData.code == "") return ElMessage({
                message: '请输入完整内容',
                type: 'error',
                duration: 3 * 1000
            })
            revampCenterRequest(data).then((res) => {
                if (res.ok) {
                    ElMessage({
                        message: '保存成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                }
            });
        }
        const clearCenter = () => {
            clearCenterFun().then((res) => {
                if (res.ok) {
                    ElMessage({
                        message: '清除成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    recordData.name = ""
                    recordData.ip = ""
                    recordData.port = ""
                    recordData.protocol = ""
                    recordData.code = ""
                    recordData.name = ""
                }
            })
        }
        // 连接测试
        const testCenter = () => {
            testCenterRequest().then((res) => {
                if (res.ok) return ElMessage({
                    message: '连接测试成功',
                    type: 'success',
                    duration: 3 * 1000
                })
            });
        }
        const exportBlurFun = () => {
            let name = document.getElementById('exportBlur').value
            recordData.objectInput = name
        }
        const backupsBlurFun = () => {
            let name = document.getElementById('backupsFun').value
            recordData.backupInput = name
        }
        const updataBlurFun = () => {
            let name = document.getElementById('updata').value
            recordData.updataInput = name
        }
        const backupsPathBlur = () => {
            let name = document.getElementById('backupsPath').value
            recordData.backupsInput = name
        }
        // 监听弹窗状态
        // 监听父组件传递的props的值 用来判断显示哪一张表格
        watch(props, (newProps) => {
            recordData.propsRecordType = newProps.systemRecordState
            if (newProps.systemRecordState == 22) {
                getCenterRequest().then((res) => {
                    recordData.name = res.data.name,
                        recordData.ip = res.data.ip,
                        recordData.port = res.data.port,
                        recordData.protocol = res.data.protocol
                    recordData.code = res.data.code
                });
            } else if (newProps.systemRecordState == 23) {
                // 每次进入升级页面时 查询当前版本
                getversionFun().then((res) => {
                    recordData.VersionData = res.data
                });
            }
            recordData.carouselTime = store.state.carouselTime / 1000
            firstRequest()
            recordData.requestObject.page = 1//页数为1
            recordData.tableId = 1//页数为1
            recordData.projectSelect = ""
            recordData.objectInput = ""
            recordData.objectId = ""
            recordData.updataInput = ""
            recordData.backupsInput = ""
            recordData.fileDataSelect = ""//切换页面 清空升级方式
        }
        );
        return {
            recordData,
            openPopup,
            offPopup,
            firstRequest,
            Request,
            handleCurrentChange,
            refresh,
            sure,
            visible,
            selectFun,
            FileselectFun,
            derive,
            up,
            backups,
            reset,
            saveCenter,
            clearCenter,
            testCenter,
            save,
            offupdataShow,
            restart,
            inspection,
            openResetShow,
            offResetShow,
            onCopy,
            onCopyTwo,
            fileCopy,
            bCopy,
            exportBlurFun,
            backupsBlurFun,
            updataBlurFun,
            backupsPathBlur
        }
    }
}
</script>
<style scoped lang="scss">
.systemRecordBox {
    width: 1760px;
    height: 884px;
    margin-left: 80px;
    margin-top: 18px;
    margin-bottom: 18px;
    background: #ffffff;

    .recordBox {

        :deep(.el-input) {
            width: 320px;
            height: 44px;
            color: #4A5CD5;
        }

        :deep(.el-input__wrapper) {
            width: 320px;
            height: 44px;
            color: #4A5CD5;
            background-color: #F7F8FC;
            border: none !important;
            box-shadow: none !important;
        }

        .demandBox {
            width: 1760px;
            height: 80px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #ffffff;

            .selectBox {
                display: flex;
                align-items: center;
            }

            .btnBox {
                height: 100px;
                display: flex;
                align-items: center;
                font-size: 20px;
                font-weight: 500;
                color: #ffffff;
                margin-right: 20px;

                .more {
                    width: 90px;
                    height: 44px;
                    background: #4a5cd5;
                    border-radius: 2px;
                    display: flex;
                    flex-direction: row;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;

                }

                .derive {
                    width: 90px;
                    height: 44px;
                    border: 2px solid #4a5cd5;
                    color: #4A5CD5;
                    font-size: 20px;
                    font-weight: 500;
                    border-radius: 2px;
                    margin-left: 12px;
                    display: flex;
                    flex-direction: row;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                }

                // 新建项目
                .new {
                    width: 120px;
                    height: 44px;
                    background: #4a5cd5;
                    border-radius: 2px;
                    font-size: 20px;
                    font-weight: 500;
                    color: #ffffff;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                }

                // 下载模板 导入 选取文件
                .operationText {
                    width: 120px;
                    font-size: 20px;
                    font-weight: 500;
                    text-decoration: underline;
                    color: #4a5cd5;
                    cursor: pointer;

                    .downloadIcon {
                        width: 18px;
                        height: 18px;
                    }
                }

                .operationText:nth-child(2),
                .operationText:nth-child(3) {
                    color: #000000;
                    text-decoration: none;
                    margin-left: 12px;
                }
            }



        }

        .tableBox {
            width: 1760px;
            height: 576px;
            position: relative;

            .alarmsTable {
                width: 1760px;

                :deep(.el-table__cell) {
                    height: 64px !important;
                    // line-height: 64px !important;
                    padding: 0px !important;
                }

                //    :deep(.el-table .cell){
                //      height: 64px !important;
                //         line-height: 64px !important;
                //         padding: 0px !important;
                //    }
                //     :deep( .cell.el-tooltip) {
                //         height: 64px !important;
                //         line-height: 64px !important;
                //         padding: 0px !important;
                //     }
                //       :deep(.el-table__header) {
                //         height: 50px !important;
                //         line-height: 50px !important;
                //         padding: 0px !important;
                //     }

            }

            // 项目列表-操作
            .objectList {
                display: flex;
                align-items: center;
                justify-content: space-around;

                .objectListBtn {
                    width: 22px;
                    height: 28px;
                    cursor: pointer;

                    .examinObjectIcon {
                        width: 22px;
                        height: 28px;
                    }
                }
            }
        }

        // 分页
        .pagingBigBox {
            width: 1760px;
            height: 61px;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10;
            position: relative;

            :deep(.number) {
                border: 1px solid #dcdfe6;
                border-radius: 2px;
            }

            :deep(.btn-prev),
            :deep(.btn-next) {
                border: 1px solid #dcdfe6;
                border-radius: 2px;
                color: #909399;
            }

            :deep(.btn-next) {
                margin-left: 12px;
            }

            :deep(.number) {
                margin-left: 12px;
            }

            // 选择器
            :deep(.el-input) {
                width: 30px;
                // height: 44px;
                background-color: #fff;
            }

            :deep(.el-input__wrapper) {
                // width: 30px;
                // height: 44px;
                background-color: #fff;
            }

            :deep(.el-input__inner) {
                // width: 300px;
                // height: 44px;
                border: 1px solid #dcdfe6;
                border-radius: 8px;
                background-color: #fff;
            }
        }

        // 打印-时间
        .timeBox,
        .alarmsListBox {
            width: 770px;
            height: 220px;
            border: 1px solid #dcdfe6;
            border-radius: 3px;
            margin-top: 100px;
            margin-left: 505px;
        }

        .timeBox,
        .alarmsListBox {
            .timeSelect {
                width: 200px;
                height: 37px;
                margin-top: 52px;
                margin-left: 57px;
                font-size: 20px;
                color: #4A5CD5;
                font-weight: 600;
            }

            .timeMsg {
                width: 700px;
                height: 110px;
                font-size: 22px;
                font-weight: 500;
                color: #000000;
                letter-spacing: 1.1px;
                display: flex;
                align-items: center;
                margin-left: 99px;
            }
        }

        .alarmsListBox {
            margin-top: 90px;
        }

        // 参数设置
        .parameterBox {
            width: 750px;
            height: 446px;
            border: 1px solid #dcdfe6;
            border-radius: 3px;
            margin-top: 100px;
            margin-left: 505px;

            .inputBox {
                width: 750px;
                height: 50px;
                font-weight: 500;
                font-size: 22px;
                color: #000000;
                letter-spacing: 1.1px;
                margin-left: 118px;
                margin-top: 36px;

            }

            .loTime {
                width: 450px;
                height: 5px;
                color: #736c6c;
                margin-left: 300px;
                margin-top: 6px;
                font-size: 10px;
            }

            .inputBox:first-child {
                margin-top: 76px;
            }

            .btnBox {
                width: 750px;
                height: 44px;
                display: flex;
                margin-top: 61px;
                justify-content: space-around;

                .btnBoxBtn {
                    width: 120px;
                    height: 44px;
                    background: #4a5cd5;
                    border-radius: 2px;
                    font-size: 20px;
                    font-weight: 500;
                    color: #ffffff;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
            }
        }

        // 远程传输
        .distanceBox {
            width: 750px;
            height: 580px;
            border: 1px solid #dcdfe6;
            border-radius: 3px;
            display: flex;
            margin-top: 100px;
            margin-left: 505px;
            flex-direction: column;

            .inputBox {
                margin-left: 161px;
                width: 450px;
                height: 45px;
                margin-top: 36px;
                margin-right: 160px;
                font-size: 22px;
                font-weight: 500;
                text-align: right;
                color: #000000;
                letter-spacing: 1.1px;
                // position: relative;

            }



            .inputBox:first-child {
                margin-top: 63px;
            }

            .distanceBtnBox {
                width: 420px;
                height: 44px;
                display: flex;
                margin-top: 46px;
                margin-left: 166px;
                justify-content: space-between;

                .distanceBtnBoxBtn {
                    width: 120px;
                    height: 44px;
                    border-radius: 2px;
                    font-size: 20px;
                    font-weight: 500;
                    background-color: #4A5CD5;
                    color: #ffffff;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                }
            }

        }

        .deriveBigBox {
            width: 1760px;
            height: 700px;
            display: flex;
            align-items: center;
            justify-content: center;

            .dataBox {
                width: 750px;
                height: 446px;
                border: 1px solid #dcdfe6;
                border-radius: 3px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                font-size: 26px;
                font-weight: 700;
                // margin-top: 138px;
                margin-left: 40px;
                color: #000000;

                .sureBox {
                    width: 300px;
                    height: 60px;
                    background: #4a5cd5;
                    border-radius: 2px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 30px;
                    font-weight: 500;
                    color: #ffffff;
                    margin-top: 32px;
                    cursor: pointer;
                }
            }

            .trxtBox {
                width: 750px;
                height: 50px;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .remindBox {
                width: 730px;
                height: 50px;
                display: flex;
                align-items: center;
                font-size: 15px;
                color: #909399;
                justify-content: center;
                // margin-right: 20px;
            }

            .deriveBox {
                height: 50px;
            }



        }

        .upBox {
            width: 1760px;
            height: 700px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .UpBox {
            width: 100%;
            height: 500px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: absolute;
            top: 120px;
            left: 0px;
            z-index: 2001;
        }

        .updataBigBox {
            width: 1760px;
            height: 700px;
            display: flex; // 数据导出
            align-items: center;
            justify-content: center;

            .upgradeBox {
                width: 750px;
                height: 446px;
                border: 1px solid #dcdfe6;
                border-radius: 3px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                font-size: 26px;
                font-weight: 700;
                color: #000000;
                position: relative;

                .updataBox {
                    margin-top: 20px;
                }

                .sureBox {
                    width: 300px;
                    height: 60px;
                    background: #4a5cd5;
                    border-radius: 2px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 30px;
                    font-weight: 500;
                    color: #ffffff;
                    margin-top: 32px;
                    cursor: pointer;
                }
            }
        }
    }
}

:deep(.el-dialog) {
    display: flex;
    flex-direction: column;
    margin: 0 !important;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    height: 600px;
    width: 1000px;
    border-radius: 8px;

    .headerBox {
        width: 1000px;
        height: 90px;
        font-size: 28px;
        font-weight: 700;
        color: #4a5cd5;
        letter-spacing: 1.4px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-bottom: 1px solid #eaeaf1;
    }

    .offBtn {
        position: absolute;
        width: 18px;
        height: 18px;
        color: #4A5CD5;
        font-size: 18px;
        cursor: pointer;
        top: 30px;
        right: 45px;
    }

    .el-dialog__body {
        padding: 0px;
    }

    .el-dialog__header {
        padding: 0px;
    }

}

.sureBox {
    width: 1000px;
    height: 80px;
    display: flex;
    flex-direction: row-reverse;
    align-items: center;
    border-top: 1px solid #eaeaf1;

    .sureBtn {

        // justify-content: center;
        width: 120px;
        height: 44px;
        background: #4a5cd5;
        border-radius: 2px;
        border: none;
        font-size: 22px;
        font-weight: 500;
        color: #ffffff;
        letter-spacing: 1.1px;
        margin-right: 43px;
        cursor: pointer;
    }

    .cancelBtn {
        width: 120px;
        height: 44px;
        border: 2px solid #4a5cd5;
        border-radius: 2px;
        cursor: pointer;
        font-size: 22px;
        font-weight: 500;
        color: #4a5cd5;
        letter-spacing: 1.1px;
        margin-right: 20px;
        background-color: #fff;
    }
}

.logoutMsg {
    width: 1000px;
    height: 430px;
    font-size: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    font-weight: 500;
    color: #000000;
    letter-spacing: 1.6px;



    .password {
        margin-left: -20px;
        width: 450px;
        display: flex;
        font-size: 20px;
        justify-content: left;
    }


}
</style>