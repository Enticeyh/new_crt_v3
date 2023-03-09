<template>
    <div class="detailBox" v-show="detailDate.detailShow">
        <div class="detailMessage">
            <div class="deviceMessage">
                <template v-if="detailDate.detailType == 1">
                    <div class="messsage">{{ detailDate.detailMessage.current }}&nbsp;&nbsp;-&nbsp;&nbsp;{{
                        detailDate.detailMessage.device_type_name
                    }}&nbsp;&nbsp;-
                        {{
                            detailDate.detailMessage.psn
                        }}&nbsp;&nbsp;-&nbsp;&nbsp;已布点&nbsp;&nbsp;;
                        描述:{{
                            detailDate.detailMessage.description
                        }}</div>
                </template>
                <template v-else-if="detailDate.detailType == 2">
                    <div class="messsage">
                        <template v-if="detailDate.detailMessage.area_name">
                            {{ detailDate.detailMessage.area_name }}&nbsp;&nbsp;-
                        </template>
                        <template v-if="detailDate.detailMessage.build_name">
                            {{ detailDate.detailMessage.build_name }}&nbsp;&nbsp;-
                        </template>
                        <template v-if="detailDate.detailMessage.name">
                            {{ detailDate.detailMessage.name }}&nbsp;&nbsp;
                        </template>
                        图片类型:{{ detailDate.detailMessage.picture_type_name }}
                    </div>
                </template>
            </div>
            <button class="return" @click="offDetail">返回上级</button>
        </div>
        <div class="detailImgBox" v-loading="detailDate.loadingImg">
            <div class="bigBox" id="bigBox" ref="tagsRef">
                <div class="alarmsImgBox" id="box">
                    <el-image id="svg1" class="alarmsImg" :src="detailDate.url" fit="contain" @mousewheel="adjust_zoom"
                        :style="{ height: detailDate.floorItem.height / 192 + 'rem', width: detailDate.floorItem.width / 192 + 'rem' }"
                        @dragstart.prevent>
                    </el-image>

                    <div class="assign-device" v-for="device in  detailDate.floorItem.floorAssign" :key="device.id"
                        :style="{ top: device.coordinate_Y / 192 + 'rem', left: device.coordinate_X / 192 + 'rem', height: 1094 * device.rate / 192 + 'rem', width: 1094 * device.rate / 192 + 'rem' }">

                        <el-tooltip class="toop-item" effect="dark" placement="top-start" :manual="false"
                            :value="detailDate.clickDeviceid === device.id">
                            <template #content>
                                <div>地址: {{ device.device_address }}</div>
                                <div style="margin-top:5px">设备类型: {{ device.device_type_name }}</div>
                                <span v-if="device.device_status == 2" style="color: #ff3d3d">首警; </span>
                                <span v-if="device.fire == 1" style="color: #ff3d3d">火警; </span>
                                <span v-if="device.linkage == 1" style="color: #ff3d3d">启动; </span>
                                <span v-if="device.feedback == 1" style="color: #ff3d3d">反馈; </span>
                                <span v-if="device.malfunction == 1" style="color: orange">故障; </span>
                                <span v-if="device.shielding == 1" style="color: orange">屏蔽; </span>
                                <span v-if="device.supervise == 1" style="color: #ff3d3d">监管; </span>
                                <span v-if="device.vl_malfunction == 1" style="color: orange">声光故障; </span>
                                <span v-if="device.vl_shielding == 1" style="color: orange">声光屏蔽; </span>
                                <div style="margin-top:5px">注释: {{ device.description }}</div>
                            </template>
                            <el-image id="deviceImg" class="deviceImg" :src="detailDate.config + device.path"
                                style="user-select:none"
                                :style="{ height: 1462 * device.rate + 'px', width: 1462 * device.rate + 'px' }">
                            </el-image>
                        </el-tooltip>

                        <div v-if="device.alarm != 0">
                            <div class="Firstcircle" v-if="device.device_status == 2 && device.fire == 1">
                                <div class="FirstCircle1">首警</div>
                                <div class="FirstCircle2"></div>
                                <div class="FirstCircle3"></div>
                                <!-- <div class="FirstCenter"></div> -->
                            </div>
                            <div class="circle"
                                v-else-if="device.fire == 1 || device.linkage == 1 || device.feedback == 1 || device.supervise == 1">
                                <div class="circle1"></div>
                                <div class="circle2"></div>
                                <div class="circle3"></div>
                                <!-- <div class="center"></div> -->
                            </div>
                            <div class="launch_circle"
                                v-if="device.malfunction === 1 || device.vl_malfunction === 1 || device.shielding == 1 || device.vl_shielding === 1">
                                <div class="launch_circle1"></div>
                                <div class="launch_circle2"></div>
                                <div class="launch_circle3"></div>
                                <!-- <div class="launch_center"></div> -->
                            </div>
                        </div>
                        <img class="arrowsUpImg" v-if="device.device_id == detailDate.currentFloorIndex"
                            src="../../assets/img/comment/arrowsUp.svg" alt=""
                            style="position: absolute;z-index:3;min-width: 30px;max-width: 50px" :style="{
                                width: 30 + 'px',
                                left: -15 + 'px',
                                top: -30 * 1.5 + 'px',
                            }" @dragstart.prevent>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { reactive, watch, ref, onMounted, getCurrentInstance } from 'vue'
import config from "../../utils/config";
import { ElMessage } from 'element-plus'
import Panzoom from '@panzoom/panzoom'
import {
    indexStationListRequest,
} from "../../api/operation";
import { imgIdRequest } from "../../api/recordData";
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
export default {
    emits: ['offDetail'],
    props: {
        detailState: Boolean,
        detailData: Object
    },

    setup(props, context) {
        const { proxy } = getCurrentInstance()
        const store = useStore();
        const router = useRouter()
        const tagsRef = ref(null)
        let detailDate = reactive({
            fs: 0,
            alarmsImgBox: "",
            detailType: 0,
            url: "",
            config: "",
            detailShow: false,
            detailMessage: {},
            request: {},
            panzoom: null,
            currentFloorIndex: "",
            floorItem: {
                id: 0,
                top: 0,
                left: 0,
                width: 1094,
                height: 670,
                path: '',
                lastTop: 0,
                lastLeft: 0,
                // 该层楼的布信息
                floorAssign: [],
                waitData: []
            },
            deviceDeatil: {},
            zoom: 1,
            deviceTop: 0,
            deviceLeft: 0,
            loadingImg: false
        })
        onMounted(() => {
            const elem = document.getElementById('box')
                detailDate.panzoom = Panzoom(elem, {
                    maxScale: 10,
                    minScale: 1,
                })
                elem.parentElement.addEventListener('wheel', detailDate.panzoom.zoomWithWheel)
                detailDate.fs = getComputedStyle(window.document.documentElement)['font-size'].slice(0, -2)

        })
        const adjust_zoom = (evt) => {
            let zoom = detailDate.zoom
            zoom = evt.wheelDelta / 120 * 0.1 + zoom
            if (zoom < 0.3)
                zoom = 0.3
            if (zoom > 3)
                zoom = 3
            detailDate.zoom = zoom
        }
        // 关闭弹窗
        const offDetail = () => {
            context.emit('offDetail', false);
        }
        // 设备居中
        const deviceCenter = (val) => {
            let tagsHeight = tagsRef.value
            let width = tagsHeight.offsetWidth / 2
            let height = tagsHeight.offsetHeight / 2
            detailDate.panzoom.pan(-detailDate.deviceDeatil.coordinate_X / 192 * detailDate.fs + width, -detailDate.deviceDeatil.coordinate_Y / 192 * detailDate.fs + height, { relative: true })
            detailDate.panzoom.zoomIn({ animate: true })
        }
        // 获取楼层布点设备列表
        const floorDeviceList = (id) => {
            detailDate.loadingImg = true
            let data = {
                page: 0,
                floor_id: id
            }
            indexStationListRequest(data).then((res) => {
                detailDate.floorItem.floorAssign = res.data
                const deviceDeatil = detailDate.floorItem.floorAssign.filter(item => {
                    return item.device_id === detailDate.detailMessage.id
                })
                detailDate.deviceDeatil = deviceDeatil[0]
                detailDate.loadingImg = false
            });

        }
        watch(props, (newProps) => {
            if (newProps.detailState == true) {
                detailDate.zoom = 1
                detailDate.config = config.baseUrl
                detailDate.detailShow = true
                detailDate.detailMessage = newProps.detailData
                // 楼层进入
                if (newProps.detailData.device_type_name == undefined) {
                    detailDate.detailType = 2
                    detailDate.url = config.baseUrl + newProps.detailData.path
                    if (sessionStorage.getItem("setSwitchRecord") == 12 || sessionStorage.getItem("setSwitchRecord") == 11) {

                    } else {
                        floorDeviceList(detailDate.detailMessage.id)
                    }

                } else {
                    // 设备进入
                    detailDate.detailType = 1
                    let alarm_log_id = newProps.detailData.assign_floor_id
                    detailDate.currentFloorIndex = detailDate.detailMessage.id
                    imgIdRequest(alarm_log_id).then((res) => {
                        detailDate.url = config.baseUrl + res.data.path
                    });
                    floorDeviceList(detailDate.detailMessage.assign_floor_id)
                    let timer = null
                    timer = setTimeout(() => {
                        deviceCenter()
                    }, 500)

                }

            } else {
                detailDate.detailShow = false
                detailDate.floorItem.floorAssign = []
                detailDate.panzoom.reset()
                detailDate.currentFloorIndex = ""
            }
        }
        );
        // 监听vuex存储状态变化
        watch(() => store.state.switchRecord, (newValue, oldValue) => {
            if (newValue != oldValue) {
                detailDate.detailShow = false
            }
        })
        return {
            detailDate,
            offDetail,
            floorDeviceList,
            adjust_zoom,
            deviceCenter,
            tagsRef
        }
    }
}
</script>
<style scoped lang="scss" >
.detailBox {
    width: 1920px;
    height: 994px;
    position: absolute;
    background-color: rgb(255, 255, 255);
    z-index: 10;

    // 设备详情
    .detailMessage {
        width: 1840px;
        height: 100px;
        margin-left: 40px;
        display: flex;
        align-items: center;
        border-bottom: 1px dashed #0469ff;

        .deviceState {
            width: 100px;
            height: 100px;
            margin-left: 50px;

            .deviceStateImg {
                width: 100px;
                height: 100px;
            }
        }

        // 设备信息
        .deviceMessage {
            width: 1600px;
            height: 100px;
            display: flex;
            flex-direction: column;
            font-size: 20px;
            justify-content: center;



            .messsage {

                margin-left: 40px;
                font-weight: 520;
                font-size: 22px;
                overflow: hidden; //超出的文本隐藏
                text-overflow: ellipsis; //溢出用省略号显示
                white-space: nowrap; //溢出不换行
            }
        }

        .return {
            width: 120px;
            height: 40px;
            font-size: 20px;
            font-weight: 500;
            border: none;
            border-radius: 2px;
            color: #ffffff;
            cursor: pointer;
            background-color: #0469ff;
        }
    }

    .detailImgBox {
        width: 1920px;
        height: 793px;
        display: flex;
        align-items: center;
        justify-content: center;

        .bigBox {
            width: 1094px;
            height: 670px;
            border: 2px solid #605d5d;

            .alarmsImgBox {
                width: 1094px;
                height: 670px;
                position: relative;

                :deep(.el-image) {
                    width: 1094px;
                    height: 670px;
                    position: absolute;
                }

                .assign-device {
                    position: absolute;
                    cursor: pointer;

                    :deep(.el-image) {
                        float: left;
                    }
                }



                /*火警动画效果*/
                .Firstcircle {
                    width: 35px;
                    height: 35px;
                    position: absolute;
                    float: left;
                    z-index: 99;


                    .FirstCircle2,
                    .FirstCircle3,
                    .FirstCenter {
                        position: absolute;
                        left: 50%;
                        top: 50%;
                        margin: -30px 0 0 -30px;
                        width: 30px;
                        height: 30px;
                        border-radius: 30px;
                        background-color: #ff3d3d;
                    }

                    .FirstCircle1 {
                        position: absolute;
                        left: 50%;
                        top: 50%;
                        margin: -30px 0 0 -30px;
                        width: 30px;
                        height: 30px;
                        border-radius: 30px;
                        z-index: 30;
                        -webkit-animation: Firstcircle 3s linear infinite;
                        animation: Firstcircle 3s linear infinite;
                    }


                    @-webkit-keyframes Firstcircle {

                        /* Safari and Chrome */
                        from {
                            opacity: 1;
                            -webkit-transform: scale(0);
                        }

                        to {
                            opacity: 0;
                            -webkit-transform: scale(3);
                        }
                    }
                }

                /*火警动画效果*/
                .circle {
                    width: 35px;
                    height: 35px;
                    position: absolute;
                    float: left;
                    z-index: 999;

                    .circle1,
                    .circle2,
                    .circle3,
                    .center {
                        position: absolute;

                        left: 50%;
                        top: 50%;
                        margin: -30px 0 0 -30px;
                        width: 30px;
                        height: 30px;
                        border-radius: 30px;
                        background-color: #ff3d3d;

                    }

                    .center {
                        position: absolute;
                        left: 50%;
                        top: 50%;
                        margin: -34px 0 0 -11px;
                        width: 10px;
                        height: 10px;
                        border-radius: 50%;
                        background: #ff3d3d;
                        text-align: center;
                        color: #ff3d3d;
                    }

                }

                /*故障动画效果*/
                .launch_circle {
                    width: 35px;
                    height: 35px;
                    z-index: 999;
                    position: absolute;

                    .launch_circle1,
                    .launch_circle2,
                    .launch_circle3,
                    .launch_center {
                        position: absolute;
                        left: 50%;
                        top: 50%;
                        margin: -30px 0 0 -30px;
                        width: 30px;
                        height: 30px;
                        border-radius: 30px;
                        background-color: #ffae00;

                    }

                    .launch_center {
                        position: absolute;
                        left: 50%;
                        top: 50%;
                        margin: -34px 0 0 -11px;
                        width: 10px;
                        height: 10px;
                        border-radius: 50%;
                        background: orange;
                        text-align: center;
                        line-height: 70px;
                        color: orange;
                        font-size: 16px;

                    }


                }

                .arrowsUpImg {
                    position: absolute;
                    z-index: 999;
                    -webkit-animation: marker 1s linear infinite;
                    animation: marker 1s linear infinite
                }

                @-webkit-keyframes marker {
                    0% {
                        -webkit-transform: scale(1);
                        //transform: translateY(-100px);
                    }

                    25% {
                        -webkit-transform: scale(1.5);
                        //transform: translateY(-80px);
                    }

                    50% {
                        -webkit-transform: scale(2);
                        //transform: translateY(-60px);
                    }

                    75% {
                        -webkit-transform: scale(1.5);
                        //transform: translateY(-30px);
                    }

                    100% {
                        -webkit-transform: scale(1);
                        //transform: translateY(0px);
                    }
                }

                .circle:hover {
                    display: none;
                }

                .Firstcircle:hover {
                    display: none;
                }

                .launch_circle:hover {
                    display: none;
                }
            }


        }
    }

}
</style>