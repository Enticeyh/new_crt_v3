import { createApp, Vue } from 'vue';
import router from './router'
import store from './store'
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';
import '../node_modules/lib-flexible' 
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import locale from "element-plus/lib/locale/lang/zh-cn";
import 'lib-flexible' 
import VueClipboard from 'vue-clipboard2'
import App from './App.vue';

const app = createApp(App)
app.use(router)
app.use(store)
app.use(Antd)
app.use(ElementPlus,{locale})
app.use(VueClipboard)
app.mount('#app')


