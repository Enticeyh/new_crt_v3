<!-- 首页 -->
<template>
  <div class="indexBox">
    <!-- 状态计数 -->
    <div class="stateNumBox">
      <!-- 火警 -->
      <div class="stateBox">
        <div class="stateImgBox">
          <template v-if="indexData.alarmsNumData.fire != 0">
            <img class="stateImg" src="../assets/img/index/fireImgNZ.svg" alt="">
          </template>
          <template v-else>
            <img class="stateImg" src="../assets/img/index/fireImg.svg" alt="">
          </template>
        </div>
        <div class="stateText">火警</div>
        <div class="stateNum">
          <template v-if="indexData.alarmsNumData.fire == undefined">
            0
          </template>
          <template v-else>
            {{ indexData.alarmsNumData.fire }}
          </template>
        </div>
      </div>
      <!-- 启动 -->
      <div class="stateBox">
        <div class="stateImgBox">
          <template v-if="indexData.alarmsNumData.linkage != 0">
            <img class="stateImg" src="../assets/img/index/startImgNZ.svg" alt="">
          </template>
          <template v-else>
            <img class="stateImg" src="../assets/img/index/startImg.svg" alt="">
          </template>
        </div>
        <div class="stateText">启动</div>
        <div class="stateNum">

          <template v-if="indexData.alarmsNumData.linkage == undefined">
            0
          </template>
          <template v-else>
            {{ indexData.alarmsNumData.linkage }}
          </template>
        </div>
      </div>
      <!-- 反馈 -->
      <div class="stateBox">
        <div class="stateImgBox">
          <template v-if="indexData.alarmsNumData.feedback != 0">
            <img class="stateImg" src="../assets/img/index/feedbackImgNZ.svg" alt="">
          </template>
          <template v-else>
            <img class="stateImg" src="../assets/img/index/feedbackImg.svg" alt="">
          </template>

        </div>
        <div class="stateText">反馈</div>
        <div class="stateNum">
          <template v-if="indexData.alarmsNumData.feedback == undefined">
            0
          </template>
          <template v-else>
            {{ indexData.alarmsNumData.feedback }}
          </template>
        </div>
      </div>
      <!-- 故障 -->
      <div class="stateBox">
        <div class="stateImgBox">
          <template v-if="indexData.alarmsNumData.malfunction != 0">
            <img class="stateImg" src="../assets/img/index/malfunctionImgNZ.svg" alt="">
          </template>
          <template v-else>
            <img class="stateImg" src="../assets/img/index/malfunctionImg.svg" alt="">
          </template>

        </div>
        <div class="stateText">故障</div>
        <div class="stateNum">
          <template v-if="indexData.alarmsNumData.malfunction == undefined">
            0
          </template>
          <template v-else>
            {{ indexData.alarmsNumData.malfunction }}
          </template>
        </div>
      </div>
      <!-- 屏蔽 -->
      <div class="stateBox">
        <div class="stateImgBox">
          <template v-if="indexData.alarmsNumData.shielding != 0">
            <img class="stateImg" src="../assets/img/index/shieldImgNZ.svg" alt="">
          </template>
          <template v-else>
            <img class="stateImg" src="../assets/img/index/shieldImg.svg" alt="">
          </template>

        </div>
        <div class="stateText">屏蔽</div>
        <div class="stateNum">
          <template v-if="indexData.alarmsNumData.shielding == undefined">
            0
          </template>
          <template v-else>
            {{ indexData.alarmsNumData.shielding }}
          </template>

        </div>
      </div>
      <!-- 监管 -->
      <div class="stateBox">
        <div class="stateImgBox">
          <template v-if="indexData.alarmsNumData.supervise != 0">
            <img class="stateImg" src="../assets/img/index/superviseImgNZ.svg" alt="">
          </template>
          <template v-else>
            <img class="stateImg" src="../assets/img/index/superviseImg.svg" alt="">
          </template>

        </div>
        <div class="stateText">监管</div>
        <div class="stateNum">

          <template v-if="indexData.alarmsNumData.supervise == undefined">
            0
          </template>
          <template v-else>
            {{ indexData.alarmsNumData.supervise }}
          </template>
        </div>
      </div>
      <!-- 声光故障 -->
      <div class="stateBox">
        <div class="stateImgBox">
          <template v-if="indexData.alarmsNumData.vl_malfunction != 0">
            <img class="stateImg" src="../assets/img/index/malfunctionImgNZ.svg" alt="">
          </template>
          <template v-else>
            <img class="stateImg" src="../assets/img/index/malfunctionImg.svg" alt="">
          </template>

        </div>
        <div class="stateText">声光故障</div>
        <div class="stateNum">
          <template v-if="indexData.alarmsNumData.vl_malfunction == undefined">
            0
          </template>
          <template v-else>
            {{ indexData.alarmsNumData.vl_malfunction }}
          </template>
        </div>
      </div>
      <!-- 声光屏蔽 -->
      <div class="stateBox">
        <div class="stateImgBox">
          <template v-if="indexData.alarmsNumData.vl_shielding != 0">
            <img class="stateImg" src="../assets/img/index/shieldImgNZ.svg" alt="">
          </template>
          <template v-else>
            <img class="stateImg" src="../assets/img/index/shieldImg.svg" alt="">
          </template>
        </div>
        <div class="stateText">声光屏蔽</div>
        <div class="stateNum">

          <template v-if="indexData.alarmsNumData.vl_shielding == undefined">
            0
          </template>
          <template v-else>
            {{ indexData.alarmsNumData.vl_shielding }}
          </template>
        </div>
      </div>
      <!-- 火警球 -->
      <div class="alarmsBallBox" @click="showfirst">
        <img class="alarmsBallImg" src="../assets/img/index/alarmsBallImg.svg" alt="">
      </div>
    </div>
    <!-- 右侧 -->
    <div class="rightBox">
      <!-- 选择框 -->
      <div class="selectBox" v-show="indexData.firstAlarmState == false">
        <div class="selectBtnBox" :class="indexData.isActive == 1 ? 'active' : 'unactive'" @click="handover(1)">
          项目图
        </div>
        <div class="selectBtnBox" :class="indexData.isActive == 2 ? 'active' : 'unactive'" @click="handover(2)">
          系统图
        </div>
        <div class="selectBtnBox" :class="indexData.isActive == 3 ? 'active' : 'unactive'" @click="handover(3)">
          应急预案
        </div>
      </div>
      <!-- 首警 -->
      <div class="firstAlarmBox" v-show="indexData.firstAlarmState == true">
        <template v-if="indexData.alarmsNumData.all_alarm !=0 &&indexData.alarmsNumData.first_fire!=0">
          <div class="firstText">
            <img class="firstIcon" src="../assets/img/comment/firstAlarmsIcon.svg" alt="">
          </div>
          <div class="firstMessageBox">
            <div class="firstAlarmTime">时间:{{ indexData.firstAlarmsData.occurred_alarm_time }} &nbsp
              地址:{{ indexData.firstAlarmsData.alarm_current }} &nbsp
              描述:{{ indexData.firstAlarmsData.device_type_name }}-{{ indexData.firstAlarmsData.description }} &nbsp
            </div>
          </div>
          <div class="examineFirstAlarm"
            @click="handlePictureCardPreview(indexData.firstAlarmsData.floor_id, indexData.firstAlarmsData.device_id,1)">
            查看首警
          </div>
        </template>
        <template v-if="indexData.alarmsNumData.all_alarm !=0 &&indexData.alarmsNumData.first_fire==0">
          <div class="noneFireText">暂无首警</div>
        </template>
      </div>
      <!-- 内容 -->
      <!-- 项目图 -->
      <div class="systemDetailBox" v-show="indexData.isActive == 1">
        <template v-if="indexData.projectListData.length==0">
          <div class="noneBox">
            <img class="noneImg" src="../assets/img/comment/none.svg" alt="">
            <div class="noneText">暂无项目图</div>
          </div>
        </template>
        <template v-else>
          <template v-if="indexData.objectImgArr.length == 1">
            <img class="objectImg" :src="indexData.objectImg" alt="">
          </template>
          <template v-else-if="indexData.objectImgArr.length == 0">
            <div class="noneBox">
              <img class="noneImg" src="../assets/img/comment/objectNone.png" alt="">
            </div>
          </template>
          <template v-else>
            <el-carousel indicator-position="outside">
              <el-carousel-item v-for="item in indexData.objectImgArr" :key="item">
                <img class="objectImg" :src="indexData.url + item.path" alt="">
              </el-carousel-item>
            </el-carousel>
          </template>
        </template>
      </div>
      <!-- 系统图 -->
      <div class="projectDetailBox" v-show="indexData.isActive == 2">
        <template v-if="indexData.projectListData.length == 0">
          <div class="noneBox">
            <img class="noneImg" src="../assets/img/comment/none.svg" alt="">
            <div class="noneText">暂无系统图</div>
          </div>
        </template>
        <template v-else>
          <template v-if="indexData.SystemImgArr.length == 1">
            <img class="objectImg" :src="indexData.SystemImg" alt="">
          </template>
          <template v-else-if="indexData.SystemImgArr.length == 0">
            <div class="noneBox">
              <img class="noneImg" src="../assets/img/comment/systemNone.png" alt="">
            </div>
          </template>
          <template v-else>
            <el-carousel indicator-position="outside">
              <el-carousel-item v-for="item in indexData.objectImgArr" :key="item">
                <img class="objectImg" :src="indexData.url + item.path" alt="">
              </el-carousel-item>
            </el-carousel>
          </template>
        </template>
      </div>
      <!-- 应急预案 -->
      <div class="planDetailBox" v-show="indexData.isActive == 3">
        <template v-if="indexData.projectListData.length==0">
          <div class="noneBox">
            <img class="noneImg" src="../assets/img/comment/none.svg" alt="">
            <div class="noneText">暂无应急预案</div>
          </div>
        </template>
        <template v-else>
          <template v-if="indexData.planImgArr.length == 1">
            <img class="objectImg" :src="indexData.planImg" alt="">
          </template>
          <template v-else-if="indexData.planImgArr.length == 0">
            <div class="noneBox">
              <img class="noneImg" src="../assets/img/comment/plan.png" alt="">
            </div>
          </template>
          <template v-else>
            <el-carousel indicator-position="outside">
              <el-carousel-item v-for="item in indexData.planImgArr" :key="item">
                <img class="objectImg" :src="indexData.url + item.path" alt="">
              </el-carousel-item>
            </el-carousel>
          </template>
        </template>

      </div>
      <div class="alarmsBox" v-show="Object.keys(indexData.carouselImgId).length >0">
        <template v-if="indexData.alarmsImgList.length == 0">

        </template>
        <template v-else>
          <div class="btnBox">
            <div class="topBtn">
              <div class="upBtn" @click="up">
                <img class="IndexBtnIcon" src="../assets/img/index/upIcon.svg" alt="" @click="up">
              </div>
            </div>
            <div class="centerBtn">
              <div class="upBtn" @click="left">
                <img class="IndexBtnIcon" src="../assets/img/index/leftIcon.svg" alt="">
              </div>
              <div class="upBtn" @click="move">
                <img class="IndexBtnIcon" src="../assets/img/index/moveIcon.svg" alt="">
              </div>
              <div class="upBtn" @click="right">
                <img class="IndexBtnIcon" src="../assets/img/index/rightIcon.svg" alt="">
              </div>
            </div>
            <div class="centerBtn">
              <div class="upBtn" id="butto" @click="big">
                <img class="IndexBtnIcon" src="../assets/img/index/bigIcon.svg" alt="">
              </div>
              <div class="upBtn" @click="down">
                <img class="IndexBtnIcon" src="../assets/img/index/downIcon.svg" alt="">
              </div>
              <div class="upBtn" @click="small">
                <img class="IndexBtnIcon" src="../assets/img/index/smallIcon.svg" alt="">
              </div>
            </div>
          </div>
          <el-carousel ref="remarkCaruselUp" arrow="never" indicator-position="none" :interval="indexData.carouselTime"
            :autoplay="indexData.autoplayState" @change="changeImg">
            <el-carousel-item v-for="(item, key, index) in indexData.carouselImgId" :key="index" :name="key"  :prev="index" :next="index">
              <!-- v-if="indexData.backupsImgIdList[item.id]==1" -->
              <template v-if="Object.keys(indexData.carouselImgId).length == 1">

              </template>
              <template v-else>
                <div class="prevNextBox">
                  <div class="prevBox" @click="prev(index)">
                    <img class="prevImg" src="../assets/img/index/back.svg" alt="">
                  </div>
                  <div class="nextBox" @click="next(index)">
                    <img class="nextImg" src="../assets/img/index/next.svg" alt="">
                  </div>
                </div>
              </template>
              <template v-if="indexData.backupsImgIdList[item.id] == 1">
                {{index}}{{key}}
                <div class="imgTitle">{{item.area_name}}-{{item.build_name}}-{{item.name}}-平面图 {{index + 1}}/{{Object.keys(indexData.carouselImgId).length}}
                </div>
                <div class="bigBox" id="bigBox" ref="assingPicRef">
                  <div class="alarmsImgBox" :id="item.myId">

                    <el-image id="svg1" class="imgbox" :src="indexData.url + item.path" fit="contain"
                      @mousemove.prevent="floorAssignMove( $event)"
                      :style="{ height: indexData.floorItem.height + 'px', width: indexData.floorItem.width + 'px' }">
                    </el-image>
                    <div class="assign-device" v-for="device in indexData.floorItem.floorAssign" :key="device.id"
                      :style="{ top: device.coordinate_Y + 'px', left: device.coordinate_X + 'px', height: 1094 * device.rate + 'px', width: 1094 * device.rate + 'px' }">
                      <img class="arrowsUpImg" v-if="device.device_id == indexData.currentDeviceIndex"
                        src="../assets/img/comment/arrowsUp.svg" alt=""
                        style="position: absolute;z-index:3;min-width: 30px;max-width: 50px" :style="{
                            width: 30+'px',
                            left: -15+'px',
                            top:-30*1.5+'px',
                        }">
                      <el-tooltip class="toop-item" effect="dark" placement="top-start" :manual="false"
                        :value="indexData.clickDeviceid === device.id" v-if="index === indexData.currentFloorIndex">
                        <template #content>
                          <div>地址: {{ device.device_address }}</div>
                          <div style="margin-top:5px">设备类型: {{ device.device_type_name }}</div>
                          <span v-if="device.device_status == 2" style="color: #ff3d3d">首警; </span>
                          <span v-if="device.fire != 0" style="color: #ff3d3d">火警; </span>
                          <span v-if="device.linkage !=0" style="color: #ff3d3d">启动; </span>
                          <span v-if="device.feedback !=0" style="color: #ff3d3d">反馈; </span>
                          <span v-if="device.malfunction !=0" style="color: orange">故障; </span>
                          <span v-if="device.shielding !=0" style="color: orange">屏蔽; </span>
                          <span v-if="device.supervise !=0" style="color: #ff3d3d">监管; </span>
                          <span v-if="device.vl_malfunction !=0" style="color: orange">声光故障; </span>
                          <span v-if="device.vl_shielding !=0" style="color: orange">声光屏蔽; </span>

                          <div style="margin-top:5px">注释: {{ device.description }}</div>
                        </template>
                        <el-image :src="indexData.url + device.path" style="user-select:none"
                          :style="{ height: device.height + 'px', width: device.width + 'px' }">
                        </el-image>
                      </el-tooltip>
                      <!-- 报警状态动画显示 -->
                      <div v-if="device.alarm != 0">
                        <div class="Firstcircle" v-if="device.device_status == 2 && device.fire != 0">
                          <div class="FirstCircle1">首警</div>
                          <div class="FirstCircle2"></div>
                          <div class="FirstCircle3"></div>
                        </div>
                        <div class="circle"
                          v-else-if="device.fire != 0 || device.linkage != 0 || device.feedback != 0 || device.supervise != 0">
                          <div class="circle1"></div>
                          <div class="circle2"></div>
                          <div class="circle3"></div>
                        </div>
                        <div class="launch_circle"
                          v-else-if="device.malfunction != 0 || device.vl_malfunction != 0 || device.shielding != 0 || device.vl_shielding != 0">
                          <div class="launch_circle1"></div>
                          <div class="launch_circle2"></div>
                          <div class="launch_circle3"></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </template>

            </el-carousel-item>
          </el-carousel>
        </template>

      </div>
      <alarmsList :alarmsListShow="indexData.alarmsListState" @offAlarmsListShow="offAlarmsListShow"
        @openDetailImg="openDetailImg"></alarmsList>
    </div>
  </div>
</template>
<script>
import { onMounted, reactive, watch, ref, nextTick, getCurrentInstance, toRaw } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import config from "../utils/config";
import Panzoom from '@panzoom/panzoom'
import { ElMessage } from 'element-plus'
import alarmsList from "../components/alarmsList/alarmsList.vue"
import { filesListRequest, alarmsImgRequest, alarmsOnlyRequest } from "../api/recordData"
import { alarmsNumListRequest, projectIndexRequest } from "../api/baseData"
import {
  indexStationListRequest,
} from "../api/operation";

export default {
  components: {
    alarmsList,
  },
  setup() {
    const stateDom = ref(null)
    let indexData = reactive({
      // gbEventTypeList: [],//国标事件列表
      alarmsImgBox: "",
      url: "",
      isActive: 1,
      firstAlarmState: false,
      alarmsListState: false,
      onlyImgState: true,
      alarmsState: true,
      panzoom: null,
      objectImg: "",
      SystemImg: "",
      planImg: "",
      alarmsNumData: {
        fire: 0,
        linkage: 0,
        feedback: 0,
        malfunction: 0,
        shielding: 0,
        supervise: 0,
        vl_malfunction: 0,
        vl_shielding: 0
      },
      objectImgData: {
        is_home: "",
        picture_type_id: ""
      },
      Request: {
        page: 0
      },
      objectImgArr: [],
      SystemImgArr: [],
      planImgArr: [],
      imgTypeList: [],
      firstAlarmsData: {},
      alarmsImgList: [],//报警图片列表
      backupsImgIdList: {},//报警图纸id
      carouselImgId: {},//轮播图纸id
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
      },
      currentFloorIndex: "",//当前图纸的索引
      currentDeviceIndex: "",//当前报警设备id
      // 鼠标中的deviceId
      clickDeviceid: 0,
      carouselTime: 500000,
      noShowDeviceData: [],
      alarmsShow: false,
      projectListData: [],
      autoplayState: true,//轮播图滚动事件状态
      examineFirstAlarms: true,//点击首警标识位状态
    })
    const { proxy } = getCurrentInstance()
    const store = useStore();
    const router = useRouter()
    const remarkCaruselUp = ref(null)
    onMounted(() => {
      indexData.url = config.baseUrl

    })
    // 绑定图纸id
    const fid = () => {
      const elem = document.getElementById(indexData.alarmsImgBox)
      indexData.panzoom = Panzoom(elem, {
        maxScale: 10,
        minScale: 1,
      })
      elem.parentElement.addEventListener('wheel', indexData.panzoom.zoomWithWheel)
    }
    // 图纸改变
    const changeImg = (active, val) => {
      indexData.lunboindexImg = active
      indexData.floorItem.floorAssign = []
      let keyID =  Object.keys(indexData.carouselImgId)[active]
      if (indexData.carouselImgId[keyID]) {
        floorAlarms(indexData.carouselImgId[keyID].id)//拉设备列表
        indexData.currentFloorIndex = active
        indexData.alarmsImgBox = indexData.carouselImgId[keyID].myId
        fid()
        move()//重置图片大小位置
      }
    }
    // 上一张
    const prev = (val) => {
      indexData.currentDeviceIndex = ""
      remarkCaruselUp.value.prev()
      if (indexData.autoplayState == false) {
        indexData.autoplayState = true
      }
    }
    // 下一张
    const next = (val) => {
      indexData.currentDeviceIndex = ""
      remarkCaruselUp.value.next()
      if (indexData.autoplayState == false) {
        indexData.autoplayState = true
      }
    }
    // 切换系统图 项目图 应急预案
    const handover = (type) => {
      indexData.isActive = type;
      if (type == 2) {
        indexData.imgTypeList = store.state.imgTypeList
        indexData.objectImgData.picture_type_id = 7
        indexData.objectImgData.is_home = 1
        filesListRequest(indexData.objectImgData).then((res) => {
          indexData.SystemImgArr = res.data.items
          if (indexData.SystemImgArr.length == 1) {
            indexData.SystemImg = indexData.url + indexData.SystemImgArr[0].path
          }
        });
      } else if (type == 3) {
        indexData.objectImgData.picture_type_id = ""
        indexData.imgTypeList = store.state.imgTypeList
        indexData.imgTypeList.forEach((item) => {
          if (item.type == 4) {
            indexData.objectImgData.picture_type_id += item.id.toString() + ",";
          }
        })
        indexData.objectImgData.picture_type_id = indexData.objectImgData.picture_type_id.substring(0, indexData.objectImgData.picture_type_id.length - 1);
        indexData.objectImgData.is_home = 1
        filesListRequest(indexData.objectImgData).then((res) => {
          indexData.planImgArr = res.data.items
          if (indexData.planImgArr.length == 1) {
            indexData.planImg = indexData.url + indexData.planImgArr[0].path
          }

        });
      } else if (type == 1) {
        indexData.objectImgData.picture_type_id = ""
        indexData.imgTypeList = store.state.imgTypeList
        indexData.imgTypeList.forEach((item) => {
          if (item.type == 1) {
            indexData.objectImgData.picture_type_id += item.id.toString() + ",";
          }
        })
        indexData.objectImgData.picture_type_id = indexData.objectImgData.picture_type_id.substring(0, indexData.objectImgData.picture_type_id.length - 1);
        indexData.objectImgData.is_home = 1
        filesListRequest(indexData.objectImgData).then((res) => {
          indexData.objectImgArr = res.data.items
          if (indexData.objectImgArr.length == 1) {
            indexData.objectImg = indexData.url + indexData.objectImgArr[0].path
          }
        });
      }
    }
    // 展示报警列表
    const showfirst = () => {
      indexData.alarmsListState = !indexData.alarmsListState;
    }
    // 关闭报警列表弹窗
    const offAlarmsListShow = () => {
      indexData.alarmsListState = false;
    }
    // 首警点击查看
    // 点击首警以后 停止轮播图轮播事件 点击上下页按钮 再次触发轮播事件
    const handlePictureCardPreview = (id, deviceval, val) => {
      if (id) {
        indexData.currentDeviceIndex = deviceval // 匹配到对应的 设备id
        if (indexData.examineFirstAlarms) {
          indexData.examineFirstAlarms = false
          if (indexData.panzoom != null) {
            move()
          }

          setTimeout(() => {
            if (indexData.panzoom != null) {
              if (indexData.currentDeviceIndex) {
                //查看对应name的图片
                remarkCaruselUp.value.setActiveItem(id.toString())

                move()
                if (val == 1) {
                  ElMessage({
                    message: '已切换到首警楼层图片',
                    type: 'success',
                    duration: 3 * 1000
                  })
                } else {
                  ElMessage({
                    message: '已切换到查询设备所在图纸',
                    type: 'success',
                    duration: 3 * 1000
                  })
                }
                let timer = null
                timer = setTimeout(() => {
                  let dd = indexData.floorItem.floorAssign.filter(item => {
                    return item.device_id == deviceval
                  })
                  let width = proxy.$refs.assingPicRef[0].offsetWidth / 2
                  let height = proxy.$refs.assingPicRef[0].offsetHeight / 2
                  indexData.panzoom.pan(-dd[0].coordinate_X + width, -dd[0].coordinate_Y + height, { relative: true })
                  indexData.panzoom.zoomIn({ animate: true })
                }, 2000)
                indexData.autoplayState = false
                // let timeState = null
                // timeState = setTimeout(() => {
                //   indexData.autoplayState = true
                // }, 10000)
              }
            }


            indexData.examineFirstAlarms = true
          }, 2000)

        }


      } else {
        ElMessage({
          message: '设备无相关布点信息',
          type: 'info',
          duration: 3 * 1000
        })
      }
    }
    // 报警列表点击查看图纸详情
    const openDetailImg = (val, deviceval) => {
      handlePictureCardPreview(val, deviceval)
    }
    const up = () => {
      indexData.panzoom.pan(0, -10, { relative: true })
    }
    const down = () => {
      indexData.panzoom.pan(0, 10, { relative: true })
    }
    const left = () => {
      indexData.panzoom.pan(-10, 0, { relative: true })
    }
    const right = () => {
      indexData.panzoom.pan(10, 0, { relative: true })
    }
    const move = () => {
      indexData.panzoom.reset()
    }
    const small = () => {
      indexData.panzoom.zoomOut({ animate: true })
    }
    const big = () => {
      indexData.panzoom.zoomIn({ animate: true })
    }
    const floorAssignMove = (e) => {
      // // 算出鼠标相对元素的位置
      // let disX = e.offsetX
      // let disY = e.offsetY
      // let YStart = e.offsetY - 50
      // let YEnd = e.offsetY + 50
      // let XStart = e.offsetX - 50
      // let XEnd = e.offsetX + 50

      // indexData.noShowDeviceData.forEach((item) => {
      //   if ((XStart <= item.coordinate_X &&item.coordinate_X<= XEnd)&&(YStart <= item.coordinate_Y &&item.coordinate_Y<= YEnd)) {
      //     indexData.floorItem.floorAssign.push(item)
      //   }
      // })

    }
    // 获取楼层报警点位设备列表
    const floorAlarms = (id) => {
      indexData.floorItem.floorAssign = []
      let data = {
        floor_id: id,
        is_alarm: 1
      }
      indexStationListRequest(data).then((res) => {
        indexData.floorItem.floorAssign = res.data
      });
      // let offData = {
      //   floor_id: id,
      //   is_alarm: 0
      // }
      // indexStationListRequest(offData).then((res) => {
      //   indexData.noShowDeviceData = res.data
      // });
    }
    watch(() => store.state.alarmsData, (newvalue, oldvalue) => {
      if (oldvalue) {
        indexData.alarmsNumData = oldvalue
      }
    })
    watch(() => store.state.resetState, (newvalue, oldvalue) => {
      if (newvalue == true) {
        indexData.firstAlarmState = false
        indexData.alarmsShow = false
        indexData.isActive = 1
        offAlarmsListShow()
        indexData.alarmsImgList = []
        indexData.floorItem.floorAssign = []
        indexData.backupsImgIdList = {}
        indexData.carouselImgId = {}
      }
    })
    // 首警
    watch(() => indexData.alarmsNumData, (newvalue, oldvalue) => {
      if (newvalue.first_fire == oldvalue.first_fire) {
      } else if (newvalue.first_fire != 0) {
        alarmsOnlyRequest(newvalue.first_fire).then((res) => {
          indexData.firstAlarmsData = res.data

          if (indexData.firstAlarmsData) {
            indexData.firstAlarmState = true
          }
        });
      } else if (newvalue.first_fire == 0) {
        indexData.firstAlarmState = false
      }
      // 判断报警事件是否未火警  不为火警时 显示暂无火警
      if (newvalue.all_alarm != 0 && newvalue.first_fire == 0) {
        if (indexData.alarmsImgList.length == 0) {
          indexData.isActive = 1
          indexData.alarmsShow = false
          indexData.firstAlarmState = true
        } else {
          indexData.firstAlarmState = true
          indexData.alarmsShow = true
          indexData.isActive = 0
        }
      } else if (newvalue.all_alarm == 0 && newvalue.first_fire == 0) {
        indexData.firstAlarmState = false
        if (indexData.isActive == 0) {
          indexData.isActive = 1
          indexData.alarmsShow = false
        }

      } else if (newvalue.all_alarm != 0 && newvalue.first_fire != 0) {
        if (indexData.alarmsImgList.length == 0) {
          indexData.firstAlarmState = true
          indexData.alarmsShow = false
          indexData.isActive = 1
        } else {
          indexData.firstAlarmState = true
          indexData.alarmsShow = true
          indexData.isActive = 0
        }
      }
      if (newvalue.first_fire != 0 && indexData.firstAlarmsData.id == undefined) {
        alarmsOnlyRequest(newvalue.first_fire).then((res) => {
          indexData.firstAlarmsData = res.data
          if (indexData.firstAlarmsData) {
            indexData.firstAlarmState = true
          }

        });
      }
    })
    // watch(() => indexData.carouselImgId, (newvalue, oldvalue) => {
    //   console.log(Object.keys(newvalue).length );
    //   if (Object.keys(newvalue).length >0) {
    //     indexData.isActive = 0
    //   }
    // })
    // 出现报警事件
    watch(() => indexData.alarmsNumData, (newvalue, oldvalue) => {
      if (newvalue.all_alarm_num != oldvalue.all_alarm_num) {
        store.state.resetState = false
        if (indexData.alarmsState) {
          indexData.alarmsState = false;
          setTimeout(() => {
            indexData.url = config.baseUrl
            // 报警图片列表 
            let data = {
              page: 0,
              is_alarm: 1
            }
            alarmsImgRequest(data).then((res) => {
              res.data.items.forEach((item) => {
                item.myId = "myId" + item.id
              })//图纸添加图纸ID 用于缩放组件绑定
              let bakeArr = []
              indexData.alarmsImgList.forEach((item) => {
                bakeArr.push(toRaw(item))
              })

              let list = {}
              res.data.items.forEach((item, index) => {
                list[item.id] = item
                
                if (indexData.backupsImgIdList[item.id] == undefined ) {
                  indexData.backupsImgIdList[item.id] = 1
                  bakeArr.push(item)
                  indexData.carouselImgId[item.id] = item
                }
                else if (indexData.backupsImgIdList[item.id] == 0) {
                  console.log(indexData.backupsImgIdList[item.id],'再次新增');
                  indexData.backupsImgIdList[item.id] = 1
                  indexData.carouselImgId[item.id] = item
                }
                console.log(indexData.backupsImgIdList, 'indexData.backupsImgIdList')
                console.log(indexData.alarmsImgList, 'indexData.alarmsImgList')
                console.log(indexData.carouselImgId, 'indexData.carouselImgId')
              })
             
              // 删除
              bakeArr.forEach((item) => {
                if (list[item.id] == null) {
                  indexData.backupsImgIdList[item.id] = 0
                  delete indexData.carouselImgId[item.id]
                  // delete indexData.backupsImgIdList[item.id]

                  // console.log(indexData.alarmsImgList[indexData.lunboindexImg].id,'indexData.alarmsImgList[indexData.lunboindexImg].id',item.id,'item.id');
                  if (indexData.alarmsImgList[indexData.lunboindexImg].id != item.id) {
                    console.log('=======');


                    // remarkCaruselUp.value.setActiveItem(Object.keys(indexData.carouselImgId)[0].toString())
                  } else {

                  }
                }
              })
              if (bakeArr.length == 1) {
                let timer = null
                timer = setTimeout(() => {
                  console.log('单张图纸时触发');
                  remarkCaruselUp.value.setActiveItem(indexData.alarmsImgList[0].id.toString())
                  indexData.currentFloorIndex = 0
                  fid()
                }, 10000);
              } else if (bakeArr.length != 0 && bakeArr.length != 1) {
                let timer = null
                timer = setTimeout(() => {
                  // 多张图片第一次进入
                  if (indexData.lunboindexImg == undefined) {
                    remarkCaruselUp.value.setActiveItem(Object.keys(indexData.carouselImgId)[0].toString())
                    indexData.currentFloorIndex = 0
                    fid()
                  } else {
                    // 多张需要改动 
                    console.log(indexData.lunboindexImg,'indexData.lunboindexImg');
                    console.log(Object.keys(indexData.carouselImgId)[indexData.lunboindexImg],'Object.keys(indexData.carouselImgId)[indexData.lunboindexImg]');
                    console.log(indexData.alarmsImgList, 'indexData.alarmsImgList')
                console.log(indexData.carouselImgId, 'indexData.carouselImgId')
                console.log(indexData.backupsImgIdList, 'indexData.backupsImgIdList')
                    remarkCaruselUp.value.setActiveItem(Object.keys(indexData.carouselImgId)[indexData.lunboindexImg])
                    indexData.currentFloorIndex = indexData.lunboindexImg
                    fid()
                  }

                }, 2000);

              }

              indexData.alarmsImgList = reactive(bakeArr)
              
              if (Object.keys(indexData.carouselImgId).length > 0) {
                indexData.isActive = 0
              }
            });
            indexData.alarmsState = true;
          }, 3000);
        }
      }
    })
    watch(() => router.currentRoute.value.path, (newValue, oldValue) => {
      if (newValue == "/") {
        indexData.carouselTime = store.state.carouselTime
        alarmsNumListRequest(indexData.Request).then((res) => {
          indexData.alarmsNumData = res.data
        });
        projectIndexRequest().then((res) => {
          indexData.projectListData = res.data
          handover(1)
        });
      }
    }, { immediate: true })
    return {
      stateDom,
      indexData,
      handover,
      showfirst,
      handlePictureCardPreview,
      offAlarmsListShow,
      openDetailImg,
      up,
      down,
      left,
      right,
      move,
      small,
      big,
      fid,
      changeImg,
      remarkCaruselUp,
      prev,
      next,
      floorAlarms,
      floorAssignMove
    }
  }
}
</script>
<style lang="less" scoped>
.indexBox {
  display: flex;
  flex-direction: row;
  background-color: #F2F6FC;

  // 状态计数
  .stateNumBox {
    margin-top: 18px;
    width: 360px;
    height: 958px;
    display: flex;
    margin-bottom: 18px;
    flex-direction: column;
    background-color: #fff;

    // 状态框
    .stateBox {
      width: 360px;
      height: 44px;
      margin-bottom: 44px;
      display: flex;
      flex-direction: row;
      align-items: center; //文字居中

      // 状态图片容器
      .stateImgBox {
        width: 42px;
        height: 42px;
        margin-left: 53px;

        .stateImg {
          width: 42px;
          height: 42px;
        }
      }

      // 状态文字
      .stateText {
        font-size: 24px;
        font-weight: 400;
        color: #000000;
        margin-left: 24px;
        letter-spacing: 1.2px;
      }

      // 状态数量
      .stateNum {
        flex-grow: 1;
        margin-right: 20px;
        text-align: right;
        font-size: 24px;
        font-weight: 400;
        color: #010101;
        letter-spacing: 0.9px;
      }

    }

    // 火警
    .stateBox:first-child {
      margin-top: 25px;
    }

    // 火警球
    .alarmsBallBox {
      width: 198px;
      height: 166px;
      margin-left: 30px;
      cursor: pointer;

      .alarmsBallImg {
        width: 198px;
        height: 166px;
      }
    }
  }

  .rightBox {
    width: 1462px;
    height: 944px;
    margin-left: 18px;
    margin-top: 18px;
    position: relative;
    margin-bottom: 18px;

    // 选择框
    .selectBox {
      width: 1462px;
      height: 56px;
      display: flex;
      flex-direction: row;
      align-items: center;
      background: #4a5cd5;

      // 选择按钮 系统图 项目图 应急预案
      .selectBtnBox {
        width: 80px;
        height: 46px;
        margin-right: 14px;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        font-size: 22px;
        font-weight: 500;
        letter-spacing: 1.1px;
      }

      // 系统图
      .selectBtnBox:first-child {
        margin-left: 32px;
      }

      // 应急预案
      .selectBtnBox:last-child {
        width: 100px;
        height: 44px;

      }

      .active {
        color: #FFF700;
        border-bottom: 2px solid #FFF700;
      }

      .unactive {
        color: #ffffff;
        // border: 2px solid #4a5cd5;
      }
    }

    // 首警
    .firstAlarmBox {
      width: 1462px;
      height: 56px;
      display: flex;
      flex-direction: row;
      align-items: center;
      background: #4a5cd5;
      position: relative;

      // 首警警报图片
      .firstText {
        width: 24px;
        height: 24px;
        margin-left: 29px;
        display: flex;
        flex-direction: row;
        align-items: center;

        .firstIcon {
          width: 24px;
          height: 24px;
        }
      }

      .noneFireText {
        font-size: 20px;
        font-weight: 500;
        color: #ffffff;
        letter-spacing: 1px;
        margin-left: 19px;
      }

      .firstMessageBox {
        width: 1180px;
        height: 66px;
        display: flex;
        flex-direction: row;
        align-items: center;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;

        .firstAlarmTime {
          font-size: 20px;
          font-weight: 500;
          color: #ffffff;
          letter-spacing: 1px;
          margin-left: 19px;
        }
      }

      .examineFirstAlarm {
        width: 110px;
        height: 66px;
        font-size: 22px;
        font-weight: 700;
        color: #fff700;
        letter-spacing: 1.3px;
        cursor: pointer;
        position: absolute;
        right: 24px;
        top: 13px;
      }

      // 首警时间

    }

    // 内容
    .systemDetailBox,
    .projectDetailBox,
    .planDetailBox {
      width: 1462px;
      height: 884px;
      margin-top: 18px;
      background: #ffffff;

      .noneBox {
        width: 1462px;
        height: 884px;
        display: flex;
        align-items: center;
        justify-content: center;

        .noneImg {
          width: 1462px;
          height: 884px;
        }

        .noneText {
          height: 100px;
          font-size: 30px;
          font-weight: 600;
          color: #4a5cd5;
          position: absolute;
          top: 700px;
          right: 200px;
        }
      }
    }

    .alarmsBox {
      width: 1462px;
      height: 884px;
      margin-top: 18px;
      position: relative;

      .btnBox {
        width: 200px;
        height: 200px;
        position: absolute;
        z-index: 100;
        right: 127px;
        bottom: 78px;

        .topBtn {
          width: 200px;
          height: 60px;
          display: flex;
          align-items: center;
          justify-content: center;

          .upBtn {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            cursor: pointer;

            .IndexBtnIcon {
              width: 60px;
              height: 60px;

            }
          }
        }

        .centerBtn {
          width: 200px;
          height: 60px;
          display: flex;
          justify-content: space-around;
          margin-top: 16px;

          .upBtn {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            cursor: pointer;

            .IndexBtnIcon {
              width: 60px;
              height: 60px;
            }
          }
        }
      }

      :deep(.el-carousel__container) {
        width: 1462px;
        height: 884px;
        display: flex;
        align-items: center;
        justify-content: center;
      }

      :deep(.el-carousel__item) {
        width: 1462px;
        height: 884px;
        display: flex;
        align-items: center;
        justify-content: center;

      }

      // :deep(.el-carousel__indicators--outside){
      //   background-color: red;
      // }


      .imgTitle {
        position: absolute;
        width: 1094px;
        height: 150px;
        font-size: 25px;
        top: 0px;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: right;
      }

      .bigBox {
        width: 1094px;
        height: 670px;
        border-radius: 5px;
        border: 2px solid #605d5d;

        .alarmsImgBox {
          width: 1094px;
          height: 670px;
          position: relative;

          .imgbox {
            width: 1094px;
            height: 670px;
          }
        }

        .assign-device {
          position: absolute;
          cursor: pointer;

          :deep(.el-image) {
            float: left;
          }

          .arrowsUpImg {
            position: absolute;
            min-width: 80px;
            max-width: 100px;
            -webkit-animation: marker 1s linear infinite;
            animation: marker 1s linear infinite;
            z-index: 999;
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


        }
      }

      // 上一张
      .prevNextBox {
        width: 1462px;
        height: 884px;
        position: absolute;
        top: 0px;
        display: flex;
        justify-content: space-between;
        align-items: center;


        .prevBox {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          background-color: grey;
          display: flex;
          flex-direction: row;
          align-items: center;
          cursor: pointer;
          margin-left: 10px;
          z-index: 100;

          .prevImg {
            width: 30px;
            height: 30px;
            margin-left: 4px;
          }
        }

        .nextBox {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          background-color: grey;
          display: flex;
          flex-direction: row;
          align-items: center;
          cursor: pointer;
          margin-right: 10px;
          z-index: 100;

          .nextImg {
            width: 30px;
            height: 30px;
            margin-left: 6px;
          }
        }


      }

    }

    .projectDetailBox,
    .planDetailBox,
    .systemDetailBox {
      :deep(.el-carousel__container) {
        width: 1462px;
        height: 850px;
      }

      .objectImg {
        width: 1462px;
        height: 850px;
      }
    }

    /*火警动画效果*/
    .Firstcircle {
      width: 35px;
      height: 35px;
      position: absolute;
      float: left;
      z-index: 999;

      .FirstCircle1,
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
        -webkit-animation: circle 3s linear infinite;
        animation: circle 3s linear infinite;
      }

      .FirstCircle2 {
        -webkit-animation: circle 3s linear 0.8s infinite;
        animation: circle 3s linear 0.8s infinite;
      }

      .FirstCircle3 {
        -webkit-animation: circle 3s linear 1.6s infinite;
        /* Safari and Chrome */
        animation: circle 3s linear 1.6s infinite;
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
      /*top: 101px;*/
      /*left: 300px;*/
      /*margin: -100px 0 0 -100px;*/

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

      // .circle1 {
      //   -webkit-animation: circle 3s linear infinite;
      //   animation: circle 3s linear infinite;
      // }

      // .circle2 {
      //   -webkit-animation: circle 3s linear 0.8s infinite;
      //   animation: circle 3s linear 0.8s infinite;
      // }

      // .circle3 {
      //   -webkit-animation: circle 3s linear 1.6s infinite;
      //   /* Safari and Chrome */
      //   animation: circle 3s linear 1.6s infinite;
      // }

      // @-webkit-keyframes circle {

      //   /* Safari and Chrome */
      //   from {
      //     opacity: 1;
      //     -webkit-transform: scale(0);
      //   }

      //   to {
      //     opacity: 0;
      //     -webkit-transform: scale(3);
      //   }
      // }
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

      .launch_circle1 {
        -webkit-animation: circle 3s linear infinite;
        animation: circle 3s linear infinite;
      }

      .launch_circle2 {
        -webkit-animation: circle 3s linear 0.8s infinite;
        animation: circle 3s linear 0.8s infinite;
      }

      .launch_circle3 {
        -webkit-animation: circle 3s linear 1.6s infinite;
        /* Safari and Chrome */
        animation: circle 3s linear 1.6s infinite;
      }

      // @-webkit-keyframes launch_circle {

      //   /* Safari and Chrome */
      //   from {
      //     opacity: 1;
      //     -webkit-transform: scale(0);
      //   }

      //   to {
      //     opacity: 0;
      //     -webkit-transform: scale(3);
      //   }
      // }
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
</style>
