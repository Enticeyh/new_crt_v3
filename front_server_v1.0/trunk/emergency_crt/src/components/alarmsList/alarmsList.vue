<template>
    <div class="alarmsList" v-show="alarmsListShow" v-loading="alarmsListData.loading">
        <!-- 报警列表的标题 -->
        <div class="listTitleBox">
            <div class="alarmsTypeSelectBox">
                <div class="selectBtn" :class="alarmsListData.isActive == 0 ? 'active' : 'unactive'"
                    @click="alarmsTypeSelect(0)">全部报警
                </div>
                <div class="selectBtn" :class="alarmsListData.isActive == 1 ? 'active' : 'unactive'"
                    @click="alarmsTypeSelect(1)">火警</div>
                <div class="selectBtn" :class="alarmsListData.isActive == 2 ? 'active' : 'unactive'"
                    @click="alarmsTypeSelect(2)">启动</div>
                <div class="selectBtn" :class="alarmsListData.isActive == 4 ? 'active' : 'unactive'"
                    @click="alarmsTypeSelect(4)">故障</div>
            </div>
            <div class="buildingSelect" id="input">
                <el-input v-model="alarmsListData.input" placeholder="请输入关键字查询" clearable @clear="clear">
                    <template #append>
                        <el-button @click="searchFun(alarmsListData.input)">
                            <el-icon>
                                <Search />
                            </el-icon>
                        </el-button>
                    </template>
                </el-input>
            </div>
            <div class="listOffBtn" @click="offAlarmsListShow">✖</div>
        </div>
        <div class="alarmsTableBox">
            <el-table :data="alarmsListData.tableData" class="alarmsTable" border
                :header-cell-style="{ color: '#000000', backgroundColor: '#F8F9FC' }">
                <el-table-column type="index" label="序号" align="center">
                    <template #default="scope">
                        <div class="deviceState">
                            <div :class="scope.$index <= 2 ? 'highlight-index' : ''">{{ scope.$index +
                            alarmsListData.tableId
                            }}</div>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="alarm_type_name" label="报警类型" align="center"  min-width="60%" />
                <el-table-column prop="occurred_alarm_time" label="报警时间" align="center" :show-overflow-tooltip="true" min-width="100%" />
                <el-table-column prop="alarm_current" label="地址" align="center"  min-width="50%"/>
                <el-table-column prop="device_type_name" label="设备类型" align="center" :show-overflow-tooltip="true" />
                <el-table-column prop="description" label="描述" align="center" :show-overflow-tooltip="true" min-width="150%"  />
                <el-table-column prop="build_name" label="楼宇" align="center" />
                <el-table-column prop="floor_name" label="楼层" align="center" />
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
                <el-table-column label="操作" align="center" min-width="40%" >

                    <template #default="scope">
                        <div class="deviceState">
                            <template v-if="scope.row.assign_status == 1">
                                
                                <div class="operation" @click="openDetailImg(scope.row.floor_id,scope.row.device_id)">
                                    查看
                                    </div>
                            </template>
                            <template v-else>
                                
                            </template>
                        </div>


                    </template>

                </el-table-column>
            </el-table>
        </div>
        <!-- 分页 -->
        <div class="pagingBigBox">
            <div class="pagingBox">
                <el-pagination layout="total,prev, pager, next " :total="alarmsListData.total"
                    :page-size="alarmsListData.page_size" @current-change="handleCurrentChange"
                    :current-page="alarmsListData.Request.page" />
            </div>
        </div>
    </div>
</template>
<script>
import { useStore } from 'vuex'
import { reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { alarmsListRequest } from "../../api/baseData";
export default {
    components: {
        Search,
    },
    props: {
        alarmsListShow: Boolean
    },
    setup(props, context) {
        let alarmsListData = reactive({
            isActive: 0,
            tableData: [],
            buildingSlect: "",//楼宇选择器
            buildingList: [],//楼宇列表
            floorsSlect: "",//楼层选择器
            floorsList: [],//楼层列表,
            Request: {
                page: 1,
                per_page: 5,
                description: "",
                alarm_type_id: ""
            },
            total: 1,
            page_size: 5,
            tableId: 1,
            input: "",
            loading: false
        })
        const store = useStore();
        const alarmsTypeSelect = (type) => {
            alarmsListData.isActive = type;
            if (type == 0) {
                alarmsListData.Request.alarm_type_id = ""
            } else {
                alarmsListData.Request.alarm_type_id = type
            }
            Request()
        }
        // 关闭报警队列弹窗
        const offAlarmsListShow = () => {
            alarmsListData.Request.page = 1//页数为1
            alarmsListData.tableId = 1//页数为1
            alarmsListData.Request.description = ""
            context.emit('offAlarmsListShow', false);
        }
        const openDetailImg = (val, deviceval) => {
            context.emit('openDetailImg', val, deviceval);
            context.emit('offAlarmsListShow', false);
        }
        const Request = () => {
            alarmsListRequest(alarmsListData.Request).then((res) => {
                alarmsListData.tableData = res.data.items
                alarmsListData.total = res.data.record_size
            });
        }
        //输入框搜索
        const searchFun = (val) => {
            alarmsListData.Request.page = 1//页数为1
            alarmsListData.tableId = 1//页数为1
            alarmsListData.Request.description = val

            Request()
        }
        // 输入框清空
        const clear = () => {
            alarmsListData.Request.page = 1,
                alarmsListData.Request.per_page = 5,
                alarmsListData.Request.description = "",
                Request()
        }
        // 切换分页
        const handleCurrentChange = (val) => {
            alarmsListData.Request.page = val;
            alarmsListRequest(alarmsListData.Request).then((res) => {
                alarmsListData.tableData = res.data.items
            });
            // 序号
            alarmsListData.tableId = (val - 1) * alarmsListData.Request.per_page + 1;
        }
        watch(() => store.state.alarmsList, (newvalue, oldvalue) => {
            if (newvalue == true) {
                alarmsListData.loading = true
                alarmsListData.Request.description = ""
                alarmsListData.Request.alarm_type_id = ""
                Request()
                if (alarmsListData.tableData) {
                    alarmsListData.loading = false
                }
                store.state.alarmsList = false
            }
        })
        watch(props, (newProps) => {
            if (newProps.alarmsListShow == true) {
                Request()
            } else if (newProps.alarmsListShow == false) {
                alarmsTypeSelect(0)
                alarmsListData.isActive == 0
                alarmsListData.input = ""
            }
        }
        );
        return {
            alarmsListData,
            alarmsTypeSelect,
            offAlarmsListShow,
            handleCurrentChange,
            searchFun,
            clear,
            openDetailImg
        }
    }
}
</script>
<style lang="scss" scoped>
.alarmsList {
    position: absolute;
    top: 74px;
    width: 1462px;
    box-shadow: 0px 0px 20px 0px rgba(0, 0, 0, 0.16);
    background: #ffffff;

    // 报警列表标题容器
    .listTitleBox {
        width: 1462px;
        height: 92px;
        position: relative;
        background-color: #fff;
        display: flex;

        .alarmsTypeSelectBox {
            width: 820px;
            height: 93px;
            display: flex;
            flex-direction: row;
            align-items: center;

            // 切换报警列表按钮
            .selectBtn {
                display: flex;
                justify-content: center;
                flex-direction: row;
                align-items: center;
                width: 50px;
                height: 40px;
                font-size: 20px;
                font-weight: 500;
                color: #000000;
                letter-spacing: 1px;
                margin-left: 20px;
                cursor: pointer;

            }

            .selectBtn:first-child {
                width: 100px;
                height: 40px;
                margin-left: 41px;
            }
            .active {
                color: #4a5cd5;
                border-bottom: 2px solid #4a5cd5;
            }

        }

        // 楼宇选择

        .buildingSelect,
        .floorSelect {
            width: 260px;
            height: 92px;
            display: flex;
            align-items: center;
        }

        .floorSelect {
            margin-left: 14px;
        }

        .buildingSelect {
            width: 260px;
            height: 92px;
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


        // 报警列表关闭按钮
        .listOffBtn {
            display: flex;
            justify-content: center;
            align-items: center;
            position: absolute;
            font-size: 28px;
            width: 18px;
            height: 18px;
            top: 36px;
            right: 44px;
            color: #4A5CD5;
            cursor: pointer;

        }
    }

    // 表格
    .alarmsTableBox {
        width: 1462px;

        .alarmsTable {
            width: 1403px;
            margin-left: 29px;

            :deep(.el-table__header-wrapper) {
                height: 58px;


                .el-table__header {
                    height: 58px;

                }
            }

            :deep(.el-table__row) {
                height: 53px;

            }
        }

        .operation {
            color: #4A5CD5;
            text-decoration: underline;
            cursor: pointer;
        }
    }

    // 分页
    .pagingBigBox {
        width: 1462px;
        height: 61px;
        display: flex;
        align-items: center;
        justify-content: center;

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
    }
}
</style>