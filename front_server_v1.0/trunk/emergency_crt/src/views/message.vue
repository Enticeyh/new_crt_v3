<template>
    <div class="messageBox">
        <!-- 切换记录按钮 -->
        <div class="switchRecord" >
            <div class="switchBtn" :class="messageData.switchBtnActive == 6 ? 'active' : 'unactive'"
                @click="switchRecord(6)">图例查询</div>
            <div class="switchBtn" :class="messageData.switchBtnActive == 7 ? 'active' : 'unactive'"
                @click="switchRecord(7)">设备查询</div>
            <div class="switchBtn" :class="messageData.switchBtnActive == 8 ? 'active' : 'unactive'"
                @click="switchRecord(8)">设备状态查询</div>
            <div class="switchBtn" :class="messageData.switchBtnActive == 9 ? 'active' : 'unactive'"
                @click="switchRecord(9)">控制器查询</div>
            <div class="switchBtn" :class="messageData.switchBtnActive == 10 ? 'active' : 'unactive'"
                @click="switchRecord(10)">设备布点图</div>
            <div class="switchBtn" :class="messageData.switchBtnActive == 11 ? 'active' : 'unactive'"
                @click="switchRecord(11)">平面图查询</div>
            <div class="switchBtn" :class="messageData.switchBtnActive == 12 ? 'active' : 'unactive'"
                @click="switchRecord(12)">控制室信息</div>
        </div>
        <messageRecord :recordType="messageData.recordType"></messageRecord>
    </div>
</template>
<script>
import { useStore } from 'vuex'
import { toNumber } from 'lodash';
import { reactive, onMounted, watch } from 'vue'
import messageRecord from "../components/messageRecord/messageRecord.vue"
export default {
    components: {
        messageRecord
    },
    setup() {
        const store = useStore();
        let messageData = reactive({
            switchBtnActive: 1,
            recordType: 1,
        })
        onMounted(() => {
            switchRecord( sessionStorage.getItem("setSwitchRecord"))
        })
        const switchRecord = (type) => {
            store.commit('setSwitchRecord', type)
             sessionStorage.setItem("setSwitchRecord", type);
            messageData.recordType = toNumber(type)
            messageData.switchBtnActive = type
        }
        // 监听vuex存储状态变化
        watch(() => store.state.switchRecord, (newvalue, oldvalue) => {
            switchRecord(newvalue)
        })
        return {
            messageData,
            switchRecord,
        }
    }
}
</script>
<style scoped lang="scss">
.messageBox {
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
            width: 110px;
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

        .switchBtn:nth-child(2) {
            width: 88px;
        }

        .switchBtn:nth-child(3) {
            width: 132px;
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