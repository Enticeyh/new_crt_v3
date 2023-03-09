<template>
    <div class="systemSetBox">
        <!-- 切换记录按钮 -->
        <div class="switchRecord">
            <div class="switchBtn" :class="systemSetData.switchBtnActive == 24 ? 'active' : 'unactive'"
                @click="switchRecord(24)">用户管理</div>
            <div class="switchBtn" :class="systemSetData.switchBtnActive == 19 ? 'active' : 'unactive'"
                @click="switchRecord(19)">打印设置</div>
            <div class="switchBtn" :class="systemSetData.switchBtnActive == 20 ? 'active' : 'unactive'"
                @click="switchRecord(20)">参数设置</div>
            <div class="switchBtn" :class="systemSetData.switchBtnActive == 21 ? 'active' : 'unactive'"
                @click="switchRecord(21)">数据导出</div>
            <div class="switchBtn" :class="systemSetData.switchBtnActive == 22 ? 'active' : 'unactive'"
                @click="switchRecord(22)">远程传输</div>
            <div class="switchBtn" :class="systemSetData.switchBtnActive == 23 ? 'active' : 'unactive'"
                @click="switchRecord(23)">升级与导入</div>
        </div>
        <systemRecord :systemRecordState="systemSetData.systemRecordState"></systemRecord>
    </div>
</template>
<script>
import { useStore } from 'vuex'
import { toNumber } from 'lodash';
import { reactive, onMounted, watch } from 'vue'
import systemRecord from "../components/systemRecord/systemRecord.vue"
export default {
    components: {
        systemRecord
    },
    setup() {
        const store = useStore();
        let systemSetData = reactive({
            switchBtnActive: 1,
            systemRecordState: 1
        })
        onMounted(() => {
            switchRecord( sessionStorage.getItem("setSwitchRecord"))
        })
        const switchRecord = (type) => {
            store.commit('setSwitchRecord', type)
             sessionStorage.setItem("setSwitchRecord", type);
            systemSetData.systemRecordState = toNumber(type)
            systemSetData.switchBtnActive = toNumber(type)
        }
        // 监听vuex存储状态变化
        watch(() => store.state.switchRecord, (newvalue, oldvalue) => {
            switchRecord(newvalue)
        })
        return {
            systemSetData,
            switchRecord
        }
    }
}
</script>
<style scoped lang="scss">
.systemSetBox {
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
            width: 88px;
            margin-left: 60px;
        }



        .switchBtn:last-child {
            width: 110px;
        }


        .active {
            color: #4A5CD5;
            border-bottom: 4px solid #4A5CD5;
        }
    }
}
</style>