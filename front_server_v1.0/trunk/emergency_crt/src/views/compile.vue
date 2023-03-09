<!-- 信息编辑页面 -->
<template>
    <div class="compileBox">
        <!-- 切换记录按钮 -->
        <div class="switchRecord">
            <div class="switchBtn" :class="compileData.switchBtnActive == 11 ? 'active' : 'unactive'"
                @click="switchRecord(11)">项目列表</div>
            <div class="switchBtn" :class="compileData.switchBtnActive == 12 ? 'active' : 'unactive'"
                @click="switchRecord(12)">小区-楼宇信息</div>
            <div class="switchBtn" :class="compileData.switchBtnActive == 13 ? 'active' : 'unactive'"
                @click="switchRecord(13)">楼层信息</div>
            <div class="switchBtn" :class="compileData.switchBtnActive == 14 ? 'active' : 'unactive'"
                @click="switchRecord(14)">控制器设置</div>
            <div class="switchBtn" :class="compileData.switchBtnActive == 15 ? 'active' : 'unactive'"
                @click="switchRecord(15)">设备设置</div>
            <div class="switchBtn" :class="compileData.switchBtnActive == 18 ? 'active' : 'unactive'"
                @click="switchRecord(18)">布点图</div>
            <div class="switchBtn" :class="compileData.switchBtnActive == 17 ? 'active' : 'unactive'"
                @click="switchRecord(17)">设备类型列表</div>
        </div>
        <!-- 记录 -->
        <compileRecord :recordType="compileData.recordType" @recordSwitch="recordSwitch"></compileRecord>
    </div>
</template>
<script>
import { useStore } from 'vuex'
import { toNumber } from 'lodash';
import { reactive, onMounted, watch } from 'vue'
import compileRecord from "../components/compileRecord/compileRecord.vue"

export default {
    components: {
        compileRecord,
    },
    setup() {
        const store = useStore();
        let compileData = reactive({
            switchBtnActive: 1,
            recordType: 1,
        })
        onMounted(() => {
            switchRecord( sessionStorage.getItem("setSwitchRecord"))
        })
        // 标题切换记录
        const switchRecord = (type) => {
            store.commit('setSwitchRecord',  toNumber(type))
             sessionStorage.setItem("setSwitchRecord",  toNumber(type));
            compileData.recordType =  toNumber(type)
            compileData.switchBtnActive =  toNumber(type)
        }
        // 创建项目/楼宇/楼层以后切换记录
        const recordSwitch = (type) => {
            switchRecord(type)
        }
        // 监听vuex存储状态变化
        watch(() => store.state.switchRecord, (newvalue, oldvalue) => {
            switchRecord(newvalue)
        })

        return {
            compileData,
            switchRecord,
            recordSwitch
        }
    }
}
</script>
<style scoped lang="scss">
.compileBox {
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
            width: 145px;
        }

        .switchBtn:nth-child(3),
        .switchBtn:nth-child(5) {
            width: 88px;
        }

        .switchBtn:nth-child(6) {
            width: 66px;
        }

        .switchBtn:last-child {
            width: 132px;
        }


        .active {
            color: #4A5CD5;
            border-bottom: 4px solid #4A5CD5;
        }
    }
}
</style>