<!-- 项目详情 -->
<template>
    <div class="objectDetailBox" v-show="objectDetailState">
        <!-- 项目基础信息 -->
        <div class="objectMessage">
            <div class="bojectText">项目基本信息</div>
            <div class="message">
                <div class="title">项目名称:</div>
                <div class="text">{{ objectDetailData.name }}</div>
            </div>
            <div class="message">
                <div class="title">项目地址:</div>
                <div class="text">{{ objectDetailData.address }}</div>
            </div>
            <div class="message">
                <div class="title">项目电话:</div>
                <div class="text">{{ objectDetailData.mobile }}</div>
            </div>
        </div>
        <div class="objectDetail">
            <!-- 切换记录按钮 -->
            <div class="switchDetailBox">
                <div class="switchBtn" :class="objectData.switchBtnActive == 1 ? 'active' : 'unactive'"
                    @click="switchRecord(1)">项目图</div>
                <div class="switchBtn" :class="objectData.switchBtnActive == 4 ? 'active' : 'unactive'"
                    @click="switchRecord(4)">应急预案</div>
                <div class="switchBtn" :class="objectData.switchBtnActive == 5 ? 'active' : 'unactive'"
                    @click="switchRecord(5)">控制室信息</div>
                <div class="switchBtn" :class="objectData.switchBtnActive == 6 ? 'active' : 'unactive'"
                    @click="switchRecord(6)">系统图</div>
                <div class="offBtn" @click="offObjectDetail">返回项目列表</div>
            </div>
            <!-- 项目图 -->
            <div class="detailBox">
                <div class="demandBox">
                    <div class="selectBox">
                        <template v-if="objectData.imgShow == true">
                            <div class="objectName">{{ objectData.imgName }}</div>
                        </template>
                    </div>
                    <div class="btnBox">
                        <template v-if="objectData.imgShow == true">
                            <div class="new" @click="objectData.imgShow = false">返回上级</div>
                        </template>
                        <template v-else>
                            <div class="new" @click="newImg">新建图纸</div>
                            <div class="new" @click="switchRecord(objectData.switchBtnActive)">刷新</div>
                        </template>
                    </div>
                </div>
                <template v-if="objectData.imgShow == true">
                    <div class="objectImgDetail">
                        <img class="detailImg" :src="objectData.imgUrl" alt="" @dragstart.prevent>
                    </div>
                </template>
                <template v-else>
                    <div class="tableBox">
                        <el-table :data="objectData.tableData" class="alarmsTable"
                            :header-cell-style="{ color: '#000000', backgroundColor: '#F8F9FC' }">
                          
                            <el-table-column type="index" label="序号" align="center">
                                <template #default="scope">
                                    <div>
                                        <div :class="scope.$index <= 2 ? 'highlight-index' : ''">{{ scope.$index +
                                        objectData.tableId}}</div>
                                    </div>
                                </template>
                            </el-table-column>
                            <el-table-column prop="name" label="名称" align="center" />
                            <el-table-column prop="picture_type_name" label="图片类型 " align="center" />
                            <el-table-column label="操作" align="center">
                                <template #default="scope">
                                    <div class="deviceState">
                                        <div class="deviuceStateImg" @click="openImg(scope.row)">
                                            <img class="deviuceStateimg" src="../../assets/img/comment/imgImg.svg"
                                                alt="" @dragstart.prevent>
                                        </div>
                                        <div class="deviuceStateImg" @click="deleteImg(scope.row)">
                                            <img class="deviuceStateimg"
                                                src="../../assets/img/comment/deleteObjectIcon.svg" alt="" @dragstart.prevent>
                                        </div>
                                    </div>

                                </template>
                            </el-table-column>
                        </el-table>
                    </div>
                    <div class="pagingBigBox">
                        <div class="pagingBox">
                            <el-pagination layout="total,prev, pager, next " :total="objectData.total"
                                :page-size="objectData.page_size" @current-change="handleCurrentChange"
                                :current-page="objectData.requestObject.page" />
                        </div>
                    </div>
                </template>
            </div>
        </div>
        <el-dialog v-model="objectData.show" :show-close="false">
            <template #header>
                <div class="headerBox">新建图纸</div>
                <div class="offBtn" @click="offShow">✖</div>
            </template>
            <div class="logoutMsg">
                <div class="account">
                    图纸类型:<el-select v-model="objectData.MoreimgType" placeholder="请选择图纸"
                        @visible-change="visibleImgType"
                        @change="selectFun(objectData.MoreimgType, objectData.switchBtnActive)" clearable>
                        <el-option v-for="item in objectData.MoreimgTypeList" :key="item.id" :label="item.name"
                            :value="item.id" />
                    </el-select>
                </div>
                <div class="password">
                    <input type="file" id="input1" @change="onchange" accept=".svg"  placeholder="上传文件">
                </div>
                <template v-if="objectData.switchBtnActive==6">
                    <template v-if="objectData.MoreimgType==7">
                        <div class="password">
                            <el-checkbox v-model="objectData.inherit" label="是否作为首页显示图" @change="inherit" border>
                            </el-checkbox>
                        </div>
                    </template>
                </template>
                <template v-else-if="objectData.switchBtnActive==5">
                
                </template>
                <template v-else>
                    <div class="password">
                        <el-checkbox v-model="objectData.inherit" label="是否作为首页显示图" @change="inherit" border>
                        </el-checkbox>
                    </div>
                </template>

            </div>
            <div class="sureBox">
                <button class="sureBtn" @click="erasure">确定</button>
                <button class="cancelBtn" @click="offShow">取消</button>
            </div>
        </el-dialog>
    </div>
</template>
<script>
import { reactive, watch, onMounted } from 'vue'
import config from "../../utils/config";
import { useStore } from 'vuex'
import { imgTypeListRequest, floorsListRequest } from "../../api/recordData";
import { deleteImgRequest } from "../../api/operation";
import axios from "axios";
import { ElMessage } from 'element-plus'
export default {
    props: {
        objectDetailState: Boolean,
        objectDetailData: Object
    },
    setup(props, context) {
        const store = useStore();
        let objectData = reactive({
            isHome: 0,
            inherit: false,
            show: false,
            imgTypeList: [],
            fileList: [],
            url: "",
            switchBtnActive: 1,
            PropsObjectData: {},//接受父组件传递数据
            tableData: [],
            imgShow: false,//项目图显示
            requestObject: {
                page: 1,
                per_page: 8,
                project_id: "",
                picture_type_ids: ""
            },//请求参数
            MoreimgType: "",
            MoreimgTypeList: [],
            total: 1,//表格总条数
            tableId: 1,//列表序号
            page_size: 8,
            imgName: "",
            imgUrl: "",
            imgId: ""
        })
        onMounted(() => {
            objectData.url = config.baseUrl
        })
        // 关闭项目详情组件
        const offObjectDetail = () => {
            context.emit('offObjectDetail', false);
        }
        // 切换 项目图 应急预案 控制室信息 系统图    
        const switchRecord = (type) => {
            objectData.switchBtnActive = type
            objectData.tableId = 1
            objectData.requestObject.page = 1//页数为1
            objectData.imgTypeList = store.state.imgTypeList
            let idstr = ""
            objectData.imgTypeList.forEach((item) => {
                if (item.type == type) {
                    idstr += item.id.toString() + ",";
                }
            })
            idstr = idstr.substring(0, idstr.length - 1);
            objectData.requestObject.page = 1//页数为1
            objectData.requestObject.project_id = objectData.PropsObjectData.id
            objectData.requestObject.picture_type_ids = idstr
            imgTypeListRequest(objectData.requestObject).then((res) => {
                objectData.tableData = res.data.items
                objectData.total = res.data.record_size
            });
            objectData.imgShow = false
        }
        // 打开项目图
        const openImg = (val) => {
            objectData.imgName = val.name
            objectData.imgUrl = objectData.url + val.path
            objectData.imgShow = true
        }
        // 打开项目图
        const Request = (type) => {
            objectData.imgTypeList = store.state.imgTypeList
            let idstr = ""
            objectData.imgTypeList.forEach((item) => {
                if (item.type == type) {
                    idstr += item.id.toString() + ",";
                }
            })
            idstr = idstr.substring(0, idstr.length - 1);
            objectData.requestObject.project_id = objectData.PropsObjectData.id
            objectData.requestObject.picture_type_ids = idstr
            imgTypeListRequest(objectData.requestObject).then((res) => {
                objectData.tableData = res.data.items
            });
        }
        // 删除项目图
        const deleteImg = (val) => {

            deleteImgRequest(val.id).then((res) => {
                if (res.ok) {
                    ElMessage({
                        message: '删除成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    switchRecord(objectData.switchBtnActive)
                }
            });
        }
        const newImg = () => {
            objectData.show = true
        }
        const offShow = () => {
            objectData.show = false
            objectData.imgId = ""
            document.getElementById('input1').value = ''
        }
        // 弹窗筛选类型
        const selectFun = (val, type) => {
            objectData.imgId = val
        }
        // 根据 类型筛选图纸类型
        const visibleImgType = () => {
            objectData.MoreimgTypeList = []
            objectData.imgTypeList = store.state.imgTypeList
            objectData.imgTypeList.forEach((item) => {
                if (item.type == objectData.switchBtnActive) {
                    objectData.MoreimgTypeList.push(item)
                }
            })
        }
        // 新建项目图
        const erasure = () => {
            if (objectData.imgId == "") return ElMessage({
                message: '请选择图片类型',
                type: 'error',
                duration: 3 * 1000
            })
            if (objectData.fileList[0] == undefined) return ElMessage({
                message: '请选择上传图片',
                type: 'error',
                duration: 3 * 1000
            })

            let file = objectData.fileList[0];
            let formData = new FormData();
            formData.append("picture", file);
            formData.append("project_id", objectData.PropsObjectData.id);
            formData.append("picture_type_id", objectData.imgId);
            formData.append("is_home", objectData.isHome);
            axios.post(config.baseUrl + '/build_drawing/project_pictures', formData, {
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
                    objectData.imgId = ""
                    document.getElementById('input1').value = ''
                    objectData.show = false
                    switchRecord(objectData.switchBtnActive)
                }
            })
        }
        // 上传文件
        const onchange = (event) => {
            objectData.fileList = event.target.files;
        }
        // 是否作为继承模板
        const inherit = () => {
            objectData.inherit != objectData.inherit
            if (objectData.inherit == true) {
                objectData.isHome = 1
            } else {
                objectData.isHome = 0
            }
        }
        // 切换分页
        const handleCurrentChange = (val) => {
            objectData.requestObject.page = val;
            Request(objectData.switchBtnActive);
            // 序号
            objectData.tableId = (val - 1) * objectData.requestObject.per_page + 1;
        }
        watch(() => objectData.show, (oldvalue, newvalue) => {
            if (newvalue == true) {
                objectData.MoreimgType = ""
                objectData.imgId = ""
                objectData.fileList = []
                document.getElementById('input1').value = ''
                objectData.isHome = 0
                objectData.inherit = false
            }
        })
        watch(props, (newProps) => {
            objectData.PropsObjectData = props.objectDetailData
            if (newProps.objectDetailState == true) {
                switchRecord(1)
            }
        }
        );
        return {
            objectData,
            offObjectDetail,
            switchRecord,
            openImg,
            handleCurrentChange,
            newImg,
            erasure,
            offShow,
            onchange,
            selectFun,
            visibleImgType,
            inherit,
            deleteImg,
            Request
        }
    }
}
</script>

<style scoped lang="scss">
.objectDetailBox {
    display: flex;
    flex-direction: row;
    background-color: #F2F6FC;
    position: absolute;
    top: 86px;
    left: 0px;
    z-index: 10;

    .objectMessage {
        width: 400px;
        height: 958px;
        background: #ffffff;
        margin-left: 80px;
        margin-top: 18px;
        display: flex;
        flex-direction: column;

        .bojectText {
            font-size: 22px;
            font-weight: 700;
            color: #4a5cd5;
            margin-top: 26px;
            margin-left: 40px;
        }

        .message {
            width: 360px;
            margin-left: 40px;
            margin-top: 26px;
            display: flex;
            flex-direction: row;

            .title {
                width: 100px;
                height: 30px;
                font-size: 20px;
                font-weight: 500;
                color: #000000;
            }

            .text {
                width: 240px;
                font-size: 20px;
                font-weight: 500;
                color: #606266;
            }
        }
    }

    .objectDetail {
        width: 1335px;
        height: 958px;
        margin-top: 18px;
        margin-left: 25px;

        .switchDetailBox {
            width: 1335px;
            height: 56px;
            display: flex;
            align-items: center;
            background: #ffffff;

            .switchBtn {
                width: 66px;
                margin-left: 50px;
                height: 56px;
                display: flex;
                flex-direction: row;
                align-items: center;
                font-size: 22px;
                font-weight: 500;
                color: #000000;
                cursor: pointer;
            }

            .switchBtn:nth-child(2) {
                width: 88px;
            }

            .switchBtn:nth-child(3) {
                width: 110px;
            }

            .active {
                color: #4A5CD5;
                border-bottom: 4px solid #4A5CD5;
            }

            .unactive {
                color: #000000;
                border-bottom: 4px solid #ffffff;
            }

            .offBtn {
                width: 160px;
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
                position: absolute;
                right: 50px;
            }

        }

        .detailBox {
            width: 1335px;
            height: 884px;
            background: #ffffff;
            margin-top: 18px;

            .demandBox {
                width: 1335px;
                height: 80px;
                display: flex;
                justify-content: space-between;
                align-items: center;

                .selectBox {
                    display: flex;
                    align-items: center;

                    .objectName {
                        font-size: 26px;
                        font-weight: 700;
                        color: #000000;
                        margin-left: 39px;
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
                        margin-left: 10px;
                    }
                }
            }

            .objectImgDetail {
                display: flex;
                align-items: center;
                justify-content: center;
                width: 1335px;
                height: 776px;

                .detailImg {
                    width: 1000px;
                    height: 700px;
                }
            }

            .tableBox {
                width: 1335px;
                height: 576px;
                position: relative;

                .alarmsTable {
                    width: 1335px;

                    :deep(.el-table__cell) {
                        height: 64px !important;
                        padding: 0px !important;
                    }
                }

                .deviceState {
                    width: 420px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    justify-content: space-around;

                    .deviuceStateImg {
                        width: 22px;
                        height: 28px;
                        cursor: pointer;

                        .deviuceStateimg {
                            width: 22px;
                            height: 28px;
                        }

                    }
                }
            }

            // 分页
            .pagingBigBox {
                width: 1335px;
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
            margin-top: 10px;
            margin-left: -20px;
            width: 450px;
            display: flex;
            font-size: 20px;
            justify-content: left;
        }


    }

    // 选择器
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
</style>