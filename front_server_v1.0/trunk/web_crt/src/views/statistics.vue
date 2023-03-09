<template>
  <div class="statisticsBox">
    <!-- 切换记录按钮 -->
    <div class="switchRecord">
      <div class="switchBtn" :class="statisticsData.switchBtnActive == 1 ? 'active' : 'unactive'"
        @click="switchRecord(1)">报警记录</div>
      <div class="switchBtn" :class="statisticsData.switchBtnActive == 2 ? 'active' : 'unactive'"
        @click="switchRecord(2)">控制器操作记录</div>
      <div class="switchBtn" :class="statisticsData.switchBtnActive == 3 ? 'active' : 'unactive'"
        @click="switchRecord(3)">值班记录</div>
      <div class="switchBtn" :class="statisticsData.switchBtnActive == 4 ? 'active' : 'unactive'"
        @click="switchRecord(4)">用户操作记录</div>
      <div class="switchBtn" :class="statisticsData.switchBtnActive == 5 ? 'active' : 'unactive'"
        @click="switchRecord(5)">维保记录</div>
    </div>
    <alarmsRecord :recordType="statisticsData.recordType"></alarmsRecord>
  </div>
</template>
<script>
import { useStore } from 'vuex'
import { reactive, onMounted, watch } from 'vue'
import { toNumber } from 'lodash';
import alarmsRecord from "../components/statistics/alarmsRecord.vue"

export default {
  components: {
    alarmsRecord
  },
  setup() {
    const store = useStore();
    let statisticsData = reactive({
      switchBtnActive: 1,
      recordType: 1
    })
    onMounted(() => {
      switchRecord( sessionStorage.getItem("setSwitchRecord"))
    })

    const switchRecord = (type) => {
      store.commit('setSwitchRecord', type)
       sessionStorage.setItem("setSwitchRecord", type);
      statisticsData.recordType = toNumber(type)
      statisticsData.switchBtnActive = type
    }
    // 监听vuex存储状态变化
    watch(() => store.state.switchRecord, (newvalue, oldvalue) => {
      switchRecord(newvalue)
    })
    return {
      statisticsData,
      switchRecord,
    }
  }
}
</script>
<style scoped lang="scss">
.statisticsBox {
  display: flex;
  flex-direction: column;
  background-color: #F2F6FC;

  .switchRecord {
    width: 1760px;
    height: 56px;
    background: #ffffff;
    margin-top: 18px;
    margin-left: 80px;
    display: flex;
    flex-direction: row;
    align-items: center;

    .switchBtn {
      width: 88px;
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

    .switchBtn:first-child {
      margin-left: 60px;
    }

    .switchBtn:nth-child(2) {
      width: 154px;
    }

    .switchBtn:nth-child(4) {
      width: 134px;
    }

    .active {
      color: #4A5CD5;
      border-bottom: 4px solid #4A5CD5;
    }

    .unactive {
      color: #000000;
    }
  }
}
</style>