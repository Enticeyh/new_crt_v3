<template>
    <div class="stationBox" id="stationBox" v-show="stationState" v-loading="recordData.loading">
        <div class="stationMsg">
            <template v-if="recordData.inheritShow">
                <div class="inheritBox">继承列表</div>
                <div class="deviceBox">
                    <div class="inheritFloorlistBox" v-loading="recordData.inheritFloorlistLoading">
                        <div class="inheritFloorBox" v-for="item in recordData.inheritList"
                            :title="item.area_name + item.build_name + item.name" @click="openPopup(item)">
                            <div class="inheritFloorImg">
                                <img class="inheritImg" :src="recordData.Url + item.path" alt="" @dragstart.prevent>
                            </div>
                            <div class="inheritFloorText">&nbsp;{{ item.area_name }}{{ item.build_name }}{{ item.name }}
                            </div>
                        </div>
                    </div>
                </div>
            </template>
            <template v-else>
                <div class="typeBox">
                    <div class="typeName" :class="recordData.switchDeviceTypeActive == 1 ? 'active' : 'unactive'"
                        @click="switchDeviceType(1)" title="控制器-回路">控制器 <img @click="switchDevice(1)"
                            class="switchDeviceImg" src="../../assets/img/comment/refresh.svg" alt="" @dragstart.prevent></div>
                    <div class="typeName" :class="recordData.switchDeviceTypeActive == 2 ? 'active' : 'unactive'"
                        @click="switchDeviceType(2)" title="小区-楼宇-楼层">地址 <img @click="switchDevice(2)"
                            class="switchDeviceImg" src="../../assets/img/comment/refresh.svg" alt="" @dragstart.prevent></div>
                </div>
                <!-- 设备列表 -->
                <div class="deviceBox">
                    <template v-if="recordData.projectSlect">
                        <template v-if="recordData.switchDeviceTypeActive == 1">
                            <div class="deviceList">
                                <!-- 控制器 -->
                                <el-collapse accordion @change="getCLd">
                                    <el-collapse-item v-for="item in recordData.controllerLoop">
                                        <template #title>
                                            <div class="controllerName">{{ item.label }}</div>
                                        </template>
                                        <!-- 回路 -->
                                        <el-collapse accordion @change="getCLd">
                                            <el-collapse-item :title="iteme.label" v-for="iteme in item.children"
                                                @click="change(iteme.id, item.id)" class="loopBox">
                                                <template #title>
                                                    <div class="loopName">{{ iteme.label }}</div>
                                                </template>
                                                <ul class="infinite-list" v-infinite-scroll="load"
                                                    v-loading="recordData.loadingDevice">
                                                    <li v-for="items in recordData.deviceList" :key="items.id"
                                                        :title="items.description"
                                                        v-show="items.loop_num === iteme.id & !recordData.selectedDeviceIds.includes(items.id)"
                                                        :id="items.id" class="infinite-list-item">
                                                        <div class="deviceDetail"
                                                            @click.stop="station(items.id, items.path, items.controller_num, items.loop_num, items.addr_num, items.description, items.psn, 0, 0, items.device_type_name, items.current, items.description)">
                                                            回路{{ items.loop_num }}-地址{{ items.addr_num }} --{{
                                                            items.device_type_name
                                                            }} -- {{ items.description }}
                                                        </div>
                                                    </li>
                                                </ul>
                                            </el-collapse-item>
                                        </el-collapse>
                                    </el-collapse-item>
                                </el-collapse>
                            </div>
                        </template>
                        <template v-else-if="recordData.switchDeviceTypeActive == 2">
                            <div class="deviceList">
                                <el-collapse accordion @change="getout">
                                    <el-collapse-item v-for="item in recordData.areaData">
                                        <template #title>
                                            <div class="areaName">{{ item.label }}</div>
                                        </template>
                                        <!-- 楼宇 -->
                                        <el-collapse accordion @change="getout">
                                            <el-collapse-item v-for="itemB in item.children">
                                                <template #title>
                                                    <div class="areaName">{{ itemB.label }}</div>
                                                </template>
                                                <!-- 单元或楼层 -->
                                                <el-collapse accordion @change="getout">
                                                    <el-collapse-item v-for="itemU in itemB.children"
                                                        @click="getDeviceList(itemU)">
                                                        <template #title>
                                                            <div class="areaName">{{
                                                            itemU.label
                                                            }}</div>
                                                        </template>
                                                        <template v-if="itemU.children">
                                                            <!-- 楼层或分区 -->
                                                            <el-collapse accordion @change="getout">
                                                                <el-collapse-item v-for="itemF in itemU.children"
                                                                    @click="getDeviceList(itemF)">
                                                                    <template #title>
                                                                        <div class="areaName">{{ itemF.label }}</div>
                                                                    </template>
                                                                    <template v-if="itemF.children">
                                                                        <!-- 分区 -->
                                                                        <el-collapse accordion @change="getout">
                                                                            <el-collapse-item
                                                                                v-for="itemD in itemF.children"
                                                                                @click="getDeviceList(itemD)">
                                                                                <template #title>
                                                                                    <div class="areaName">{{ itemD.label
                                                                                    }}
                                                                                    </div>
                                                                                </template>
                                                                                <template v-if="itemD.children">
                                                                                    <!-- 房间 -->
                                                                                    <el-collapse accordion
                                                                                        @change="getout">
                                                                                        <el-collapse-item
                                                                                            v-for="itemR in itemD.children"
                                                                                            @click="getDeviceList(itemR)">
                                                                                            <template #title>
                                                                                                <div class="areaName">{{
                                                                                                itemR.label
                                                                                                }}
                                                                                                </div>
                                                                                            </template>
                                                                                            <ul class="infinite-list"
                                                                                                    v-infinite-scroll="load"
                                                                                                    v-loading="recordData.loadingDevice">
                                                                                                    <li v-for="items in recordData.deviceList"
                                                                                                        :title="items.description"
                                                                                                        v-show="items.district === itemD.label.split('-')[0] & !recordData.selectedDeviceIds.includes(items.id)"
                                                                                                        @click="station(items.id, items.path, items.controller_num, items.loop_num, items.addr_num, items.description, items.psn, 0, 0, items.device_type_name, items.current, items.description)"
                                                                                                        class="infinite-list-item">
                                                                                                        回路{{
                                                                                                        items.loop_num
                                                                                                        }}-地址{{
                                                                                                        items.addr_num
                                                                                                        }} --{{
                                                                                                        items.device_type_name
                                                                                                        }} --
                                                                                                        {{
                                                                                                        items.description
                                                                                                        }}
                                                                                                    </li>
                                                                                                </ul>

                                                                                        </el-collapse-item>
                                                                                    </el-collapse>
                                                                                </template>
                                                                                <template v-else>
                                                                                    <ul class="infinite-list"
                                                                                        v-infinite-scroll="load"
                                                                                        v-loading="recordData.loadingDevice">
                                                                                        <li v-for="items in recordData.deviceList"
                                                                                            :title="items.description"
                                                                                            v-show="items.district === itemD.label.split('-')[0] & !recordData.selectedDeviceIds.includes(items.id)"
                                                                                            @click="station(items.id, items.path, items.controller_num, items.loop_num, items.addr_num, items.description, items.psn, 0, 0, items.device_type_name, items.current, items.description)"
                                                                                            class="infinite-list-item">
                                                                                            回路{{ items.loop_num }}-地址{{
                                                                                            items.addr_num
                                                                                            }} --{{
                                                                                            items.device_type_name
                                                                                            }} --
                                                                                            {{ items.description }}
                                                                                        </li>
                                                                                    </ul>
                                                                                </template>

                                                                            </el-collapse-item>
                                                                        </el-collapse>
                                                                    </template>
                                                                    <template v-else>
                                                                        <template
                                                                            v-if="recordData.floorordistrict == true">
                                                                            <ul class="infinite-list"
                                                                                v-infinite-scroll="load"
                                                                                v-loading="recordData.loadingDevice">
                                                                                <li v-for="items in recordData.deviceList"
                                                                                    :title="items.description"
                                                                                    v-show="items.district === itemF.label.split('-')[0] & !recordData.selectedDeviceIds.includes(items.id)"
                                                                                    @click="station(items.id, items.path, items.controller_num, items.loop_num, items.addr_num, items.description, items.psn, 0, 0, items.device_type_name, items.current, items.description)"
                                                                                    class="infinite-list-item">
                                                                                    回路{{ items.loop_num
                                                                                    }}-地址{{ items.addr_num }}
                                                                                    --{{ items.device_type_nam }} -- {{
                                                                                    items.description
                                                                                    }}
                                                                                </li>
                                                                            </ul>
                                                                        </template>
                                                                        <template v-else>
                                                                            <ul class="infinite-list"
                                                                                v-infinite-scroll="load"
                                                                                v-loading="recordData.loadingDevice">
                                                                                <li v-for="items in recordData.deviceList"
                                                                                    :title="items.description"
                                                                                    v-show="items.floor === itemF.label.split('-')[0] & !recordData.selectedDeviceIds.includes(items.id)"
                                                                                    @click="station(items.id, items.path, items.controller_num, items.loop_num, items.addr_num, items.description, items.psn, 0, 0, items.device_type_name, items.current, items.description)"
                                                                                    class="infinite-list-item">
                                                                                    回路{{ items.loop_num
                                                                                    }}-地址{{ items.addr_num }}
                                                                                    --{{ items.device_type_nam }} -- {{
                                                                                    items.description
                                                                                    }}
                                                                                </li>
                                                                            </ul>

                                                                        </template>

                                                                    </template>
                                                                </el-collapse-item>
                                                            </el-collapse>
                                                        </template>
                                                        <template v-else>
                                                            <ul class="infinite-list" v-infinite-scroll="load"
                                                                v-loading="recordData.loadingDevice">
                                                                <li v-for="items in recordData.deviceList"
                                                                    :title="items.description"
                                                                    v-show="items.floor === itemU.label.split('-')[0] & !recordData.selectedDeviceIds.includes(items.id)"
                                                                    @click="station(items.id, items.path, items.controller_num, items.loop_num, items.addr_num, items.description, items.psn, 0, 0, items.device_type_name, items.current, items.description)"
                                                                    class="infinite-list-item">
                                                                    回路{{ items.loop_num }}-地址{{ items.addr_num }} --{{
                                                                    items.device_type_name
                                                                    }} -- {{ items.description }}
                                                                </li>
                                                            </ul>
                                                        </template>
                                                    </el-collapse-item>
                                                </el-collapse>
                                            </el-collapse-item>
                                        </el-collapse>
                                    </el-collapse-item>
                                </el-collapse>
                            </div>
                        </template>
                    </template>
                    <template v-else>
                        <div class="noneText">请选择项目</div>
                    </template>
                </div>
            </template>
        </div>
        <div class="station" ref="assingPicRef">
            <div class="demandBox" id="demandBox">
                <div class="selectBox" v-show="recordData.onlyObject">
                    <el-select v-model="recordData.projectSlect" placeholder="请选择项目" clearable
                        @change="selectFun(recordData.projectSlect, 1)" @clear="clrarSlect(1)">
                        <el-option v-for="item in recordData.projectList" :key="item.id" :label="item.name"
                            :value="item.id" />
                    </el-select>
                </div>
                <div class="selectBox">
                    <el-select v-model="recordData.areaSelect" placeholder="请选择小区" clearable
                        @change="selectFun(recordData.areaSelect, 2)" @clear="clrarSlect(2)"
                        @visible-change="visibleArea">
                        <el-option v-for="item in recordData.areaList" :key="item.id" :label="item.name"
                            :value="item.id" />
                    </el-select>
                </div>
                <div class="selectBox">
                    <el-select v-model="recordData.buildsSelect" placeholder="请选择楼宇" clearable
                        @change="selectFun(recordData.buildsSelect, 3)" @clear="clrarSlect(3)"
                        @visible-change="visibleBuild">
                        <el-option v-for="item in recordData.buildsList" :key="item.id" :label="item.name"
                            :value="item.id" />
                    </el-select>
                </div>
                <div class="selectBox">
                    <el-select v-model="recordData.floorsSlect" placeholder="请选择楼层" clearable
                        @change="selectFun(recordData.floorsSlect, 4)" @clear="clrarSlect(4)"
                        @visible-change="visibleFloor">
                        <el-option v-for="item in recordData.floorsList" :key="item.id" :label="item.name"
                            :value="item.id" />
                    </el-select>
                </div>
                <div class="btnBox" @click="showInherit">继承</div>

                <div class="btnBox" @click="openSavePopup">保存</div>
                <button class="saveSvgBtn" @click="saveSvg">合成SVG</button>
            </div>
            <div class="stationImgBox" v-loading="recordData.loadingImg">
                <template v-if="recordData.stationImgUrl == ''">
                    <div class="noneBox">
                        <img class="noneImg" src="../../assets/img/comment/none.svg" alt="" @dragstart.prevent>
                    </div>
                </template>
                <template v-else>
                    <div class="stationImgBigBox"
                        :style="{ top: recordData.floorItem.top + 'px', left: recordData.floorItem.left + 'px', height: recordData.floorItem.height + 'px', width: recordData.floorItem.width + 'px' }">
                        <el-image @mousedown.prevent="floorAssignMove(recordData.floorsSlect, $event)"
                            @dblclick="dbClickAddDevice($event)" @mousewheel.native="watchMouseWheel"
                            :src="recordData.stationImgUrl" fit="contain"
                            :style="{ height: recordData.floorItem.height + 'px', width: recordData.floorItem.width + 'px' }">
                        </el-image>
                        <div class="assign-device" v-for="item in recordData.floorItem.floorAssign" :key="item.id"
                            @mousedown.prevent="deviceMove(item.device_id, $event)"
                            @contextmenu.prevent="showDeviceDelete(item.device_id, item)"
                            :style="{ top: item.coordinate_Y + 'px', left: item.coordinate_X + 'px', height: item.height + 'px', width: item.width + 'px' }">
                            <el-tooltip class="toop-item" effect="dark" :content="item.description" fit="contain"
                                placement="top-start">
                                <template v-if="item.rate">
                                    <el-image :src="recordData.Url + item.path" :id="item.id"
                                        @dblclick="rotateImg(item)"
                                        :style="{ height: item.height + 'px', width: item.width + 'px', transform: `rotate(${item.angle}deg)`  }">
                                    </el-image>
                                </template>

                                <template v-else>
                                    <el-image :src="recordData.Url + item.path" :id="item.id"
                                        @dblclick="rotateImg(item)"
                                        :style="{ height: item.height + 'px', width: item.width + 'px', transform: `rotate(${item.angle}deg)` }">
                                    </el-image>
                                </template>

                            </el-tooltip>

                            <template v-if="recordData.rightClickId == item.device_id">
                                <el-dialog v-model="recordData.popupShow" :show-close="false">
                                    <template #header>
                                        <div class="headerBox">设备详情</div>
                                        <div class="offBtn" @click="recordData.rightClickId = 0">✖</div>
                                    </template>
                                    <div class="loginBox">
                                        <div class="account">
                                            设备类型:{{ item.device_type_name || recordData.deviceType }}
                                        </div>
                                        <div class="account">
                                            设备地址:{{ item.device_address ||
                                            recordData.deviceCurrent}}
                                        </div>
                                        <div class="account">
                                            设备描述:{{ recordData.deviceDescription }}
                                        </div>
                                    </div>
                                    <div class="sureBox">
                                        <button class="sureBtn" @click="revampDevice(19,item)">修改</button>
                                        <button class="sureBtn" @click="deleteDevice(item.device_id)">删除</button>
                                    </div>
                                </el-dialog>
                            </template>
                        </div>
                    </div>
                </template>
            </div>
        </div>
        <!-- 布点保存弹窗 -->
        <el-dialog v-model="recordData.savePopupShow" :show-close="false">
            <template #header>
                <div class="headerBox">布点保存</div>
                <div class="offBtn" @click="offsavePopup">✖</div>
            </template>
            <div class="loginBox">
                <div class="account">
                    图纸信息:
                    {{ recordData.floorData.area_name }}{{ recordData.floorData.build_name }}{{
                    recordData.floorData.name
                    }}
                </div>
                <div class="account">
                    图纸类型:{{ recordData.floorData.picture_type_name }}
                </div>
                <div class="account">
                    已布点数量:{{ recordData.floorItem.floorAssign.length }}
                </div>
                <div class="account">
                    此次新增或修改布点数量(包含自动保存点位):{{ recordData.createUpdateDevcieIds.length }}
                </div>
                <div class="account">
                    <el-checkbox v-model="recordData.inherit" label="是否作为继承模板" @change="inherit" border></el-checkbox>
                </div>
                <div class="account">
                    <!-- 设备描述:{{ item.description }} -->
                </div>
            </div>
            <div class="sureBox">
                <button class="sureBtn" @click="saveAssign">保存</button>
            </div>
        </el-dialog>
        <el-dialog v-model="recordData.dialogShow" :show-close="false">
            <template #header>
                <div class="headerBox">
                    继承
                </div>
                <div class="offBtn" @click="offPopup">✖</div>
            </template>
            <div class="inheritFunBox">
                <div class="leftBox">
                    <div class="account">
                        <div class="textBox">起始控制器号</div>
                        <div class="inputBox">
                            <el-input v-model="recordData.start_controller_num" placeholder="请输入内容"></el-input>
                        </div>
                    </div>
                    <div class="account">
                        <div class="textBox">起始回路号</div>
                        <div class="inputBox">
                            <el-input v-model="recordData.start_loop_num" placeholder="请输入内容"></el-input>
                        </div>
                    </div>
                    <div class="account">
                        <div class="textBox">起始地址号</div>
                        <div class="inputBox">
                            <el-input v-model="recordData.start_addr_num" placeholder="请输入内容"></el-input>
                        </div>
                    </div>
                </div>
                <div class="rightBox">
                    <div class="account">
                        <div class="textBox">结束控制器号</div>
                        <div class="inputBox">
                            <el-input v-model="recordData.end_controller_num" placeholder="请输入内容"></el-input>
                        </div>
                    </div>
                    <div class="account">
                        <div class="textBox">结束回路号</div>
                        <div class="inputBox">
                            <el-input v-model="recordData.end_loop_num" placeholder="请输入内容"></el-input>
                        </div>
                    </div>
                    <div class="account">
                        <div class="textBox">结束地址号</div>
                        <div class="inputBox">
                            <el-input v-model="recordData.end_addr_num" placeholder="请输入内容"></el-input>
                        </div>
                    </div>
                </div>

            </div>
            <div class="sureBox">
                <button class="sureBtn" @click="inheritFun">确定</button>
            </div>
        </el-dialog>
        <popup :popupType="recordData.popupType" :popupData="recordData.popupData" @offPopup="offPopup" @sure="sure">
        </popup>
    </div>
</template>
<script>
import config from "../../utils/config";
import { useStore } from 'vuex'
import { reactive, onMounted, watch, getCurrentInstance } from 'vue';
import {
    projectListRequest,
    areaListRequest,
    buildingListRequest,
    floorsListRequest,
    areaBuildsRequest,
    controllerLoopRequest,
    deviceListRequest
} from "../../api/baseData";
import {
    addStationRequest,
    stationListRequest,
    deleteStationRequest,
    deletedevice_idStationRequest,
    saveSVG,
    inheritStationRequest,
    revampDevicesRequest
} from "../../api/operation";
import popup from "../popup/popup"
import { ElMessage } from 'element-plus'

export default ({
    props: {
        stationState: Boolean,
    },
    components: {
        popup,
    },
    setup(props) {
        const { proxy } = getCurrentInstance()
        const store = useStore();
        let recordData = reactive({
            loading: false,
            loadingDevice: false,
            loadingImg: false,
            inheritFloorlistLoading: false,
            inherit: false,//继承按钮开关
            dialogShow: false,
            switchDeviceTypeActive: 1,//切换布点设备分级类型
            onlyObject: true,
            Request: {
                page: 0
            },
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
                floorAssign: []
            },
            Url: "",//获取地址
            stationImgUrl: "",//布点图纸路径
            areaData: [],//小区楼宇楼层 层级关系
            controllerLoop: [],//控制器 回路层级关系
            projectSlect: "",//项目选择器
            projectList: [],//项目列表
            areaSelect: "",//小区选择器
            areaList: [],//小区列表
            buildsSelect: "",//楼宇选择器
            buildsList: [],//楼宇列表
            floorsSlect: "",//楼层选择器
            floorsList: [],//楼层列表
            deviceList: [],//设备列表
            floorId: "",//楼层id
            loopId: "",//当前选择回路号
            controllerId: "",//当前选择控制器号
            floorData: [],//选中的楼层信息
            deleteData: [],
            // 新增或修改的布点设备devcie_id
            createUpdateDevcieIds: [],
            // 左侧列表上已经选择过的设备列表
            selectedDeviceIds: [],
            // 左侧device点击选择的device
            clickDeviceId: 0,
            // 鼠标右键点击的device id
            rightClickId: 0,
            switchInheritState: 0,
            selectControllerNum: "",//选中的控制器号
            // 删除
            isOnrightMenu: true,
            popupShow: false,
            savePopupShow: false,
            inheritShow: false,
            lastAssign: {
                loop: 0,
                addr: 0
            },
            assignItem: {
                id: 0,
                // assign_id=0表示该设备是本次需要新布点的设备，
                assign_id: 0,
                top: 0,
                left: 0,
                width: 30,
                height: 30,
                path: '',
                description: '',
                coordinate_Y: 0,
                coordinate_X: 0,
                rate: 1
            },
            deviceType: "",//右键点击新增设备 设备类型
            deviceCurrent: "",//右键点击新增设备 设备地址
            deviceDescription: "",//右键点击新增设备 设备描述
            inheritList: [],//继承列表
            // 继承
            father_floor_id: "",//继承id
            start_controller_num: "",//起始控制器号
            start_loop_num: "",//起始回路号
            start_addr_num: "",//起始地址号
            end_controller_num: "",//结束控制器号
            end_loop_num: "",//结束回路号
            end_addr_num: "",//结束地址号,
            huiId: {},//用来存储 地址分级点击数据
            popupType: 0,//控制弹窗显示隐藏
            popupData: {},
            collapseState: false,//控制折叠面板状态
            collapseCState: false,//控制折叠面板状态
            inheritance_templateState: "",//继承状态
        })
        onMounted(() => {


        })
        // 切换布点设备类型分类
        const switchDeviceType = (type) => {
            recordData.switchDeviceTypeActive = type
            if (recordData.projectList.length != 1 && recordData.projectSlect == "") {
                ElMessage({
                    message: '请先选择项目',
                    type: 'error',
                    duration: 3 * 1000
                })
            }
            if (recordData.projectList.length == 1) {
                recordData.projectSlect = recordData.projectList[0].id
                let data = {
                    page: 0,
                    project_id: recordData.projectList[0].id
                }
                if (type == 1) {
                    // 获取控制器层级关系
                    controllerLoopRequest(data).then((res) => {
                        recordData.controllerLoop = res.data
                    });
                } else {
                    // 获取地址层级关系
                    areaBuildsRequest(data).then((res) => {
                        recordData.areaData = res.data
                    });
                }
            }
        }
        const switchDevice = (type) => {
            if (recordData.projectList.length != 1 && recordData.projectSlect == "") {
                // ElMessage({
                //     message: '请先选择项目',
                //     type: 'error',
                //     duration: 3 * 1000
                // })
            }
            let data = {
                page: 0,
                project_id: recordData.projectList[0].id
            }
            if (type == 1) {
                // 获取控制器层级关系
                controllerLoopRequest(data).then((res) => {
                    recordData.controllerLoop = res.data
                });
            } else {
                // 获取地址层级关系
                areaBuildsRequest(data).then((res) => {
                    recordData.areaData = res.data
                });
            }
        }

        // 选择器选择小区楼宇楼层
        const selectFun = (val, type) => {
            if (type == 1) {
                if (val) {
                    // 小区列表
                    let data = {
                        page: 0,
                        project_id: val
                    }
                    recordData.areaData = []
                    recordData.controllerLoop = []
                    recordData.areaSelect = ""
                    recordData.areaList = []
                    recordData.buildsSelect = ""
                    recordData.buildsList = []
                    recordData.floorsSlect = ""
                    recordData.floorsList = []
                    areaListRequest(data).then((res) => {
                        recordData.areaList = res.data.items
                    });
                    // 获取地址层级关系
                    areaBuildsRequest(data).then((res) => {
                        recordData.areaData = res.data
                    });
                    // 获取控制器层级关系
                    controllerLoopRequest(data).then((res) => {
                        recordData.controllerLoop = res.data
                    });

                    recordData.switchDeviceTypeActive = 1
                }
            } else if (type == 2) {

                // 楼宇列表
                let data = {
                    page: 0,
                    area_id: val
                }
                buildingListRequest(data).then((res) => {
                    recordData.buildsList = res.data.items
                });

            } else if (type == 3) {
                // 楼层列表
                let data = {
                    page: 0,
                    area_id: recordData.areaSelect,
                    build_id: val
                }
                floorsListRequest(data).then((res) => {
                    recordData.floorsList = res.data.items
                });
                // 
            } else if (type == 4) {
                recordData.loadingImg = true
                recordData.Url = config.baseUrl
                recordData.floorItem.left = 0
                recordData.floorItem.top = 0
                recordData.floorItem.width = 1094
                recordData.floorItem.height = 670
                recordData.inheritShow = false
                recordData.floorsList.forEach((item) => {
                    if (item.id == val) {
                        recordData.floorId = item.id
                        recordData.floorData = item
                        recordData.stationImgUrl = recordData.Url + item.path
                        recordData.inheritance_templateState = item.inheritance_template
                    }
                })
                getAssignList(recordData.floorId)
                if (recordData.stationImgUrl) {
                    recordData.loadingImg = false
                }
            }
        }
        // 获取布点列表
        const getAssignList = (floorId) => {
            let data = {
                floor_id: floorId
            }
            stationListRequest(data).then((res) => {
                recordData.floorItem.floorAssign = res.data
                // 鼠标悬浮显示文字
                recordData.floorItem.floorAssign.forEach((item) => {
                    item.description = "地址:" + item.device_address + ";" + "psn:" + item.psn + ";" + item.description
                })
            });

        }
        // 清空选择器状态
        const clrarSlect = (type) => {
            if (type == 1) {
                recordData.areaSelect = ""
                recordData.areaList = []
                recordData.buildsSelect = ""
                recordData.buildsList = []
                recordData.floorsSlect = ""
                recordData.floorsList = []
                recordData.stationImgUrl = ""
                recordData.switchDeviceTypeActive = 1
            } else if (type == 2) {
                recordData.buildsSelect = ""
                recordData.buildsList = []
                recordData.floorsSlect = ""
                recordData.floorsList = []

            }
            else if (type == 3) {
                recordData.floorsSlect = ""
                recordData.floorsList = []
            }
            else if (type == 4) { }
            recordData.stationImgUrl = ""
        }
        // 选择器提示
        const visibleArea = (val) => {
            if (recordData.projectList.length == 0) {
                ElMessage({
                    message: '请先创建项目',
                    type: 'info',
                    duration: 3 * 1000
                })
            } else if (recordData.projectList.length == 1) {

            } else {
                if (val == true && recordData.projectSlect == "") return ElMessage({
                    message: '请先选择项目',
                    type: 'info',
                    duration: 3 * 1000
                })
            }
        }
        const visibleBuild = (val) => {
            if (val == true && recordData.areaSelect == "") return ElMessage({
                message: '请先选择小区',
                type: 'info',
                duration: 3 * 1000
            })
        }
        const visibleFloor = (val) => {
            if (val == true && recordData.buildsSelect == "") return ElMessage({
                message: '请先选择楼宇',
                type: 'info',
                duration: 3 * 1000
            })
        }
        // 请求项目列表
        // 点击控制器层级关系获取设备列表
        const change = (loopId, controllerId) => {
            if (recordData.collapseCState == true) {
                recordData.loadingDevice = true
                recordData.loopId = loopId,
                    recordData.controllerId = controllerId
                let request = {
                    controller_num: controllerId,
                    loop_num: loopId,
                    is_assign: 0,
                    page: 0
                }
                deviceListRequest(request).then((res) => {
                    recordData.deviceList = res.data.items.sort((a, b) => {
                        if (a.loop_num === b.loop_num) return (a.addr_num - b.addr_num)
                        else return (a.id - b.id)
                    })
                    if (recordData.deviceList.length == 0) {
                        ElMessage({
                            message: '该回路下暂无设备',
                            type: 'info',
                            duration: 3 * 1000
                        })
                    }
                    if (recordData.deviceList) {
                        recordData.loadingDevice = false
                    }
                });
            } else {

            }

        }
        // 点击地址层级关系获取设备列表
        const getDeviceList = (val) => {
            if (val.children && recordData.collapseState == false) {

            } else if (recordData.collapseState == true) {
                if (val.children) {

                } else {
                    recordData.huiId = val
                    let request = {
                        is_assign: 0,
                        page: 0
                    }
                    recordData.loadingDevice = true
                    if (val.level == "floor") {
                        request.floor = val.label
                        recordData.floorName = val.label
                    } else if (val.level == "district") {
                        request.district = val.label
                        recordData.districtName = val.label
                    } else if (val.level == "room") {
                        request.room = val.label
                        recordData.roomName = val.label
                        console.log(recordData.deviceList);
                        console.log(recordData.roomName.split('-')[0]);
                    }
                    deviceListRequest(request).then((res) => {
                        recordData.deviceList = res.data.items.sort((a, b) => {
                            if (a.loop_num === b.loop_num) return (a.addr_num - b.addr_num)
                            else return (a.id - b.id)
                        })
                        if (recordData.deviceList.length == 0) {
                            ElMessage({
                                message: '该楼层下暂无设备',
                                type: 'info',
                                duration: 3 * 1000
                            })
                            recordData.loadingDevice = false
                        }
                        if (recordData.deviceList[0].district == null) {
                            recordData.floorordistrict = false//楼层
                        } else {
                            recordData.floorordistrict = true//分区
                            if (recordData.deviceList[0].room == null) {
                                recordData.districtroom = false//房间
                            } else {
                                recordData.districtroom = true//房间
                            }
                        }
                        if (recordData.deviceList) {
                            recordData.loadingDevice = false
                        }
                    });
                }

            }
        }
        // 获取折叠面板状态
        const getCLd = (val) => {
            if (val != '') {
                recordData.collapseCState = true
            } else {
                recordData.collapseCState = false
            }
        }
        // 获取折叠面板状态
        const getout = (val) => {
            if (val != '') {
                recordData.collapseState = true
            } else {
                recordData.collapseState = false
            }
        }
        // 点击设备列表布点
        const station = (id, path, connum, loopnum, addrnum, description, psn, X, Y, device_type_name, current, deviceDescription) => {
            // 判断是否选择图纸
            if (recordData.floorsSlect == "") return ElMessage({
                message: '请选择图纸',
                type: 'error',
                duration: 3 * 1000
            })
            let assItem = _.cloneDeep(recordData.assignItem)
            recordData.clickDeviceId = id
            recordData.lastAssign.loop = loopnum
            recordData.lastAssign.addr = addrnum
            if (psn) {
                assItem.description = `地址: ${connum}-${loopnum}-${addrnum}; psn: ${psn}; ${description}`
            } else {
                assItem.description = `地址: ${connum}-${loopnum}-${addrnum}; ${description}`
            }
            assItem.path = path
            assItem.coordinate_X = X - recordData.floorItem.lastLeft
            assItem.coordinate_Y = Y - recordData.floorItem.lastTop
            assItem.rate = 0
            assItem.width = 30
            assItem.height = 30
            assItem.angle = 0
            assItem.device_id = id
            assItem.device_type_name = device_type_name
            assItem.device_address = current
            assItem.deviceDescription = deviceDescription
            recordData.floorItem.floorAssign.push(assItem)
            recordData.createUpdateDevcieIds.push(id)
            recordData.deleteData.push(id)
            recordData.selectedDeviceIds.push(id)
            // recordData.selectedDeviceNames.push()

        }
        // 双击布点
        const dbClickAddDevice = (e) => {
            if (!recordData.lastAssign.loop | !recordData.lastAssign.addr) return ElMessage({
                message: '请先在左侧单击选择一个设备作为双击布点起始点位',
                type: 'error',
                duration: 3 * 1000
            })
            let stationBox = document.getElementById('stationBox')
            let demandBox = document.getElementById('demandBox')
            const cx = e.x - proxy.$refs.assingPicRef.offsetLeft
            const cy = e.y - stationBox.offsetTop - demandBox.offsetHeight
            if (!recordData.selectControllerNum) {
                recordData.selectControllerNum = recordData.controllerLoop[0].id
            }
            // 楼宇地址
            if (recordData.switchDeviceTypeActive == 2) {
                let addDevices = []
                if (recordData.floorordistrict == true) {
                    if (recordData.districtroom == true) {
                        addDevices = recordData.deviceList.filter(item => {
                            return item.room.split('-')[0] === recordData.roomName.split('-')[0]
                                & item.loop_num == recordData.lastAssign.loop
                                & item.addr_num > recordData.lastAssign.addr
                        })
                    } else {
                        addDevices = recordData.deviceList.filter(item => {
                            return item.district.split('-')[0] === recordData.districtName.split('-')[0]
                                & item.loop_num == recordData.lastAssign.loop
                                & item.addr_num > recordData.lastAssign.addr
                        })
                    }

                } else {
                    addDevices = recordData.deviceList.filter(item => {
                        return item.floor.split('-')[0] === recordData.floorName.split('-')[0]
                            & item.loop_num == recordData.lastAssign.loop
                            & item.addr_num > recordData.lastAssign.addr
                    })
                }
                // else {

                // }
                if (addDevices.length === 0) return ElMessage({
                    message: '当前选择起点范围内设备已布完',
                    type: 'error',
                    duration: 3 * 1000
                })
                const addDevice = addDevices[0]
                station(addDevice.id, addDevice.path, addDevice.controller_num, addDevice.loop_num, addDevice.addr_num, addDevice.description, addDevice.psn, cx, cy, addDevice.device_type_name, addDevice.current, addDevice.description)
            }
            // 控制器 
            else {
                const addDevices = recordData.deviceList.filter(item => {
                    return (item.loop_num == recordData.lastAssign.loop
                        & item.addr_num > recordData.lastAssign.addr)
                })

                if (addDevices.length == 0) return ElMessage({
                    message: '当前选择起点范围内设备已布完',
                    type: 'error',
                    duration: 3 * 1000
                })

                const addDevice = addDevices[0]
                station(addDevice.id, addDevice.path, addDevice.controller_num, addDevice.loop_num, addDevice.addr_num, addDevice.description, addDevice.psn, cx, cy, addDevice.device_id, addDevice.current)
            }
        }
        // 点击旋转
        const rotateImg = (val) => {
            const like = document.getElementById(val.id);
            val.angle += 90
            if (val.angle >= 360) {
                val.angle = 0
            }
        }
        // 设备列表滚动事件
        const load = () => {

        }
        // 图纸移动
        const floorAssignMove = (id, e) => {
            //   let odiv = e.target // 获取目标元素
            // 算出鼠标相对元素的位置
            let disX = e.clientX
            let disY = e.clientY
            let top = 0
            let left = 0
            document.onmousemove = (e) => {
                // 鼠标按下并移动的事件
                // 每次移动，计算鼠标的X,Y相对初始位置的移动量，加上上个鼠标事件已经移动的量
                // 因为img居中对齐，所以还要减去目标元素距离body的偏移量
                left = e.clientX - disX
                top = e.clientY - disY
                if (Math.abs(left) > 10 | Math.abs(top) > 10) {
                    recordData.floorItem.top = top + recordData.floorItem.lastTop
                    recordData.floorItem.left = left + recordData.floorItem.lastLeft
                }
            }
            document.onmouseup = (e) => {
                // 记录上个鼠标移动事件已经移动的量
                recordData.floorItem.lastTop = recordData.floorItem.top
                recordData.floorItem.lastLeft = recordData.floorItem.left
                document.onmousemove = null
                document.onmouseup = null
            }
        }
        // 图纸缩放
        const watchMouseWheel = (e) => {
            let zoom = 1.2
            let x = e.offsetX
            let y = e.offsetY
            if (e.wheelDelta > 0) {
                if (recordData.floorItem.floorAssign.length > 0) {
                    if (recordData.floorItem.floorAssign[0].width >= 30) {
                        return
                    }
                }
                recordData.floorItem.width *= zoom
                recordData.floorItem.height *= zoom
                recordData.floorItem.floorAssign.forEach(item => {
                    item.coordinate_X *= zoom
                    item.coordinate_Y *= zoom
                    item.width *= zoom
                    item.height *= zoom
                    item.lastTop *= zoom
                    item.lastLeft *= zoom
                })
                // 以鼠标为所在位置中心点进行放大，
                recordData.floorItem.top -= y * (zoom - 1)
                recordData.floorItem.left -= x * (zoom - 1)
                recordData.floorItem.lastTop = recordData.floorItem.top
                recordData.floorItem.lastLeft = recordData.floorItem.left
            }
            if (e.wheelDelta < 0) {
                if (recordData.floorItem.width <= 1094) {
                    return
                }
                recordData.floorItem.width /= zoom
                recordData.floorItem.height /= zoom
                recordData.floorItem.floorAssign.forEach(item => {
                    item.coordinate_X /= zoom
                    item.coordinate_Y /= zoom
                    item.width /= zoom
                    item.height /= zoom
                    item.lastTop /= zoom
                    item.lastLeft /= zoom
                })
                // 以鼠标为所在位置中心点进行缩小
                recordData.floorItem.top += y - y / zoom
                recordData.floorItem.left += x - x / zoom
                recordData.floorItem.lastTop = recordData.floorItem.top
                recordData.floorItem.lastLeft = recordData.floorItem.left
            }
        }
        // 设备移动
        const deviceMove = (id, e) => {
            // 算出鼠标相对元素的位置
            let disX = e.clientX
            let disY = e.clientY
            let top = 0
            let left = 0
            let dindex = recordData.floorItem.floorAssign.findIndex(item => {
                return item.device_id === id
            })
            let assignDevice = recordData.floorItem.floorAssign[dindex]

            document.onmousemove = (e) => {
                left = e.clientX - disX
                top = e.clientY - disY
                if (Math.abs(left) > 0.5 | Math.abs(top) > 0.5) {
                    disX += left
                    disY += top
                    assignDevice.coordinate_X = left + assignDevice.coordinate_X
                    assignDevice.coordinate_Y = top + assignDevice.coordinate_Y
                }
            }
            document.onmouseup = (e) => {
                document.onmousemove = null
                document.onmouseup = null
            }
            if (!recordData.createUpdateDevcieIds.includes(id)) {
                recordData.createUpdateDevcieIds.push(id)
            }
        }
        // 右键点击设备显示设备操作删除弹窗
        const showDeviceDelete = (val, value) => {
            // console.log(val,value);
            // console.log(recordData.floorItem.floorAssign);
            recordData.floorItem.floorAssign.forEach((item) => {
                if (value.device_id == item.device_id) {
                    recordData.deviceDescription = item.description.split(";")[2]
                }
            })
            if (recordData.deviceList) {
                recordData.deviceList.forEach((item) => {
                    if (item.id == val) {
                        recordData.deviceType = item.device_type_name
                        recordData.deviceCurrent = item.current
                    }
                })
            }
            recordData.rightClickId = val
            recordData.popupShow = true
        }
        // 删除设备
        const deleteDevice = (id) => {
            const aindex = recordData.floorItem.floorAssign.findIndex(item => {
                return item.device_id === id
            })
            const device = recordData.floorItem.floorAssign[aindex]
            const sdindex = recordData.selectedDeviceIds.findIndex(item => {
                return item === id
            })
            const cudindex = recordData.createUpdateDevcieIds.findIndex(item => {
                return item === id
            })
            const deleteIndex = recordData.deleteData.findIndex(item => {
                return item === id
            })
            recordData.selectedDeviceIds.splice(sdindex, 1)
            // 点位已保存在数据库中
            if (device.id !== 0) {
                recordData.loadingImg = true
                deleteStationRequest(device.id).then((res) => {
                    if (res.ok) {
                        ElMessage({
                            message: '点位删除成功',
                            type: 'success',
                            duration: 3 * 1000
                        })
                        if (recordData.switchDeviceTypeActive == 1) {
                            change(device.device_address.split('-')[1], device.device_address.split('-')[0])
                        } else if (recordData.switchDeviceTypeActive == 2) {
                            getDeviceList(recordData.huiId)
                        }
                        recordData.loadingImg = false
                    }
                });
            } else {
                const addDevices = recordData.deleteData.filter(item => {
                    return item === device.device_id
                })
                if (addDevices.length == 0) {
                    deletedevice_idStationRequest(device.device_id).then((res) => {
                        if (res.ok) {
                            ElMessage({
                                message: '点位删除成功',
                                type: 'success',
                                duration: 3 * 1000
                            })
                            if (recordData.switchDeviceTypeActive == 1) {
                                change(device.device_address.split('-')[1], device.device_address.split('-')[0])
                            } else if (recordData.switchDeviceTypeActive == 2) {
                                getDeviceList(recordData.huiId)
                            }
                        }
                    });
                } else {
                }
            }
            recordData.createUpdateDevcieIds.splice(cudindex, 1)
            recordData.floorItem.floorAssign.splice(aindex, 1)
            recordData.deleteData.splice(deleteIndex, 1)
            recordData.rightClickId = ""
            recordData.clickDeviceId = 0
            recordData.lastAssign.loop = 0
            recordData.lastAssign.addr = 0
        }
        // 修改设备
        const revampDevice = (type, item) => {
            let request = {
                controller_num: item.device_address.split('-')[0],
                loop_num: item.device_address.split('-')[1],
                addr_num: item.device_address.split('-')[2],
            }
            deviceListRequest(request).then((res) => {
                recordData.popupData = res.data.items[0]
            });
            recordData.popupType = type
        }
        // 弹窗功能
        const sure = (popupData, operationType, selectData) => {
            revampDeviceFun(popupData)
        }
        // 修改设备
        const revampDeviceFun = (popupData) => {
            revampDevicesRequest(popupData).then((res) => {
                if (res.ok) {
                    ElMessage({
                        message: '修改成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    recordData.floorItem.floorAssign.forEach((item) => {
                        if (item.device_id == popupData.device_id) {
                            if (popupData.psn != "") {
                                item.description = "地址:" + item.device_address + ";" + "psn:" + popupData.psn + ";" + popupData.description
                            } else {
                                item.description = "地址:" + item.device_address + ";" + "psn:" + item.psn + ";" + popupData.description
                            }

                        }
                    })
                    recordData.popupShow = false
                    recordData.popupType = 0
                }
            });
        }
        // 保存
        const openSavePopup = () => {
            if (recordData.stationImgUrl) {
                recordData.savePopupShow = true
                if (recordData.inheritance_templateState == 1) {
                    recordData.inherit = true
                } else {
                    recordData.inherit = false
                }
            } else {
                ElMessage({
                    message: '请选择图纸',
                    type: 'info',
                    duration: 3 * 1000
                })
            }

        }
        const offsavePopup = () => {
            recordData.savePopupShow = false
        }
        // 保存
        const saveAssign = () => {
            recordData.loading = true
            let assigns = []
            if (recordData.floorsSlect == "") return ElMessage({
                message: '请先选择图纸',
                type: 'info',
                duration: 3 * 1000
            })
            let currentFloorItem = _.cloneDeep(recordData.floorItem)
            // let currentFloorItem = recordData.floorItem
            let azoom = 1094 / currentFloorItem.width
            // 统一按照第一个布点的缩放比,如果未进行过azoom换算
            let rate = 0
            if (currentFloorItem.floorAssign.length > 0) {
                rate = currentFloorItem.floorAssign[0].width / currentFloorItem.width
            }
            // 从所有的布点列表中，筛选出新增和修改的列表
            const saveAssignDevices = currentFloorItem.floorAssign.filter(item => {
                return recordData.createUpdateDevcieIds.includes(item.device_id)
            })
            saveAssignDevices.forEach(item => {
                // axios需要的参数
                let device = {}
                // 还原以1440 为基础宽度布点图对应的设备位置及大小
                // 统一按照第一个布点的缩放比,如果未进行过azoom换算
                if (rate === 0) device['rate'] = item.width / currentFloorItem.width
                else device['rate'] = rate
                // 兼容旧系统中rate计算方法，防止图标过度缩小，看不到任何图标
                if (device.rate * 1094 < 3) {
                    device.rate = 3 / 1094
                }
                device.coordinate_X = item.coordinate_X * azoom
                device.coordinate_Y = item.coordinate_Y * azoom
                device.device_id = item.device_id
                device.width = 1094 * device.rate
                device.height = 1094 * device.rate
                if (item.angle) {
                    device.angle = item.angle
                } else {
                    device.angle = 0
                }
                assigns.push(device)
            })
            if (assigns.length == 0) {
                recordData.loading = false
                return ElMessage({
                    message: '暂无新增或修改信息',
                    type: 'info',
                    duration: 3 * 1000
                })
            } else {
                let data = {
                    assign_info: assigns,
                    floor_id: recordData.floorId,
                    inheritance_template: recordData.switchInheritState
                }
                addStationRequest(data).then((res) => {
                    if (res.ok) {
                        ElMessage({
                            message: '保存布点数据成功',
                            type: 'success',
                            duration: 3 * 1000
                        })
                        // 布点成功后清除页面信息
                        recordData.savePopupShow = false
                        recordData.inheritShow = false
                        recordData.Newrate = []
                        recordData.floorItem.floorAssign = []
                        recordData.floorItem.path = ''
                        recordData.floorItem.left = 0
                        recordData.floorItem.top = 0
                        recordData.floorItem.width = 1094
                        recordData.floorItem.height = 670
                        recordData.stationImgUrl = ""
                        recordData.floorId = ""
                        recordData.switchInheritState = 0
                        // this.getLconList()
                        recordData.createUpdateDevcieIds = []
                        recordData.lastAssign.loop = 0
                        recordData.lastAssign.addr = 0
                        recordData.areaSelect = ""
                        recordData.buildsSelect = ""
                        recordData.floorsSlect = ""
                        recordData.inherit = false
                        recordData.loading = false
                        if (recordData.switchDeviceTypeActive == 1) {
                            change(recordData.loopId, recordData.controllerId)
                        } else if (recordData.switchDeviceTypeActive == 2) {
                            getDeviceList(recordData.huiId)
                        }

                    }
                });
            }
        }
        // 自动保存
        const voluntarilySave = () => {
            let assigns = []
            if (recordData.floorsSlect == "") {
                return ElMessage({
                    message: '请先选择图纸',
                    type: 'info',
                    duration: 3 * 1000
                })
            }
            let currentFloorItem = recordData.floorItem
            let azoom = 1094 / currentFloorItem.width
            // 统一按照第一个布点的缩放比,如果未进行过azoom换算
            let rate = 0
            if (currentFloorItem.floorAssign.length > 0) {
                rate = currentFloorItem.floorAssign[0].width / currentFloorItem.width
            }
            // 从所有的布点列表中，筛选出新增和修改的列表
            const saveAssignDevices = currentFloorItem.floorAssign.filter(item => {
                return recordData.createUpdateDevcieIds.includes(item.device_id)
            })
            saveAssignDevices.forEach(item => {
                // axios需要的参数
                let device = {}
                // 还原以1440 为基础宽度布点图对应的设备位置及大小
                // 统一按照第一个布点的缩放比,如果未进行过azoom换算
                if (rate === 0) device['rate'] = item.width / 1094
                else device['rate'] = rate
                // 兼容旧系统中rate计算方法，防止图标过度缩小，看不到任何图标
                if (device.rate * 1094 < 3) {
                    device.rate = 3 / 1094
                }
                device.coordinate_X = item.coordinate_X * azoom
                device.coordinate_Y = item.coordinate_Y * azoom
                device.device_id = item.device_id

                device.width = item.width * azoom
                device.height = item.height * azoom
                device.angle = 0
                assigns.push(device)
            })
            if (assigns.length == 0) {
                return ElMessage({
                    message: '暂无新增或修改信息',
                    type: 'info',
                    duration: 3 * 1000
                })
            } else {
                let data = {
                    assign_info: assigns,
                    floor_id: recordData.floorId,
                }
                addStationRequest(data).then((res) => {
                    if (res.ok) {
                        ElMessage({
                            message: '保存布点数据成功',
                            type: 'success',
                            duration: 3 * 1000
                        })
                        recordData.createUpdateDevcieIds = []
                        recordData.deleteData = []
                    }
                });
            }
        }
        // 是否作为继承模板
        const inherit = () => {
            recordData.inherit != recordData.inherit
            if (recordData.inherit == true) {
                recordData.switchInheritState = 1
            } else {
                recordData.switchInheritState = 0
            }
        }
        // 生成SVG
        const saveSvg = () => {

            if (recordData.createUpdateDevcieIds.length != 0) {
                ElMessage({
                    message: '请先保存布点信息',
                    type: 'error',
                    duration: 3 * 1000
                })
            } else {
                if (recordData.floorId == "") {
                    ElMessage({
                        message: '请选选择图纸布点',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else {
                    recordData.loading = true
                    let data = {
                        floor_id: recordData.floorId
                    }
                    saveSVG(data).then((res) => {
                        if (res.ok) {
                            ElMessage({
                                message: '合成成功',
                                type: 'success',
                                duration: 3 * 1000
                            })
                            recordData.loading = false
                        }
                    });
                }

            }

        }
        // 获取继承列表
        const showInherit = () => {
            if (recordData.stationImgUrl) {
                recordData.inheritFloorlistLoading = true
                recordData.inheritShow = !recordData.inheritShow
                let data = {
                    page: 0,
                    area_id: recordData.areaSelect,
                    inheritance_template: 1
                }
                floorsListRequest(data).then((res) => {
                    recordData.inheritList = res.data.items

                });
                recordData.inheritFloorlistLoading = false

            } else {
                ElMessage({
                    message: '请选择图纸',
                    type: 'info',
                    duration: 3 * 1000
                })
            }
        }
        const openPopup = (val) => {
            recordData.dialogShow = true
            recordData.father_floor_id = val.id
        }
        // 关闭继承弹窗
        const offPopup = () => {
            recordData.popupType = 0
            recordData.dialogShow = false
            recordData.start_controller_num = ""
            recordData.start_loop_num = ""
            recordData.start_addr_num = ""
            recordData.end_controller_num = ""
            recordData.end_loop_num = ""
            recordData.end_addr_num = ""
        }
        // 继承
        const inheritFun = () => {
            recordData.loading = true
            let data = {
                father_floor_id: recordData.father_floor_id,
                son_floor_id: recordData.floorId,
                start_controller_num: Number(recordData.start_controller_num),
                start_loop_num: Number(recordData.start_loop_num),
                start_addr_num: Number(recordData.start_addr_num),
                end_controller_num: Number(recordData.end_controller_num),
                end_loop_num: Number(recordData.end_loop_num),
                end_addr_num: Number(recordData.end_addr_num),
            }
            inheritStationRequest(data).then((res) => {
                if (res.ok == true) {
                    ElMessage({
                        message: '继承完成',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    recordData.floorItem.left = 0
                    recordData.floorItem.top = 0
                    recordData.floorItem.width = 1094
                    recordData.floorItem.height = 670
                    recordData.dialogShow = false
                    recordData.floorItem.floorAssign = res.data
                    recordData.loading = false
                    recordData.inheritShow = false
                } else {
                    ElMessage({
                        message: res.msg,
                        type: 'error',
                        duration: 3 * 1000
                    })
                }
            });
        }
        watch(() => recordData.dialogShow, (newvalue, oldvalue) => {
            if (newvalue == false) {
                recordData.start_controller_num = ""
                recordData.start_loop_num = ""
                recordData.start_addr_num = ""
                recordData.end_controller_num = ""
                recordData.end_loop_num = ""
                recordData.end_addr_num = ""
            }
        })
        watch(() => recordData.projectSlect, (newvalue, oldvalue) => {
            if (newvalue != oldvalue) {
                recordData.areaSelect = ""
                recordData.areaList = []
                recordData.buildsSelect = ""
                recordData.buildsList = []
                recordData.floorsSlect = ""
                recordData.floorsList = []
                recordData.stationImgUrl = ""
            }
        })
        watch(() => recordData.areaSelect, (newvalue, oldvalue) => {
            if (newvalue != oldvalue) {
                recordData.buildsSelect = ""
                recordData.buildsList = []
                recordData.floorsSlect = ""
                recordData.floorsList = []
                recordData.stationImgUrl = ""
            }
        })
        watch(() => recordData.buildsSelect, (newvalue, oldvalue) => {
            if (newvalue != oldvalue) {
                recordData.floorsSlect = ""
                recordData.floorsList = []
                recordData.stationImgUrl = ""
            }
        })
        watch(() => recordData.stationImgUrl, (newvalue, oldvalue) => {
            if (newvalue == "") {
                recordData.floorItem.floorAssign = []
                recordData.floorItem.path = ''
                recordData.floorItem.left = 0
                recordData.floorItem.top = 0
                recordData.floorItem.width = 1094
                recordData.floorItem.height = 670
                recordData.stationImgUrl = ""
                recordData.floorId = ""
                recordData.switchInheritState = 0
                recordData.createUpdateDevcieIds = []
                recordData.lastAssign.loop = 0
                recordData.lastAssign.addr = 0
            }
        })
        // 监听布点数组  每布五个点 自动保存
        watch(() => [recordData.deleteData], (newvalue, oldvalue) => {
            if (newvalue[0].length != 0) {
                let num = newvalue[0].length / 30
                if (Number.isInteger(num) == true) {
                    voluntarilySave()
                }
            }
        }, {
            deep: true
        })
        watch(props, (newProps) => {
            if (newProps.stationState == true) {
                recordData.floorItem = {
                    id: 0,
                    top: 0,
                    left: 0,
                    width: 1094,
                    height: 670,
                    path: '',
                    lastTop: 0,
                    lastLeft: 0,
                    // 该层楼的布信息
                    floorAssign: []
                },
                    recordData.inheritList = []
                recordData.inheritShow = ""
                recordData.areaData = []
                recordData.controllerLoop = []
                recordData.projectSlect = ""
                recordData.areaSelect = ""
                recordData.buildsSelect = ""
                recordData.floorsSlect = ""
                recordData.stationImgUrl = ""
                projectListRequest(recordData.Request).then((res) => {
                    recordData.projectList = res.data.items
                    if (recordData.projectList.length == 1) {
                        // 控制项目选择器是否可见
                        recordData.onlyObject = false
                        selectFun(recordData.projectList[0].id, 1)
                        switchDeviceType(1)
                    } else {
                        recordData.onlyObject = true
                    }
                });
            }
        }
        );
        return {
            recordData,
            switchDeviceType,
            switchDevice,
            selectFun,
            clrarSlect,
            change,
            load,
            station,
            dbClickAddDevice,
            floorAssignMove,
            watchMouseWheel,
            getDeviceList,
            getout,
            getCLd,
            deviceMove,
            showDeviceDelete,
            openSavePopup,
            saveAssign,
            inherit,
            saveSvg,
            voluntarilySave,
            getAssignList,
            deleteDevice,
            revampDevice,
            revampDeviceFun,
            offsavePopup,
            showInherit,
            openPopup,
            offPopup,
            inheritFun,
            sure,
            visibleArea,
            visibleBuild,
            visibleFloor,
            rotateImg
        };
    },
});
</script>
<style  scoped lang="less">
.stationBox {
    display: flex;
    flex-direction: row;
    background-color: #F2F6FC;
    // position: absolute;
    // top: 178px;
    // left: 0px;
    width: 1760px;
    height: 884px;
    margin-left: 80px;
    margin-top: 18px;
    margin-bottom: 18px;
    z-index: 10;

    // 左侧
    .stationMsg {
        width: 300px;
        height: 884px;
        background: #ffffff;
        // margin-left: 80px;

        .typeBox {
            width: 300px;
            height: 80px;
            font-size: 20px;
            display: flex;

            .typeName {
                width: 150px;
                height: 80px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;

                .switchDeviceImg {
                    width: 15px;
                    height: 15px;
                    margin-left: 10px;
                }
            }

            .active {
                color: #4A5CD5;
                font-weight: 600;
            }
        }

        .deviceBox {
            width: 300px;
            height: 804px;
            border-top: 2px solid #a3a4ab;

            .noneText {
                width: 300px;
                height: 50px;
                font-size: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-top: 300px;
                color: #a3a4ab;
            }

            .deviceList {
                width: 300px;
                height: 804px;
                overflow-y: auto;
                overflow-x: hidden;

                // 控制器名称 小区名称
                .controllerName,
                .areaName {
                    padding-left: 10px;
                    font-size: 20px;
                }

                //回路名称 楼宇名称
                .loopName,
                .buildsName {
                    padding-left: 20px;
                    font-size: 20px;
                }

                .floorsName {
                    padding-left: 30px;
                    font-size: 20px;
                }

                ul {
                    height: 500px;
                    list-style: none;
                    font-size: 20px;
                    overflow-y: auto;
                    overflow-x: hidden;

                    li {
                        // width: 100%-30px;
                        overflow: hidden; //超出的文本隐藏
                        text-overflow: ellipsis; //溢出用省略号显示
                        white-space: nowrap; //溢出不换行
                        height: 40px;
                        font-size: 12px;
                        border-bottom: 1px solid #3b4e61;
                        cursor: pointer;
                        margin-left: 30px;
                        font-size: 20px;
                    }
                }

                ul::-webkit-scrollbar {
                    width: 5px;
                    /*高宽分别对应横竖滚动条的尺寸*/
                    height: 10px;
                    // display: none;
                    border-radius: 5px;
                }

                ul::-webkit-scrollbar-thumb {
                    border-radius: 5px;
                    background-color: rgb(188, 180, 180);
                }

                ul::-webkit-scrollbar-track {
                    background: #3b4e61;
                    border-radius: 2px;
                }
            }

            .deviceList::-webkit-scrollbar {
                width: 5px;
                /*高宽分别对应横竖滚动条的尺寸*/
                height: 10px;
                display: none;
                border-radius: 5px;
            }

            .deviceList::-webkit-scrollbar-thumb {
                border-radius: 5px;
                background-color: rgb(255, 250, 250);
            }

            .deviceList::-webkit-scrollbar-track {
                background: #3b4e61;
                border-radius: 2px;
            }

            .inheritFloorlistBox {
                width: 300px;
                height: 804px;
                overflow-y: auto;
                overflow-x: hidden;
                background-color: #4A5CD5;

                .inheritFloorBox {
                    width: 280px;
                    height: 180px;
                    background-color: #ffffff;
                    margin-left: 10px;
                    margin-top: 10px;
                    cursor: pointer;

                    .inheritFloorImg {
                        width: 280px;
                        height: 150px;

                        .inheritImg {
                            width: 280px;
                            height: 150px;
                        }
                    }

                    .inheritFloorText {
                        width: 280px;
                        height: 30px;
                        font-size: 20px;
                        overflow: hidden; //超出的文本隐藏
                        text-overflow: ellipsis; //溢出用省略号显示
                        white-space: nowrap; //溢出不换行
                    }
                }
            }

            .inheritFloorlistBox::-webkit-scrollbar {
                width: 5px;
                /*高宽分别对应横竖滚动条的尺寸*/
                height: 10px;
                display: none;
                border-radius: 5px;
            }

            .inheritFloorlistBox::-webkit-scrollbar-thumb {
                border-radius: 5px;
                background-color: rgb(255, 250, 250);
            }

            .inheritFloorlistBox::-webkit-scrollbar-track {
                background: #3b4e61;
                border-radius: 2px;
            }
        }

        .inheritBox {
            width: 300px;
            height: 80px;
            font-size: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
    }

    .station {
        width: 1440px;
        height: 884px;
        background: #ffffff;
        margin-left: 20px;

        .demandBox {
            width: 1440px;
            height: 82px;
            border-bottom: 2px solid #a3a4ab;
            display: flex;
            align-items: center;

            .selectBox {
                width: 260px;
                height: 44px;
                margin-left: 5px;
            }

            .btnBox,
            .saveSvgBtn {
                width: 100px;
                height: 44px;
                background: #4a5cd5;
                border-radius: 2px;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 22px;
                font-weight: 500;
                color: #ffffff;
                letter-spacing: 1.1px;
                cursor: pointer;
                margin-left: 5px;
            }

            .saveSvgBtn {
                width: 150px;
                border: none;
            }
        }

        .stationImgBox {
            width: 1440px;
            height: 804px;
            box-sizing: border-box;
            overflow: hidden;

            // background-color: #4A5CD5;
            .noneBox {
                width: 1440px;
                height: 804px;
                display: flex;
                align-items: center;
                justify-content: center;
                // background-color: #4A5CD5;

                .noneImg {
                    width: 1440px;
                    height: 804px;
                }
            }

            .stationImgBigBox {
                position: relative;

                .assign-device {
                    position: absolute;

                    :deep(.el-image) {
                        float: left;
                    }

                }

                .rightContex {
                    position: absolute;
                    z-index: 500;
                    width: 70px;
                    height: 100px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;

                    :deep(.el-button) {
                        height: 30px;
                        margin-top: 2px;
                        font-size: 15px;
                        border: none;
                        background-color: #a3a4ab;
                    }

                    :deep(.el-button):hover {

                        background-color: #4a5cd5;
                    }

                    .btnBox {}
                }
            }
        }
    }

    // 选择器
    :deep(.el-select) {
        width: 250px;
        height: 44px;
        color: #4A5CD5;
    }

    :deep(.el-input__wrapper) {
        width: 250px;
        height: 44px;
        color: #4A5CD5;
        background-color: #F7F8FC;
        border: none !important;
        box-shadow: none !important;
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

    .loginBox {
        width: 1000px;
        height: 430px;
        font-size: 22px;
        font-weight: 500;
        color: #000000;
        letter-spacing: 1.1px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;

        :deep(.el-input) {
            width: 320px;
            height: 44px;
            background: #f7f8fc;
        }

        :deep(.el-input__wrapper) {
            width: 320px;
            height: 44px;
            background: #f7f8fc;
            border: none !important;
            box-shadow: none !important;
        }

        .account {
            width: 500px;
            // height: 44px;

            :deep(.el-checkbox__label) {
                font-size: 20px;
            }
        }

    }

    .inheritFunBox {
        width: 1000px;
        height: 430px;
        font-size: 20px;
        font-weight: 500;
        color: #000000;
        letter-spacing: 1.1px;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;

        .leftBox,
        .rightBox {
            width: 500px;
            height: 430px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;

            .account {
                width: 400px;
                height: 50px;
                display: flex;
                justify-content: space-between;
                margin-top: 10px;

                .textBox {
                    width: 150px;
                    height: 50px;
                    display: flex;
                    align-items: center;
                    justify-items: right;
                }

                .inputBox {
                    width: 240px;
                    height: 50px;
                }
            }
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
    }


}
</style>