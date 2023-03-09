<template>
    <div>
        <div class="keyAll" id="keyAll" v-show="showKey"
            :style="`transition:all 0.5s; transform: translateX(${xData}px) translateY(${yData}px);`">
            <div id="main"></div>
            <div class="keybtnBox">
                <button class="button" style="background:red;color:#ffffff" @click="offKey">X</button>
                <button class="button" @click="yData -= 20">上</button>
                <button class="button" @click="yData += 20">下</button>
                <button class="button" @click="xData -= 20">左</button>
                <button class="button" @click="xData += 20">右</button>
            </div>
        </div>
    </div>
</template>

<script>
import '../../plugins/index'
export default {
    name: "SimpleKeyboard",
    data: () => ({
        xData: 0,
        yData: 0,
        showKey: false
    }),
    props: {
        input: {
            type: String
        },
        state: Boolean
    },
    
    mounted() {
        const keyboard = new aKeyboard.keyboard({
            el: '#main',
            style: {},
            // fixedBottomCenter: true
        })
        keyboard.inputOn('#input', 'value')


    },
    methods: {
        offKey() {
            this.showKey = false
            this.$emit("offKey", false);
        },
    },
    watch: {
        xData(newValue, oldValue) {
            if (newValue < 0) {
                this.xData = 0
            } else if (newValue > 566) {
                this.xData = 566
            }
        },
        yData(newValue, oldValue) {
            if (newValue < 0) {
                this.yData = 0
            } else if (newValue > 538) {
                this.yData = 538
            }
        },
        state(newValue, oldValue) {
            if (newValue == true) {
                this.showKey = true
            }
        },
    }
};
</script>
<style>
.keyAll {
    height: 260px;
    width: 800px;
    position: absolute;
    /* left: 0px; */
    /* bottom: 10px; */
    border-radius: 5px;
    z-index: 1000;
    display: flex;
    background-color: #1E9FFF;
}

.keybtnBox {
    width: 50px;
    height: 260px;
}

.button {
    width: 40px;
    height: 40px;
    border: none;
    margin-top: 10px;
    margin-left: 5px;
    border-radius: 5px;
    cursor: pointer;
}

.akeyboard-keyboard {
    height: 260px;
    width: 750px;
    background: #f0f0f0;
    border-radius: 5px;
    padding: 5px;
    padding-top: 9px;
    box-sizing: border-box;

}

.akeyboard-keyboard-innerKeys {
    text-align: center;
}

.akeyboard-keyboard-keys {
    height: 40px;
    width: 40px;
    border-radius: 5px;
    background: white;
    display: inline-block;
    line-height: 40px;
    text-align: center;
    box-sizing: border-box;
    margin: 4px;
    cursor: pointer;
    user-select: none;
}

.akeyboard-keyboard-keys:hover {
    background: #1E9FFF;
    color: white;
}

.akeyboard-keyboard-keys-Delete {
    width: 80px;
}

.akeyboard-keyboard-keys-Tab {
    width: 80px;
}

.akeyboard-keyboard-keys-Caps {
    width: 77px;
}

.akeyboard-keyboard-keys-Enter {
    width: 90px;
}

.akeyboard-keyboard-keys-Shift {
    width: 106px;
}

.akeyboard-keyboard-keys-Space {
    width: 350px;
}

.keyboard-keyboard-keys-focus {
    background: #1E9FFF;
    color: white;
}

/* .akeyboard-keyboard-fixedBottomCenter {
    width: 100% !important;
    position: fixed;
    bottom: 0px;
    left: 0px;
    border-radius: 0 !important;
} */
</style>