<template>

  <Head></Head>
  <div class="Btn" id="testBtn" @click="test">
    <template v-if="appData.testShow == true">
      <img class="BtnImg" src="./assets/img/comment/onTestBtn.svg" alt="" @dragstart.prevent>
    </template>
    <template v-else>
      <img class="BtnImg" src="./assets/img/comment/testBtn.svg" alt="" @dragstart.prevent>
    </template>
  </div>
  <!-- <div class="Btn" id="keyboardBtn" @click="openkeyBoard">
    <img class="keyboardBtnImg" src="./assets/img/comment/keyboardBtnImg.svg" alt="">
  </div> -->
  <div class="Btn" id="helpBtn" @click="openHelp">
    <img class="helpBtnImg" src="./assets/img/comment/helpBtnImg.svg" alt="" @dragstart.prevent>
  </div>
  <div class="Btn" id="menuBtn" @click="openMenu">
    <template v-if="appData.menuShow == true">
      <img class="menuBtnImg" src="./assets/img/comment/onMenuBtnImg.svg" alt="" @dragstart.prevent>
    </template>
    <template v-else>
      <img class="menuBtnImg" src="./assets/img/comment/menuBtnImg.svg" alt="" @dragstart.prevent>
    </template>
  </div>
  <popup :popupType="appData.popupType" @offPopup="offPopup"></popup>
  <menuList :menuState="appData.menuState" @offMenu="offMenu"></menuList>
  <!-- <template v-if="appData.key==true">
  </template> -->
  <!-- <SimpleKeyboard :input="appData.input" @offKey="offKey" :state="appData.keyshow" /> -->

  <router-view />
</template>
<script>
import { reactive } from 'vue'
import { useStore } from 'vuex'
import config from "./utils/config";
import { ElMessage } from 'element-plus'
import Head from "../src/components/head/head.vue"
import popup from "../src/components/popup/popup"
import menuList from "../src/components/menu/menu"
// import SimpleKeyboard from "../src/components/SimpleKeyboard/SimpleKeyboard"
import { helpRequest } from "./api/baseData"
export default {
  components: {
    Head,
    popup,
    menuList,
    // SimpleKeyboard
  },
  setup() {
    const store = useStore();
    let appData = reactive({
      popupType: 0,//控制顶部导航条显示弹窗类型
      menuState: true,
      testShow: false,//控制测试按钮选中状态
      menuShow: true,//控制菜单按钮选中状态
      input: "",
      state: "",
      key: false,
      keyshow: false
    })
    const offKey = (data) => {
      appData.keyshow = data
    }
    // 打开模拟测试弹窗
    const test = () => {
      if ( sessionStorage.getItem("userInfo", store.state.token)) {
        appData.popupType = 6
        appData.testShow = true
      } else {
        ElMessage({
          message: '请登录后,再进行后续操作',
          type: 'error',
          duration: 3 * 1000
        })
      }

    }
    // 打开菜单按钮
    const openMenu = () => {
      appData.menuState = !appData.menuState
      appData.menuShow = true
    }
    const openHelp = () => {
      helpRequest().then((res) => {
        window.open(config.baseUrl + res.data.help_path, 'PDF', 'height=500,width=500,top:100,left:100,')
      });
    }
    // 关闭菜单按钮
    const offMenu = (val) => {
      if (val == true) {
        appData.menuState = false
        appData.menuShow = false
      } else {
        appData.menuState = true
        appData.menuShow = true
      }
    }
    // 关闭弹窗
    const offPopup = () => {
      appData.popupType = 0
      appData.testShow = false
    }
    const openkeyBoard = () => {
      // appData.key = true
      // appData.keyshow = true
    }
    return {
      appData,
      test,
      offPopup,
      openMenu,
      offMenu,
      openkeyBoard,
      offKey,
      openHelp
    }
  }
}
</script>
<style lang="scss">
* {
  margin: 0px;
  padding: 0px;
  user-select: none;

  .Btn {
    width: 70px;
    height: 70px;
    background: #ffffff;
    border: 1px solid #d5d5d5;
    border-radius: 36px;
    box-shadow: 0px 0px 10px 0px #dcdcdc;
    z-index: 101;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;

    .BtnImg,
    .menuBtnImg {
      width: 33px;
      height: 16px;
    }
  }

  #testBtn {
    // position: absolute;
    // bottom: 348px;
    // right: 11px;
    position: absolute;
    bottom: 258px;
    right: 11px;
  }

  #keyboardBtn {
    position: absolute;
    bottom: 258px;
    right: 11px;
  }

  #helpBtn {
    position: absolute;
    bottom: 168px;
    right: 11px;
  }

  #menuBtn {
    position: absolute;
    bottom: 78px;
    right: 11px;
  }


}
</style>
