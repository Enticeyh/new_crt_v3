import {
  createStore
} from 'vuex'

export default createStore({
  state: {
    token: "",
    switchRecord:"",
    alarmsList:false,
    resetState:false,
    carouselTime:10000,
    superPassword:false,
    uploading:false,
    deviceRevampState:false,
  },
  mutations: {
    // token
    setToken(state, value) {
      state.token = value;
    },
    // // token
    setSwitchRecord(state, value) {
      state.switchRecord = value;
    },
    // token
    userInfo(state, value) {
      state.userInfo = value;
    },
    // token
    userTypeData(state, value) {
      state.userType = value;
    },
    // 轮巡接口 报警
    alarmsNumData(state, value) {
      state.alarmsData = value;
    },
    // 图片列表
    imgTypeData(state, value) {
      state.imgTypeList = value;
    },
    // 报警类型列表
    alarmsTypeData(state, value) {
      state.alarmsTypeList = value;
    },
    // 用户列表
    userListData(state, value) {
      state.userList = value;
    },
    // 项目列表
    projectListData(state, value) {
      state.projectList = value;
    },
    // 小区列表
    areaListData(state, value) {
      state.areaList = value;
    },
    // 楼宇列表
    buildingListData(state, value) {
      state.buildingList = value;
    },
    // 楼层列表
    floorsListData(state, value) {
      state.floorsList = value;
    },
    // 控制器列表
    controllersListData(state, value) {
      state.controllersList = value;
    },
    // 设备类型列表
    deviceTypeListData(state, value) {
      state.deviceTypeList = value;
    },
    // 国标事假列表
    gbEventTypeData(state, value) {
      state.gbEventTypeList = value;
    },
  },
  actions: {},
  modules: {}
})