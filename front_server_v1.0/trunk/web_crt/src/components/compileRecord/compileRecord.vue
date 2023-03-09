<template >
    <!-- 项目列表 -->
    <div class="recordBox" v-if="recordData.propsRecordType == 11" v-loading="recordData.loading">
        <div class="demandBox">
            <div class="selectBox">
                <div class="selectorBox">
                    <el-input v-model="recordData.input" placeholder="请输入项目名称查询" clearable @clear="clear">
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
                <div class="new" @click="openPopup(7)">新建项目</div>
                <div class="derive" @click="refresh">刷新</div>
            </div>
        </div>
        <div class="tableBox">
            <el-table :data="recordData.tableData" class="alarmsTable"
                :header-cell-style="{ color: '#000000', backgroundColor: '#F8F9FC' }">
                <el-table-column type="index" label="序号" align="center">
                    <template #default="scope">
                        <div class="deviceState">
                            <div :class="scope.$index <= 2 ? 'highlight-index' : ''">
                                {{ scope.$index + recordData.tableId }}</div>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="name" label="项目名称" align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="address" label="项目地址 " align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="mobile" label="项目电话 " align="center" />
                <!-- <el-table-column label="是否为主项目" align="center">
                    <template #default="scope">
                        <div class="deviceState">
                            <template v-if="scope.row.is_active != 0">
                                是
                            </template>
                            <template v-else>
                                否
                            </template>

                        </div>
                    </template>
                </el-table-column> -->
                <el-table-column label="操作" align="center">
                    <template #default="scope">
                        <div class="objectList">
                            <div class="objectListBtn" @click="openObjectDetail(scope.row)">
                                <img class="examinObjectIcon" src="../../assets/img/comment/examinObjectIcon.svg"
                                    alt="" @dragstart.prevent>
                            </div>
                            <div class="objectListBtn" @click="openPopup(8, scope.row)">
                                <img class="examinObjectIcon" src="../../assets/img/comment/redactObjectIcon.svg"
                                    alt="" @dragstart.prevent>
                            </div>
                            <div class="objectListBtn" @click="openPopup(9, scope.row)">
                                <img class="examinObjectIcon" src="../../assets/img/comment/deleteObjectIcon.svg"
                                    alt="" @dragstart.prevent>
                            </div>
                            <div class="objectListBtn" @click="openPopup(10, scope.row)">
                                <img class="examinObjectIcon" src="../../assets/img/comment/addObjectIcon.svg" alt="" @dragstart.prevent>
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
    <!-- 小区-楼宇列表 -->
    <div class="recordBox" v-if="recordData.propsRecordType == 12" v-loading="recordData.loading">
        <div class="demandBox">
            <div class="selectBox">
                <div class="selectorBox">
                    <el-input v-model="recordData.input" placeholder="请输入楼宇查询" clearable @clear="clear">
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
                <div class="newAreaBuild" @click="openPopup(14)">创建小区楼宇</div>
                <div class="derive" @click="refresh">刷新</div>
            </div>
        </div>
        <div class="tableBox">
            <el-table :data="recordData.tableData" class="alarmsTable"
                :header-cell-style="{ color: '#000000', backgroundColor: '#F8F9FC' }">
                <el-table-column type="index" label="序号" align="center">
                    <template #default="scope">
                        <div class="deviceState">
                            <div :class="scope.$index <= 2 ? 'highlight-index' : ''">
                                {{ scope.$index + recordData.tableId }}</div>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="area_name" label="小区" align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="name" label="楼宇 " align="center" />
                <el-table-column label="图片 " align="center">
                    <template #default="scope">
                        <div class="deviceState">

                            <div class="deviuceStateImg" @click="openDetail(scope.row)">
                                <img class="deviuceStateimg" src="../../assets/img/comment/imgImg.svg" alt="" @dragstart.prevent>
                            </div>
                        </div>
                    </template>
                </el-table-column>

                <el-table-column label="操作" align="center">
                    <template #default="scope">
                        <div class="objectList">
                            <div class="objectListBtn" @click="openPopup(13, scope.row)">
                                <img class="examinObjectIcon" src="../../assets/img/comment/redactObjectIcon.svg"
                                    alt="" @dragstart.prevent>
                            </div>
                            <div class="objectListBtn" @click="openPopup(12, scope.row)">
                                <img class="examinObjectIcon" src="../../assets/img/comment/deleteObjectIcon.svg"
                                    alt="" @dragstart.prevent>
                            </div>
                            <div class="objectListBtn" @click="openPopup(11, scope.row)">
                                <img class="examinObjectIcon" src="../../assets/img/comment/addObjectIcon.svg" alt="" @dragstart.prevent>
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
    <!-- 楼层信息 -->
    <div class="recordBox" v-if="recordData.propsRecordType == 13" v-loading="recordData.loading">
        <div class="demandBox">
            <div class="selectBox">
                <div class="selectorBox">
                    <el-input v-model="recordData.input" placeholder="请输入楼层查询" clearable  @clear="clear">
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
                <div class="moreDeleteFloor" @click="OpenMoreDeleteFloor">批量删除</div>
                <div class="new" @click="openPopup(15)">创建楼层</div>
                <div class="derive" @click="refresh">刷新</div>
            </div>
        </div>
        <div class="tableBox">
            <el-table :data="recordData.tableData" class="alarmsTable" @selection-change="handleFloors"
                :header-cell-style="{ color: '#000000', backgroundColor: '#F8F9FC' }">
                <el-table-column type="selection"></el-table-column>
                <el-table-column type="index" label="序号" align="center">
                    <template #default="scope">
                        <div class="deviceState">
                            <div :class="scope.$index <= 2 ? 'highlight-index' : ''">
                                {{ scope.$index + recordData.tableId }}</div>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="area_name" label="小区" align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="build_name" label="楼宇 " align="center" />
                <el-table-column prop="name" label="楼层 " align="center" />
                <el-table-column label="图片 " align="center">
                    <template #default="scope">
                        <div class="deviceState">
                            <div class="deviuceStateImg" @click="openDetail(scope.row)">
                                <img class="deviuceStateimg" src="../../assets/img/comment/imgImg.svg" alt="" @dragstart.prevent>
                            </div>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column label="操作" align="center">
                    <template #default="scope">
                        <div class="objectList">
                            <div class="objectListBtn" @click="openPopup(16, scope.row)">
                                <img class="examinObjectIcon" src="../../assets/img/comment/redactObjectIcon.svg"
                                    alt="" @dragstart.prevent>
                            </div>
                            <div class="objectListBtn" @click="openPopup(17, scope.row)">
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
             <!-- 删除楼层弹窗 -->
        <div class="deleteFloor">
            <el-dialog v-model="recordData.deleteFloorsShow" :show-close="false">
                <template #header>
                    <div class="headerBox">是否删除以下楼层</div>
                    <div class="offBtn" @click="OffMoreDeleteFloor">✖</div>
                </template>
                <div class="logoutMsg">
                    <el-table :data="recordData.deleteFloorTableData" class="alarmsTable"
                        :header-cell-style="{ color: '#000000', backgroundColor: '#F8F9FC' }">
                        <el-table-column type="index" label="序号" align="center">
                            <template #default="scope">
                                <div class="deviceState">
                                    <div :class="scope.$index <= 2 ? 'highlight-index' : ''">
                                        {{ scope.$index + recordData.tableId }}</div>
                                </div>
                            </template>
                        </el-table-column>
                        <el-table-column prop="area_name" label="小区" align="center" />
                        <el-table-column prop="build_name" label="楼宇" align="center" />
                        <el-table-column prop="name" label="楼层 " align="center" :show-overflow-tooltip="true" />
                        <el-table-column prop="picture_type_name" label="图片类型 " align="center" />
                        <!-- <el-table-column prop="floor" label="楼层" align="center" /> -->
                    </el-table>
                </div>

                <div class="sureBox">
                    <button class="sureBtn" @click="detaleFloors(recordData.floorsIdstr)">确定</button>
                    <button class="cancelBtn" @click="OffMoreDeleteFloor">取消</button>
                </div>
            </el-dialog>
        </div>
    </div>
    <!-- 控制器设置 -->
    <div class="recordBox" v-if="recordData.propsRecordType == 14" v-loading="recordData.loading">
        <div class="demandBox">
            <div class="selectBox">
                <div class="selectorBox">
                    <el-input v-model="recordData.input" placeholder="请输入控制器名称" clearable @clear="clear">
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
                <div class="operationText">
                    <a :href="recordData.templateUrl">下载模板</a>
                    </div>
                <div class="new" @click="openPopup(23)">上传文件</div>
                <div class="derive" @click="refresh">刷新</div>
            </div>
        </div>
        <div class="tableBox">
            <el-table :data="recordData.tableData" class="alarmsTable"
                :header-cell-style="{ color: '#000000', backgroundColor: '#F8F9FC' }">
                <el-table-column type="index" label="序号" align="center">
                    <template #default="scope">
                        <div class="deviceState">
                            <div :class="scope.$index <= 2 ? 'highlight-index' : ''">
                                {{ scope.$index + recordData.tableId }}</div>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="name" label="控制器名称" align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="code" label="编号" align="center" />
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
                <el-table-column prop="setup_date" label="装机日期" align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="project_name" label="项目" align="center" :show-overflow-tooltip="true" />
                <el-table-column label="操作" align="center">
                    <template #default="scope">
                        <div class="objectList">
                            <div class="objectListBtn" @click="openPopup(18, scope.row)">
                                <img class="examinObjectIcon" src="../../assets/img/comment/redactObjectIcon.svg"
                                    alt="" @dragstart.prevent>
                            </div>
                            <div class="objectListBtn" @click="openPopup(25, scope.row)">
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
        <!-- 单个上传控制器 -->
        <el-dialog v-model="recordData.onlyUpFileShow" :show-close="false">
            <template #header>
                <div class="headerBox">上传控制器</div>
                <div class="offBtn" @click="offonlyUpFileShow">✖</div>
            </template>
            <div class="onlyUpFileBox">
                <div class="onlySelectBox">
                    <div class="onlySelect">
                        <div class="onlySelectText">
                            已上传控制器:
                        </div>
                        <div class="onlyselect">
                            <el-select v-model="recordData.OnlyControllersSlect" placeholder="请选择控制器" clearable
                                @change="onlyController(recordData.OnlyControllersSlect)">
                                <el-option v-for="item in recordData.OnlyControllersList" :key="item.id"
                                    :label="item.name" :value="item.code" />
                            </el-select>
                        </div>
                    </div>
                    <div class="onlySelect">
                        <!-- <div class="onlySelectText">
                            <span style="color: red;">*</span> PSN显示:
                        </div>
                        <div class="onlyselect">
                            <el-select v-model="recordData.OnlyControllersSlect" placeholder="请选择控制器" clearable
                                @visible-change="visibleControllers"
                                @change="moreSelectFun(recordData.OnlyControllersSlect, 1)">
                                <el-option v-for="item in recordData.OnlyControllersList" :key="item.id"
                                    :label="item.name" :value="item.code" />
                            </el-select>
                        </div> -->
                    </div>
                </div>
                <div class="onlySelectBox">
                    <div class="onlySelect">
                        <div class="onlySelectText">
                            <span style="color: red;">*</span> 名称:
                        </div>
                        <div class="onlyselect">
                            <el-input v-model="recordData.onlyControllerName" placeholder="请输入控制器名称" clearable>
                            </el-input>
                        </div>
                    </div>
                    <div class="onlySelect">
                        <div class="onlySelectText">
                            <span style="color: red;">*</span> 编号:
                        </div>
                        <div class="onlyselect">
                            <el-input v-model="recordData.onlyControllerCode" placeholder="请输入控制器编号" clearable>
                            </el-input>
                        </div>
                    </div>
                </div>
                <div class="onlySelectBox">
                    <div class="onlySelect">
                        <div class="onlySelectText">
                            <span style="color: red;">*</span> 装机日期:
                        </div>
                        <div class="onlyselect">
                            <el-input v-model="recordData.onlyControllerSetDate" placeholder="请输入格式:2010-08-08"
                                clearable>
                            </el-input>
                        </div>
                    </div>
                    <div class="onlySelect">
                        <div class="onlySelectText">
                            <span style="color: red;">*</span> 型号:
                        </div>
                        <div class="onlyselect">
                            <el-input v-model="recordData.onlyControllerModel" placeholder="请输入控制器型号" clearable>
                            </el-input>
                        </div>
                    </div>
                </div>
                <div class="onlySelectBox">
                    <div class="onlySelect">
                        <div class="onlySelectText">
                            <span style="color: red;">*</span> 制造商:
                        </div>
                        <div class="onlyselect">
                            <el-input v-model="recordData.onlyControllerManufacturer" placeholder="请输入重置密码" clearable>
                            </el-input>
                        </div>
                    </div>
                    <div class="onlySelect">
                        <div class="onlySelectText">
                            主从机选择:
                        </div>
                        <div class="onlyselect">
                            <el-select v-model="recordData.onlyControllerType" placeholder="请选择控制器类型" clearable>
                                <el-option v-for="item in recordData.onlyControllerTypeList" :key="item.value"
                                    :label="item.label" :value="item.value" />
                            </el-select>
                        </div>
                    </div>
                </div>
            </div>
            <div class="sureBox">
                <button class="sureBtn" @click="onlyUp">导入</button>
            </div>
        </el-dialog>
    </div>
    <!-- 设备设置 -->
    <div class="recordBox" v-if="recordData.propsRecordType == 15" v-loading="recordData.loading">
        <div class="demandBox">
            <div class="selectBox">
                <div class="selectorBox">
                    <el-input v-model="recordData.input" placeholder="请输入描述查询" clearable @clear="clear">
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
                <div class="operationText">
                    <a :href="recordData.templateUrl">下载模板</a>
                    </div>
                <!-- <div class="deleteBtn"  ><a :href="recordData.templateUrl">下载模板</a></div> -->
                <div class="deleteBtn" @click="openDeviceShow()">删除设备</div>
                <div class="new" @click="openPopup(24)">上传文件</div>
                <div class="more" @click="switchMoreSelectBox">更多筛选</div>
                <div class="derive" @click="refresh">刷新</div>
            </div>
        </div>
        <div class="tableBox">
            <el-table :data="recordData.tableData" class="alarmsTable" @selection-change="handleSelectionChange"
                :header-cell-style="{ color: '#000000', backgroundColor: '#F8F9FC' }">
                <el-table-column type="selection"></el-table-column>
                <el-table-column type="index" label="序号" align="center">
                    <template #default="scope">
                        <div class="deviceState">
                            <div :class="scope.$index <= 2 ? 'highlight-index' : ''">
                                {{ scope.$index + recordData.tableId }}</div>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="device_type_name" label="类型" align="center" />
                <el-table-column prop="current" label="地址号" align="center" />
                <el-table-column prop="description" label="注释" align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="area" label="小区 " align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="unit" label="单元 " align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="build" label="楼宇 " align="center" />
                <el-table-column prop="floor" label="楼层" align="center" />
                <el-table-column prop="district" label="防火分区" align="center" />
                <el-table-column prop="room" label="防烟分区" align="center" />
                <el-table-column label="布点状态" align="center">
                    <template #default="scope">
                        <div class="deviceState">
                            <template v-if="scope.row.is_assign != 0">
                                <div class="deviuceStateText">{{ scope.row.xuhao }} </div>
                                <div class="deviuceStateImg" @click="openDetail(scope.row)">
                                    <img class="deviuceStateimg" src="../../assets/img/comment/imgImg.svg" alt="" @dragstart.prevent>
                                </div>
                            </template>

                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="manufacturer" label="厂商" align="center" :show-overflow-tooltip="true" />
                <el-table-column label="状态" align="center">
                    <template #default="scope">
                        <div class="deviceState">
                            注册:是 <br>
                            在线:是
                        </div>
                    </template>
                </el-table-column>
                <el-table-column label="操作" align="center">
                    <template #default="scope">
                        <div class="objectList">
                            <div class="objectListBtn" @click="openPopup(19, scope.row)">
                                <img class="examinObjectIcon" src="../../assets/img/comment/redactObjectIcon.svg"
                                    alt="" @dragstart.prevent>
                            </div>
                            <div class="objectListBtn" @click="openDeviceOnlyShow(scope.row)">
                                <img class="examinObjectIcon" src="../../assets/img/comment/deleteObjectIcon.svg"
                                    alt="" @dragstart.prevent>
                            </div>
                        </div>
                    </template>
                </el-table-column>
            </el-table>
            <!-- 更多筛选 -->
            <div class="moreSelectBox" v-show="recordData.moreSelect">
                <div class="testMsgBox">
                    <div class="testTextBox">控制器号</div>
                    <div class="testSelectBox">
                        <el-select v-model="recordData.controllersSlect" placeholder="请选择控制器" clearable
                            @visible-change="visibleControllers"
                            @change="moreSelectFun(recordData.controllersSlect, 1)">
                            <el-option v-for="item in recordData.controllersList" :key="item.id" :label="item.name"
                                :value="item.code" />
                        </el-select>
                    </div>
                </div>
                <div class="testMsgBox">
                    <div class="testTextBox">回路</div>
                    <div class="testSelectBox">
                        <el-select v-model="recordData.loopSlect" placeholder="请选择回路号" clearable
                            @change="moreSelectFun(recordData.loopSlect, 2)">
                            <el-option v-for="(item, index) in recordData.loopList" :key="item" :label="item"
                                :value="item" />
                        </el-select>
                    </div>
                </div>
                <div class="testMsgBox">
                    <div class="testTextBox">地址</div>
                    <div class="testSelectBox">
                        <el-select v-model="recordData.partNumSlect" placeholder="请选择地址号" clearable
                            @change="moreSelectFun(recordData.partNumSlect, 3)">
                            <el-option v-for="item in recordData.partNumList" :key="item.addr_num"
                                :label="item.addr_num" :value="item.addr_num" />
                        </el-select>
                    </div>

                </div>
                <div class="testMsgBox">
                    <div class="testTextBox">布点</div>
                    <div class="testSelectBox">
                        <el-select v-model="recordData.stationingSlect" placeholder="请选择布点状态" clearable
                            @change="moreSelectFun(recordData.stationingSlect, 4)">
                            <el-option v-for="item in recordData.stationingList" :key="item.value" :label="item.label"
                                :value="item.value" />
                        </el-select>
                    </div>

                </div>
                <div class="sureBtnBox">
                    <div class="sureBtn" @click="switchMoreSelectBox(false)"> <img
                            src="../../assets/img/comment/searchImg.svg" alt="" @dragstart.prevent>&nbsp; 查询</div>
                </div>
            </div>
        </div>
        <div class="pagingBigBox">
            <div class="pagingBox">
                <el-pagination layout="total,prev, pager, next,jumper " :total="recordData.total"
                    :page-size="recordData.page_size" @current-change="handleCurrentChange"
                    :current-page="recordData.requestObject.page" />
            </div>
        </div>
        <div class="deleteBox">
            <!-- 删除设备弹窗 -->
            <el-dialog v-model="recordData.deleteDevicesShow" :show-close="false">
                <template #header>
                    <div class="headerBox">是否删除以下设备</div>
                    <div class="offBtn" @click="offDeviceShow">✖</div>
                </template>
                <div class="logoutMsg">
                    <el-table :data="recordData.deleteTableData" class="alarmsTable"
                        :header-cell-style="{ color: '#000000', backgroundColor: '#F8F9FC' }">
                        <el-table-column type="index" label="序号" align="center">
                            <template #default="scope">
                                <div class="deviceState">
                                    <div :class="scope.$index <= 2 ? 'highlight-index' : ''">
                                        {{ scope.$index + recordData.tableId }}</div>
                                </div>
                            </template>
                        </el-table-column>
                        <el-table-column prop="device_type_name" label="类型" align="center" />
                        <el-table-column prop="current" label="地址号" align="center" />
                        <el-table-column prop="area" label="小区 " align="center" :show-overflow-tooltip="true" />
                        <el-table-column prop="build" label="楼宇 " align="center" />
                        <el-table-column prop="floor" label="楼层" align="center" />
                    </el-table>
                </div>

                <div class="sureBox">
                    <button class="sureBtn" @click="deleteDevice">确定</button>
                    <button class="cancelBtn" @click="offDeviceShow">取消</button>
                </div>
            </el-dialog>
        </div>
        <div class="deleteOnlyBox">
            <!-- 删除设备弹窗 -->
            <el-dialog v-model="recordData.deleteDeviceShow" :show-close="false">
                <template #header>
                    <div class="headerBox">是否删除该设备</div>
                    <div class="offBtn" @click="offDeviceOnlyShow">✖</div>
                </template>
                <div class="deviceBox">
                    <div class="topBox">
                        <div class="leftBox">
                            <div class="deviceName">设备类型:{{recordData.deleteDeviceData.device_type_name}}</div>
                            <div class="deviceName">地址号:{{recordData.deleteDeviceData.current}}</div>
                            <div class="deviceName">PSN:{{recordData.deleteDeviceData.psn}}</div>
                        </div>
                        <div class="rightBox">
                            <div class="deviceName">
                                <img class="deviceImg"
                                    :src="recordData.url+recordData.deleteDeviceData.path" alt="" @dragstart.prevent>
                            </div>
                        </div>
                    </div>
                    <div class="bottomBox">
                        <div class="deviceName">描述:{{recordData.deleteDeviceData.description}}</div>
                        <div class="deviceName">制造商:{{recordData.deleteDeviceData.manufacturer}}</div>
                        <div class="deviceName">装机日期:{{recordData.deleteDeviceData.setup_date}}</div>
                        <div class="deviceName">设备状态:{{recordData.deleteDeviceData.dev_state}}</div>
                        <template v-if="recordData.deleteDeviceData.is_assign==1">
                            <div class="deviceName">布点情况:已布点</div>
                        </template>
                        <template v-else>
                            <div class="deviceName">布点情况:未布点</div>
                        </template>


                    </div>
                </div>
                <div class="sureBox">
                    <button class="sureBtn" @click="deleteDevice">确定</button>
                    <button class="cancelBtn" @click="offDeviceOnlyShow">取消</button>
                </div>
            </el-dialog>
        </div>
    </div>
    <!-- 设备类型列表 -->
    <div class="recordBox" v-if="recordData.propsRecordType == 17" v-loading="recordData.loading">
        <div class="deviceTypeBox">
            <div class="infinite-list">
                <div class="infinite-list-item" v-for="(item, index) in recordData.deviceIconData">
                    <div class="xuhao">{{ index + 1 }}</div>
                    <div class="deviceName"> {{ item.name }}</div>
                    <div class="deviceIcon">
                        <img class="deviceState" :src="recordData.imgUrl + item.path" alt="" :title="item.name" @dragstart.prevent>
                    </div>
                </div>
            </div>
            <div class="noneBox"></div>
            <div class="deviceTypeSelectBox">
                <div class="selectBox">
                    <div class="selectorBox">
                        <el-select v-model="recordData.deviceTypeImgSelect" placeholder="请选择设备类型" clearable
                            @change="deviceTypeImg(recordData.deviceTypeImgSelect)">
                            <el-option v-for="item in recordData.deviceTypeList" :key="item.id" :label="item.name"
                                :value="item.id" />
                        </el-select>
                    </div>
                    <div class="fileBox">
                        <input type="file" @change="changeDeviceIcon" placeholder="上传文件">
                    </div>
                    <div class="BtnBox">
                        <template v-if="recordData.deciceIconState == true">
                            <button class="removeButton" @click="addDeviceIcon">新增</button>
                        </template>
                        <template v-else-if="recordData.deciceIconState == false">
                            <button class="removeButton" @click="putDeviceIcon">修改</button>
                        </template>
                    </div>

                </div>
            </div>
        </div>
    </div>
    <station :stationState="recordData.stationState"></station>
    <detail :detailState="recordData.detailState" :detailData="recordData.detailData" @offDetail="offDetail"></detail>
    <objectDetail :objectDetailState="recordData.objectDetailState" :objectDetailData="recordData.objectDetailData"
        @offObjectDetail="offObjectDetail"></objectDetail>
    <popup :popupType="recordData.popupType" :popupData="recordData.popupData" @offPopup="offPopup" @sure="sure">
    </popup>
</template>
<script>
import { reactive, watch, onMounted } from 'vue'
import popup from "../popup/popup"
import detail from "../detail/detail"
import config from "../../utils/config";
import { Search } from '@element-plus/icons-vue'
import { useStore } from 'vuex'
import axios from "axios";
import station from "../../components/stationing/stationing.vue"
// import station from "../../components/stationing/station.vue"
import { ElMessage } from 'element-plus'
import objectDetail from "../objectDetail/objectDetail"
import {
    projectListRequest,
    buildingListRequest,
    floorsListRequest,
    controllersListRequest,
    inquireLoopRequest,
    deviceListRequest,
    deviceIconRequest
} from "../../api/baseData";
import {
    addObjectRequest,
    deleteObjectRequest,
    revampObjectRequest,
    deteleBuildsRequest,
    deteleFloorsRequest,
    revampDevicesRequest,
    revampControllersRequest,
    addControllersRequest,
    deleteControllersRequest,
    getHelpRequest,
    deleteDevicesRequest
} from "../../api/operation";
import { forEach } from 'lodash'
export default {
    emits: ['recordSwitch'],
    components: {
        Search,
        popup,
        detail,
        objectDetail,
        station
    },
    props: {
        recordType: Number
    },
    setup(props, context) {
        const store = useStore();
        let recordData = reactive({
            templateUrl:"",//下载模板UrL
            loading: false,
            deviceIconData: [],//设备图标列表
            deviceTypeList: [],//设备类型列表
            deciceIconState: false,
            deviceTypeImgSelect: "",//图标选择器
            deviceImg: {},
            imgUrl: "",
            fileList: [],
            detailData: {},
            detailState: false,//控制图片详情组件显示隐藏
            url: "",
            objectDetailData: {},
            objectDetailState: false,//控制项目详情组件显示隐藏
            tableData: [],
            propsRecordType: 1,
            stationState: false,
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
            input: "",
            moreSelect: false,//控制更多筛选显示隐藏
            requestObject: {
                page: 1,
                per_page: 8,
                user_id: "",//用户id
                name: "",//项目名称
                build_name: "",//楼宇名称
                floor_name: "",//楼层名称
                name: "",//控制器名称
                description: "",//设备关键字查询
                loop_num: "",//回路号
                addr_num: "",//地址号
                controller_num: "",//控制器号
                is_assign: "",//是否布点
            },//请求参数
            Request: {
                page: 0
            },
            total: 1,//表格总条数
            tableId: 1,//列表序号
            page_size: 8,
            userList: [],//用户列表
            popupType: 0,//控制弹窗显示隐藏
            popupData: {},
            deteleData: {
                project_id: ""
            },
            controllersSlect: "",//控制器选择器
            controllersList: [],//控制器列表
            loopSlect: "",//回路号 选择器
            loopList: [],//回路号列表
            partNumSlect: "",//部位号选择器
            partNumList: [],//部位号列表
            stationingSlect: "",//设备布点状态
            stationingList: [
                {
                    value: '0',
                    label: '未布点',
                },
                {
                    value: '1',
                    label: '已布点',
                },

            ],//设备布点状态
            onlyUpFileShow: false,//单个控制器上传弹窗
            OnlyControllersSlect: "",//单个控制器选择器
            OnlyControllersList: [],//单个控制器选择器数组
            onlyControllerName: "",//
            onlyControllerCode: "",//
            onlyControllerSetDate: "",//
            onlyControllerModel: "",//
            onlyControllerId: "",
            onlyControllerManufacturer: "",
            onlyControllerType: "",
            onlyControllerTypeList: [
                {
                    value: 1,
                    label: '主机',
                },
                {
                    value: 2,
                    label: '从机',
                },
            ],
            deleteDevicesShow: false,
            deleteDeviceShow: false,
            deleteTableData: [],
            deleteDeviceIdstr: "",
            deleteDeviceState: false,//判断是否未单个删除设备
            deleteDeviceData: {},
            floorsIdstr:"",//批量删除楼层id
            deleteFloorTableData:[],
            deleteFloorsShow:false,
        })
        onMounted(() => {
            recordData.url = config.baseUrl
            recordData.userList = store.state.userList
            recordData.controllersList = store.state.controllersList
            recordData.deviceTypeList = store.state.deviceTypeList
        })
        const handleSelectionChange = (val) => {
            recordData.deleteTableData = val
            // 获取批量删除 设备id
            var idstr = "";
            val.forEach((item) => {
                idstr += item.id + ",";
            })
            idstr = idstr.substring(0, idstr.length - 1)
            recordData.deleteDeviceIdstr = idstr
        }
        // 打开删除设备弹窗
        const openDeviceShow = () => {
            recordData.deleteDevicesShow = true
        }
        const offDeviceShow = () => {
            recordData.deleteDevicesShow = false

        }
        const openDeviceOnlyShow = (val) => {
            recordData.deleteDeviceShow = true
            recordData.deleteDeviceData = val
            recordData.deleteDeviceIdstr = val.id.toString()
        }
        const offDeviceOnlyShow = () => {
            recordData.deleteDeviceShow = false
            recordData.deleteDeviceData = {}
            recordData.deleteDeviceIdstr = ""
        }
        const deleteDevice = () => {
            let data = {
                device_ids: recordData.deleteDeviceIdstr
            }
            if(data.device_ids=="") return ElMessage({
                        message: '请勾选要删除的设备,再进行删除',
                        type: 'error',
                        duration: 3 * 1000
                    })
            deleteDevicesRequest(data).then((res) => {
                if (res.ok) {
                    ElMessage({
                        message: '删除成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    recordData.deleteDevicesShow = false
                    recordData.deleteDeviceShow = false
                    recordData.deleteTableData = []
                    recordData.deleteDeviceData = {}
                    recordData.deleteDeviceIdstr = ""
                    refresh()
                }
            });
        }
        const clear = () => {
            recordData.requestObject.page = 1//页数为1
            recordData.tableId = 1//页数为1
            if (recordData.propsRecordType == 1) {
                recordData.requestObject.name = ""
            } else if (recordData.propsRecordType == 2) {
                recordData.requestObject.build_name = ""
            } else if (recordData.propsRecordType == 3) {
                recordData.requestObject.floor_name = ""
            } else if (recordData.propsRecordType == 4) {
                recordData.requestObject.name = ""
            } else if (recordData.propsRecordType == 5) {
                recordData.requestObject.description = ""
            }
            firstRequest(recordData.propsRecordType)
        }
        // 第一次请求记录 计算总数
        const firstRequest = (type) => {
            recordData.loading = true
            // 1 项目列表 2 小区-楼宇列表 3 楼层信息 4 控制器设置 5 设备设置 6 布点图 7 设备类型列表
            if (type == 11) {
                projectListRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                    store.commit('projectListData', res.data.items)
                    recordData.total = res.data.record_size

                    if (recordData.total==0) return ElMessage({
                            message: '暂无数据',
                            type: 'info',
                            duration: 3 * 1000
                        })
                });
            } else if (type == 12) {
                buildingListRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                    store.commit('buildingListData', res.data.items)
                    recordData.total = res.data.record_size
                    if (recordData.total==0) return ElMessage({
                            message: '暂无数据',
                            type: 'info',
                            duration: 3 * 1000
                        })
                });
            } else if (type == 13) {
                floorsListRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                    store.commit('floorsListData', res.data.items)
                    recordData.total = res.data.record_size
                    if (recordData.total==0) return ElMessage({
                            message: '暂无数据',
                            type: 'info',
                            duration: 3 * 1000
                        })
                });
            } else if (type == 14) {
                controllersListRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                    recordData.total = res.data.record_size
                    if (recordData.total==0) return ElMessage({
                            message: '暂无数据',
                            type: 'info',
                            duration: 3 * 1000
                        })
                });
            } else if (type == 15) {
                recordData.loading = true
                deviceListRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                    recordData.total = res.data.record_size
                    if (recordData.total==0) return ElMessage({
                            message: '暂无数据',
                            type: 'info',
                            duration: 3 * 1000
                        })
                });

            } else if (type == 6) {
            } else if (type == 17) {
                recordData.imgUrl = config.baseUrl
                // 设备图标
                deviceIconRequest(recordData.Request).then((res) => {
                    recordData.deviceIconData = res.data.items
                    if (recordData.deviceIconData.length==0) return ElMessage({
                            message: '暂无数据',
                            type: 'info',
                            duration: 3 * 1000
                        })
                });
            }
            if (recordData.tableData) {
                recordData.loading = false
            }
        }
        const Request = (type) => {
            // 1 项目列表 2 小区-楼宇列表 3 楼层信息 4 控制器设置 5 设备设置 6 布点图 7 设备类型列表
            if (type == 11) {
                projectListRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                });
            } else if (type == 12) {
                buildingListRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                });
            } else if (type == 13) {
                floorsListRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                });
            } else if (type == 14) {
                controllersListRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                });
            } else if (type == 15) {
                deviceListRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                });
            } else if (type == 16) {

            } else if (type == 17) {
                recordData.imgUrl = config.baseUrl
                deviceIconRequest(recordData.requestObject).then((res) => {
                    recordData.tableData = res.data.items
                });
            }
        }
        // 选择框下拉拉取控制器列表
        const visibleControllers = () => {
            controllersListRequest(recordData.Request).then((res) => {
                recordData.controllersList = res.data.items
            });
        }
        const deviceTypeImg = (val) => {
            let icon = 0
            recordData.deviceIconData.forEach((item) => {
                if (item.device_type_id == val) {
                    recordData.deviceImg.icon_id = item.id
                    recordData.deciceIconState = false
                    icon = 1
                }
            })
            if (icon == 0) {
                recordData.deviceImg.deviceTypeId = val
                recordData.deciceIconState = true
            }
        }
        // 修改设备图标
        const putDeviceIcon = () => {
            let file = recordData.fileList[0];
            let formData = new FormData();
            formData.append("icon", file);
            formData.append("icon_id", recordData.deviceImg.icon_id);
            axios.put(recordData.url + '/basic_data/device_icons/', formData, {
                headers: {
                    'Authorization': 'Bearer' + ' ' + JSON.parse(sessionStorage.getItem('userInfo'))['token']
                }
            }).then(res => {
                if (res.data.ok == true) {
                    ElMessage({
                        message: '修改成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    recordData.deviceTypeImgSelect = ""
                    firstRequest(7)
                }
            })
        }
        // 新增设备图标
        const addDeviceIcon = () => {
            let file = recordData.fileList[0];
            let formData = new FormData();
            formData.append("icon", file);
            formData.append("device_type_id", recordData.deviceImg.deviceTypeId);
            axios.post(recordData.url + '/basic_data/device_icons/', formData, {
                headers: {
                    'Authorization': 'Bearer' + ' ' + JSON.parse(sessionStorage.getItem('userInfo'))['token']
                }
            }).then(res => {
                if (res.data.ok == true) {
                    ElMessage({
                        message: '新增成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    recordData.deviceTypeImgSelect = ""
                    firstRequest(7)
                }
            })
        }
        const changeDeviceIcon = (event) => {
            recordData.fileList = event.target.files;
        }
        // 打开弹窗
        const openPopup = (type, item) => {
            recordData.popupData = item
            if(type==19){
                store.state.deviceRevampState = false
            }
            
            recordData.popupType = type
        }
        // 关闭弹窗
        const offPopup = (val) => {
            recordData.popupType = 0
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
        // 弹窗功能
        const sure = (popupData, operationType, selectData) => {
            // 7 新建项目 9 删除项目 8 编辑 10快捷创建小区楼宇 13 编辑楼宇 14 新建楼宇
            if (operationType == 7) {
                addObject(popupData)
            } else if (operationType == 9) {
                deleteObject(popupData)
            } else if (operationType == 8) {
                revampObject(popupData, selectData)
            } else if (operationType == 10) {
                newBuilds(popupData)
            } else if (operationType == 11) {
                newFloors(popupData)
            } else if (operationType == 12) {
                deteleBuilds(popupData)
            } else if (operationType == 13) {
                revampBuild(popupData)
            } else if (operationType == 14) {
                newBuilds(popupData)
            } else if (operationType == 15) {
                newFloors(popupData)
            } else if (operationType == 16) {
                revampFloor(popupData)
            } else if (operationType == 17) {
                detaleFloors(popupData)
            } else if (operationType == 18) {
                revampControllersRequest(popupData).then((res) => {
                    if (res.ok) {
                        ElMessage({
                            message: '修改控制器信息成功',
                            type: 'success',
                            duration: 3 * 1000
                        })
                        refresh()
                        recordData.popupType = 0
                    }
                    //新建项目以后 更新项目列表
                    controllersListRequest(recordData.Request).then((res) => {
                        store.commit('controllersListData', res.data.items)
                    });
                });
            } else if (operationType == 19) {
                revampDevice(popupData)
            } else if (operationType == 23) {
                if (selectData == 1) {
                    upFile(popupData)
                } else if (selectData == 2) {
                    onlyUpFile(popupData)
                }
            } else if (operationType == 24) {
                upFileDevice(popupData)
            } else if (operationType == 25) {
                deleteController(popupData)
            }
        }
        // 新增项目
        const addObject = (popupData) => {
            addObjectRequest(popupData).then((res) => {
                    if (res.ok) {
                        ElMessage({
                            message: '创建成功',
                            type: 'success',
                            duration: 3 * 1000
                        })
                        refresh()
                        recordData.popupType = 0
                    }
                    //新建项目以后 更新项目列表
                    projectListRequest(recordData.Request).then((res) => {
                        store.commit('projectListData', res.data.items)
                    });
                    firstRequest(2)
                });
        }
        // 删除项目
        const deleteObject = (popupData) => {
            recordData.deteleData.project_id = popupData
            deleteObjectRequest(recordData.deteleData.project_id).then((res) => {
                if (res.ok) {
                    ElMessage({
                        message: '删除成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    refresh()
                    recordData.popupType = 0
                    //删除项目以后 更新项目列表
                    projectListRequest(recordData.Request).then((res) => {
                        store.commit('projectListData', res.data.items)
                    });
                }
            });
        }
        // 编辑项目
        const revampObject = (popupData, selectData) => {
            let idstr = "" 
            let revampData = {
                project_id: popupData.project_id,
                name: popupData.name,
                address: popupData.address,
                mobile: popupData.mobile,
                is_active:popupData.is_active
            }
            if(selectData){
                selectData.forEach((item) => {
                idstr += item.toString() + ",";
            });
            idstr = idstr.substring(0, idstr.length - 1);
            revampData.user_ids = idstr
            }
            revampObjectRequest(revampData).then((res) => {
                if (res.ok) {
                    ElMessage({
                        message: '修改成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    refresh()
                    recordData.popupType = 0
                    //编辑项目以后 更新项目列表
                    projectListRequest(recordData.Request).then((res) => {
                        store.commit('projectListData', res.data.items)
                    });
                }
            });
        }
        // 快捷创建小区楼宇
        const newBuilds = (popupData) => {
            let formData = new FormData();
            if (popupData.file[0]) {
                let file = popupData.file[0];
                formData.append("picture", file);
                formData.append("picture_type_id", 1);
            } else {

            }
            formData.append("name", popupData.name);
            formData.append("start", popupData.start);
            formData.append("end", popupData.end);
            formData.append("area_id", popupData.areaID);
            axios.post(recordData.url + '/build_drawing/builds', formData, {
                headers: {
                    'Authorization': 'Bearer' + ' ' + JSON.parse(sessionStorage.getItem('userInfo'))['token']
                }
            }).then(res => {
                if (res.data.ok == true) {
                    ElMessage({
                        message: '新增楼宇信息成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    recordData.popupType = 0
                    if(sessionStorage.getItem("setSwitchRecord")==12){
                        refresh()
                    }else{
                        context.emit('recordSwitch', 12);
                    }
                   
                }
            })
        }
        // 删除楼宇
        const deteleBuilds = (popupData) => {
            let data = {
                build_id: popupData
            }

            deteleBuildsRequest(data.build_id).then((res) => {
                if (res.ok) {
                    ElMessage({
                        message: '删除楼宇成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    refresh()
                    recordData.popupType = 0
                    //删除楼宇以后更新 楼宇列表
                    buildingListRequest(recordData.Request).then((res) => {
                        store.commit('buildingListData', res.data.items)
                   
                    });
                    
                }
            });
        }
        // 修改楼宇
        const revampBuild = (popupData) => {
            let file = popupData.file[0];
            let formData = new FormData();
            formData.append("picture", file);
            formData.append("name", popupData.name);
            formData.append("picture_type_id", 1);
            formData.append("build_id", popupData.build_id);

            axios.put(recordData.url + '/build_drawing/builds', formData, {
                headers: {
                    'Authorization': 'Bearer' + ' ' + JSON.parse(sessionStorage.getItem('userInfo'))['token']
                }
            }).then(res => {
                if (res.data.ok == true) {
                    ElMessage({
                        message: '修改成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    refresh()
                    recordData.popupType = 0
                    //修改楼宇以后更新 楼宇列表
                    buildingListRequest(recordData.Request).then((res) => {
                        store.commit('buildingListData', res.data.items)
                    });
                }
            })
        }
        // 快捷创建楼层
        const newFloors = (popupData) => {
            let file = popupData.file[0];
            let formData = new FormData();
            formData.append("picture", file);
            formData.append("name", popupData.name);
            formData.append("start", popupData.start);
            formData.append("end", popupData.end);
            formData.append("picture_type_id", 2);
            formData.append("area_id", popupData.area_id);
            formData.append("build_id", popupData.build_id);
            axios.post(recordData.url + '/build_drawing/floors', formData, {
                headers: {
                    'Authorization': 'Bearer' + ' ' + JSON.parse(sessionStorage.getItem('userInfo'))['token']
                }
            }).then(res => {
                if (res.data.ok == true) {
                    ElMessage({
                        message: '新增楼层信息成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    recordData.popupType = 0

                    if(sessionStorage.getItem("setSwitchRecord")==13){
                        refresh()
                    }else{
                        context.emit('recordSwitch', 13);
                    }
                }
            })
        }
        // 修改楼层信息
        const revampFloor = (popupData) => {
            let file = popupData.file[0];
            let formData = new FormData();
            formData.append("picture", file);
            formData.append("floor_id", popupData.floor_id);
            formData.append("name", popupData.name);
            formData.append("picture_type_id", 2);
            axios.put(recordData.url + '/build_drawing/floors', formData, {
                headers: {
                    'Authorization': 'Bearer' + ' ' + JSON.parse(sessionStorage.getItem('userInfo'))['token']
                }
            }).then(res => {
                if (res.data.ok == true) {
                    ElMessage({
                        message: '修改成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    refresh()
                    recordData.popupType = 0
                    // 修改楼层以后 更新楼层列表
                    floorsListRequest(recordData.Request).then((res) => {
                        store.commit('floorsListData', res.data.items)
                    });
                }
            })
        }
        // 删除楼层
        const detaleFloors = (popupData) => {
            let data = {
                floor_ids: popupData
            }
            if(data.floor_ids=="")return   ElMessage({
                        message: '请勾选要删除的楼层,再进行删除',
                        type: 'error',
                        duration: 3 * 1000
                    })
            deteleFloorsRequest(data.floor_ids).then((res) => {
                if (res.ok) {
                    ElMessage({
                        message: '删除成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    refresh()
                    recordData.deleteFloorTableData = []
                    recordData.deleteFloorsShow = false
                    recordData.popupType = 0
                    // 删除楼层以后 更新楼层列表
                    floorsListRequest(recordData.Request).then((res) => {
                        store.commit('floorsListData', res.data.items)
                    });
                }
            });
        }
        // 批量删除楼层 全选事件
        const handleFloors = (val)=>{
            recordData.deleteFloorTableData = val
            // 获取批量删除 楼层id
            var idstr = "";
            val.forEach((item) => {
                idstr += item.id + ",";
            })
            idstr = idstr.substring(0, idstr.length - 1)
            recordData.floorsIdstr = idstr
        }
        // 批量删除
        const OpenMoreDeleteFloor = ()=>{
            recordData.deleteFloorsShow = true
        }
        // 批量删除
        const OffMoreDeleteFloor = ()=>{
            recordData.deleteFloorsShow = false
        }
        const revampDevice = (popupData) => {
            revampDevicesRequest(popupData).then((res) => {
                if (res.ok) {
                    ElMessage({
                        message: '修改设备信息成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    recordData.popupType = 0
                    refresh()
                }
            });
        }
        // 打开项目详情组件
        const openObjectDetail = (val) => {
            recordData.objectDetailData = val
            recordData.objectDetailState = true
        }
        // 关闭项目详情组件
        const offObjectDetail = () => {
            recordData.objectDetailState = false
        }
        // 选择人员 项目
        const selectFun = (val, num) => {

            if (recordData.propsRecordType == 1) {
                if (num == 1) {
                    recordData.requestObject.user_id = val
                } else if (num == 2) {

                }

            } else if (recordData.propsRecordType == 2) {
                // if (num == 1) {
                //     recordData.requestObject.user_id = val
                // } else {
                //     recordData.requestObject.project_id = val
                // }
            } else if (recordData.propsRecordType == 4) {

            }
            firstRequest(recordData.propsRecordType)
        }
        //输入框搜索
        const searchFun = (val) => {
            recordData.requestObject.page = 1//页数为1
            recordData.tableId = 1//页数为1
            if (recordData.propsRecordType == 11) {
                recordData.requestObject.name = val
            } else if (recordData.propsRecordType == 12) {
                recordData.requestObject.build_name = val
            } else if (recordData.propsRecordType == 13) {
                recordData.requestObject.floor_name = val
            } else if (recordData.propsRecordType == 14) {
                recordData.requestObject.name = val
            } else if (recordData.propsRecordType == 15) {
                recordData.requestObject.description = val
            }
            firstRequest(recordData.propsRecordType)
        }
        // 更多筛选 查询
        const switchMoreSelectBox = (type) => {
            recordData.moreSelect = !recordData.moreSelect
            if (type == false) {
                recordData.requestObject.page = 1
                recordData.tableId = 1
                firstRequest(recordData.propsRecordType)
                recordData.controllersSlect = ""
                recordData.loopSlect = ""
                recordData.partNumSlect = ""
                recordData.stationingSlect = ""
            }
        }
        const moreSelectFun = (val, type) => {
            if (type == 1) {
                recordData.partNumList = []
                recordData.loopList = []
                let loopRequest = {
                    page: 0,
                }
                loopRequest.controller_num = val
                recordData.requestObject.controller_num = val
                inquireLoopRequest(loopRequest).then((res) => {
                    recordData.loopList = res.data.loops
                });
                // 选择控制器时 清空回路号和地址号选择器
                recordData.loopSlect = ""
                recordData.requestObject.loop_num = ""
                recordData.partNumSlect = ""
                recordData.requestObject.addr_num = ""
            } else if (type == 2) {
                recordData.partNumList = []
                recordData.partNumSlect = ""
                recordData.requestObject.addr_num = ""
                recordData.requestObject.loop_num = val//回路号
                let deviceRequest = {
                    page: 0,
                    controller_num: recordData.controllersSlect,
                    loop_num: val
                }
                deviceListRequest(deviceRequest).then((res) => {
                    recordData.partNumList = res.data.items
                });
            } else if (type == 3) {
                recordData.requestObject.addr_num = val//部位号
            } else if (type == 4) {
                recordData.requestObject.is_assign = val//清空布点状态
            }
        }
        // 删除控制器
        const deleteController = (popupData) => {
            deleteControllersRequest(popupData).then((res) => {
                if (res.ok) {
                    ElMessage({
                        message: '删除控制器成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    refresh()
                    recordData.popupType = 0
                }
            });
        }
        // 导入控制器 全部
        const upFile = (popupData) => {
            let file = popupData.file[0];
            let formData = new FormData();
            formData.append("controller_excel", file);
            formData.append("project_id", popupData.project_id);
            formData.append("is_parse", 0);
            axios.post(recordData.url + '/build_drawing/controllers_file', formData, {
                headers: {
                    'Authorization': 'Bearer' + ' ' + JSON.parse(sessionStorage.getItem('userInfo'))['token']
                }
            }).then(res => {
                if (res.data.ok == true) {
                    ElMessage({
                        message: '创建成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    refresh()
                    recordData.popupType = 0
                    controllersListRequest(recordData.requestObject).then((res) => {
                        store.commit('controllersListData', res.data.items)
                    });
                }
            })
        }
        // 导入单个控制器 打开弹窗
        const onlyUpFile = (popupData) => {
            recordData.onlyControllerId = popupData.project_id
            recordData.onlyUpFileShow = true
            recordData.popupType = 0
            let file = popupData.file[0];
            let formData = new FormData();
            formData.append("controller_excel", file);
            formData.append("project_id", popupData.project_id);
            formData.append("is_parse", 1);
            axios.post(recordData.url + '/build_drawing/controllers_file', formData, {
                headers: {
                    'Authorization': 'Bearer' + ' ' + JSON.parse(sessionStorage.getItem('userInfo'))['token']
                }
            }).then(res => {
                if (res.data.ok == true) {
                    recordData.OnlyControllersList = res.data.data
                }
            })
        }
        // 上传单个控制器
        const onlyUp = () => {
            if (recordData.onlyControllerName == "" || recordData.onlyControllerCode == "" || recordData.onlyControllerModel == "" || recordData.onlyControllerManufacturer == "" || recordData.onlyControllerSetDate == "") return ElMessage({
                message: '请输入完整信息',
                type: 'error',
                duration: 3 * 1000
            })
            let data = {
                project_id: recordData.onlyControllerId,
                name: recordData.onlyControllerName,
                code: recordData.onlyControllerCode,
                model: recordData.onlyControllerModel,
                manufacturer: recordData.onlyControllerManufacturer,
                setup_date: recordData.onlyControllerSetDate,
                controller_type: recordData.onlyControllerType
            }
            addControllersRequest(data).then((res) => {
                if (res.ok) {
                    ElMessage({
                        message: '导入成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    recordData.OnlyControllersSlect = ""
                    recordData.onlyControllerName = ""
                    recordData.onlyControllerCode = ""
                    recordData.onlyControllerModel = ""
                    recordData.onlyControllerManufacturer = ""
                    recordData.onlyControllerSetDate = ""
                    recordData.onlyControllerType = ""
                    refresh()
                }
            });
        }
        const offonlyUpFileShow = () => {
            recordData.onlyUpFileShow = false
            recordData.OnlyControllersSlect = ""
            recordData.OnlyControllersList = []
            recordData.onlyControllerId = ""
            recordData.onlyControllerName = ""
            recordData.onlyControllerCode = ""
            recordData.onlyControllerModel = ""
            recordData.onlyControllerManufacturer = ""
            recordData.onlyControllerSetDate = ""
            recordData.onlyControllerType = ""
        }
        // 控制器 设备下载模板
        const getHelp = () => {
            if (recordData.propsRecordType == 14) {
                getHelpRequest(2).then((res) => {
                    recordData.templateUrl = recordData.url  + res.data.template_path
                    // window.open(recordData.url  + res.data.template_path, 'height=500,width=500,top:100,left:100,')
                });
            }else if(recordData.propsRecordType == 15){
                getHelpRequest(1).then((res) => {
                    recordData.templateUrl = recordData.url  + res.data.template_path
                    // window.open(recordData.url  + res.data.help_path, 'PDF', 'height=500,width=500,top:100,left:100,')
                });
            }
        }
        // 选择控制器带出数据
        const onlyController = (val) => {
            recordData.OnlyControllersList.forEach((item) => {
                if (item.code == val) {
                    recordData.onlyControllerName = item.name
                    recordData.onlyControllerCode = item.code
                    recordData.onlyControllerModel = item.model
                    recordData.onlyControllerSetDate = item.setup_date
                    recordData.onlyControllerManufacturer = item.manufacturer
                }
            })
        }
        // 导入设备
        const upFileDevice = (popupData) => {
            let file = popupData.file[0];
            let formData = new FormData();
            formData.append("device_excel", file);
            formData.append("controller_id", popupData.controller_id);
            formData.append("controller_num", popupData.controller_num);
            axios.post(recordData.url + '/build_drawing/devices_file', formData, {
                headers: {
                    'Authorization': 'Bearer' + ' ' + JSON.parse(sessionStorage.getItem('userInfo'))['token']
                }
            }).then(res => {
                if (res.data.ok == true) {
                    ElMessage({
                        message: '导入成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    refresh()
                    recordData.popupType = 0
                }
            })
        }
        // 切换分页
        const handleCurrentChange = (val) => {
            recordData.requestObject.page = val;
            Request(recordData.propsRecordType);
            // 序号
            recordData.tableId = (val - 1) * recordData.requestObject.per_page + 1;
        }
        // 刷新
        const refresh = () => {
            recordData.input = ""
            recordData.tableId = 1
            recordData.requestObject.page = 1//页数为1
            recordData.loopSlect = ""//清空回路号选择器
            recordData.partNumSlect = ""//清空部位号选择器
            recordData.controllersSlect = ""//清空控制器号选择器
            recordData.stationingSlect = ""//清空布点选择
            recordData.requestObject.page = 1//页数为1
            recordData.requestObject.user_id = "" //清空用户id
            recordData.requestObject.name = ""//清空项目名称
            recordData.requestObject.build_name = ""//清空楼宇名称
            recordData.requestObject.floor_name = ""//清空楼层名称
            recordData.requestObject.name = ""//清空控制器名称
            recordData.requestObject.description = "",//清空设备关键字查询
                recordData.requestObject.loop_num = ""//清空回路号选择
            recordData.requestObject.addr_num = ""//清空部位号选择
            recordData.requestObject.controller_num = ""//清空控制器号选择
            recordData.requestObject.is_assign = ""//清空布点状态

            firstRequest(recordData.propsRecordType)
        }
        // 监听 导入单个控制器弹窗状态
        watch(() => recordData.onlyUpFileShow, (newvalue, oldvalue) => {
            if (oldvalue == true) {
                recordData.OnlyControllersSlect = ""
                recordData.OnlyControllersList = []
                recordData.onlyControllerId = ""
                recordData.onlyControllerName = ""
                recordData.onlyControllerCode = ""
                recordData.onlyControllerModel = ""
                recordData.onlyControllerManufacturer = ""
                recordData.onlyControllerSetDate = ""
                recordData.onlyControllerType = ""
            }
        })
        // 监听 删除设备数组
        watch(() => recordData.deleteTableData, (newvalue, oldvalue) => {
            if(newvalue.length==0){
                recordData.deleteDeviceData = {}
                recordData.deleteDeviceIdstr = ""
            }
        })
        // 监听 单个删除设备弹窗的状态
        watch(() => recordData.deleteDeviceShow, (newvalue, oldvalue) => {
            if (oldvalue == true) {
                recordData.deleteDeviceData = {}
                recordData.deleteDeviceIdstr = ""
            }
        })
        watch(props, (newProps) => {
            recordData.propsRecordType = newProps.recordType
            if (newProps.recordType == 18) {
                recordData.stationState = true
            } else {
                recordData.stationState = false
            }
            recordData.objectDetailState = false
            recordData.requestObject.page = 1//页数为1
            recordData.requestObject.user_id = "" //清空用户id
            recordData.requestObject.name = ""//清空项目名称
            recordData.requestObject.build_name = ""//清空楼宇名称
            recordData.requestObject.floor_name = ""//清空楼层名称
            recordData.requestObject.name = ""//清空控制器名称
            recordData.requestObject.description = "",//清空设备关键字查询
            recordData.requestObject.loop_num = ""//清空回路号选择
            recordData.requestObject.addr_num = ""//清空部位号选择
            recordData.requestObject.controller_num = ""//清空控制器号选择
            recordData.requestObject.is_assign = ""//清空布点状态
            recordData.deleteTableData = []
            recordData.deleteDeviceIdstr = ""
            recordData.deleteDevicesShow = false
            recordData.deleteDeviceShow = false
            recordData.deleteFloorTableData = []
            recordData.floorsIdstr = ""
            recordData.deleteFloorsShow = false
            recordData.tableId = 1//页数为1
            recordData.input = "",//清空输入框
                recordData.moreSelect = false//关闭更多号筛选
            recordData.loopSlect = ""//清空回路号选择器
            recordData.partNumSlect = ""//清空部位号选择器
            recordData.controllersSlect = ""//清空控制器号选择器
            recordData.stationingSlect = ""//清空布点选择
            firstRequest(recordData.propsRecordType)
            getHelp()
            recordData.userList = store.state.userList
            recordData.controllersList = store.state.controllersList
            recordData.deviceTypeList = store.state.deviceTypeList
        }
        );
        return {
            clear,
            recordData,
            openObjectDetail,
            offObjectDetail,
            handleCurrentChange,
            selectFun,
            searchFun,
            refresh,
            offPopup,
            openPopup,
            sure,
            switchMoreSelectBox,
            moreSelectFun,
            onlyController,
            offonlyUpFileShow,
            deleteController,
            visibleControllers,
            openDetail,
            offDetail,
            upFile,
            onlyUpFile,
            onlyUp,
            upFileDevice,
            deviceTypeImg,
            putDeviceIcon,
            changeDeviceIcon,
            addDeviceIcon,
            getHelp,
            handleSelectionChange,
            openDeviceShow,
            offDeviceShow,
            deleteDevice,
            openDeviceOnlyShow,
            offDeviceOnlyShow,
            handleFloors,
            OpenMoreDeleteFloor,
            OffMoreDeleteFloor,
            detaleFloors
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
        position: relative;


        .selectBox {
            display: flex;
            align-items: center;


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

                .removeButton {
                    width: 144px;
                    height: 44px;
                    background: #4a5cd5;
                    border-radius: 2px;
                    display: flex;
                    flex-direction: row;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                    margin-left: 12px;
                    border: none;
                    color: #ffffff;
                    font-size: 20px;
                }

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

                .more,.deleteBtn {
                width: 144px;
                height: 44px;
                background: #4a5cd5;
                border-radius: 2px;
                display: flex;
                flex-direction: row;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                margin-left: 12px;
            }
            .deleteBtn{
                margin-right: 12px;
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
            .new,
            .newAreaBuild {
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

            .newAreaBuild {
                width: 150px;
            }
            .moreDeleteFloor{
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
                margin-right: 12px;
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

            .upload-wrap {
                width: 120px;
                height: 44px;
                position: relative;
                display: inline-block;
                overflow: hidden;
                margin-right: 10px;
                border-radius: 3px;
            }

            .upload-wrap .file-ele {
                position: absolute;
                top: 0;
                right: 0;
                opacity: 0;
                height: 100%;
                width: 100%;
                cursor: pointer;
            }

            .upload-wrap .file-open {
                width: 120px;
                height: 44px;
                display: flex;
                justify-content: center;
                align-items: center;
                color: #fff;
                background-color: #4A5CD5;
            }

        }

        .btnBox:first-child {
            width: 250px;
        }

        .fileBox {
            position: absolute;
            width: 400px;
            height: 50px;
            background-color: #2d78f4;
            right: 0px;
            top: -50px;
            display: flex;
            align-items: center;
            border-radius: 5px;

            .fileName {
                font-size: 20px;
                color: #000000;
                margin-right: 20px;
                margin-left: 10px;
            }

            .fileUpBtn {
                width: 80px;
                height: 30px;
                border: 1px solid #ffffff;
                border-radius: 5px;
                font-size: 20px;
                background-color: #2d78f4;
                cursor: pointer;
                margin-left: 20px;
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

        // 更多筛选
        .moreSelectBox {
            width: 1680px;
            height: 180px;
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
    }

    // 设备类型页面
    .deviceTypeBox {
        display: flex;

        .infinite-list {
            width: 460px;
            height: 884px;
            background: #ffffff;
            overflow-y: auto;
            overflow-x: hidden;

            .infinite-list-item {
                width: 370px;
                height: 80px;
                margin-top: 10px;
                display: flex;
                font-size: 20px;
                margin-left: 40px;
                border-bottom: 1px solid #132b63;

                .xuhao {
                    width: 25px;
                    height: 80px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }

                .deviceName {
                    width: 290px;
                    height: 80px;
                    margin-left: 14px;
                    display: flex;
                    align-items: center;
                }

                .deviceIcon {
                    width: 50px;
                    height: 80px;
                    margin-left: 10px;
                    display: flex;
                    align-items: center;

                    .deviceState {
                        width: 50px;
                        height: 50px;
                    }
                }


            }
        }

        .infinite-list::-webkit-scrollbar {
            width: 5px;
            /*高宽分别对应横竖滚动条的尺寸*/
            height: 10px;
            // display: none;
            border-radius: 5px;
        }

        .infinite-list::-webkit-scrollbar-thumb {
            border-radius: 5px;
            background-color: rgb(181, 178, 178);
        }

        .infinite-list::-webkit-scrollbar-track {
            background: #000000;
            border-radius: 2px;
        }

        .noneBox {
            width: 10px;
            height: 884px;
            background-color: #F2F6FC;
        }

        .deviceTypeSelectBox {
            width: 1282px;
            height: 884px;
            background: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;

            .selectBox {
                width: 600px;
                height: 300px;
                border: 1px solid #dcdfe6;
                border-radius: 3px;

                .selectorBox {
                    width: 600px;
                    margin-top: 53px;
                    display: flex;
                    align-items: center;
                    justify-content: center;

                    // 选择器
                    :deep(.el-select) {
                        width: 320px;
                        height: 44px;
                    }

                    :deep(.el-input__wrapper) {
                        width: 320px;
                        height: 44px;
                        background-color: #F7F8FC;
                        border: none !important;
                        box-shadow: none !important;
                    }
                }

                .fileBox {
                    width: 600px;
                    height: 40px;
                    font-size: 18px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin-top: 47px;
                }

                .BtnBox {
                    width: 600px;
                    height: 40px;
                    display: flex;
                    margin-top: 20px;
                    align-items: center;
                    justify-content: center;

                    .removeButton {
                        width: 144px;
                        height: 44px;
                        background: #4a5cd5;
                        border-radius: 2px;
                        display: flex;
                        flex-direction: row;
                        align-items: center;
                        justify-content: center;
                        cursor: pointer;

                        border: none;
                        color: #ffffff;
                        font-size: 20px;
                    }
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

    .onlyUpFileBox {
        width: 900px;
        height: 430px;
        margin-left: 50px;
        overflow: hidden;

        .onlySelectBox {
            width: 900px;
            height: 50px;
            display: flex;
            margin-top: 50px;

            .onlySelect {
                width: 450px;
                height: 50px;
                margin-left: 10px;
                display: flex;
                align-items: center;


                .onlySelectText {
                    width: 100px;
                    height: 50px;
                    font-size: 15px;
                    display: flex;
                    align-items: center;
                    justify-content: right;
                }

                .onlyselect {
                    margin-left: 10px;

                    // 选择器
                    :deep(.el-input) {
                        width: 320px;
                        height: 49px;
                        color: #4A5CD5;
                    }

                    :deep(.el-input__wrapper) {
                        width: 320px;
                        height: 49px;
                        color: #4A5CD5;
                        background-color: #F7F8FC;
                        border: none !important;
                        box-shadow: none !important;
                    }
                }

            }
        }
    }

    .sureBox {
        width: 1000px;
        height: 60px;
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

    .deleteBox {
        :deep(.el-dialog) {
            display: flex;
            flex-direction: column;
            margin: 0 !important;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            height: 800px;
            width: 1300px;
            border-radius: 8px;

            .headerBox {
                width: 1300px;
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
            width: 1260px;
            height: 650px;
            overflow: hidden;
            margin-left: 20px;

            .alarmsTable {
                width: 1260px;

                :deep(.el-table__cell) {
                    height: 82px !important;
                    padding: 0px !important;
                }
            }
        }

        .sureBox {
            width: 1300px;
            height: 60px;
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

    .deleteOnlyBox {
        :deep(.el-dialog) {
            display: flex;
            flex-direction: column;
            margin: 0 !important;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 1000px;
            height: 700px;
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

        .deviceBox {
            width: 960px;
            height: 550px;
            overflow: hidden;
            margin-left: 20px;
            font-size: 20px;
            color: #000000;
            display: flex;
            flex-direction: column;

            .topBox {
                width: 900px;
                height: 195px;
                display: flex;
                flex-direction: row;

                .leftBox {
                    width: 770px;
                    height: 195px;

                    .deviceName {
                        width: 1100px;
                        height: 50px;
                        margin-top: 15px;
                        display: flex;
                        align-items: center;
                    }
                }

                .rightBox {
                    width: 130px;
                    height: 130px;
                    margin-top: 15px;
                    display: flex;
                    align-items: center;
                    justify-content: center;

                    .deviceName {
                        width: 130px;
                        height: 130px;

                        .deviceImg {
                            width: 130px;
                            height: 130px;
                        }
                    }
                }
            }

            .bottomBox {
                width: 900px;
                height: 570px;
                display: flex;
                flex-direction: column;

                .deviceName {
                    width: 900px;
                    height: 50px;
                    margin-top: 15px;
                    display: flex;
                    align-items: center;
                }
            }

        }


        .sureBox {
            width: 1000px;
            height: 60px;
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
    .deleteFloor{
        :deep(.el-dialog) {
            display: flex;
            flex-direction: column;
            margin: 0 !important;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            height: 800px;
            width: 1300px;
            border-radius: 8px;

            .headerBox {
                width: 1300px;
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
            width: 1260px;
            height: 650px;
            overflow: hidden;
            margin-left: 20px;

            .alarmsTable {
                width: 1260px;

                :deep(.el-table__cell) {
                    height: 82px !important;
                    padding: 0px !important;
                }
            }
        }

        .sureBox {
            width: 1300px;
            height: 60px;
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
}
</style>