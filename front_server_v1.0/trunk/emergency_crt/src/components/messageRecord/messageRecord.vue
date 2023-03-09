<!-- 信息查询记录 -->
<template>
    <!-- 图例查询 -->
    <div class="recordBox" v-if="recordData.propsRecordType == 6">
        <div class="imgInquire">

            <div class="deviceBox" v-for="(item, index) in recordData.tableData" :key="index">
                <div class="deviceImgBox">
                    <img class="deviceImg" :src="recordData.url + item.path" alt="" :title="item.name" @dragstart.prevent>
                </div>
                <div class="deviceTextBox">{{ item.name }}</div>
            </div>
        </div>
        <div class="pagingBigBox">
            <div class="pagingBox">
                <el-pagination layout="total,prev, pager, next,jumper " :total="recordData.total"
                    :page-size="recordData.imgPage_size" @current-change="ImgHandleCurrentChange"
                    :current-page="recordData.ImgRequestObject.page" />
            </div>
        </div>
    </div>
    <!-- 设备查询 -->
    <div class="recordBox" v-if="recordData.propsRecordType == 7">
        <div class="demandBox">
            <div class="selectBox">
                <div class="selectorBox">
                    描述 &nbsp; <el-input v-model="recordData.input" placeholder="请输入描述" clearable @clear="clear">
                        <template #append>
                            <el-button @click="searchFun(recordData.input)">
                                <el-icon>
                                    <Search />
                                </el-icon>
                            </el-button>
                        </template>
                    </el-input>
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
                <el-table-column label="设备图片" align="center">
                    <template #default="scope">
                        <div class="deviceState">
                            <img class="deviuceImg" :src="recordData.url + scope.row.path" alt="" @dragstart.prevent>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="device_type_name" label="设备类型 " align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="current" label="地址号" align="center" />
                <el-table-column prop="description" label="描述" align="center" :show-overflow-tooltip="true" />
                <el-table-column label="是否布点" align="center">
                    <template #default="scope">
                        <div class="deviceState">
                            <template v-if="scope.row.is_assign == 1">
                                是
                            </template>
                            <template v-else>否</template>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column label="布点" align="center">
                    <template #default="scope">
                        <div class="deviceState">
                            <template v-if="scope.row.is_assign == 1">
                                <div class="deviuceStateImg" @click="openDetail(scope.row)">
                                    <img class="deviuceStateimg" src="../../assets/img/comment/imgImg.svg" alt="" @dragstart.prevent>
                                </div>
                            </template>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="manufacturer" label="厂家" align="center" :show-overflow-tooltip="true" />
                <el-table-column label="维保周期" align="center">
                    <template #default="scope">
                        <div class="deviceState">
                            <template v-if="scope.row.maintain_cycle == null"></template>
                            <template v-else>{{ scope.row.maintain_cycle }}天</template>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="status" label="状态" align="center">
                    <template #default="scope">
                        <div class="deviceState">
                            注册:是 <br>
                            在线:是
                        </div>
                    </template>
                </el-table-column>


            </el-table>
            <!-- 更多筛选 -->
            <div class="moreSelectBox" v-show="recordData.moreSelect">
                <div class="testMsgBox">
                    <div class="testTextBox">控制器号</div>
                    <div class="testSelectBox">
                        <el-select v-model="recordData.controllersSlect" placeholder="请选择控制器" clearable  @visible-change="visibleControllers"
                            @change="moreSelectFun(recordData.controllersSlect, 1)" @clear="clrarSlect(1)">
                            <el-option v-for="item in recordData.controllersList" :key="item.id" :label="item.name"
                                :value="item.code" />
                        </el-select>
                    </div>
                </div>
                <div class="testMsgBox">
                    <div class="testTextBox">回路号</div>
                    <div class="testSelectBox">
                        <el-select v-model="recordData.loopSlect" placeholder="请选择回路号" clearable
                            @change="moreSelectFun(recordData.loopSlect, 2)" @clear="clrarSlect(2)" @visible-change="visibleLoop">
                            <el-option v-for="item in recordData.loopList" :key="item" :label="item" :value="item" />
                        </el-select>
                    </div>

                </div>
                <div class="testMsgBox">
                    <div class="testTextBox">地址号</div>
                    <div class="testSelectBox">
                        <el-select v-model="recordData.partNumSlect" placeholder="请选择地址号" clearable
                            @change="moreSelectFun(recordData.partNumSlect, 3)" @clear="clrarSlect(3)"  @visible-change="visibleAddrnum">
                            <el-option v-for="item in recordData.partNumList" :key="item.addr_num"
                                :label="item.addr_num" :value="item.addr_num" />
                        </el-select>
                    </div>

                </div>
                <!-- <div class="testMsgBox">
                    <div class="testTextBox">小区</div>
                    <div class="testSelectBox">
                        <el-select v-model="recordData.areaSlect" placeholder="请选择小区" clearable  @visible-change="visibleAreaList"
                            @change="moreSelectFun(recordData.areaSlect, 4)">
                            <el-option v-for="item in recordData.areaList" :key="item.id" :label="item.name"
                                :value="item.id" />
                        </el-select>
                    </div>
                </div> -->
                <div class="testMsgBox">
                    <div class="testTextBox">布点状态</div>
                    <div class="testSelectBox">
                        <el-select v-model="recordData.stationingSlect" placeholder="请选择布点状态" clearable
                            @change="moreSelectFun(recordData.stationingSlect, 5)">
                            <el-option v-for="item in recordData.stationingData" :key="item.value" :label="item.label"
                                :value="item.value" />
                        </el-select>
                    </div>
                </div>
                <div class="sureBtn" @click="moreSelect"> <img src="../../assets/img/comment/searchImg.svg"
                        alt="" @dragstart.prevent>&nbsp; 查询</div>
            </div>
        </div>
        <div class="pagingBigBox">
            <div class="pagingBox">
                <el-pagination layout="total,prev, pager, next,jumper " :total="recordData.total"
                    :page-size="recordData.page_size" @current-change="handleCurrentChange"
                    :current-page="recordData.requestObject.page" />
            </div>
        </div>
    </div>
    <!-- 设备状态查询 -->
    <div class="recordBox" v-if="recordData.propsRecordType == 8">
        <div class="demandBox">
            <div class="selectBox">
                <div class="switchBtnBox">
                    <div class="switchBtn" :class="recordData.switchBtnActive == 1 ? 'active' : 'unactive'"
                        @click="switchRecord(1)">火警</div>
                    <div class="switchBtn" :class="recordData.switchBtnActive == 2 ? 'active' : 'unactive'"
                        @click="switchRecord(2)">启动</div>
                    <div class="switchBtn" :class="recordData.switchBtnActive == 3 ? 'active' : 'unactive'"
                        @click="switchRecord(3)">反馈</div>
                    <div class="switchBtn" :class="recordData.switchBtnActive == 4 ? 'active' : 'unactive'"
                        @click="switchRecord(4)">故障</div>
                    <div class="switchBtn" :class="recordData.switchBtnActive == 5 ? 'active' : 'unactive'"
                        @click="switchRecord(5)">屏蔽</div>
                    <div class="switchBtn" :class="recordData.switchBtnActive == 6 ? 'active' : 'unactive'"
                        @click="switchRecord(6)">监管</div>

                </div>
                <div class="selectorBox">
                    描述 &nbsp; <el-input v-model="recordData.input" placeholder="请输入描述" clearable @clear="clear">
                        <template #append>
                            <el-button @click="searchFun(recordData.input)">
                                <el-icon>
                                    <Search />
                                </el-icon>
                            </el-button>
                        </template>
                    </el-input>
                </div>
            </div>
            <div class="btnBox">
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
                <el-table-column label="设备图片" align="center">
                    <template #default="scope">
                        <div class="deviceState">
                            <img class="deviuceImg" :src="recordData.url + scope.row.path" alt="" @dragstart.prevent>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="device_type_name" label="设备类型 " align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="current" label="地址号" align="center" />
                <el-table-column prop="description" label="描述" align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="area" label="小区" align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="unit" label="单元" align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="build" label="楼宇" align="center" />
                <el-table-column prop="floor" label="楼层" align="center" />
                <el-table-column prop="district" label="防火分区" align="center" />
                <el-table-column prop="room" label="防烟分区" align="center" />
                <el-table-column prop="dev_state" label="状态" align="center" />

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
    <!-- 控制器查询 -->
    <div class="recordBox" v-if="recordData.propsRecordType == 9">
        <div class="demandBox">
            <div class="selectBox">
                <div class="selectorBox">
                    控制器名称 &nbsp; <el-input v-model="recordData.input" placeholder="请输入控制器名称" clearable @clear="clear">
                        <template #append>
                            <el-button @click="searchFun(recordData.input)">
                                <el-icon>
                                    <Search />
                                </el-icon>
                            </el-button>
                        </template>
                    </el-input>
                </div>
            </div>
            <div class="btnBox">
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
                <el-table-column prop="name" label="控制器名称" align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="code" label="编号 " align="center" />
                <el-table-column prop="model" label="型号" align="center" />
                <el-table-column prop="controller_type" label="主从机" align="center">
                    <template #default="scope">
                        <div class="deviceState">
                            <template v-if="scope.row.controller_type == 1">
                                主机
                            </template>
                            <template v-else>
                                从机
                            </template>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="is_online" label="在线" align="center">
                    <template #default="scope">
                        <div class="deviceState">
                            <template v-if="scope.row.is_online == 1">
                                在线
                            </template>
                            <template v-else>
                                离线
                            </template>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="power_type" label="主备电" align="center">
                    <template #default="scope">
                        <div class="deviceState">
                            <template v-if="scope.row.power_type == 1">
                                主电
                            </template>
                            <template v-else-if="scope.row.power_type == 2">
                                备电
                            </template>
                            <template v-else>
                                其他
                            </template>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="manufacturer" label="制造商" align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="setup_date" label="装机日期" align="center" />
                <el-table-column prop="project_name" label="项目" align="center" :show-overflow-tooltip="true" />

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
    <!-- 设备布点图查询 -->
    <div class="recordBox" v-if="recordData.propsRecordType == 10">
        <div class="demandBox">
            <div class="selectBox">
                <div class="selectorBox">
                    小区 &nbsp;
                    <el-select v-model="recordData.areaSlect" placeholder="请选择小区" clearable @visible-change="visibleAreaList"
                        @change="selectFun(recordData.areaSlect, 1)" @clear="clearStation(1)">
                        <el-option v-for="item in recordData.areaList" :key="item.id" :label="item.name"
                            :value="item.id" />
                    </el-select>
                </div>
                <div class="selectorBox">
                    楼宇 &nbsp;
                    <el-select v-model="recordData.buildingSlect" placeholder="请选择楼宇" clearable
                        @change="selectFun(recordData.buildingSlect, 2)" @clear="clearStation(2)" @visible-change="visibleBuild">
                        <el-option v-for="item in recordData.buildingList" :key="item.id" :label="item.name"
                            :value="item.id" />
                    </el-select>
                </div>
                <div class="selectorBox">
                    楼层 &nbsp;
                    <el-select v-model="recordData.floorsSlect" placeholder="请选择楼层" clearable
                        @change="selectFun(recordData.floorsSlect, 3)" @clear="clearStation(3)" @visible-change="visibleBuild">
                        <el-option v-for="item in recordData.floorsList" :key="item.id" :label="item.name"
                            :value="item.name" />
                    </el-select>
                </div>
            </div>
            <div class="btnBox">
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
                <el-table-column prop="area_name" label="小区" align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="build_name" label="楼宇" align="center" />
                <el-table-column prop="name" label="楼层" align="center" />
                <el-table-column label="操作" width="80" align="center">
                    <template #default="scope">
                        <div class="operation" @click="openDetail(scope.row)">
                            查看
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
    <!-- 平面图查询 -->
    <div class="recordBox" v-if="recordData.propsRecordType == 11">
        <div class="demandBox">
            <div class="selectBox">
                <div class="selectorBox">
                    项目 &nbsp;
                    <el-select v-model="recordData.projectSelect" placeholder="请选择项目" @visible-change="visibleObjectList"
                        @change="selectFun(recordData.projectSelect, 1)" clearable>
                        <el-option v-for="item in recordData.projectList" :key="item.id" :label="item.name"
                            :value="item.id" />
                    </el-select>
                </div>
                <div class="selectorBox">
                    图纸类型 &nbsp;
                    <el-select v-model="recordData.imgTypeSelect" placeholder="请选择" clearable
                        @change="selectFun(recordData.imgTypeSelect, 2)">
                        <el-option v-for="item in recordData.planList" :key="item.id" :label="item.name"
                            :value="item.id" />
                    </el-select>
                </div>
            </div>
            <div class="btnBox">
                <div class="derive" @click="refreshTwo">刷新</div>
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
                <el-table-column prop="name" label="名称" align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="picture_type_name" label="类型 " align="center" />
                <el-table-column label="操作" align="center">
                    <template #default="scope">
                        <div class="operation" @click="openDetail(scope.row)">
                            查看
                        </div>
                    </template>

                </el-table-column>
            </el-table>
        </div>
        <div class="pagingBigBox">
            <template v-if="recordData.tableData.length != 0">
                <div class="pagingBox">
                    <el-pagination layout="total,prev, pager, next,jumper " :total="recordData.total"
                        :page-size="recordData.page_size" @current-change="handleCurrentChange"
                        :current-page="recordData.requestObject.page" />
                </div>
            </template>

        </div>
    </div>
    <!-- 控制室信息 -->
    <div class="recordBox" v-if="recordData.propsRecordType == 12">
        <div class="demandBox">
            <div class="selectBox">
                <div class="selectorBox">
                    <el-select v-model="recordData.imgTypeSelect" placeholder="请选择" clearable
                        @change="selectFun(recordData.imgTypeSelect)">
                        <el-option v-for="item in recordData.planList" :key="item.id" :label="item.name"
                            :value="item.id" />
                    </el-select>
                </div>
            </div>
        </div>
        <div class="tableBox">
            <div class="controlRoom">
                <template v-if="recordData.tableData.length == 0">
                    <img class="controlRoomImg" src="../../assets/img/comment/none.svg" alt="" @dragstart.prevent>
                </template>
                <template v-else-if="recordData.tableData.length == 1">
                    <img class="controlRoomImg" :src="recordData.controlRoomImgUrl" alt="" @dragstart.prevent>
                </template>
                <template v-else>
                    <el-carousel indicator-position="outside" v-for="(item, index) in recordData.tableData">
                        <el-carousel-item>
                            <img class="controlRoomImg" :src="recordData.url + item.path" alt="" @dragstart.prevent>
                        </el-carousel-item>
                    </el-carousel>
                </template>
            </div>
        </div>
    </div>
    <detail :detailState="recordData.detailState" :detailData="recordData.detailData" @offDetail="offDetail"></detail>
</template>
<script>
import { reactive, watch, onMounted } from 'vue'
import config from "../../utils/config";
import { Search } from '@element-plus/icons-vue'
import { ElMessage } from "element-plus";
import detail from "../detail/detail"
import popup from "../popup/popup"
import { useStore } from 'vuex'
import objectDetail from "../objectDetail/objectDetail"
import {
    deviceIconsRequest, 
    deviceListRequest,
    controllersListRequest, 
    objectImgRequest, 
    buildingListRequest,
    floorsListRequest, 
    inquireLoopRequest,
    areaListRequest,
    projectListRequest
} from "../../api/baseData";
import { filesListRequest } from "../../api/recordData";

export default {
    components: {
        Search,
        detail,
        popup,
        objectDetail
    },
    props: {
        recordType: Number
    },
    setup(props) {
        let recordData = reactive({
            url: "",
            detailState: false,//控制图片详情组件显示隐藏
            switchBtnActive: 0,
            tableData: [],//表格数据page_size
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
            stationingSlect: "",//是否布点选择器
            // 布点状态
            stationingData: [
                {
                    value: '1',
                    label: '已布点',
                },
                {
                    value: '0',
                    label: '未布点',
                },

            ],
            input: "",
            moreSelect: false,//控制更多筛选显示隐藏
            popupType: 0,//控制弹窗显示隐藏
            objectDetailState: false,//控制项目详情组件显示隐藏
            requestObject: {
                page: 1,
                per_page: 8,
                device_state: "",
                description: "",// 描述
                area_id: "",//小区id
                build_id: "",//楼宇id
                floor_name: "",//楼层名称
                controller_num: "",//控制器号
                loop_num: "",//回路号
                addr_num: "",//地址号
                is_online: "",//是否布点
                picture_type_id: "",//图片类型
                project_id: "",//项目id
                name: "",//kongzhiqi mingcheng 
            },//请求参数
            ImgRequestObject: {
                page: 1,
                per_page: 20,
            },
            request:{
                page:0
            },
            total: 1,
            page_size: 8,
            imgPage_size: 20,
            tableId: 1,//列表序号
            projectSelect: "",//项目选择器
            projectList: [],//项目列表
            imgTypeSelect: "",//图纸类型选择器
            planList: [],//图片类型
            areaSlect: "",//小区选择器
            areaList: [],//小区列表
            buildingSlect: "",//楼宇选择器
            buildingList: [],//楼宇列表
            floorsSlect: "",//楼层选择器
            floorsList: [],//楼层列表,
            controllersSlect: "",//控制器选择器
            controllersList: [],//控制器列表
            loopSlect: "",//回路号 选择器
            loopList: [],//回路号列表
            partNumSlect: "",//部位号选择器
            partNumList: [],//部位号列表,
            detailData: {},
            controlRoomImgUrl: "",//控制室信息图片
        })
        let messageBox = null;
        const store = useStore();
        onMounted(() => {
            firstRequest(store.state.switchRecord)
            recordData.url = config.baseUrl
        })
        // 第一次请求记录 计算总数
        const firstRequest = (type) => {
            // 6 图标查询 7 设备查询 8 设备状态查询 9 控制器查询 10 设备布点图查询 11 平面图查询 12 控制室信息
            if (type == 6) {
                deviceIconsRequest(recordData.ImgRequestObject).then((res) => {
                    recordData.tableData = res.data.items
                    recordData.total = res.data.record_size
                    if (recordData.total==0) return ElMessage({
                            message: '暂无数据',
                            type: 'info',
                            duration: 3 * 1000
                        })
                });
            } else if (type == 7) {
                deviceListRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                    recordData.total = res.data.record_size
                    if (recordData.total==0) return ElMessage({
                            message: '暂无数据',
                            type: 'info',
                            duration: 3 * 1000
                        })
                });
            } else if (type == 8) {
                deviceListRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                    recordData.total = res.data.record_size
                    if (recordData.total==0) return ElMessage({
                            message: '暂无数据',
                            type: 'info',
                            duration: 3 * 1000
                        })
                });
            } else if (type == 9) {
                controllersListRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                    recordData.total = res.data.record_size
                    if (recordData.total==0) return ElMessage({
                            message: '暂无数据',
                            type: 'info',
                            duration: 3 * 1000
                        })
                });
            } else if (type == 10) {
                floorsListRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                    recordData.total = res.data.record_size
                });

            } else if (type == 11) {
                recordData.tableData = []
                recordData.planList = []
                store.state.imgTypeList.forEach((item) => {
                    if (item.type == 2 || item.type == 3 || item.type == 6) {
                        recordData.planList.push(item)
                    }
                })
                if (recordData.planList.length==0) return ElMessage({
                            message: '暂无数据',
                            type: 'info',
                            duration: 3 * 1000
                        })
            } else if (type == 12) {
                recordData.tableData = []
                recordData.planList = []
                store.state.imgTypeList.forEach((item) => {
                    if (item.type == 5) {
                        recordData.planList.push(item)
                    }
                })
            }
        }
        const Request = (type) => {
            // 6 图标查询 7 设备查询 8 设备状态查询 9 控制器查询 10 设备布点图查询 11 平面图查询 12 控制室信息
            if (type == 6) {
                deviceIconsRequest(recordData.ImgRequestObject).then((res) => {
                    recordData.tableData = res.data.items
                });
            } else if (type == 7) {
                deviceListRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                });
            } else if (type == 8) {
                deviceListRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                });
            } else if (type == 9) {
                controllersListRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                });
            } else if (type == 10) {
                floorsListRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                });
            } else if (type == 11) {
                objectImgRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                });
            } else if (type == 12) {

            }
        }
        // 打开图片详情弹窗
        const openDetail = (val) => {
            recordData.detailData = val
            recordData.detailState = true
        }
        // 关闭图片详情弹窗
        const offDetail = (val) => {
            recordData.detailState = val
        }
        // 切换分页
        const handleCurrentChange = (val) => {
            recordData.requestObject.page = val;
            Request(recordData.propsRecordType);
            // 序号
            recordData.tableId = (val - 1) * recordData.requestObject.per_page + 1;
        }
        const ImgHandleCurrentChange = (val) => {
            recordData.ImgRequestObject.page = val;
            Request(recordData.propsRecordType);
        }
        //选择器查询
        const selectFun = (val, num) => {
            if (recordData.propsRecordType == 10) {
                if (num == 1) {
                    if (val) {
                        recordData.requestObject.area_id = val
                        let data = {
                            area_id: val,
                            page: 0
                        }
                        buildingListRequest(data).then((res) => {
                            recordData.buildingList = res.data.items
                        });
                        firstRequest(recordData.propsRecordType)
                    }
                    recordData.buildingSlect = ""
                    recordData.floorsSlect = ""
                } else if (num == 2) {
                    if (val) {
                        recordData.requestObject.build_id = val
                        let data = {
                            build_id: val,
                            page: 0
                        }
                        floorsListRequest(data).then((res) => {
                            recordData.floorsList = res.data.items
                        });
                        firstRequest(recordData.propsRecordType)
                    }
                    recordData.floorsSlect = ""
                } else if (num == 3) {
                    recordData.requestObject.floor_name = val
                    firstRequest(recordData.propsRecordType)
                }
            } else if (recordData.propsRecordType == 11) {
                if (num == 1) {
                    // 项目
                    recordData.requestObject.project_id = val
                    if (recordData.requestObject.picture_type_id == "") {
                        let messageBox = null;
                        messageBox = ElMessage({
                            message: "请选择图片类型",
                            type: "info",
                            duration: 3 * 1000
                        });
                    } else {
                        filesListRequest(recordData.requestObject).then((res) => {
                            recordData.tableData = res.data.items
                            recordData.total = res.data.record_size
                        });
                    }

                } else {
                    // 图纸类型
                    recordData.requestObject.picture_type_id = val
                    if (recordData.requestObject.picture_type_id == "") {

                    } else {
                        filesListRequest(recordData.requestObject).then((res) => {
                            recordData.tableData = res.data.items
                            recordData.total = res.data.record_size
                        });
                    }

                }

                firstRequest(recordData.propsRecordType)
            } else if (recordData.propsRecordType == 12) {
                // 图纸类型
                recordData.requestObject.picture_type_id = val
                if (recordData.requestObject.picture_type_id == "") {
                } else {
                    filesListRequest(recordData.requestObject).then((res) => {
                        recordData.tableData = res.data.items
                        if (recordData.tableData.length == 1) {
                            recordData.controlRoomImgUrl = config.baseUrl  + recordData.tableData[0].path
                        } else if (recordData.tableData.length == 0) {
                            messageBox = ElMessage({
                                message: "暂无数据",
                                type: "info",
                                duration: 3 * 1000
                            });
                        }
                    });
                }
                firstRequest(recordData.propsRecordType)
            }
        }
         // 选择框下拉拉取控制器列表
        const visibleControllers = () => {
            controllersListRequest(recordData.request).then((res) => {
                recordData.controllersList = res.data.items
            });
        }
          // 选择框下拉拉取小区列表
        const visibleAreaList = () => {
            areaListRequest(recordData.request).then((res) => {
                recordData.areaList = res.data.items
            });
        }
         // 选择框下拉拉取项目列表
        const visibleObjectList = () => {
            projectListRequest(recordData.request).then((res) => {
                recordData.projectList = res.data.items
            });
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
        // 设备布点图清空选择器
        const clearStation = (type) => {
            if (type == 1) {
                recordData.requestObject.area_id = ""
                recordData.requestObject.build_id = ""
                recordData.requestObject.floor_name = ""
                recordData.buildingSlect = ""
                recordData.buildingList = []
                recordData.floorsSlect = ""
                recordData.floorsList = []
            } else if (type == 2) {
                recordData.requestObject.build_id = ""
                recordData.requestObject.floor_name = ""
                recordData.floorsSlect = ""
                recordData.floorsList = []
            } else if (type == 3) {
                recordData.requestObject.floor_name = ""
            }
            firstRequest(recordData.propsRecordType)
        }
        //输入框搜索
        const searchFun = (val) => {
            recordData.requestObject.page = 1//页数为1
            recordData.tableId = 1//页数为1

            if (recordData.propsRecordType == 9) {
                recordData.requestObject.name = val
            } else {
                recordData.requestObject.description = val
            }
            firstRequest(recordData.propsRecordType)
        }
        const clear = () => {
            recordData.requestObject.page = 1//页数为1
            recordData.tableId = 1//页数为1
            if (recordData.propsRecordType == 9) {
                recordData.requestObject.name = ""
            } else {
                recordData.requestObject.description = ""
            }

            firstRequest(recordData.propsRecordType)
        }
        // 设备状态记录 筛选报警状态
        const switchRecord = (type) => {
            if (recordData.switchBtnActive == type) {
                recordData.switchBtnActive = 0
                recordData.requestObject.device_state = ""
            } else {
                recordData.switchBtnActive = type//选中样式
                recordData.requestObject.device_state = type
            }

            recordData.input = ""
            recordData.requestObject.description = ""
            // 切换状态 页数重置为1 
            recordData.requestObject.page = 1
            recordData.tableId = (1 - 1) * recordData.requestObject.per_page + 1;
            // 重新计算记录总数
            firstRequest(recordData.propsRecordType)
        }
        // 打开关闭默认筛选
        const switchMoreSelectBox = (type, val) => {
            recordData.moreSelect = !recordData.moreSelect
        }
        const moreSelect = () => {
            recordData.moreSelect = false
            recordData.requestObject.page = 1
            recordData.tableId = 1
            firstRequest(recordData.propsRecordType)
        }
        // 更多筛选清空选择器
        const clrarSlect = (type) => {
            if (type == 1) {
                recordData.loopSlect = ""
                recordData.requestObject.loop_num = ""
                recordData.partNumSlect = ""
                recordData.requestObject.addr_num = ""
                recordData.requestObject.controller_num = ""
                recordData.loopList = []
                recordData.partNumList = []
            } else if (type == 2) {
                recordData.requestObject.loop_num = ""
                recordData.requestObject.addr_num = ""
                recordData.partNumList = []
            }
        }
        // 更多筛选
        const moreSelectFun = (val, type) => {
            if (type == 1) {
                if (val) {
                    recordData.requestObject.controller_num = val//控制器号
                    let loopRequest = {
                        page:0
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
            } else if (type == 2) {
                if (val) {
                    recordData.requestObject.loop_num = val//回路号
                    let deviceRequest = {
                        controller_num: recordData.controllersSlect,
                        loop_num: val,
                        page:0
                    }
                    deviceListRequest(deviceRequest).then((res) => {
                        recordData.partNumList = res.data.items
                    });
                }
                recordData.partNumSlect = ""
                recordData.requestObject.addr_num = ""
            } else if (type == 3) {
                recordData.requestObject.addr_num = val//部位号
            } else if (type == 4) {
                recordData.requestObject.area_id = val//小区id
            } else if (type == 5) {
                recordData.requestObject.is_assign = val//是否布点
            }
        }
        // 刷新
        const refresh = () => {
            recordData.input = ""
            recordData.tableId = 1
            recordData.requestObject.page = 1//页数为1
            recordData.ImgRequestObject.page = 1//页数为1
            recordData.requestObject.description = ""//清空描述
            recordData.requestObject.device_state = "" //清空报警类型
            recordData.requestObject.area_id = ""//清空小区选择查询
            recordData.requestObject.build_id = ""//清空楼宇查询
            recordData.requestObject.floor_name = ""//清空楼层查询
            recordData.requestObject.controller_num = ""//清空控制器选择
            recordData.requestObject.loop_num = ""//清空回路号选择
            recordData.requestObject.addr_num = ""//清空部位号选择
            recordData.requestObject.is_online = ""//清空是否布点查询
            recordData.requestObject.picture_type_id = ""//清空图片类型选择
            recordData.requestObject.project_id = ""//清空项目选择
            recordData.requestObject.name = ""//清空控制器名称选择
            recordData.switchBtnActive = 0//选中样式
            recordData.areaSlect = ""//清空输入框内容
            recordData.buildingSlect = ""//清空输入框内容
            recordData.floorsSlect = ""//清空输入框内容
            recordData.controllersSlect = ""//清空控制器选择器
            recordData.loopSlect = ""//清空回路号选择器
            recordData.partNumSlect = ""//清空部位号选择器
            recordData.stationingSlect = ""//清空是否布点选择器
            recordData.imgTypeSelect = ""//清空图片类型选择器
            recordData.projectSelect = ""//清空项目选择器
            firstRequest(recordData.propsRecordType)
        }
        const refreshTwo = ()=>{
            recordData.requestObject.picture_type_id = ""//清空图片类型选择
            recordData.requestObject.project_id = ""//清空项目选择
                recordData.projectSelect = "",
                recordData.imgTypeSelect = "",
                recordData.tableData = []
                
        }
        watch(props, (newProps) => {
            recordData.propsRecordType = newProps.recordType
            if(newProps.recordType==6){
                recordData.requestObject.per_page = 20
            }else{
                recordData.requestObject.per_page = 8
            }
            recordData.switchBtnActive = 0//选中样式
            recordData.requestObject.page = 1//页数为1
            recordData.ImgRequestObject.page = 1//页数为1
            recordData.tableId = 1//页数为1
            recordData.input = ""//清空输入框内容
            recordData.moreSelect = false//切换记录关闭更多筛选
            recordData.areaSlect = ""//清空输入框内容
            recordData.buildingSlect = ""//清空输入框内容
            recordData.floorsSlect = ""//清空输入框内容
            recordData.controllersSlect = ""//清空控制器选择器
            recordData.loopSlect = ""//清空回路号选择器
            recordData.partNumSlect = ""//清空地址号选择器
            recordData.stationingSlect = ""//清空是否布点选择器
            recordData.imgTypeSelect = ""//清空图片类型选择器
            recordData.projectSelect = ""//清空项目选择器
            recordData.requestObject.description = ""//清空描述
            recordData.requestObject.device_state = "" //清空报警类型
            recordData.requestObject.area_id = ""//清空小区选择查询
            recordData.requestObject.build_id = ""//清空楼宇查询
            recordData.requestObject.floor_name = ""//清空楼层查询
            recordData.requestObject.is_online = ""//清空是否布点查询
            recordData.requestObject.picture_type_id = ""//清空图片类型选择
            recordData.requestObject.project_id = ""//清空项目选择
            recordData.requestObject.controller_num = ""//清空控制器选择
            recordData.requestObject.loop_num = ""//清空回路号选择
            recordData.requestObject.addr_num = ""//清空地址号选择
            recordData.requestObject.name = ""//清空控制器名称选择
            firstRequest(recordData.propsRecordType)
            recordData.projectList = store.state.projectList
            recordData.areaList = store.state.areaList
            // recordData.controllersList = store.state.controllersList
        }
        );
        return {
            recordData,
            Request,
            firstRequest,
            handleCurrentChange,
            ImgHandleCurrentChange,
            searchFun,
            switchRecord,//设备状态查询 切换报警状态
            switchMoreSelectBox,//更多筛选显示隐藏
            selectFun,//选择器筛选
            clearStation,
            refresh,
            moreSelect,
            clrarSlect,
            moreSelectFun,//更多筛选
            openDetail,
            offDetail,
            clear,
            refreshTwo,
            visibleControllers,
            visibleAreaList,
            visibleObjectList,
            visibleLoop,
            visibleAddrnum,
            visibleBuild,
            visibleFloor
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
            height: 160px;
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

                .testTextBox {
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
            }

            // 更多筛选 确认按钮
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

        // 表格操作按钮
        .operation {
            color: #4A5CD5;
            text-decoration: underline;
            cursor: pointer;
        }

        // 布点状态div
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
            .deviuceImg{
                width: 40px;
                height: 40px;
            }
        }

        // 控制室信息
        .controlRoom {
            width: 1720px;
            margin-left: 20px;
            height: 720px;
            margin-top: 20px;

            .controlRoomImg {
                width: 1720px;
                height: 720px;
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

    // 图例查询
    .imgInquire {
        width: 1680px;
        height: 656px;
        margin-left: 40px;
        display: flex;
        flex-wrap: wrap;

        .deviceBox {
            margin-top: 64px;
            margin-left: 40px;

            .deviceImgBox {
                width: 126px;
                height: 126px;

                .deviceImg {
                    width: 126px;
                    height: 126px;
                }
            }

            .deviceTextBox {
                width: 126px;
                font-size: 20px;
                font-weight: 500;
                color: #000000;

            }
        }

    }


}
</style>