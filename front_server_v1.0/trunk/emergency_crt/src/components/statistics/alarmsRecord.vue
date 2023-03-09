<!-- 统计查询表格 -->
<template>
    <!-- 报警记录 -->
    <div class="recordBox" v-if="recordData.propsRecordType == 1">
        <div class="demandBox">
            <div class="selectBox">
                <div class="switchBtnBox">
                    <div class="switchBtn" :class="recordData.switchBtnActive == 0 ? 'active' : 'unactive'"
                        @click="switchRecord(0, 1)">全部</div>
                        <div class="switchBtn" :class="recordData.switchBtnActive == 1 ? 'active' : 'unactive'"
                        @click="switchRecord(1, 1)">火警</div>
                    <div class="switchBtn" :class="recordData.switchBtnActive == 2 ? 'active' : 'unactive'"
                        @click="switchRecord(2, 1)">启动</div>
                    <div class="switchBtn" :class="recordData.switchBtnActive == 4 ? 'active' : 'unactive'"
                        @click="switchRecord(4, 1)">故障</div>
                </div>
                <div class="dateBox">
                    <div class="dateText">日期 &nbsp;</div>
                    <div class="dateSelect">
                        <el-date-picker v-model="recordData.value1" type="daterange" unlink-panels format="YYYY-MM-DD"
                            value-format="YYYY-MM-DD" range-separator="至" start-placeholder="开始日期"
                            end-placeholder="结束日期" :shortcuts="recordData.shortcuts" @change="changeDate" />
                    </div>
                </div>
            </div>
            <div class="btnBox">
                <div class="more" @click="switchMoreSelectBox">更多筛选</div>
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
                <el-table-column prop="occurred_alarm_time" label="报警时间" align="center" min-width="120%"  />
                <el-table-column prop="alarm_current" label="地址号" align="center" />
                <el-table-column prop="device_type_name" label="设备类型" align="center" :show-overflow-tooltip="true" min-width="120%" />
                <el-table-column prop="alarm_type_name" label="报警类型" align="center" :show-overflow-tooltip="true"  min-width="60%" />
                <el-table-column prop="alarm_status" label="报警状态" align="center" :show-overflow-tooltip="true" min-width="60%" 
                    :formatter="formatState" />

                <el-table-column prop="description" label="描述" align="center" :show-overflow-tooltip="true" min-width="200%" />
                <el-table-column prop="area_name" label="小区" align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="build_name" label="楼宇" align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="floor_name" label="楼层" align="center" :show-overflow-tooltip="true" />
                <el-table-column label="报警方式" align="center" :show-overflow-tooltip="true" min-width="60%" >
                    <template #default="scope">
                        <div class="deviceState">
                            <template v-if="scope.row.alarm_type == 1">
                                模拟报警
                            </template>
                            <template v-else>
                                真实报警
                            </template>
                        </div>
                    </template>
                </el-table-column>
            </el-table>
            <!-- 更多筛选 -->
            <div class="moreSelectBox" v-show="recordData.moreSelect">
                <div class="testMsgBox">
                    <div class="testTextBox">操作员</div>
                    <div class="testSelectBox">
                        <el-select v-model="recordData.userSelect" clearable placeholder="请选择"
                            @visible-change="visibleUserList" @change="moreSelectFun(recordData.userSelect, 1)">
                            <el-option v-for="item in recordData.userList" :key="item.role_id" :label="item.user_name"
                                :value="item.id" />
                        </el-select>
                    </div>
                </div>
                <div class="testMsgBox">
                    <div class="testTextBox">小区</div>
                    <div class="testSelectBox">
                        <el-select v-model="recordData.areaSlect" placeholder="请选择小区" clearable @clear="clear(2)"
                            @visible-change="visibleAreaList" @change="moreSelectFun(recordData.areaSlect, 2)">
                            <el-option v-for="item in recordData.areaList" :key="item.id" :label="item.name"
                                :value="item.id" />
                        </el-select>
                    </div>
                </div>
                <div class="testMsgBox">
                    <div class="testTextBox">楼宇</div>
                    <div class="testSelectBox">
                        <el-select v-model="recordData.buildingSlect" placeholder="请选择楼宇" clearable @clear="clear(3)"
                            @change="moreSelectFun(recordData.buildingSlect, 3)" @visible-change="visibleBuild">
                            <el-option v-for="item in recordData.buildingList" :key="item.id" :label="item.name"
                                :value="item.id" />
                        </el-select>
                    </div>

                </div>
                <div class="testMsgBox">
                    <div class="testTextBox">楼层</div>
                    <div class="testSelectBox">
                        <el-select v-model="recordData.floorsSlect" placeholder="请选择楼层" clearable @clear="clear(4)"
                            @change="moreSelectFun(recordData.floorsSlect, 4)" @visible-change="visibleFloor">
                            <el-option v-for="item in recordData.floorsList" :key="item.id" :label="item.name"
                                :value="item.id" />
                        </el-select>
                    </div>
                </div>
                <div class="testMsgBox">
                    <div class="testTextBox">控制器号</div>
                    <div class="testSelectBox">
                        <el-select v-model="recordData.controllersSlect" placeholder="请选择控制器" clearable
                            @clear="clear(5)" @visible-change="visibleControllers"
                            @change="moreSelectFun(recordData.controllersSlect, 5)">
                            <el-option v-for="item in recordData.controllersList" :key="item.id" :label="item.name"
                                :value="item.code" />
                        </el-select>
                    </div>
                </div>
                <div class="testMsgBox">
                    <div class="testTextBox">回路号</div>
                    <div class="testSelectBox">
                        <el-select v-model="recordData.loopSlect" placeholder="请选择回路号" clearable @clear="clear(6)"
                            @change="moreSelectFun(recordData.loopSlect, 6)" @visible-change="visibleLoop">
                            <el-option v-for="item in recordData.loopList" :key="item" :label="item" :value="item" />
                        </el-select>
                    </div>
                </div>
                <div class="testMsgBox">
                    <div class="testTextBox">地址号</div>
                    <div class="testSelectBox">
                        <el-select v-model="recordData.partNumSlect" placeholder="请选择地址号" clearable
                            @change="moreSelectFun(recordData.partNumSlect, 7)" @visible-change="visibleAddrnum">
                            <el-option v-for="item in recordData.partNumList" :key="item.addr_num"
                                :label="item.addr_num" :value="item.addr_num" />
                        </el-select>
                    </div>
                </div>
                <div class="testMsgBox">
                    <div class="checkBox">
                        <input type="checkbox" class="check" v-model="recordData.testType" @click="putAlarmsType">
                    </div>
                    <div class="checkTextBox">包含模拟报警</div>
                </div>
                <div class="sureBtnBox">
                    <div class="sureBtn" @click="moreSelect"> <img src="../../assets/img/comment/searchImg.svg"
                            alt="" @dragstart.prevent>&nbsp; 查询</div>
                </div>
            </div>
        </div>
        <div class="pagingBigBox">
            <div class="pagingBox">
                <el-pagination layout="total,prev, pager, next,jumper " :total="recordData.total"
                    :page-size="recordData.page_size" @current-change="handleCurrentChange"
                    :current-page="recordData.requestObject.page" />
            </div>
            <div class="export" @click="exportFlag">导出</div>
        </div>
    </div>
    <!-- 控制器操作记录 -->
    <div class="recordBox" v-if="recordData.propsRecordType == 2">
        <div class="demandBox">
            <div class="selectBox">
                <div class="switchBtnBox">
                    <div class="switchBtn" :class="recordData.switchBtnActive == 0 ? 'active' : 'unactive'"
                        @click="switchRecord(0)">全部</div>
                    <div class="switchBtn" :class="recordData.switchBtnActive == 122 ? 'active' : 'unactive'"
                        @click="switchRecord(122)">复位</div>
                    <div class="switchBtn" :class="recordData.switchBtnActive == 129 ? 'active' : 'unactive'"
                        @click="switchRecord(129)">消音</div>
                    <div class="switchBtn" :class="recordData.switchBtnActive == 120 ? 'active' : 'unactive'"
                        @click="switchRecord(120)">开机</div>
                    <div class="switchBtn" :class="recordData.switchBtnActive == 121 ? 'active' : 'unactive'"
                        @click="switchRecord(121)">关机</div>
                    <div class="switchBtn" :class="recordData.switchBtnActive == 123 ? 'active' : 'unactive'"
                        @click="switchRecord(123)">自检</div>
                    <div class="switchBtn" :class="recordData.switchBtnActive == 306 ? 'active' : 'unactive'"
                        @click="switchRecord(306)">强点</div>
                    <div class="switchBtn" :class="recordData.switchBtnActive == 308 ? 'active' : 'unactive'"
                        @click="switchRecord(308)">强制应急</div>
                </div>
                <div class="dateBox">
                    <div class="dateText">日期 &nbsp;</div>
                    <div class="dateSelect">
                        <el-date-picker v-model="recordData.value1" type="daterange" unlink-panels format="YYYY-MM-DD"
                            value-format="YYYY-MM-DD" range-separator="至" start-placeholder="开始日期"
                            end-placeholder="结束日期" :shortcuts="recordData.shortcuts" @change="changeDate" />
                    </div>
                </div>
            </div>

            <div class="btnBox">
                <div class="derive" @click="refresh">刷新</div>
            </div>
        </div>
        <div class="tableBox">
            <el-table :data="recordData.tableData" class="alarmsTable"
                :header-cell-style="{ color: '#000000', backgroundColor: '#F8F9FC' }">
                <el-table-column prop="op_time" label="日期" align="center" />
                <el-table-column prop="controller_num" label="控制器号" align="center" />
                <el-table-column prop="controller_name" label="控制器名称" align="center" />
                <el-table-column prop="description" label="操作类型" align="center" :show-overflow-tooltip="true" />
            </el-table>
        </div>
        <div class="pagingBigBox">
            <div class="pagingBox">
                <el-pagination layout="total,prev, pager, next,jumper " :total="recordData.total"
                    :page-size="recordData.page_size" @current-change="handleCurrentChange"
                    :current-page="recordData.requestObject.page" />
            </div>
            <div class="export" @click="exportFlag">导出</div>
        </div>
    </div>
    <!-- 值班记录 -->
    <div class="recordBox" v-if="recordData.propsRecordType == 3">
        <div class="demandBox">
            <div class="selectBox">
                <div class="selectorBox">
                    操作员 &nbsp;
                    <el-select v-model="recordData.userSelect" clearable placeholder="请选择"
                        @visible-change="visibleUserList" @change="switchRecordFun(recordData.userSelect)">
                        <el-option v-for="item in recordData.userList" :key="item.id" :label="item.user_name"
                            :value="item.id" />
                    </el-select>
                </div>
                <div class="dateBox">
                    <div class="dateText">日期 &nbsp;</div>
                    <div class="dateSelect">

                        <el-date-picker v-model="recordData.value1" type="daterange" unlink-panels format="YYYY-MM-DD"
                            value-format="YYYY-MM-DD" range-separator="至" start-placeholder="开始日期"
                            end-placeholder="结束日期" :shortcuts="recordData.shortcuts" @change="changeDate" />
                    </div>
                </div>
            </div>

            <div class="btnBox">

                <div class="derive" @click="refresh">刷新</div>
            </div>
        </div>
        <div class="tableBox">
            <el-table :data="recordData.tableData" class="alarmsTable"
                :header-cell-style="{ color: '#000000', backgroundColor: '#F8F9FC' }">
                <el-table-column prop="shift_time" label="日期" align="center" />
                <el-table-column prop="watch_user_name" label="交班用户" align="center" />
                <el-table-column prop="change_user_name" label="接班用户 " align="center" />
            </el-table>
        </div>
        <div class="pagingBigBox">
            <div class="pagingBox">
                <el-pagination layout="total,prev, pager, next,jumper " :total="recordData.total"
                    :page-size="recordData.page_size" @current-change="handleCurrentChange"
                    :current-page="recordData.requestObject.page" />
            </div>
            <div class="export" @click="exportFlag">导出</div>
        </div>
    </div>
    <!-- 用户操作记录 -->
    <div class="recordBox" v-if="recordData.propsRecordType == 4">
        <div class="demandBox">
            <div class="selectBox">
                <div class="selectorBox">
                    操作员 &nbsp;
                    <el-select v-model="recordData.userSelect" clearable placeholder="请选择"
                        @visible-change="visibleUserList" @change="funRecordFun(recordData.userSelect)">
                        <el-option v-for="item in recordData.userList" :key="item.role_id" :label="item.user_name"
                            :value="item.id" />
                    </el-select>
                </div>
                <div class="selectorBox">
                    关键字 &nbsp; <el-input v-model="recordData.input" placeholder="请输入关键字" clearable
                        @clear="clearOperation">
                        <template #append>
                            <el-button @click="searchFun(recordData.input)">
                                <el-icon>
                                    <Search />
                                </el-icon>
                            </el-button>
                        </template>
                    </el-input>
                </div>
                <div class="dateBox">
                    <div class="dateText">日期 &nbsp;</div>
                    <div class="dateSelect">
                        <el-date-picker v-model="recordData.value1" type="daterange" unlink-panels format="YYYY-MM-DD"
                            value-format="YYYY-MM-DD" range-separator="至" start-placeholder="开始日期"
                            end-placeholder="结束日期" :shortcuts="recordData.shortcuts" @change="changeDate" clearable />
                    </div>
                </div>
            </div>

            <div class="btnBox">
                <div class="derive" @click="refresh">刷新</div>
            </div>
        </div>
        <div class="tableBox">
            <el-table :data="recordData.tableData" class="alarmsTable"
                :header-cell-style="{ color: '#000000', backgroundColor: '#F8F9FC' }">
                <el-table-column prop="op_time" label="日期" align="center" />
                <el-table-column prop="user_name" label="操作员" align="center" />
                <el-table-column prop="description" label="内容 " align="center" />
            </el-table>
        </div>
        <div class="pagingBigBox">
            <div class="pagingBox">
                <el-pagination layout="total,prev, pager, next,jumper " :total="recordData.total"
                    :page-size="recordData.page_size" @current-change="handleCurrentChange"
                    :current-page="recordData.requestObject.page" />
            </div>
            <div class="export" @click="exportFlag">导出</div>
        </div>
    </div>
    <!-- 维保记录 -->
    <div class="recordBox" v-if="recordData.propsRecordType == 5">
        <div class="demandBox">
            <div class="selectBox">
                <div class="selectorBox">
                    操作员 &nbsp;
                    <el-select v-model="recordData.userSelect" clearable placeholder="请选择"
                        @visible-change="visibleUserList" @change="selectFun(recordData.userSelect, 1)">
                        <el-option v-for="item in recordData.userList" :key="item.role_id" :label="item.user_name"
                            :value="item.id" />
                    </el-select>
                </div>
                <div class="selectorBox">
                    项目 &nbsp;
                    <el-select v-model="recordData.projectSelect" placeholder="请选择" @visible-change="visibleObjectList"
                        @change="selectFun(recordData.projectSelect, 2)" clearable>
                        <el-option v-for="item in recordData.projectList" :key="item.id" :label="item.name"
                            :value="item.id" />
                    </el-select>
                </div>
                <div class="dateBox">
                    <div class="dateText">日期 &nbsp;</div>
                    <div class="dateSelect">
                        <el-date-picker v-model="recordData.value1" type="daterange" unlink-panels format="YYYY-MM-DD"
                            value-format="YYYY-MM-DD" range-separator="至" start-placeholder="开始日期"
                            end-placeholder="结束日期" :shortcuts="recordData.shortcuts" @change="changeDate" clearable />
                    </div>
                </div>
            </div>
            <div class="btnBox">
                <div class="derive" @click="refresh">刷新</div>
            </div>
        </div>
        <div class="tableBox">
            <el-table :data="recordData.tableData" class="alarmsTable"
                :header-cell-style="{ color: '#000000', backgroundColor: '#F8F9FC' }">
                <el-table-column prop="maintenance_time" label="日期" align="center" />
                <el-table-column prop="user_name" label="操作员" align="center" />
                <el-table-column prop="operator_name" label="操作名称 " align="center" />
                <el-table-column prop="description" label="维保内容" align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="project_id" label="项目" align="center" />

            </el-table>
        </div>
        <div class="pagingBigBox">
            <div class="pagingBox">
                <el-pagination layout="total,prev, pager, next,jumper " :total="recordData.total"
                    :page-size="recordData.page_size" @current-change="handleCurrentChange"
                    :current-page="recordData.requestObject.page" />
            </div>
            <div class="export" @click="exportFlag">导出</div>
        </div>
    </div>
</template>
<script>
import { reactive, watch, onMounted } from 'vue'
import { Search } from '@element-plus/icons-vue'
import detail from "../detail/detail"
import { ElMessage } from 'element-plus'
import { useStore } from 'vuex'

import { alarmsRequest, controllerOperationRequest, changeShiftRequest, operationRequest, maintenanceRequest } from "../../api/recordData";
import {
    inquireLoopRequest,
    deviceListRequest,
    buildingListRequest,
    floorsListRequest,
    userListRequest,
    areaListRequest,
    controllersListRequest,
    projectListRequest
} from "../../api/baseData";
export default {
    components: {
        Search,
        detail,
    },
    props: {
        recordType: Number
        //表格类型: 1:报警记录 2:控制器操作记录 3:值班记录 4:用户操作记录 5:维保记录
        //         6:图例查询 7:设备查询 8:设备状态查询 9:控制器查询 10:设备布点图查询 11:平面图查询 12:控制室信息
        // 13:项目列表 14:小区-楼宇列表 15:楼层信息 16:控制器设置 17:设备设置
    },
    setup(props) {
        let recordData = reactive({
            switchBtnActive: 0,
            tableData: [],//表格数据
            userSelect: "",//操作员选择器
            userList: [],//用户列表
            projectSelect: "",//项目选择器
            projectList: [],//项目列表
            areaSlect: "",//小区选择器
            areaList: [],//小区列表
            buildingSlect: "",//楼宇选择器
            buildingList: [],//楼宇列表
            floorsSlect: "",//楼层选择器
            floorsList: [],//楼层列表
            controllersSlect: "",//控制器选择器
            controllersList: [],//控制器列表
            loopSlect: "",//回路号 选择器
            loopList: [],//回路号列表
            partNumSlect: "",//部位号选择器
            partNumList: [],//部位号列表
            value1: "",
            propsRecordType: 1,
            shortcuts: [
                {
                    text: '最近一周',
                    value: () => {
                        const end = new Date()
                        const start = new Date()
                        start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
                        return [start, end]
                    },
                },
                {
                    text: '最近一个月',
                    value: () => {
                        const end = new Date()
                        const start = new Date()
                        start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
                        return [start, end]
                    },
                },
                {
                    text: '最近三个月',
                    value: () => {
                        const end = new Date()
                        const start = new Date()
                        start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
                        return [start, end]
                    },
                },
            ],
            building: "",
            buildingArr: [
                {
                    value: 'Option1',
                    label: '1栋',
                },
                {
                    value: 'Option2',
                    label: '2栋',
                },
                {
                    value: 'Option3',
                    label: '3栋',
                },
                {
                    value: 'Option4',
                    label: '4栋',
                },
                {
                    value: 'Option5',
                    label: '5栋',
                },
            ],
            input: "",
            moreSelect: false,//控制更多筛选显示隐藏
            requestObject: {
                page: 1,
                per_page: 8,
                alarm_type_id: "",
                st: "",//开始日期
                et: "",//结束日期
                user_id: "",//操作人id
                gb_evt_type_id: "",//国标事件类型id
                gb_evt_type_ids:"",//应急疏散
                description: "",// 描述
                project_id: "",//项目id
                area_id: "",//小区id
                build_id: "",//楼宇id
                floor_id: "",//楼层id
                controller_num: "",//控制器号
                loop_num: "",//回路号
                addr_num: "",//地址号
                alarm_type: "",//是否未模拟报警
                export_flag: "",
                watch_user_id: "",
                change_user_id: "",
            },//请求参数
            total: 1,
            page_size: 8,
            tableId: 1,
            testType: true,//是否未模拟报警
            request: {
                page: 0,
            }
        })
        const store = useStore();
        onMounted(() => {
            firstRequest(store.state.switchRecord)
            recordData.userList = store.state.userList
            recordData.projectList = store.state.projectList
            recordData.areaList = store.state.areaList
            recordData.controllersList = store.state.controllersList
        })

        const formatState = (row, column, cellValue) => {
            if (cellValue == 1) {
                return '出现';
            } else if (cellValue == 0) {
                return '消失';
            } else if (cellValue == 2) {
                return '丢弃';
            }
        }
        // 选择框下拉拉取用户列表
        const visibleUserList = () => {

            userListRequest(recordData.request).then((res) => {
                recordData.userList = res.data.items
            });
        }
        // 选择框下拉拉取小区列表
        const visibleAreaList = () => {
            areaListRequest(recordData.request).then((res) => {
                recordData.areaList = res.data.items
            });
        }
        // 选择框下拉拉取控制器列表
        const visibleControllers = () => {
            controllersListRequest(recordData.request).then((res) => {
                recordData.controllersList = res.data.items
            });
        }
        // 选择框下拉拉取项目列表
        const visibleObjectList = () => {
            projectListRequest(recordData.request).then((res) => {
                recordData.projectList = res.data.items
            });
        }
        // 用于打开选择器的时候提示
        const visibleBuild = (val)=>{
            if(val==true&&recordData.areaSlect=="")return  ElMessage({
                            message: '请先选择小区',
                            type: 'info',
                            duration: 3 * 1000
                        })
        }
        const visibleFloor = (val)=>{
            if(val==true&&recordData.buildingSlect=="")return  ElMessage({
                            message: '请先选择楼宇',
                            type: 'info',
                            duration: 3 * 1000
                        })
        }
        const visibleLoop = (val)=>{
            if(val==true&&recordData.controllersSlect=="")return  ElMessage({
                            message: '请先选择控制器',
                            type: 'info',
                            duration: 3 * 1000
                        })
        }
        const visibleAddrnum = (val)=>{
            if(val==true&&recordData.loopSlect=="")return  ElMessage({
                            message: '请先选择回路号',
                            type: 'info',
                            duration: 3 * 1000
                        })
        }
        // 刷新
        const refresh = () => {
            clearFun()
            switchRecord("", recordData.propsRecordType)
        }
        const clearFun = ()=>{
            recordData.value1 = ""
            recordData.requestObject.st = ""
            recordData.requestObject.et = ""
            recordData.requestObject.description = ""
            recordData.requestObject.user_id = ""//清空用户id
            recordData.requestObject.area_id = ""//清空小区选择
            recordData.requestObject.build_id = ""//清空楼宇选择
            recordData.requestObject.floor_id = ""//清空楼层选择
            recordData.requestObject.controller_num = ""//清空控制器选择
            recordData.requestObject.loop_num = ""//清空回路号选择
            recordData.requestObject.addr_num = ""//清空部位号选择
            recordData.requestObject.alarm_type = ""//清空部位号选择
            recordData.requestObject.project_id = ""//清空项目选择
            recordData.requestObject.watch_user_id = ""
            recordData.requestObject.change_user_id = ""
            recordData.requestObject.gb_evt_type_id = ""
                    recordData.requestObject.gb_evt_type_ids = ""
            recordData.input = ""
            recordData.userSelect = ""
            recordData.projectSelect = ""//清空项目选择器
            recordData.areaSlect = ""//清空小区选择器
            recordData.buildingSlect = ""//清空楼宇选择器
            recordData.floorsSlect = ""//清空楼层选择器
            recordData.controllersSlect = ""//清空控制器选择器
            recordData.loopSlect = ""//清空回路号选择器
            recordData.partNumSlect = ""//清空部位号选择器
            recordData.testType = ""
        }
        //输入框搜索
        const searchFun = (val) => {
            recordData.requestObject.page = 1//页数为1
            recordData.tableId = 1//页数为1
            recordData.requestObject.description = val
            firstRequest(recordData.propsRecordType)
        }
        // 清空操作记录输入框
        const clearOperation = () => {
            recordData.requestObject.page = 1//页数为1
            recordData.tableId = 1//页数为1
            recordData.requestObject.description = ""
            firstRequest(recordData.propsRecordType)
        }
        // 更多筛选 查询
        const switchMoreSelectBox = (type) => {
            recordData.moreSelect = !recordData.moreSelect
        }
        // 更多筛选查询
        const moreSelect = () => {
            recordData.requestObject.page = 1
            recordData.tableId = 1
            firstRequest(recordData.propsRecordType)
            recordData.moreSelect = false
        }
        // 清空选择器
        const clear = (type) => {
            if (type == 2) {
                recordData.requestObject.area_id = "",
                    recordData.requestObject.build_id = "",
                    recordData.requestObject.floor_id = ""
                recordData.buildingList = [],
                    recordData.floorsList = []
            } else if (type == 3) {
                recordData.requestObject.build_id = "",
                    recordData.requestObject.floor_id = ""
                recordData.floorsList = []
            } else if (type == 4) {
                recordData.requestObject.floor_id = ""
            } else if (type == 5) {
                recordData.requestObject.controller_num = "",
                    recordData.requestObject.loop_num = "",
                    recordData.requestObject.addr_num = ""
                recordData.loopList = [],
                    recordData.partNumList = []
                recordData.partNumSlect = ""
            } else if (type == 6) {
                recordData.partNumList = [],
                    recordData.requestObject.addr_num = "",
                    recordData.partNumSlect = ""
            }
        }
        // 选择人员 项目
        const selectFun = (val, num) => {

            if (recordData.propsRecordType == 4) {
                recordData.requestObject.user_id = val
            } else if (recordData.propsRecordType == 5) {
                if (num == 1) {
                    recordData.requestObject.user_id = val
                } else {
                    recordData.requestObject.project_id = val
                }
            }
            firstRequest(recordData.propsRecordType)
        }
        // 更多筛选
        const moreSelectFun = (val, type) => {
            if (type == 1) {
                recordData.requestObject.user_id = val//项目人员
            } else if (type == 2) {
                if (val) {
                    recordData.requestObject.area_id = val//小区
                    let data = {
                        area_id: val,
                        page: 0
                    }
                    buildingListRequest(data).then((res) => {
                        recordData.buildingList = res.data.items
                    });
                }
                recordData.buildingSlect = ""
                recordData.floorsSlect = ""
            } else if (type == 3) {
                if (val) {
                    let data = {
                        build_id: val,
                        page: 0
                    }
                    floorsListRequest(data).then((res) => {
                        recordData.floorsList = res.data.items
                    });

                    recordData.requestObject.build_id = val//楼宇
                }
                recordData.floorsSlect = ""
            } else if (type == 4) {
                if(recordData.buildingSlect=="")return  ElMessage({
                            message: '请先选择回路号',
                            type: 'info',
                            duration: 3 * 1000
                        })
                recordData.requestObject.floor_id = val//楼层
            } else if (type == 5) {
                if (val != null) {
                    recordData.requestObject.controller_num = val//控制器号
                    let loopRequest = {
                        page: 0
                    }
                    loopRequest.controller_num = val
                    inquireLoopRequest(loopRequest).then((res) => {
                        recordData.loopList = res.data.loops
                    });
                }

                // 选择控制器时 清空回路号和地址号选择器
                recordData.loopSlect = ""
                recordData.requestObject.loop_num = ""
                recordData.partNumSlect = ""
                recordData.requestObject.addr_num = ""
            } else if (type == 6) {
                if (val != null) {
                    recordData.requestObject.loop_num = val//回路号
                    let deviceRequest = {
                        controller_num: recordData.controllersSlect,
                        loop_num: val, page: 0
                    }
                    deviceListRequest(deviceRequest).then((res) => {
                        recordData.partNumList = res.data.items
                    });
                    recordData.partNumSlect = ""
                }

            } else if (type == 7) {
                recordData.requestObject.addr_num = val//部位号
            }
        }
        const putAlarmsType = () => {
            if (recordData.testType == false) {
                recordData.requestObject.alarm_type = ""
            } else {
                recordData.requestObject.alarm_type = 0
            }
        }
        // 切换记录筛选
        const switchRecord = (type) => {
            console.log(type);
            recordData.switchBtnActive = type//选中样式
            recordData.value1 = ""//清空时间选择器
            recordData.requestObject.st = ""
            recordData.requestObject.et = ""
            // 1 报警记录 2 控制器操作记录
            if (recordData.propsRecordType == 1) {
                recordData.requestObject.alarm_type_id = type
            } else if (recordData.propsRecordType == 2) {
                if (type == 0) {
                    recordData.requestObject.gb_evt_type_id = ""
                    recordData.requestObject.gb_evt_type_ids = ""
                } else if(type==308){
                    recordData.requestObject.gb_evt_type_ids = '308,309'
                    recordData.requestObject.gb_evt_type_id = ""
                } else if(type==306){
                    recordData.requestObject.gb_evt_type_ids = '306,307'
                    recordData.requestObject.gb_evt_type_id = ""
                } else {
                    recordData.requestObject.gb_evt_type_id = type
                    recordData.requestObject.gb_evt_type_ids = ''
                }

            }
            // 切换状态 页数重置为1 
            recordData.requestObject.page = 1
            recordData.tableId = (1 - 1) * recordData.requestObject.per_page + 1;
            // 重新计算记录总数
            firstRequest(recordData.propsRecordType)
        }
        // 切换日期
        const changeDate = (val) => {
            if (val == null) {
                recordData.requestObject.st = ""
                recordData.requestObject.et = ""
            } else {
                recordData.requestObject.st = val[0]
                recordData.requestObject.et = val[1]
            }
            recordData.requestObject.page = 1;
            firstRequest(recordData.propsRecordType)
            recordData.tableId = (1 - 1) * recordData.requestObject.per_page + 1;

        }
        // 切换分页
        const handleCurrentChange = (val) => {
            recordData.requestObject.page = val;
            Request(recordData.propsRecordType);
            // 序号
            recordData.tableId = (val - 1) * recordData.requestObject.per_page + 1;
        }
        // 值班记录 交班用户搜索
        const switchRecordFun = (val) => {
            recordData.requestObject.watch_user_id = val
            changeShiftRequest(recordData.requestObject).then((res) => {
                recordData.tableData = res.data.items
                recordData.total = res.data.record_size
                if (recordData.total==0) return ElMessage({
                            message: '暂无数据',
                            type: 'info',
                            duration: 3 * 1000
                        })
            });
        }
        // 用户操作记录
        const funRecordFun = (val) => {
            recordData.requestObject.user_id = val
            operationRequest(recordData.requestObject).then((res) => {
                recordData.tableData = res.data.items
                recordData.total = res.data.record_size
                if (recordData.total==0) return ElMessage({
                            message: '暂无数据',
                            type: 'info',
                            duration: 3 * 1000
                        })
            });
        }
        // 第一次请求记录 计算总数
        const firstRequest = (type) => {
            // 1 报警记录 2 控制器操作记录 3 值班记录 4 用户操作记录 5 维保记录
            if (type == 1) {
                alarmsRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                    recordData.total = res.data.record_size
                    if (recordData.total==0) return ElMessage({
                            message: '暂无数据',
                            type: 'info',
                            duration: 3 * 1000
                        })
                });
            } else if (type == 2) {
                controllerOperationRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                    recordData.total = res.data.record_size
                    if (recordData.total==0) return ElMessage({
                            message: '暂无数据',
                            type: 'info',
                            duration: 3 * 1000
                        })
                });
            } else if (type == 3) {
                changeShiftRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                    recordData.total = res.data.record_size
                    if (recordData.total==0) return ElMessage({
                            message: '暂无数据',
                            type: 'info',
                            duration: 3 * 1000
                        })
                });
            } else if (type == 4) {
                operationRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                    recordData.total = res.data.record_size
                    if (recordData.total==0) return ElMessage({
                            message: '暂无数据',
                            type: 'info',
                            duration: 3 * 1000
                        })
                });
            } else if (type == 5) {
                maintenanceRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                    recordData.total = res.data.record_size
                    if (recordData.total==0) return ElMessage({
                            message: '暂无数据',
                            type: 'info',
                            duration: 3 * 1000
                        })
                });
            }
        }
        const Request = (type) => {
            // 1 报警记录 2 控制器操作记录 3 值班记录 4 用户操作记录 5 维保记录
            if (type == 1) {
                alarmsRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                  
                });
            } else if (type == 2) {
                controllerOperationRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                });
            } else if (type == 3) {
                changeShiftRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                });
            } else if (type == 4) {
                operationRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                });
            } else if (type == 5) {
                maintenanceRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                });
            }
           
        }
        // 导出
        const exportFlag = () => {
            ElMessage({
                message: '正在处理需要下载的数据 请等待开始下载',
                type: 'success',
                duration: 3 * 1000
            })
            recordData.requestObject.export_flag = 1
            firstRequest(recordData.propsRecordType)
            recordData.requestObject.export_flag = ""
        }
        watch(props, (newProps) => {
            recordData.propsRecordType = newProps.recordType
            recordData.switchBtnActive = 0//选中样式
            recordData.requestObject.page = 1//页数为1
            recordData.tableId = 1//页数为1
            clearFun()
            recordData.testType = false //清空模拟报警选择
            recordData.moreSelect = false//切换记录关闭更多筛选
            recordData.userList = store.state.userList
            recordData.projectList = store.state.projectList
            recordData.areaList = store.state.areaList
            recordData.controllersList = store.state.controllersList
            firstRequest(newProps.recordType)
        }
        );
        return {
            clearFun,
            recordData,
            switchRecord,
            moreSelect,
            switchMoreSelectBox,
            clear,
            Request,
            handleCurrentChange,
            firstRequest,
            changeDate,
            refresh,
            selectFun,
            searchFun,
            moreSelectFun,
            formatState,
            putAlarmsType,
            clearOperation,
            exportFlag,
            visibleUserList,
            visibleAreaList,
            visibleControllers,
            visibleObjectList,
            switchRecordFun,
            funRecordFun,
            visibleBuild,
            visibleFloor,
            visibleLoop,
            visibleAddrnum
        }
    }
}
</script>
<style scoped lang="scss">
.recordBox {
    width: 1760px;
    height: 884px;
    margin-left: 80px;
    margin-top: 18px;
    margin-bottom: 18px;
    background: #ffffff;

    .demandBox {
        width: 1760px;
        height: 80px;
        display: flex;
        justify-content: space-between;
        align-items: center;

        .selectBox {
            display: flex;
            align-items: center;

            // 切换状态按钮
            .switchBtnBox {
                display: flex;

                .switchBtn {
                    width: 90px;
                    height: 44px;
                    border-radius: 2px;
                    margin-left: 12px;
                    font-size: 20px;
                    font-weight: 500;
                    text-align: left;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    cursor: pointer;
                }

                .switchBtn:first-child {
                    margin-left: 40px;
                }

                .switchBtn:nth-child(8),
                .switchBtn:nth-child(9) {
                    width: 120px;
                    height: 44px;
                    border-radius: 2px;
                }

                .active {
                    color: #4A5CD5;
                    border: 1px solid #4a5cd5;
                }

                .unactive {
                    color: #909399;
                    border: 1px solid #c5c9d4;
                }

            }

            // 选择器
            .selectorBox {
                display: flex;
                align-items: center;
                height: 100px;
                font-size: 22px;
                font-weight: 500;
                color: #000000;
                letter-spacing: 1.1px;
                margin-left: 23px;

                // 选择器
                :deep(.el-select) {
                    width: 260px;
                    height: 44px;
                }

                :deep(.el-input__wrapper) {
                    width: 260px;
                    height: 44px;
                    background-color: #F7F8FC;
                    border: none !important;
                    box-shadow: none !important;
                }

                :deep(.el-input) {
                    width: 260px;
                    height: 44px;
                    background: #f7f8fc;
                }

                :deep(.el-input-group__append) {
                    border: none !important;
                    box-shadow: none !important;
                    height: 46px;
                }

                :deep(.el-button) {

                    height: 44px;
                }
            }

            // 日期
            .dateBox {
                display: flex;
                flex-direction: row;
                align-items: center;
                height: 100px;
                margin-left: 23px;

                .dateText {
                    font-size: 22px;
                    font-weight: 500;
                    color: #000000;
                    letter-spacing: 1.1px;
                }

                // 日期选择器
                .dateSelect {
                    width: 360px;
                    height: 44px;

                    :deep(.el-range-editor.el-input__wrapper) {
                        height: 46px;
                        color: #000000;
                        border: none !important;
                        box-shadow: none !important;
                        background-color: #F7F8FC !important;
                    }

                    :deep(.el-range-separator) {
                        height: 46px;
                        border: none !important;
                        box-shadow: none !important;
                        color: #000000;
                    }

                    :deep(.el-range-input) {
                        height: 46px;

                    }

                }
            }
        }


        // 更多筛选 导出 新建项目
        .btnBox {
            height: 100px;
            display: flex;
            align-items: center;
            font-size: 20px;
            font-weight: 500;
            color: #ffffff;
            margin-right: 20px;

            .more {
                width: 144px;
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

        .btnBox:first-child {
            width: 250px;
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

        // 更多筛选
        .moreSelectBox {
            width: 1680px;
            height: 260px;
            margin-left: 40px;
            position: absolute;
            top: 0px;
            background: #ffffff;
            box-shadow: 0px 0px 20px 0px rgba(0, 0, 0, 0.16);
            z-index: 10;
            display: flex;
            flex-wrap: wrap;

            // 选择器
            :deep(.el-select) {
                width: 260px;
                height: 44px;
                color: #4A5CD5;
            }

            :deep(.el-input__wrapper) {
                width: 260px;
                height: 44px;
                color: #4A5CD5;
                background-color: #F7F8FC;
                border: none !important;
                box-shadow: none !important;
            }

            .testMsgBox {
                width: 400px;
                height: 44px;
                display: flex;
                margin-top: 30px;

                .testTextBox,
                .checkTextBox {
                    width: 120px;
                    height: 44px;
                    display: flex;
                    align-items: center;
                    justify-content: right;
                    font-size: 22px;
                    font-weight: 500;
                    color: #000000;
                    letter-spacing: 1.1px;
                    margin-left: 20px;
                }

                .testSelectBox {
                    width: 260px;
                    height: 44px;
                    margin-left: 18px;
                }

                .checkBox {
                    width: 120px;
                    height: 44px;
                    display: flex;
                    flex-direction: row-reverse;
                    border: none;
                    align-items: center;

                    .check {
                        width: 24px;
                        height: 24px;
                        border: 1px solid #f7f8fc;
                    }
                }

                .checkTextBox {
                    width: 150px;
                }
            }

            .sureBtnBox {
                width: 1680px;
                height: 44px;
            }

            .sureBtn {
                width: 120px;
                height: 44px;
                background: #4a5cd5;
                border-radius: 2px;
                margin-right: 57px;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 22px;
                font-weight: 500;
                color: #ffffff;
                letter-spacing: 1.1px;
                cursor: pointer;
                position: absolute;
                right: 20px;
                bottom: 30px;
            }
        }

        .operation {
            color: #4A5CD5;
            text-decoration: underline;
            cursor: pointer;
        }

        .deviceState {

            display: flex;
            align-items: center;
            justify-content: center;

            .deviuceStateImg {
                width: 28px;
                height: 20px;
                cursor: pointer;

                .deviuceStateimg {
                    width: 28px;
                    height: 20px;
                }

            }
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

        .export {
            width: 90px;
            height: 44px;
            background: #4a5cd5;
            border-radius: 2px;

            font-size: 20px;

            font-weight: 500;

            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            position: absolute;
            right: 40px;
            cursor: pointer;
            top: 42px;
        }
    }



}
</style>