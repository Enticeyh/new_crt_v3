<template>
  <div class="headBox">
    <!-- 公司logo -->
    <div class="unitMark" @click="goIndex">
      <img class="unitMarkImg" src="../../assets/img/head/unitMark.svg" alt="" @dragstart.prevent>
    </div>
    <!-- 消防控制室图形显示系统  -->
    <div class="unitName" @click="goIndex">消防控制室图形显示系统</div>
    <!-- 主机通讯 -->
    <div class="hostBox">
      <template v-if="headData.controllerLinked == 1">
        <div class="hostColorBox">
          <div class="hostColorInterior"></div>
        </div>
      </template>
      <template v-else>
        <div class="offline">
          <div class="offlineInterior"></div>
        </div>
      </template>
      <div class="hostText">主机通讯</div>
    </div>
    <!-- 中心通讯 -->
    <div class="messageBox">
      <template v-if="headData.centerLinked == 1">
        <div class="hostColorBox">
          <div class="hostColorInterior"></div>
        </div>
      </template>
      <template v-else>
        <div class="offline">
          <div class="offlineInterior"></div>
        </div>
      </template>
      <div class="hostText">中心通讯</div>
    </div>
    <div class="rightBox">
      <!-- 用户信息 -->
      <template v-if="headData.userShow == true">
        <div class="userBox" v-if="headData.userShow" @click="openPopup(1)">
          <el-button class="loginBtn">登录</el-button>
          <div class="timeBox">{{ headData.currentDate }} {{ headData.week }} {{ headData.currentTime }}</div>

        </div>
      </template>
      <!-- 登录以后 -->
      <template v-else>
        <div class="loginBox" v-if="!headData.userShow">
          <!-- 空白占位 -->
          <div class="noneBox"></div>
          <!-- 注销换班 -->
          <div class="loginButtonBox">
            <!-- 换班 -->
            <div class="box" @click="openPopup(3)">
              <div class="imgBox">
                <img class="img" src="../../assets/img/head/changeShift.svg" alt="" @dragstart.prevent>
              </div>
              <div class="text">换班</div>
            </div>
            <!-- 注销 -->
            <div class="box" @click="openPopup(2)">
              <div class="imgBox">
                <img class="img" src="../../assets/img/head/logoutImg.svg" alt="" @dragstart.prevent>
              </div>
              <div class="text">关机</div>
            </div>
          </div>
          <div class="userLoginBox">
            <!-- 头像 -->
            <div class="userImgBox">
              <div class="userImg">
                <img class="userimg" src="../../assets/img/head/userImg.svg" alt="" @dragstart.prevent>
              </div>
              <div class="userNameBox">{{ headData.userData.user_name }}</div>
            </div>
            <div class="timeBox">{{ headData.currentDate }} {{ headData.week }} {{ headData.currentTime }}</div>
          </div>
        </div>
      </template>
      <!-- 按钮 -->
      <div class="buttonBox">
        <!-- 打印 -->
        <div class="printBox" @click="openPopup(4)">
          <div class="printImgBox">
            <img class="img" src="../../assets/img/head/printImg.svg" alt="" @dragstart.prevent>
          </div>
          <div class="printText">
            打印
          </div>
        </div>
        <!-- 复位 -->
        <div class="restorationBox" @click="openPopup(5)">
          <div class="printImgBox">
            <img class="img" src="../../assets/img/head/restorationImg.svg" alt="" @dragstart.prevent>
          </div>
          <div class="printText">
            复位
          </div>
        </div>
        <!-- 消音 -->
        <div class="erasureBox" @click="openShow()">
          <div class="printImgBox">
            <img class="img" src="../../assets/img/head/erasureImg.svg" alt="" @dragstart.prevent>
          </div>
          <div class="printText">
            消音
          </div>
        </div>
      </div>
    </div>
    <el-dialog v-model="headData.show" :show-close="false">
      <template #header>
        <div class="headerBox">消音</div>
        <div class="offBtn" @click="offShow">✖</div>
      </template>
      <div class="logoutMsg">
        您确认要进行消音吗？
      </div>
      <div class="sureBox">
        <button class="sureBtn" @click="erasure">确定</button>
        <button class="cancelBtn" @click="offShow">取消</button>
      </div>
    </el-dialog>
    <div class="alarmsTableBox" id="alarmsTableBox" v-show="headData.alarmsShow">
      <el-table :data="headData.tableData" class="alarmsTable" border
        :header-cell-style="{ color: '#000000', backgroundColor: '#F8F9FC' }">
        <el-table-column type="index" label="序号" align="center">
          <template #default="scope">
            <!-- <div class="deviceState">
              {{index}}
            </div> -->
          </template>
        </el-table-column>
        <el-table-column prop="alarm_type_name" label="报警类型" align="center" />
        <el-table-column prop="occurred_alarm_time" label="报警时间" align="center" :show-overflow-tooltip="true" />
        <el-table-column prop="alarm_current" label="地址" align="center" />
        <el-table-column prop="device_type_name" label="设备类型" align="center" :show-overflow-tooltip="true" />
        <el-table-column prop="description" label="描述" align="center" :show-overflow-tooltip="true" />
        <el-table-column prop="build_name" label="楼宇" align="center" />
        <el-table-column prop="floor_name" label="楼层" align="center" />
        <el-table-column label="报警方式" align="center" :show-overflow-tooltip="true">
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
        <el-table-column label="操作" width="80" align="center">
          <template #default="scope">
            <div class="operation" @click="openDetailImg(scope.row.floor_id)">
              查看
            </div>
          </template>

        </el-table-column>
      </el-table>
    </div>
    <div class="firstAlarms">
      <el-dialog v-model="headData.firstAlarmsShow" :show-close="false">
        <div class="logoutMsg">
          检测到首火警,是否立即跳转到首页进行查看？
        </div>
        <div class="sureBox">
          <button class="sureBtn" @click="SuregoIndex">确定({{headData.sureTime}})</button>
          <button class="cancelBtn" @click="offfirstAlarmsShow">取消</button>
        </div>
      </el-dialog>
    </div>
    <audio id="audio" muted autoplay :src="headData.videoUrl" />
    <popup :popupType="headData.popupType" @offPopup="offPopup" @sure="sure"></popup>
  </div>
</template>
<script>
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessage } from "element-plus";
import { reactive, onMounted, watch } from 'vue'
import popup from "../popup/popup"
import md5 from 'js-md5' //引入
import { logoutRequest, shiftUserRequest, loginRequest } from "../../api/login";
import {
  areaListRequest,
  userListRequest,
  projectListRequest,
  buildingListRequest,
  floorsListRequest,
  controllersListRequest,
  alarmsNumListRequest,
  deviceTypeRequest,
  imgTypeRequest,
  alarmsTypeRequest,
  gbEventTypeRequest,
  userTypeRequest
} from "../../api/baseData";
import { resetRequest, resetUpdateRequest } from "../../api/operation";
import { alarmsListRequest } from "../../api/baseData";
export default {
  components: {
    popup
  },
  props: {
    msg: String
  },
  setup() {
    let headData = reactive({
      videoUrl: "",
      show: false,//消音弹窗
      userData: {},///用户信息
      userShow: true,//控制用户登录以后显示页面
      popupType: 0,//控制顶部导航条显示弹窗类型
      message: {
        user_name: "",
        password: ""
      },
      Request: {
        page: 0
      },
      alarmsListRequest: {
        page: 0
      },
      currentTime: "",
      currentDate: "",
      week: "",
      centerLinked: 1,//控制器通讯
      controllerLinked: 1,//主机通讯
      alarmsNumList: {},
      musicState: true,
      firstAlarmsShow: false,
      firstAlarmsState: false,
      sureTime: 10
    })
    const store = useStore();
    const router = useRouter()
    let countdownInte = null
    let timer = null
    let timerr = null
    onMounted(() => {
      if (sessionStorage.getItem("userInfo")) {
        headData.userData = JSON.parse(sessionStorage.getItem('userInfo'))
        headData.userShow = false
      }
      request()
      alarmsList()
      alarmsList()
      timer = setInterval(() => {
        alarmsList()
      }, 3000)
      timer = setInterval(() => {
        getData();
      }, 1000);
    })
    // 播放报警
    const playAudio = () => {
      const audioObj = document.getElementById('audio')
      audioObj.muted = false
      if (audioObj) {
        audioObj.play()

      }
    }
    // 停止播放
    const stopAudio = () => {
      const audioObj = document.getElementById('audio')
      if (audioObj)
        audioObj.pause()
    }
    // 请求基础数据
    const request = () => {
      // 设备类型
      deviceTypeRequest(headData.Request).then((res) => {
        // 设备类型列表
        store.commit('deviceTypeListData', res.data.items)
      });
      // // 用户类型列表
      userTypeRequest(headData.Request).then((res) => {
        store.commit('userTypeData', res.data.items)
      });
      // 图片类型
      imgTypeRequest(headData.Request).then((res) => {
        store.commit('imgTypeData', res.data.items)
      });
      // 报警类型
      alarmsTypeRequest(headData.Request).then((res) => {
        store.commit('alarmsTypeData', res.data.items)
      });
      // 国标事件类型
      gbEventTypeRequest(headData.Request).then((res) => {
        store.commit('gbEventTypeData', res.data.items)
      });
    }
    // 获取报警数量列表
    const alarmsList = () => {
      alarmsNumListRequest(headData.Request).then((res) => {
        headData.alarmsNumList = res.data
        headData.centerLinked = res.data.center_linked
        headData.controllerLinked = res.data.controller_linked
        store.commit('alarmsNumData', res.data)
      });
    }
    // 打开弹窗
    const openPopup = (type) => {
      if (type == 4 || type == 5) {
        router.push({ name: 'webCrtIndex' })
      }

      if (type == 5 && headData.alarmsNumList.all_alarm == 0) return ElMessage({
        message: '暂无警报,无需复位',
        type: 'info',
        duration: 3 * 1000
      })
      headData.popupType = type
    }
    // 关闭弹窗
    const offPopup = () => {
      headData.popupType = 0
    }
    const goIndex = () => {
      router.push({ name: 'webCrtIndex' })
    }
    const sure = (popupData, operationType, selectData) => {
      if (operationType == 2) {
        logou(popupData)
      } else if (operationType == 3) {
        shift(popupData)
      } else if (operationType == 1) {
        login(popupData)
      } else if (operationType == 5) {
        resetRequest().then((res) => {
          if (res.ok) {

            headData.popupType = 0
            store.state.resetState = true
          }
        })
      } else if (operationType == 4) {
        headData.popupType = 0
        alarmsListRequest(headData.alarmsListRequest).then((res) => {
          headData.tableData = res.data.items
          let setItem = null
          setItem = setTimeout(() => {
            print()
          }, 1000)


        });
      }
    }
    const login = (popupData) => {
      loginRequest(popupData).then((res) => {
        if (res.ok) {
          headData.popupType = 0
          ElMessage({
            message: '登录成功',
            type: 'success',
            duration: 3 * 1000
          })
          headData.userData = res.data
          headData.userShow = false
          store.commit('setToken', res.data.token)
          store.commit('userInfo', res.data)
          sessionStorage.setItem("role_id", res.data.role_id);
          sessionStorage.setItem("userInfo", JSON.stringify(store.state.userInfo));
          // // 项目列表
          projectListRequest(headData.Request).then((res) => {
            store.commit('projectListData', res.data.items)
          });
          // 小区列表
          areaListRequest(headData.Request).then((res) => {
            store.commit('areaListData', res.data.items)
          });
          // 楼宇列表
          buildingListRequest(headData.Request).then((res) => {
            store.commit('buildingListData', res.data.items)
          });
          // 楼层列表
          floorsListRequest(headData.Request).then((res) => {
            store.commit('floorsListData', res.data.items)
          });
          // 控制器列表
          controllersListRequest(headData.Request).then((res) => {
            store.commit('controllersListData', res.data.items)
          });
        }
      });
    }
    // 退出登录
    const logou = (popupData) => {
      popupData.password = md5(popupData.password)
      logoutRequest(popupData).then((res) => {
        if (res.ok) {
          headData.userShow = true
          headData.popupType = 0
          sessionStorage.clear()
          router.push({ name: 'webCrtIndex' })
        }

      });
    }
    const shift = (val) => {

      let data = {
        user_name: val.user_name,
        password: md5(val.password),
      }
      shiftUserRequest(data).then((res) => {
        if (res.ok) {
          ElMessage({
            message: '换班成功',
            type: 'success',
            duration: 3 * 1000
          })
          headData.popupType = 0
          headData.userData = res.data
          store.commit('setToken', res.data.token)
          store.commit('userInfo', res.data)
          sessionStorage.setItem("role_id", res.data.role_id);
          sessionStorage.setItem("userInfo", JSON.stringify(store.state.userInfo));
          // // 项目列表
          projectListRequest(headData.Request).then((res) => {
            store.commit('projectListData', res.data.items)
          });
          // 小区列表
          areaListRequest(headData.Request).then((res) => {
            store.commit('areaListData', res.data.items)
          });
          // 楼宇列表
          buildingListRequest(headData.Request).then((res) => {
            store.commit('buildingListData', res.data.items)
          });
          // 楼层列表
          floorsListRequest(headData.Request).then((res) => {
            store.commit('floorsListData', res.data.items)
          });
          // 控制器列表
          controllersListRequest(headData.Request).then((res) => {
            store.commit('controllersListData', res.data.items)
          });
        }
      });
    }
    const print = () => {
      const printHTML = document.querySelector('#alarmsTableBox').innerHTML;
      const newWindow = window.open('', '');
      newWindow.document.write(printHTML);
      newWindow.window.print();
      newWindow.window.close();
      headData.popupType = 0
    }
    // 打开消音弹窗
    const openShow = () => {
      router.push({ name: 'webCrtIndex' })
      headData.show = true
    }
    const offShow = () => {
      headData.show = false
    }
    // 消音
    const erasure = () => {
      stopAudio()
      headData.musicState = false
      headData.show = false
    }
    // 获取当前时间
    const getData = () => {
      headData.currentTime = "";
      headData.currentDate = "";
      headData.week = "";

      let wk = new Date().getDay();
      let yy = new Date().getFullYear();
      let mm = new Date().getMonth() + 1;
      let dd = new Date().getDate();
      let weeks = [
        "星期日",
        "星期一",
        "星期二",
        "星期三",
        "星期四",
        "星期五",
        "星期六",
      ];
      let week = weeks[wk];
      headData.week = week;
      headData.currentDate = yy + "/" + mm + "/" + dd;

      let hh = new Date().getHours();
      let mf =
        new Date().getMinutes() < 10
          ? "0" + new Date().getMinutes()
          : new Date().getMinutes();
      let ss =
        new Date().getSeconds() < 10
          ? "0" + new Date().getSeconds()
          : new Date().getSeconds();
      headData.currentTime = hh + ":" + mf + ":" + ss;
    }
    const offfirstAlarmsShow = () => {
      headData.firstAlarmsShow = false
      headData.firstAlarmsState = false
    }
    const SuregoIndex = () => {
      router.push({ name: 'webCrtIndex' })
      headData.firstAlarmsShow = false
      headData.firstAlarmsState = false
      clearInterval(countdownInte)
    }
    watch(() => store.state.resetState, (newvalue, oldvalue) => {
      if (newvalue == true) {
        alarmsList()
      }
    })
    // 监听轮巡接口数据  播放声音 控制器复位
    watch(() => headData.alarmsNumList, (newvalue, oldvalue) => {
      // 预留 监听轮巡事件  当消音过后再次出现报警时 打开声音 
      if (newvalue.all_alarm != oldvalue.all_alarm) {
        headData.musicState = true
      }
      if (newvalue.controller_linked == 0 && headData.musicState == true) {
        headData.videoUrl = "../../../static/audio/guzhang.mp3"
        playAudio()
      } else if (newvalue.controller_linked == 1) {
        stopAudio()
      }
      if (newvalue.fire != 0 && headData.musicState == true) {
        // headData.videoUrl = "../../assets/img/audio/huojing.mp3"
        headData.videoUrl = "../../../static/audio/huojing.mp3"
        playAudio()
      } else if (newvalue.malfunction != 0 && headData.musicState == true) {
        // headData.videoUrl = "../../assets/img/audio/guzhang.mp3"
        headData.videoUrl = "../../../static/audio/guzhang.mp3"
        playAudio()
      } else if (newvalue.vl_malfunction != 0 && headData.musicState == true) {
        // headData.videoUrl = "../../assets/img/audio/guzhang.mp3"
        headData.videoUrl = "../../../static/audio/guzhang.mp3"
        playAudio()
      } else if (newvalue.malfunction != 0 && headData.musicState == true) {
        // headData.videoUrl = "../../assets/img/audio/guzhang.mp3"
        headData.videoUrl = "../../../static/audio/guzhang.mp3"
        playAudio()
      } else if (newvalue.feedback != 0 && headData.musicState == true) {
        // headData.videoUrl = "../../assets/img/audio/fankui.mp3"
        headData.videoUrl = "../../../static/audio/fankui.mp3"
        playAudio()
      } else if (newvalue.linkage != 0 && headData.musicState == true) {
        // headData.videoUrl = "../../assets/img/audio/liandong.mp3"
        headData.videoUrl = "../../../static/audio/liandong.mp3"
        playAudio()
      }


      if (newvalue.is_reset) {
        ElMessage({
          message: 'CRT复位成功,等待控制器请求数据',
          type: 'success',
          duration: 3 * 1000
        })
        resetUpdateRequest().then((res) => {
          if (res.ok) {
            store.state.resetState = true
            headData.firstAlarmsState = true
          }
        })
      }
      if (oldvalue.first_fire != undefined) {
        if (newvalue.first_fire != oldvalue.first_fire) {
          headData.firstAlarmsState = true
          if (router.currentRoute.value.path != '/'&&newvalue.first_fire!=0) {
            headData.firstAlarmsShow = true
          }
        }
      }

    })
    watch(() => headData.firstAlarmsShow, (newvalue, oldvalue) => {
      if (newvalue == true && headData.firstAlarmsState == true) {
        countdownInte = setInterval(() => {
          headData.sureTime -= 1
          if (headData.sureTime == 0) {
            clearInterval(countdownInte)
            headData.sureTime = 10
          }
        }, 1000)
      }
    })
    watch(() => headData.sureTime, (newvalue, oldvalue) => {
      if(newvalue==10&&headData.firstAlarmsShow==true){
        SuregoIndex()
      }
    
    })
    watch(() => sessionStorage.getItem("userInfo"), (oldvalue, newvalue) => {
      if (sessionStorage.getItem("userInfo")) {
        headData.userData = JSON.parse(sessionStorage.getItem('userInfo'))
        headData.userShow = false
      } else {
        headData.userShow = true
      }
    })

    return {
      headData,
      request,
      offPopup,
      openPopup,
      alarmsList,
      goIndex,
      getData,
      sure,
      login,
      openShow,
      offShow,
      erasure,
      playAudio,
      stopAudio,
      SuregoIndex,
      offfirstAlarmsShow
    }
  }
}
</script>
<style lang="scss" scoped>
.headBox {

  height: 86px;
  display: flex;
  flex-direction: row;
  align-items: center;
  background-color: #4A5CD5;

  // 公司logo
  .unitMark {
    width: 52px;
    height: 64px;
    margin-left: 40px;
    cursor: pointer;

    .unitMarkImg {
      width: 52px;
      height: 64px;
    }
  }

  // 消防控制室图形显示系统
  .unitName {
    width: 380px;
    height: 100px;
    display: flex;
    flex-direction: row;
    align-items: center;
    cursor: pointer;
    font-size: 30px;
    color: #FFFFFF;
    font-weight: 700;
    margin-left: 8px;
  }

  // 主机通讯 中心通讯
  .hostBox,
  .messageBox {
    width: 120px;
    height: 100px;
    margin-left: 53px;
    display: flex;
    align-items: center;

    .hostColorBox,
    .offline {
      width: 18px;
      height: 18px;
      background: #00ffba;
      border-radius: 50%;
      box-shadow: 0px 0px 6px 0px #000000 inset;

      .hostColorInterior,
      .offlineInterior {
        width: 12px;
        height: 12px;
        background: #00ffba;
        border-radius: 50%;
        margin-top: 3px;
        margin-left: 3px;
      }
    }

    .offline {
      background-color: #FFA200;

      .offlineInterior {
        background-color: #FFA200;
      }
    }

    .hostText {
      width: 90px;
      font-size: 20px;
      font-weight: 500;
      margin-left: 10px;
      color: #FFFFFF;
    }
  }

  // 中心通讯
  .messageBox {
    margin-left: 20px;
  }

  .rightBox {
    width: 1200px;
    height: 100px;
    align-items: center;
    display: flex;
    flex-direction: row-reverse;

    // 用户信息
    .userBox {
      width: 350px;
      display: flex;
      flex-direction: column;
      align-items: center;

      // 登录按钮
      .loginBtn {
        width: 90px;
        height: 36px;
        display: flex;
        align-items: center;
        background: #ffffff;
        border-radius: 2px;
        margin-left: 36px;
        font-size: 20px;
        color: #4A5CD5;
        font-weight: 700;
        margin-top: 10px;

        :deep(.el-button) {
          line-height: 36px;
        }
      }

      .timeBox {
        width: 350px;
        // height: 20px;
        margin-top: 8px;
        font-size: 20px;
        text-align: center;
        font-weight: 500;
        color: #FFFFFF;
      }
    }

    // 登录以后
    .loginBox {
      width: 566px;
      height: 100px;
      display: flex;
      flex-direction: row;

      // 空白占位
      .noneBox {
        width: 8px;
        height: 100px;
        background: #ffffff;
      }

      // 换班注销
      .loginButtonBox {
        height: 86px;
        display: flex;
        flex-direction: row;

        .box {
          width: 80px;
          height: 86px;
          margin-left: 26px;
          display: flex;
          align-items: center;
          cursor: pointer;

          .imgBox {
            width: 30px;
            height: 40px;

            .img {
              width: 26px;
              height: 26px;
            }
          }

          .text {
            display: flex;
            align-items: center;
            width: 50px;
            font-size: 20px;
            text-align: center;
            font-weight: 500;
            margin-left: 9px;
            color: #ffffff;
          }
        }
      }

      .userLoginBox {
        width: 350px;
        height: 100px;

        // 头像
        .userImgBox {
          // width: 350px;
          height: 30px;
          margin-top: 17px;
          display: flex;

          // 头像
          .userImg {
            width: 30px;
            height: 30px;

            margin-left: 106px;

            .userimg {
              width: 30px;
              height: 30px;
            }
          }

          .userNameBox {
            margin-left: 12px;
            font-size: 22px;
            font-weight: 700;
            color: #ffffff;
          }
        }

        // 时间
        .timeBox {
          width: 350px;
          margin-top: 8px;
          font-size: 20px;
          text-align: center;
          font-weight: 500;
          color: #FFFFFF;
        }
      }
    }


    // 按钮
    .buttonBox {
      width: 300px;
      height: 100px;
      display: flex;
      flex-direction: row-reverse;

      .printBox,
      .restorationBox,
      .erasureBox {
        width: 100px;
        display: flex;
        cursor: pointer;
        align-items: center;
        margin-right: 28px;

        // 图片
        .printImgBox {
          width: 42px;
          height: 42px;

          .img {
            width: 42px;
            height: 42px;
          }
        }

        .printText {
          width: 40px;
          height: 100px;
          font-size: 20px;
          font-weight: 500;
          display: flex;
          align-items: center;
          margin-left: 12px;
          color: #ffffff;
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
      font-size: 28px;
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

    .password {
      margin-top: 50px;
    }

    .changeBox {
      margin-top: 36px;
    }

    .testMsgBox {
      width: 490px;
      height: 44px;
      display: flex;
      margin-top: 36px;

      .testTextBox {
        width: 115px;
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
        width: 320px;
        height: 44px;
        margin-left: 10px;
      }
    }

    .fastBoxBtn {
      width: 80px;
      height: 44px;
      border: 1px solid #4a5cd5;
      border-radius: 2px;
      font-size: 22px;
      font-weight: 500;
      color: #4a5cd5;
      letter-spacing: 1.1px;
      display: flex;
      align-items: center;
      justify-content: center;
      position: absolute;
      top: 240px;
      right: 200px;
      cursor: pointer;
    }

    .account {
      position: relative;

      .upload-wrap {
        width: 120px;
        height: 44px;
        position: relative;
        display: inline-block;
        overflow: hidden;
        position: absolute;
        top: -43px;
        left: 200px;
        border-radius: 3px;
      }
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
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    font-weight: 500;
    color: #000000;
    letter-spacing: 1.6px;
  }

  // 选择器
  :deep(.el-select) {
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

  .firstAlarms {
    :deep(.el-dialog) {
      display: flex;
      flex-direction: column;
      margin: 0 !important;
      position: absolute;
      top: 20%;
      left: 50%;
      transform: translate(-50%, -50%);
      height: 170px;
      width: 500px;
      border-radius: 8px;

      .offBtn {
        position: absolute;
        width: 18px;
        height: 18px;
        color: #4A5CD5;
        font-size: 28px;
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
      width: 500px;
      height: 100px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      font-weight: 500;
      color: #000000;
      letter-spacing: 1.6px;
    }

    .sureBox {
      width: 500px;
      height: 70px;
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
  }
}

// dialog上下左右居中
</style>