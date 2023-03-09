<template>
    <div class="menuBox">
        <div class="btnBox" v-if="menuData.btnShow">
            <!-- 首页 -->
            <div class="menuBtn" @click="goIndex(1)" :class="menuData.isActive == 1 ? 'active' : 'unactive'">
                <div class="btn">
                    <div class="btnImgBox">
                        <template v-if="menuData.isActive == 1">
                            <img class="btnImg" src="../../assets/img/menu/indexOn.svg" alt="" @dragstart.prevent>
                        </template>
                        <template v-else>
                            <img class="btnImg" src="../../assets/img/menu/indexOff.svg" alt="" @dragstart.prevent>
                        </template>
                    </div>
                    <div class="btnText">首页</div>
                </div>
            </div>
            <!-- 统计查询 -->
            <div class="menuBtn" @click="goStatistics(2)" :class="menuData.isActive == 2 ? 'active' : 'unactive'">
                <div class="btn">
                    <div class="btnImgBox">
                        <template v-if="menuData.isActive == 2">
                            <img class="btnImg" src="../../assets/img/menu/statisticsOn.svg" alt="" @dragstart.prevent>
                        </template>
                        <template v-else>
                            <img class="btnImg" src="../../assets/img/menu/statisticsOff.svg" alt="" @dragstart.prevent>
                        </template>
                    </div>
                    <div class="btnText">统计查询</div>
                </div>
            </div>
            <!-- 统计查询选择器 -->
            <template v-if="menuData.isActive == 2">
                <div class="statisticsTypeBox" v-show="menuData.statisticsPitchOn">
                    <!-- 报警记录跳转按钮 -->
                    <div class="typeBtn" @click="goStatisticsRecord(1)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/alarmsIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">报警记录</div>
                    </div>
                    <!-- 控制器操作 -->
                    <div class="typeBtn" @click="goStatisticsRecord(2)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/controller.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">控制器操作</div>
                    </div>
                    <!-- 值班记录 -->
                    <div class="typeBtn" @click="goStatisticsRecord(3)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/dutyIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">值班记录</div>
                    </div>
                    <!-- 用户操作 -->
                    <div class="typeBtn" @click="goStatisticsRecord(4)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/userIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">用户操作</div>
                    </div>
                    <!-- 维保记录 -->
                    <div class="typeBtn" @click="goStatisticsRecord(5)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/maintenanceIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">维保记录</div>
                    </div>
                </div>
            </template>
            <!-- 信息查询 -->
            <div class="menuBtn" @click="goMessage(3)" :class="menuData.isActive == 3 ? 'active' : 'unactive'">

                <div class="btn">
                    <div class="btnImgBox">
                        <template v-if="menuData.isActive == 3">
                            <img class="btnImg" src="../../assets/img/menu/messageOn.svg" alt="" @dragstart.prevent>
                        </template>
                        <template v-else>
                            <img class="btnImg" src="../../assets/img/menu/messageOff.svg" alt="" @dragstart.prevent>
                        </template>

                    </div>
                    <div class="btnText">信息查询</div>
                </div>
            </div>
            <!-- 信息查询选择器 -->
            <template v-if="menuData.isActive == 3">
                <div class="messageTypeBox" v-show="menuData.messagepitchOn">
                    <!-- 图例查询 -->
                    <div class="typeBtn" @click="goMessageRecord(6)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/legendIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">图例查询</div>
                    </div>
                    <!-- 设备查询 -->
                    <div class="typeBtn" @click="goMessageRecord(7)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/deviceIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">设备查询</div>
                    </div>
                    <!-- 设备状态 -->
                    <div class="typeBtn" @click="goMessageRecord(8)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/deviceStateIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">设备状态</div>
                    </div>
                    <!-- 控制器列表 -->
                    <div class="typeBtn" @click="goMessageRecord(9)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/controllerListIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">控制器列表</div>
                    </div>
                    <!-- 设备布点图 -->
                    <div class="typeBtn" @click="goMessageRecord(10)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/deviceDiagramIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">设备布点图</div>
                    </div>
                    <!-- 平面图 -->
                    <div class="typeBtn" @click="goMessageRecord(11)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/ichnographyIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">平面图</div>
                    </div>
                    <!-- 控制室信息 -->
                    <div class="typeBtn" @click="goMessageRecord(12)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/controlRoomIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">控制室信息</div>
                    </div>
                </div>

            </template>
            <!-- 信息编辑 -->
            <div class="menuBtn" @click="goCompile(4)" :class="menuData.isActive == 4 ? 'active' : 'unactive'">

                <div class="btn">
                    <div class="btnImgBox">
                        <template v-if="menuData.isActive == 4">
                            <img class="btnImg" src="../../assets/img/menu/compileOn.svg" alt="" @dragstart.prevent>
                        </template>
                        <template v-else>
                            <img class="btnImg" src="../../assets/img/menu/compileOff.svg" alt="" @dragstart.prevent>
                        </template>
                    </div>
                    <div class="btnText">信息编辑 </div>
                </div>
            </div>
            <template v-if="menuData.isActive == 4">
                <div class="compileTypeBox" v-show="menuData.compilepitchOn">
                    <!-- 项目列表 -->
                    <div class="typeBtn" @click="goCompileRecord(11)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/projectListIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">项目列表</div>
                    </div>
                    <!-- 小区-楼宇 -->
                    <div class="typeBtn" @click="goCompileRecord(12)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/buildingIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">小区-楼宇</div>
                    </div>
                    <!-- 楼层信息 -->
                    <div class="typeBtn" @click="goCompileRecord(13)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/floorIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">楼层信息</div>
                    </div>
                    <!-- 控制器设置 -->
                    <div class="typeBtn" @click="goCompileRecord(14)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/controlIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">控制器设置</div>
                    </div>
                    <!-- 设备设置 -->
                    <div class="typeBtn" @click="goCompileRecord(15)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/deviceSetIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">设备设置</div>
                    </div>
                    <!-- 布点 -->
                    <div class="typeBtn" @click="goCompileRecord(18)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/stationingIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">布点</div>
                    </div>
                    <!-- 设备类型 -->
                    <div class="typeBtn" @click="goCompileRecord(17)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/deviceTypeIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">设备类型</div>
                    </div>
                </div>
            </template>
            <!-- 系统设置 -->
            <div class="menuBtn" @click="goSystem(5)" :class="menuData.isActive == 5 ? 'active' : 'unactive'">

                <div class="btn">
                    <div class="btnImgBox">
                        <template v-if="menuData.isActive == 5">
                            <img class="btnImg" src="../../assets/img/menu/systemOn.svg" alt="" @dragstart.prevent>
                        </template>
                        <template v-else>
                            <img class="btnImg" src="../../assets/img/menu/systemOff.svg" alt="" @dragstart.prevent>
                        </template>
                    </div>
                    <div class="btnText">系统设置 </div>
                </div>
            </div>
            <template v-if="menuData.isActive == 5">
                <div class="systemSetBox" v-show="menuData.systemSetOn">
                    <!-- 用户管理 -->
                    <div class="typeBtn" @click="goSystemRecord(24)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/usermanagementIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">用户管理</div>
                    </div>
                    <!-- 打印设置 -->
                    <div class="typeBtn" @click="goSystemRecord(19)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/printIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">打印设置</div>
                    </div>
                    <!-- 参数设置 -->
                    <div class="typeBtn" @click="goSystemRecord(20)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/parameterIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">参数设置</div>
                    </div>
                    <!-- 数据导出 -->
                    <div class="typeBtn" @click="goSystemRecord(21)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/dataIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">数据导出</div>
                    </div>
                    <!-- 远程传输 -->
                    <div class="typeBtn" @click="goSystemRecord(22)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/distanceIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">远程传输</div>
                    </div>
                    <!-- 升级 -->
                    <div class="typeBtn" @click="goSystemRecord(23)">
                        <div class="typeImg">
                            <img class="typeimg" src="../../assets/img/menu/upgradeIcon.svg" alt="" @dragstart.prevent>
                        </div>
                        <div class="typeText">升级与导入</div>
                    </div>

                </div>
            </template>
        </div>
        <template v-if="menuData.btnShow == true">
            <div class="triangleOn" @click="showBtn"></div>
        </template>
        <template v-else>
            <div class="triangleOff" @click="showBtn"></div>
        </template>
        <div class="baseBox"></div>
        <el-dialog v-model="menuData.popupShow" :show-close="false">
            <template #header>
                <div class="headerBox">提示</div>
                <div class="offBtn" @click="offsuperPassword">✖</div>
            </template>
            <div class="logoutMsg">
                <div class="password">
                    请输入超级密码:&nbsp;<el-input v-model="menuData.superPasswordInput" type="password" placeholder="请输入超级密码"
                        id="superPassword" @change="passBlur">
                    </el-input>
                </div>
                <div class="tit">
                    注意:可进入时间为30分钟
                </div>
            </div>
            <div class="sureBox">
                <button class="sureBtn" @click="superPassword">确定</button>
                <button class="sureBtn" @click="offsuperPassword">取消</button>
            </div>
        </el-dialog>
    </div>
</template>
<script>
import { useStore } from 'vuex'
import { reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { toNumber } from 'lodash';
import md5 from 'js-md5' //引入
import {
    checkPasswordRequest
} from "../../api/operation";
import {
    verifyLoginStateRequest
} from "../../api/login";
export default {
    props: {
        menuState: Boolean
    },
    setup(props, context) {
        const store = useStore();
        const router = useRouter()
        let menuData = reactive({
            isActive: 0,
            btnShow: true,
            statisticsPitchOn: false,//控制统计查询弹窗显示
            messagepitchOn: false,//控制信息查询弹窗显示
            compilepitchOn: false,//控制信息编辑弹窗显示
            systemSetOn: false,//控制系统设置弹窗显示
            popupShow: false,
            superPasswordInput: ""
        })
        // 点击首页按钮
        let goIndex = (type) => {
            router.push({ name: 'webCrtIndex', query: { userId: '123' } })
            menuData.isActive = type
            menuData.messagepitchOn = false
            menuData.statisticsPitchOn = false
            menuData.compilepitchOn = false
            menuData.systemSetOn = false
        }
        // 点击统计查询按钮
        let goStatistics = (type) => {
            if (sessionStorage.getItem("userInfo", store.state.token)) {
                menuData.isActive = type
                menuData.messagepitchOn = false
                menuData.compilepitchOn = false
                menuData.systemSetOn = false
                menuData.statisticsPitchOn = !menuData.statisticsPitchOn
            } else {
                ElMessage({
                    message: '请登录后,再进行后续操作',
                    type: 'error',
                    duration: 3 * 1000
                })
            }

        }
        // 跳转统计查询
        let goStatisticsRecord = (type) => {
            if (sessionStorage.getItem("userInfo", store.state.token)) {
                store.commit('setSwitchRecord', type)
                sessionStorage.setItem("setSwitchRecord", type);
                router.push({ name: 'statistics' })
                menuData.statisticsPitchOn = false
            } else {
                ElMessage({
                    message: '请登录后,再进行后续操作',
                    type: 'error',
                    duration: 3 * 1000
                })
            }
        }
        // 点击信息查询按钮
        let goMessage = (type) => {
            if (sessionStorage.getItem("userInfo", store.state.token)) {
                menuData.isActive = type
                menuData.statisticsPitchOn = false
                menuData.compilepitchOn = false
                menuData.systemSetOn = false
                menuData.messagepitchOn = !menuData.messagepitchOn
            } else {
                ElMessage({
                    message: '请登录后,再进行后续操作',
                    type: 'error',
                    duration: 3 * 1000
                })
            }

        }
        // 跳转信息查询
        let goMessageRecord = (type) => {
            if (sessionStorage.getItem("userInfo", store.state.token)) {
                store.commit('setSwitchRecord', type)
                sessionStorage.setItem("setSwitchRecord", type);
                router.push({ name: 'message' })
                menuData.messagepitchOn = false
            } else {
                ElMessage({
                    message: '请登录后,再进行后续操作',
                    type: 'error',
                    duration: 3 * 1000
                })
            }
        }
        // 点击信息编辑按钮
        let goCompile = (type) => {
            if (sessionStorage.getItem("userInfo", store.state.token)) {
                menuData.isActive = type
                menuData.compilepitchOn = !menuData.compilepitchOn
                menuData.messagepitchOn = false
                menuData.statisticsPitchOn = false
                menuData.systemSetOn = false
            } else {
                ElMessage({
                    message: '请登录后,再进行后续操作',
                    type: 'error',
                    duration: 3 * 1000
                })
            }

        }
        // 跳转信息编辑
        let goCompileRecord = (type) => {
            if (sessionStorage.getItem("userInfo", store.state.token)) {
                store.commit('setSwitchRecord', type)
                sessionStorage.setItem("setSwitchRecord", type);
                menuData.compilepitchOn = false
                router.push({ name: 'compile' })

            } else {
                ElMessage({
                    message: '请登录后,再进行后续操作',
                    type: 'error',
                    duration: 3 * 1000
                })
            }
        }
        let goSystem = (type) => {
            if (sessionStorage.getItem("userInfo", store.state.token)) {
                verifyLoginStateRequest().then((res) => {
                    if (res.ok) {
                        if (sessionStorage.getItem("role_id") != 3) {
                            menuData.isActive = type
                            menuData.systemSetOn = !menuData.systemSetOn
                            menuData.statisticsPitchOn = false
                            menuData.messagepitchOn = false
                            menuData.compilepitchOn = false
                        } else {
                            if (store.state.superPassword == false) {
                                menuData.popupShow = true
                            } else {
                                menuData.isActive = type
                                menuData.systemSetOn = !menuData.systemSetOn
                                menuData.statisticsPitchOn = false
                                menuData.messagepitchOn = false
                                menuData.compilepitchOn = false
                            }
                        }
                    }
                });

            } else {
                ElMessage({
                    message: '请登录后,再进行后续操作',
                    type: 'error',
                    duration: 3 * 1000
                })
            }


        }
        // 验证超级密码
        const superPassword = () => {
            let data = {
                password: md5(menuData.superPasswordInput)
            }
            checkPasswordRequest(data).then((res) => {
                if (res.ok) {
                    ElMessage({
                        message: '验证成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    store.state.superPassword = true
                    menuData.popupShow = false
                    menuData.isActive = 5
                    menuData.systemSetOn = !menuData.systemSetOn
                    menuData.statisticsPitchOn = false
                    menuData.messagepitchOn = false
                    menuData.compilepitchOn = false
                }
            });
        }
        const offsuperPassword = () => {
            menuData.popupShow = false
            menuData.superPasswordInput = ""
        }
        // 跳转系统设置页面
        let goSystemRecord = (type) => {
            if (sessionStorage.getItem("userInfo", store.state.token)) {
                store.commit('setSwitchRecord', type)
                sessionStorage.setItem("setSwitchRecord", type);

                router.push({ name: 'systemSet' })
                menuData.systemSetOn = false

            } else {
                ElMessage({
                    message: '请登录后,再进行后续操作',
                    type: 'error',
                    duration: 3 * 1000
                })
            }
        }
        let showBtn = () => {
            menuData.btnShow = !menuData.btnShow
        }
        const passBlur = () => {
            let name = document.getElementById('superPassword').value
            menuData.superPasswordInput = name
        }
        // 监听 输入超级密码弹窗
        watch(() => menuData.popupShow, (newvalue, oldvalue) => {
            if (oldvalue == true) {
                menuData.superPasswordInput = ""
            }
        })
        // 监听父组件传递的props的值 用来判断是否显示菜单按钮
        watch(props, (newProps) => {
            if (newProps.menuState == true) {
                menuData.btnShow = true
            } else if (newProps.menuState == false) {
                menuData.btnShow = false
            }
        }
        );
        //  // 监听菜单按钮显示状态
        watch(() => menuData.btnShow, (oldvalue, newvalue) => {
            if (newvalue == true) {
                context.emit('offMenu', newvalue);
            } else {
                context.emit('offMenu', newvalue);
            }
        })
        watch(() => router.currentRoute.value.path, (newValue, oldValue) => {
            if (newValue == "/") {
                menuData.isActive = 1
            } else if (newValue == "/statistics") {
                menuData.isActive = 2
            } else if (newValue == "/message") {
                menuData.isActive = 3
            } else if (newValue == "/compile") {
                menuData.isActive = 4
            } else if (newValue == "/systemSet") {
                menuData.isActive = 5
            }
        }, { immediate: true })
        return {
            menuData,
            goIndex,
            goStatistics,
            goMessage,
            goCompile,
            goSystem,
            showBtn,
            goStatisticsRecord,
            goMessageRecord,
            goCompileRecord,
            goSystemRecord,
            superPassword,
            offsuperPassword,
            store,
            passBlur
        }
    }
}
</script>
<style scoped  lang="scss">
.menuBox {
    width: 700px;
    // height: 200px;
    position: absolute;
    bottom: 0px;
    z-index: 100;
    margin-left: 610px;
    display: flex;
    align-items: center;
    flex-direction: column;

    // background-color: red;
    .btnBox {
        height: 150px;
        width: 660px;
        margin-bottom: 50px;
        display: flex;
        align-items: center;

        // background-color: #fff700;
        .menuBtn {
            width: 110px;
            height: 110px;
            border-radius: 50%;
            margin-left: 28px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            // background-color: red;

            .btnOn {
                width: 107px;
                height: 107px;
                border-radius: 50%;
                border: 1px solid #4A5CD5;
                position: absolute;
                top: 0px;

                display: flex;
                align-items: center;
                justify-content: center;
            }

            .btn {
                width: 100px;
                height: 100px;
                border-radius: 50%;
                background-color: #4A5CD5;

                position: relative;

                .btnImgBox {
                    width: 30px;
                    height: 30px;
                    position: absolute;
                    top: 27px;
                    left: 35px;

                    .btnImg {
                        width: 30px;
                        height: 30px;
                    }
                }

                .btnText {
                    width: 100px;
                    text-align: center;
                    font-size: 16px;
                    font-weight: 500;
                    letter-spacing: 0.8px;
                    position: absolute;
                    top: 67px;

                }
            }
        }

        .menuBtn:first-child {
            margin-left: 0px;
        }

        .statisticsTypeBox {
            position: absolute;
            bottom: 180px;
            right: 140px;
            width: 713px;
            height: 223px;
            display: flex;
            background-image: url("../../assets/img/menu/statisticsTypeBox.svg");
            background-size: 100% 100%;

            .typeBtn {
                width: 100px;
                height: 100px;
                margin-top: 60px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                margin-left: 36px;
                cursor: pointer;

                .typeImg {
                    width: 42px;
                    height: 42px;

                    .typeimg {
                        width: 42px;
                        height: 42px;
                    }
                }

                .typeText {
                    width: 100px;
                    font-size: 20px;
                    font-weight: 500;
                    margin-top: 10px;
                    color: #000000;
                    display: flex;
                    justify-content: center;
                }

            }

        }

        .messageTypeBox {
            width: 964px;
            height: 223px;
            display: flex;
            position: absolute;
            bottom: 180px;
            right: -161px;

            background-image: url("../../assets/img/menu/messageTypeBox.svg");
            background-size: 100% 100%;

            .typeBtn {
                width: 100px;
                height: 100px;
                margin-top: 60px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                margin-left: 33px;
                cursor: pointer;

                .typeImg {
                    width: 42px;
                    height: 42px;

                    .typeimg {
                        width: 42px;
                        height: 42px;
                    }
                }

                .typeText {

                    width: 100px;
                    font-size: 20px;
                    font-weight: 500;
                    margin-top: 10px;
                    color: #000000;
                    display: flex;
                    justify-content: center;
                }

            }
        }

        .compileTypeBox {
            width: 964px;
            height: 223px;
            display: flex;
            position: absolute;
            bottom: 180px;
            right: -300px;
            background-image: url("../../assets/img/menu/messageTypeBox.svg");
            background-size: 100% 100%;

            .typeBtn {
                width: 100px;
                height: 100px;
                margin-top: 60px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                margin-left: 32px;
                cursor: pointer;

                .typeImg {
                    width: 42px;
                    height: 42px;

                    .typeimg {
                        width: 42px;
                        height: 42px;
                    }
                }

                .typeText {
                    width: 100px;
                    font-size: 20px;
                    font-weight: 500;
                    margin-top: 10px;
                    color: #000000;
                    display: flex;
                    justify-content: center;
                }

            }
        }

        .systemSetBox {
            width: 850px;
            height: 223px;
            display: flex;
            position: absolute;
            bottom: 180px;
            right: -290px;
            background-image: url("../../assets/img/menu/systemBox.svg");
            background-size: 100% 100%;

            .typeBtn {
                width: 100px;
                height: 100px;
                margin-top: 60px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                margin-left: 20px;
                cursor: pointer;

                .typeImg {
                    width: 42px;
                    height: 42px;

                    .typeimg {
                        width: 42px;
                        height: 42px;
                    }
                }

                .typeText {
                    width: 100px;
                    font-size: 20px;
                    font-weight: 500;
                    margin-top: 10px;
                    color: #000000;
                    display: flex;
                    justify-content: center;
                }

            }
            .typeBtn:nth-child(1){
                margin-left: 70px;
            }
        }

    }

    .baseBox {
        width: 440px;
        height: 18px;
        border-bottom: 18px solid #CCD1DC;
        border-left: 50px solid transparent;
        border-right: 50px solid transparent;
        position: absolute;
        bottom: 0px;
    }

    .triangleOn {
        width: 0;
        height: 0;
        border: 22px solid transparent;
        border-bottom-color: #4A5CD5;
        border-top: none;
        border-left-color: transparent;
        border-right-color: transparent;
        cursor: pointer;
        position: absolute;
        bottom: 25px;
    }

    .triangleOff {
        width: 0;
        height: 0;
        border: 22px solid transparent;
        border-top-color: #4A5CD5;
        border-bottom: none;
        border-left-color: transparent;
        border-right-color: transparent;
        cursor: pointer;
        position: absolute;
        bottom: 25px;
    }

    .active {
        color: #fff700;
        border: 1px solid #4A5CD5;
    }

    .unactive {
        color: #ffffff;
        border: 1px solid transparent;
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
            width: 1000px;
            display: flex;
            font-size: 20px;
            align-items: center;
            justify-content: center;

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
        }

        .tit {
            width: 485px;
            display: flex;
            font-size: 20px;
            margin-top: 20px;
            align-items: center;
            justify-content: left;

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

}
</style>