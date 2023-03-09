<template>
    <div class="popupBox">
        <!-- 登录 换班弹窗 -->
        <el-dialog v-model="popupData.loginShow" :show-close="false">
            <template #header>
                <div class="headerBox">
                    <template v-if="popupType == 1">欢迎登录</template>
                    <template v-else-if="popupType == 3">换班</template>
                </div>
                <div class="offBtn" @click="offPopup">✖</div>
            </template>
            <div class="loginBox">
                <template v-if="popupType == 1">
                    <div class="account">
                        <span style="color: red;">*</span>登录账号 <el-input v-model="popupData.loginAccount" id="refname"
                            @change="nameBlur" placeholder="请输入内容">
                        </el-input>
                    </div>
                    <div class="password">
                        <span style="color: red;">*</span>登录密码 <el-input v-model="popupData.loginPassword" id="refpass"
                            placeholder="请输入密码" type="password" @change="passBlur" @keydown.enter="sure">
                        </el-input>
                    </div>
                </template>
                <template v-else-if="popupType == 3">
                    <div class="changeBox">
                        <span style="color: red;">*</span>换班账号 <el-input v-model="popupData.shiftAccount" id="newname"
                            @change="newnameBlur" placeholder="请输入换班账号">
                        </el-input>
                    </div>
                    <div class="changeBox">
                        <span style="color: red;">*</span>换班密码 <el-input v-model="popupData.shiftPassword"
                            id="newpassword" @change="newpasswordBlur" placeholder="请输入换班密码" type="password">
                        </el-input>
                    </div>
                </template>

            </div>
            <div class="sureBox">
                <template v-if="popupType == 1">
                    <button class="sureBtn" @click="sureLogin">默认账号</button>
                    <button class="sureBtn" @click="sure">登录</button>

                </template>
                <template v-else-if="popupType == 3"><button class="sureBtn" @click="sure">确定</button></template>
            </div>
        </el-dialog>
        <!-- 模拟测试弹窗 -->
        <el-dialog v-model="popupData.testShow" :show-close="false">
            <template #header>
                <div class="headerBox">模拟测试</div>
                <div class="offBtn" @click="offPopup">✖</div>
            </template>
            <div class="testBox">
                <div class="testMsgBox">
                    <div class="testTextBox"><span style="color: red;">*</span>控制器号</div>
                    <div class="testSelectBox">
                        <el-select v-model="popupData.controllersSlect" placeholder="请选择控制器" clearable
                            @change="testSelectFun(popupData.controllersSlect, 1)"
                            @visible-change="testvisibleControllerList">
                            <el-option v-for="item in popupData.controllersList" :key="item.id" :label="item.code"
                                :value="item.code" />
                        </el-select>
                    </div>
                </div>
                <div class="testMsgBox">
                    <div class="testTextBox"> <span style="color: red;">*</span>回路号</div>
                    <div class="testSelectBox">
                        <el-select v-model="popupData.loopSlect" placeholder="请选择回路号" clearable
                            @change="testSelectFun(popupData.loopSlect, 2)">
                            <el-option v-for="item in popupData.loopList" :key="item" :label="item" :value="item" />
                        </el-select>
                    </div>

                </div>
                <div class="testMsgBox">
                    <div class="testTextBox"> <span style="color: red;">*</span>地址号</div>
                    <div class="testSelectBox">
                        <el-select v-model="popupData.partNumSlect" placeholder="请选择部位号" clearable
                            @change="testSelectFun(popupData.partNumSlect, 3)">
                            <el-option v-for="item in popupData.partNumList" :key="item.addr_num" :label="item.addr_num"
                                :value="item.addr_num" />
                        </el-select>
                    </div>
                </div>
                <div class="testMsgBox">
                    <div class="testTextBox">通道号</div>
                    <div class="testSelectBox">
                        <el-input v-model="popupData.testRequest.pass_num" placeholder="请输入通道号" clearable>
                        </el-input>
                    </div>
                </div>
                <div class="testMsgBox">
                    <div class="testTextBox"><span style="color: red;">*</span>模拟类型</div>
                    <div class="testSelectBox">
                        <el-select v-model="popupData.alarmsTypeSelsct" placeholder="请选择报警类型" clearable
                            @change="testSelectFun(popupData.alarmsTypeSelsct, 4)">
                            <el-option v-for="item in popupData.alarmsTypeList" :key="item.value" :label="item.label"
                                :value="item.value" />
                        </el-select>
                    </div>

                </div>
                <div class="testMsgBox" v-if="popupData.testObjectState">
                    <div class="testTextBox"><span style="color: red;">*</span>项目</div>
                    <div class="testSelectBox">
                        <el-select v-model="popupData.testOnjectSelsct" placeholder="请选择项目" clearable
                            @change="testSelectFun(popupData.testOnjectSelsct, 5)">
                            <el-option v-for="item in popupData.projectList" :key="item.id" :label="item.name"
                                :value="item.id" />
                        </el-select>
                    </div>

                </div>
                <div class="remarkBox">
                    <div class="remarkText">
                        备注
                    </div>
                    <div class="remarkInput">
                        <textarea class="explaininput" v-model="popupData.testRequest.note" />
                    </div>

                </div>
            </div>
            <div class="sureBox">
                <button class="sureBtn" @click="sure">确认</button>
            </div>
        </el-dialog>
        <!-- 7新建项目 新增用户弹窗 控制器上传 设备上传 -->
        <el-dialog v-model="popupData.newObjectShow" :show-close="false">
            <template #header>
                <div class="headerBox">
                    <template v-if="popupType == 7">新建项目</template>

                    <template v-else-if="popupType == 15">新建楼层</template>
                    <template v-else-if="popupType == 20">新增用户</template>
                    <template v-else-if="popupType == 23">导入控制器</template>
                    <template v-else-if="popupType == 24">导入设备</template>
                </div>
                <div class="offBtn" @click="offPopup">✖</div>
            </template>
            <!-- 新建项目 -->
            <template v-if="popupType == 7">
                <div class="loginBox">
                    <div class="account">
                        <span style="color: red;">*</span>项目名称 <el-input v-model="popupData.addObjectData.name"
                            clearable placeholder="请输入项目名称">
                        </el-input>
                    </div>
                    <div class="password">
                        <span style="color: red;">*</span>项目地址 <el-input v-model="popupData.addObjectData.address"
                            clearable placeholder="请输入项目地址">
                        </el-input>
                    </div>
                    <div class="password">
                        &nbsp;项目电话 <el-input v-model="popupData.addObjectData.mobile"
                            clearable placeholder="请输入项目电话">
                        </el-input>
                    </div>
                
                </div>
            </template>
            <!-- 新增用户 -->
            <template v-else-if="popupType == 20">
                <div class="loginBox">
                    <div class="newUserBox">
                        <div class="text">
                            <span style="color: red;">*</span>用户
                        </div>
                        <div class="input">
                            <el-input v-model="popupData.addUsser" placeholder="请输入角色名">
                            </el-input>
                        </div>
                    </div>
                    <div class="newUserBox">
                        <div class="text">
                            <span style="color: red;">*</span>角色名
                        </div>
                        <div class="input">
                            <el-select v-model="popupData.userTypeSelect" placeholder="请选择用户角色" clearable
                                @change="selectFun(popupData.userTypeSelect)">
                                <el-option v-for="item in popupData.userTypeList" :key="item.id" :label="item.name"
                                    :value="item.id" />
                            </el-select>
                        </div>


                    </div>
                    <div class="newUserBox">
                        <div class="text">
                            <span style="color: red;">*</span>密码
                        </div>
                        <div class="input">
                            <el-input v-model="popupData.addPassword" type="password" placeholder="请输入密码">
                            </el-input>
                        </div>

                    </div>
                    <div class="newUserBox">
                        <div class="text">
                            <span style="color: red;">*</span>确认密码
                        </div>
                        <div class="input">
                            <el-input v-model="popupData.addPasswordAgain" type="password" placeholder="请确认密码">
                            </el-input>
                        </div>


                    </div>
                </div>
            </template>
            <!-- 控制器上传 -->
            <template v-else-if="popupType == 23">
                <div class="controllerUploadingBox">
                    <div class="objectSelectBox">
                        <div class="selectBox">
                            项目: <el-select v-model="popupData.projectSelect" placeholder="请选择项目" clearable
                                @change="selectFun(popupData.projectSelect)" @visible-change="visibleObject">
                                <el-option v-for="item in popupData.projectList" :key="item.id" :label="item.name"
                                    :value="item.id" />
                            </el-select>
                        </div>
                        <div class="fileBox"><input type="file" @change="onchange" placeholder="上传文件"></div>
                    </div>
                </div>
            </template>
            <!-- 设备上传 -->
            <template v-else-if="popupType == 24">
                <div class="loginBox" v-loading="popupData.loading">
                    <div class="account">
                        控制器: <el-select v-model="popupData.controllersSlect" placeholder="请选择控制器" clearable
                            @change="selectFun(popupData.controllersSlect)" @visible-change="visibleControllerList">
                            <el-option v-for="item in popupData.controllersList" :key="item.id" :label="item.name"
                                :value="item.id" />
                        </el-select>
                    </div>
                    <div class="password">
                        <input type="file" @change="onchange" placeholder="上传文件">
                    </div>
                </div>
            </template>
            <div class="sureBox">
                <template v-if="popupType == 23">
                    <button class="sureBtn" @click="sure(1)">全部上传</button>
                    <button class="sureBtn" @click="sure(2)">单个上传</button>
                    <!-- <button class="sureBtn" @click="Onlysure">单个上传</button> -->
                </template>
                <template v-else>
                    <button class="sureBtn" @click="sure">确定</button>
                </template>
            </div>
        </el-dialog>
        <!-- 修改项目 修改楼宇 修改楼层 修改用户弹窗 -->
        <el-dialog v-model="popupData.redactObjectShow" :show-close="false">
            <template #header>
                <div class="headerBox">
                    <template v-if="popupType == 13">修改小区-楼宇</template>
                    <template v-else-if="popupType == 8">修改项目</template>
                    <template v-else-if="popupType == 16">修改楼层</template>
                    <template v-else-if="popupType == 22">修改用户</template>
                </div>
                <div class="offBtn" @click="offPopup">✖</div>
            </template>
            <!-- 修改项目 -->
            <template v-if="popupType == 8">
                <div class="loginBox">
                    <div class="account">
                        项目名称 <el-input v-model="popupData.revampName" clearable>
                        </el-input>
                    </div>
                    <div class="password">
                        项目地址 <el-input v-model="popupData.revampAddress" clearable>
                        </el-input>
                    </div>
                    <div class="password">
                        项目电话 <el-input v-model="popupData.revampMobile" clearable>
                        </el-input>
                    </div>
                    <div class="testMsgBox">
                        <div class="testTextBox">项目人员</div>
                        <div class="testSelectBox">
                            <el-select v-model="popupData.userSelect" multiple collapse-tags collapse-tags-tooltip
                                placeholder="请选择项目人员" @change="selectFun(popupData.userSelect, 1)"
                                @visible-change="visibleUser" clearable>
                                <el-option v-for="item in popupData.userList" :key="item.role_id"
                                    :label="item.user_name" :value="item.id" />
                            </el-select>
                        </div>
                    </div>
                </div>
            </template>
            <!-- 修改小区-楼宇 -->
            <template v-else-if="popupType == 13">
                <div class="loginBox">
                    <div class="areaBoxDetail">
                        <!-- :placeholder="popupData.popupFData.area_name" -->
                        小区名称 <el-input v-model="popupData.remopAreaName">
                        </el-input>
                        <div class="fastBoxBtn" @click="rempArea">修改</div>
                    </div>
                    <div class="password">
                        <!-- :placeholder="popupData.popupFData.name" -->
                        楼宇名称 <el-input v-model="popupData.revampBuildName">
                        </el-input>
                    </div>
                    <div class="password">
                        <input type="file" @change="onchange" accept=".svg" placeholder="上传文件">
                    </div>

                </div>
            </template>
            <!-- 修改楼层 -->
            <template v-else-if="popupType == 16">
                <div class="loginBox">

                    <div class="password">
                        <span style="color: red;">*</span>楼层名称 <el-input v-model="popupData.floorsName">
                        </el-input>
                    </div>
                    <div class="password">
                        <input type="file" @change="onchange" accept=".svg" placeholder="上传文件">
                    </div>
                </div>
            </template>
            <!-- 修改用户 -->
            <template v-else-if="popupType == 22">
                <div class="loginBox">
                    <div class="account">
                        <span style="color: red;">*</span>用户名&nbsp;<el-input v-model="popupData.addUsser" disabled
                            :placeholder="popupData.popupFData.user_name">
                        </el-input>
                    </div>
                    <div class="password">
                        <span style="color: red;">*</span>角色名
                        <el-select v-model="popupData.userTypeSelect" :placeholder="popupData.popupFData.role_name"
                            clearable @change="selectFun(popupData.userTypeSelect)">
                            <el-option v-for="item in popupData.userTypeList" :key="item.id" :label="item.name"
                                :value="item.id" />
                        </el-select>
                    </div>
                    <div class="password">
                        <span>&nbsp;&nbsp;</span> <span style="color: red;">*</span>密码 <el-input type="password"
                            v-model="popupData.addPassword" placeholder="请输入密码">
                        </el-input>
                    </div>
                    <div class="password">
                        <span>&nbsp;&nbsp;</span> <span style="color: red;">*</span>确认&nbsp;<el-input
                            v-model="popupData.addPasswordAgain" type="password" placeholder="请确认密码">
                        </el-input>
                        &nbsp;&nbsp;
                    </div>
                </div>
            </template>
            <div class="sureBox">
                <button class="sureBtn" @click="sure">确定</button>
            </div>
        </el-dialog>
        <!-- 注销 打印 消音/复位 删除项目 12删除楼宇 删除楼层 删除用户弹窗 -->
        <el-dialog v-model="popupData.deleteObjectShow" :show-close="false">
            <template #header>
                <div class="headerBox">
                    <template v-if="popupType == 2 || popupType == 4 || popupType == 5">提示</template>
                    <template v-else>删除</template>
                </div>
                <div class="offBtn" @click="offPopup">✖</div>
            </template>
            <div class="logoutMsg">
                <!-- 删除项目 -->
                <template v-if="popupType == 9">
                    请问您要删除
                    <span style="color:red">{{ popupData.popupFData.name }}</span>
                    项目吗?
                </template>
                <!-- 删除楼宇 -->
                <template v-else-if="popupType == 12">
                    此操作将永久删除<span style="color:red">{{ popupData.popupFData.name }}</span>楼宇信息,是否继续?
                </template>
                <!-- 删除楼层 -->
                <template v-else-if="popupType == 17">
                    此操作将永久删除<span style="color:red">{{ popupData.popupFData.name }}</span>楼层信息,是否继续?
                </template>
                <!-- 注销 -->
                <template v-else-if="popupType == 2">
                    <div class="inputSlect">
                        <span style="color: red;">*</span>请输入超级密码 &nbsp;
                        <el-input v-model="popupData.logout" placeholder="请输入密码" type="password" id="outlogin"
                            @change="outloginBlur">
                        </el-input>
                    </div>

                </template>
                <!-- 打印 -->
                <template v-else-if="popupType == 4">
                    请问您要将已撤警的警报也打印出来吗？
                </template>
                <!-- 复位 -->
                <template v-else-if="popupType == 5">
                    您确认要进行复位吗？
                </template>
                <!-- 删除用户 -->
                <template v-else-if="popupType == 21">
                    此操作将永久删除用户信息 是否继续?
                </template>
                <!-- 删除控制器 -->
                <template v-else-if="popupType == 25">
                    <span style="margin-left: 10px;">
                        此操作将永久删除<span style="color:red">{{ popupData.popupFData.name }}</span>信息及绑定的设备、设备布点信息,是否继续?
                    </span>
                </template>
            </div>
            <div class="sureBox">
                <button class="sureBtn" @click="sure">确定</button>
                <button class="cancelBtn" @click="offPopup">取消</button>
            </div>
        </el-dialog>
        <!-- 快捷创建项目 楼宇弹窗  14新建楼宇 15 新建楼层-->
        <div class="fastEstablish" v-show="popupData.fastEstablishShow">
            <el-dialog v-model="popupData.fastEstablishShow" :show-close="false">
                <template #header>
                    <template v-if="popupType == 10">
                        <div class="headerBox">快捷创建</div>
                    </template>
                    <template v-else-if="popupType == 11">
                        <div class="headerBox">快捷创建</div>
                    </template>
                    <template v-else-if="popupType == 14">
                        <div class="headerBox">新建楼宇</div>
                    </template>
                    <template v-else-if="popupType == 15">
                        <div class="headerBox">新建楼层</div>
                    </template>
                    <div class="offBtn" @click="offPopup">✖</div>
                </template>
                <!-- 项目列表快捷创建楼宇 -->
                <template v-if="popupType == 10">
                    <div class="fastEstablishMsg">
                        <div class="fastBox">项目名称 &nbsp;
                            <el-input v-model="popupData.loginAccount" :placeholder=popupData.popupFData.name
                                :disabled="true">
                            </el-input>
                        </div>
                        <div class="fastBox">
                            <span style="color: red;">*</span>小区名称 &nbsp;
                            <el-select v-model="popupData.areaSlect" placeholder="请选择小区" clearable
                                @change="selectFun(popupData.areaSlect)" @visible-change="visibleFast">
                                <el-option v-for="item in popupData.areaList" :key="item.id" :label="item.name"
                                    :value="item.id" />
                            </el-select>
                            <div class="fastBoxBtn" @click="openEstablishEstate">创建</div>

                        </div>
                        <div class="fastBox">
                            <el-switch v-model="popupData.switchValue" active-text="楼宇编号" inactive-text="楼宇名称">
                            </el-switch>
                            <template v-if="popupData.switchValue == false">
                                <div class="inputSlect">
                                    <span style="color: red;">*</span>楼宇名称 &nbsp;
                                    <el-input v-model="popupData.newBuilding" placeholder="请输入楼宇名称" clearable>
                                    </el-input>
                                </div>
                            </template>
                            <template v-else>
                                <div class="numberSlect">
                                    <span style="color: red;">*</span>楼宇编号 &nbsp;&nbsp;
                                    <el-input-number v-model="popupData.numOne" />
                                    ~
                                    <el-input-number v-model="popupData.numTwo" />
                                </div>
                            </template>
                        </div>

                        <div class="fastBox">
                            楼宇图片 &nbsp;
                            <input type="file" @change="onchange" accept=".svg" placeholder="上传文件">
                        </div>
                    </div>
                    <div class="sureBox">
                        <button class="sureBtn" @click="sure">确定</button>
                    </div>
                </template>
                <!-- 快捷创建楼层 -->
                <template v-else-if="popupType == 11">
                    <div class="fastEstablishMsg">
                        <div class="fastBox">
                            <span style="color: red;">*</span>小区名称 &nbsp;
                            <el-select v-model="popupData.areaSlect" disabled
                                :placeholder="popupData.popupFData.area_name" clearable
                                @change="selectFun(popupData.areaSlect, 1)">
                                <el-option v-for="item in popupData.areaList" :key="item.id" :label="item.name"
                                    :value="item.id" />
                            </el-select>
                            &nbsp; <span style="color: red;">*</span>楼宇名称 &nbsp;
                            <el-select v-model="popupData.buildingSlect" disabled
                                :placeholder="popupData.popupFData.name" clearable
                                @change="selectFun(popupData.buildingSlect, 2)">
                            </el-select>
                        </div>
                        <div class="fastBox">
                            <el-switch v-model="popupData.switchValue" active-text="楼层编号" inactive-text="楼层名称">
                            </el-switch>
                            <template v-if="popupData.switchValue == false">
                                <div class="inputSlect">
                                    <span style="color: red;">*</span>楼层名称 &nbsp;
                                    <el-input v-model="popupData.newFloors" placeholder="请输入楼层名称" clearable>
                                    </el-input>
                                </div>
                            </template>
                            <template v-else>
                                <div class="numberSlect">
                                    <span style="color: red;">*</span>楼层编号 &nbsp;&nbsp;
                                    <el-input-number v-model="popupData.floorStart" />
                                    ~
                                    <el-input-number v-model="popupData.floorEnd" />
                                </div>
                            </template>
                        </div>
                        <div class="fastBox">
                            <span style="color: red;">*</span>楼层图片 &nbsp;
                            <input type="file" @change="onchange" accept=".svg" placeholder="上传文件">
                        </div>
                    </div>
                    <div class="sureBox">
                        <button class="sureBtn" @click="sure">确定</button>
                    </div>
                </template>
                <!-- 新建楼宇 -->
                <template v-else-if="popupType == 14">
                    <div class="fastEstablishMsg">
                        <div class="fastBox">项目名称 &nbsp;<el-select v-model="popupData.projectSelect" placeholder="请选择项目"
                                clearable @change="selectFun(popupData.projectSelect,1)"
                                @visible-change="visibleObject">
                                <el-option v-for="item in popupData.projectList" :key="item.id" :label="item.name"
                                    :value="item.id" />
                            </el-select>
                        </div>
                        <div class="fastBox">
                            <span style="color: red;">*</span>小区名称 &nbsp;
                            <el-select v-model="popupData.areaSlect" placeholder="请选择小区" clearable
                                @change="selectFun(popupData.areaSlect,2)" @visible-change="visibleFast">
                                <el-option v-for="item in popupData.areaList" :key="item.id" :label="item.name"
                                    :value="item.id" />
                            </el-select>
                            <div class="fastBoxBtn" @click="openEstablishEstate">创建</div>
                            <div class="fastBoxBtn" @click="deleteArea">删除</div>

                        </div>
                        <div class="fastBox">
                            <el-switch v-model="popupData.switchValue" active-text="楼宇编号" inactive-text="楼宇名称">
                            </el-switch>
                            <template v-if="popupData.switchValue == false">
                                <div class="inputSlect">
                                    <span style="color: red;">*</span>楼宇名称 &nbsp;
                                    <el-input v-model="popupData.newBuilding" clearable placeholder="请输入楼宇名称">
                                    </el-input>
                                </div>
                            </template>
                            <template v-else>
                                <div class="numberSlect">
                                    <span style="color: red;">*</span>楼宇编号 &nbsp;&nbsp;
                                    <el-input-number v-model="popupData.numOne" />
                                    ~
                                    <el-input-number v-model="popupData.numTwo" />
                                </div>
                            </template>
                        </div>
                        <div class="fastBox">
                            楼宇图片 &nbsp;
                            <input type="file" @change="onchange" accept=".svg" placeholder="上传文件">
                        </div>
                    </div>
                    <div class="sureBox">
                        <button class="sureBtn" @click="sure">确定</button>
                    </div>
                </template>
                <!-- 新建楼层 -->
                <template v-else-if="popupType == 15">
                    <div class="fastEstablishMsg">
                        <div class="fastBox">
                            <span style="color: red;">*</span>小区名称 &nbsp;
                            <el-select v-model="popupData.areaSlect" placeholder="请选择小区" clearable
                                @change="selectFun(popupData.areaSlect, 1)" @visible-change="visible">
                                <el-option v-for="item in popupData.areaList" :key="item.id" :label="item.name"
                                    :value="item.id" />
                            </el-select>
                            &nbsp; <span style="color: red;">*</span>楼宇名称 &nbsp;
                            <el-select v-model="popupData.buildingSlect" placeholder="请选择楼宇" clearable
                                @change="selectFun(popupData.buildingSlect, 2)" @visible-change="visibleNewFloors">
                                <el-option v-for="item in popupData.buildingList" :key="item.id" :label="item.name"
                                    :value="item.id" />
                            </el-select>
                        </div>
                        <div class="fastBox">
                            <el-switch v-model="popupData.switchValue" active-text="楼层编号" inactive-text="楼层名称">
                            </el-switch>
                            <template v-if="popupData.switchValue == false">
                                <div class="inputSlect">
                                    <span style="color: red;">*</span>楼层名称 &nbsp;
                                    <el-input v-model="popupData.newFloors" placeholder="请输入楼层名称" clearable>
                                    </el-input>
                                </div>
                            </template>
                            <template v-else>
                                <div class="numberSlect">
                                    <span style="color: red;">*</span>楼层编号 &nbsp;&nbsp;
                                    <el-input-number v-model="popupData.floorStart" />
                                    ~
                                    <el-input-number v-model="popupData.floorEnd" />
                                </div>
                            </template>
                        </div>
                        <div class="fastBox">
                            <span style="color: red;">*</span>楼层图片 &nbsp;
                            <input type="file" @change="onchange" accept=".svg" placeholder="上传文件">
                        </div>
                    </div>
                    <div class="sureBox">
                        <button class="sureBtn" @click="sure">确定</button>
                    </div>
                </template>
            </el-dialog>
        </div>
        <!-- 创建小区弹窗 -->
        <el-dialog v-model="popupData.establishEstateShow" :show-close="false">
            <template #header>
                <div class="headerBox">创建-修改小区</div>
                <div class="offBtn" @click="offEstablishEstateShow">✖</div>
            </template>
            <div class="loginBox">
                <div class="changeBox">
                    小区名称 <el-input v-model="popupData.newAreaName" placeholder="请输入小区名称">
                    </el-input>
                </div>
            </div>
            <div class="sureBox">
                <button class="sureBtn" @click="sureoffEstablishEstateShow">确定</button>
                <button class="cancelBtn" @click="offEstablishEstateShow">取消</button>
            </div>
        </el-dialog>
        <!-- 控制器编辑 设备编辑弹窗 -->
        <div class="controllerBox">
            <el-dialog v-model="popupData.controllerShow" :show-close="false">
                <template #header>
                    <div class="headerBox">
                        <template v-if="popupType == 18">控制器编辑</template>
                        <template v-else-if="popupType == 19">设备编辑</template>
                    </div>
                    <div class="offBtn" @click="offPopup">✖</div>
                </template>
                <!-- 控制器编辑弹窗 -->
                <template v-if="popupType == 18">
                    <div class="controllerMsg">
                        <div class="controllerBox">
                            <span style="color: red;">*</span>名称 &nbsp;
                            <el-input v-model="popupData.controllerName" clearable>
                            </el-input>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                            <span style="color: red;">*</span>编号 &nbsp;
                            <el-input v-model="popupData.controllerCode" clearable>
                            </el-input>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                            <span style="color: red;">*</span>装机日期 &nbsp;
                            <el-input v-model="popupData.controllersetupdate" clearable>
                            </el-input>
                        </div>
                        <div class="controllerBox">
                            <span style="color: red;">*</span>型号 &nbsp;
                            <el-input v-model="popupData.controllerType" clearable>
                            </el-input>&nbsp;&nbsp;
                            主从机选择 &nbsp;
                            <el-select v-model="popupData.controllerTypeSelect" clearable>
                                <el-option v-for="item in popupData.controllerTypeArr" :key="item.value"
                                    :label="item.label" :value="item.value" />
                            </el-select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                            <span style="color: red;">*</span>供应商&nbsp;
                            <el-input v-model="popupData.controllerManufacturer" clearable>
                            </el-input>
                        </div>
                    </div>
                </template>
                <!-- 设备编辑弹窗 -->
                <template v-else-if="popupType == 19">
                    <div class="deviceMsg">
                        <div class="deviceBox">
                            回路号 &nbsp;
                            <input class="deviceInput" type="text" :disabled="true"
                                :placeholder="popupData.popupFData.loop_num"
                                style="backgroundColor: #D5D8E4;">&nbsp;&nbsp;&nbsp;&nbsp;
                            地址号 &nbsp;
                            <input class="deviceInput" type="text" :disabled="true"
                                :placeholder="popupData.popupFData.addr_num"
                                style="backgroundColor: #D5D8E4;">&nbsp;&nbsp;
                            设备类型 &nbsp;
                            <el-select v-model="popupData.deviceTypeSlect"
                                :placeholder="popupData.popupFData.device_type_name" clearable
                                @change="selectFun(popupData.deviceTypeSlect)">
                                <el-option v-for="item in popupData.deviceTypeList" :key="item.id" :label="item.name"
                                    :value="item.id" />
                            </el-select>
                        </div>
                        <div class="deviceBox">
                            制造商 &nbsp;
                            <input class="deviceInput" type="text" :disabled="true"
                                :placeholder="popupData.popupFData.manufacturer"
                                style="backgroundColor: #D5D8E4;">&nbsp;
                            安装日期 &nbsp;
                            <input class="deviceInput" type="text" :disabled="true"
                                :placeholder="popupData.popupFData.setup_date"
                                style="backgroundColor: #D5D8E4;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                            型号 &nbsp;
                            <input class="deviceInput" type="text" :disabled="true"
                                :placeholder="popupData.popupFData.device_model" style="backgroundColor: #D5D8E4;">
                        </div>
                        <div class="deviceBox">
                            维保周期 &nbsp;
                            <input class="deviceInput" type="text" :disabled="true"
                                :placeholder="popupData.popupFData.maintain_cycle"
                                style="backgroundColor: #D5D8E4;">&nbsp;&nbsp;&nbsp;&nbsp;
                            有效期 &nbsp;
                            <input class="deviceInput" type="text" :disabled="true"
                                :placeholder="popupData.popupFData.expiration_date"
                                style="backgroundColor: #D5D8E4;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                            PSN &nbsp;
                            <input class="deviceInput" type="text" v-model="popupData.devicePsn"
                                style="backgroundColor: #F7F8FC;">
                        </div>
                        <div class="deviceRemark">
                            设备图标&nbsp;
                            <div class="deviceImg">
                                <img class="deviceimg" :src="popupData.url + popupData.popupFData.path" alt="" @dragstart.prevent>
                            </div>
                            备注 &nbsp;
                            <div class="remarkInput">
                                <textarea class="explaininput" v-model="popupData.deviceDescription" />
                                <span style="color:red">注意:修改注释需按照格式</span>
                            </div>

                        </div>
                    </div>
                </template>
                <div class="sureBox">
                    <button class="sureBtn" @click="sure">确定</button>
                </div>
            </el-dialog>
        </div>
    </div>
</template>
<script>
import { reactive, watch, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import config from "../../utils/config";
import { ElMessage } from 'element-plus'
import { loginRequest } from "../../api/login";
import { newAreaRequest, revampAreaRequest, testRequest, deleteAreaRequest } from "../../api/operation";
import {
    areaListRequest,
    userListRequest,
    projectListRequest,
    buildingListRequest,
    controllersListRequest,
    inquireLoopRequest,
    deviceListRequest,
    alarmsNumListRequest,
    floorsListRequest
} from "../../api/baseData";
import md5 from 'js-md5' //引入
import { Plus } from '@element-plus/icons-vue'
import { toNumber } from 'lodash';

export default {
    props: {
        popupType: Number,
        popupData: Object
    },
    components: {
        Plus
    },
    setup(props, context) {
        let popupData = reactive({
            upFileInfo: {
                headerToken: {},
                upFileUrl: 'http://127.0.0.1:8000/api/v1/controllers/files'
            },
            url: "",
            routerData: "",
            fileList: [],
            userTypeSelect: "",//用户类型选择器
            userTypeList: [],//用户类型列表
            popupFData: {},//父组件传递数据
            userSelect: "",//用户选择器
            userList: [],//用户列表
            selectData: "",
            projectSelect: "",//项目选择器
            testOnjectSelsct: "",//模拟测试项目选择器
            projectList: [],//项目列表
            areaSlect: "",//小区选择器
            areaList: [],//小区列表
            buildingSlect: "",//楼宇选择器
            buildingList: [],//楼宇列表
            controllersSlect: "",//控制器选择器
            controllersList: [],//控制器列表
            loopSlect: "",//回路号 选择器
            loopList: [],//回路号列表
            partNumSlect: "",//部位号选择器
            partNumList: [],//部位号列表
            alarmsTypeSelsct: "",//报警类型选择器
            alarmsTypeList: [
                {
                    value: '1',
                    label: '火警',
                },
                {
                    value: '2',
                    label: '启动',
                },
                {
                    value: '4',
                    label: '故障',
                },
            ],//报警类型列表
            deviceTypeSlect: "",//设备类型选择器
            deviceTypeList: [],//设备类型列表
            loginShow: false,//控制登录弹窗显示隐藏
            loginAccount: "",//登录账号
            loginPassword: "",//登录密码
            logout: "",//注销密码
            testShow: false,//控制模拟测试弹窗个显示隐藏
            newObjectShow: false,//控制新建项目弹窗显示隐藏
            redactObjectShow: false,//控制修改项目弹窗显示隐藏
            deleteObjectShow: false,//控制注销 消音/复位 打印 删除项目 删除楼宇 删除楼层 弹窗显示隐藏
            fastEstablishShow: false,//控制快捷创建项目 楼宇弹窗显示隐藏
            switchValue: false,//切换楼宇输入名称或选择
            numOne: 0,//控制楼层选择器
            numTwo: 0,
            establishEstateShow: false,//控制创建小区名称弹窗显示隐藏
            loading: false,
            message: {
                user_name: "",
                password: ""
            },
            addObjectData: {
                name: "",//项目名称
                address: "",//项目地址
                mobile: "",//项目电话
                is_active:""
            },
            objectTypeSelect:"",
            objectTypeSelectArr: [
                {
                    value: '1',
                    label: '是',
                },
                {
                    value: '0',
                    label: '否',
                },
            ],
            testRequest: {
                controller_num: "",
                loop_num: "",
                addr_num: "",
                pass_num: "",
                alarm_type_id: "",
                note: "",
                project_id:""
            },
            Request: {
                page: 0
            },
            newBuilding: "",
            newAreaName: "",
            // 修改楼宇小区
            revampBuildName: "",//楼宇名称
            remopAreaName: "",
            // 快捷创建楼层
            newFloors: "",
            floorStart: 0,
            floorEnd: 0,
            // 修改楼层
            floorsName: "",
            controllerShow: false,//控制器编辑弹窗
            controllerTypeSelect: "",
            controllerTypeArr: [
                {
                    value: '1',
                    label: '主机',
                },
                {
                    value: '2',
                    label: '从机',
                },
            ],
            controllerName: "",//控制器名称
            controllerCode: "",//控制器编号
            controllersetupdate: "",//控制器装机日期
            controllerType: "",//控制器型号
            controllerManufacturer: "",//控制器制造商
            // 换班
            shiftAccount: "",//换班账号
            shiftPassword: "",//换班密码
            // 修改设备
            devicePsn: "",//设备psn
            deviceDescription: "",//设备描述
            // 新增用户
            addUsser: "",//新增用户名称
            addPassword: "",//新增用户密码
            addPasswordAgain: "",//新增用户确定密码
            testObjectState: false,//模拟测试多项目选择器
        })
        popupData.url = config.baseUrl
        const store = useStore()
        const router = useRouter()
        const visibleObject = (val) => {
            if (val == true && popupData.projectSelect == "") {
                let Request = {
                    page: 0,
                }
                projectListRequest(Request).then((res) => {
                    popupData.projectList = res.data.items
                });
            }

        }
        onMounted(() => {

        });

        // 快捷创建小区 下拉框
        const visible = () => {
            let Request = {
                page: 0,
            }
            areaListRequest(Request).then((res) => {
                popupData.areaList = res.data.items
                store.commit('areaListData', res.data.items)
            });
            popupData.areaList = []
            popupData.areaList = store.state.areaList
        }
        // 新建楼层弹窗 下拉楼宇
        const visibleNewFloors = (val) => {
            if (val == true && popupData.areaSlect == "") {
                ElMessage({
                    message: '请先选择小区',
                    type: 'info',
                    duration: 3 * 1000
                })
            }

        }
        // 快捷创建小区 下拉框
        const visibleFast = (val) => {
            let Request = {}
            // 判断是否为项目列表快捷创建 小区楼宇创建
            if (props.popupType == 10) {
                Request.page = 0
                Request.project_id = popupData.popupFData.id
            } else if (props.popupType == 14) {
                Request.page = 0
                Request.project_id = popupData.projectSelect
            }
            if (Request.project_id != '') {
                areaListRequest(Request).then((res) => {
                    popupData.areaList = res.data.items
                    store.commit('areaListData', res.data.items)
                });
                popupData.areaList = []
                popupData.areaList = store.state.areaList
            } else if (val == true && Request.project_id == "") {
                ElMessage({
                    message: '请先选择项目',
                    type: 'info',
                    duration: 3 * 1000
                })
            }


        }
        // 修改项目 下拉项目人员
        const visibleUser = () => {
            userListRequest(popupData.Request).then((res) => {
                popupData.userList = res.data.items
            });
        }
        // 模拟测试控制器下拉
        const testvisibleControllerList = (val) => {
            if (popupData.projectList.length != 1 && popupData.projectList.length != 0 && popupData.testOnjectSelsct == "" && val == true) return ElMessage({
                message: '请先选择项目',
                type: 'info',
                duration: 3 * 1000
            })
            if (val == true) {
                popupData.Request.project_id = popupData.testOnjectSelsct
                controllersListRequest(popupData.Request).then((res) => {
                    store.commit('controllersListData', res.data.items)
                    popupData.controllersList = res.data.items
                    if (val == true) {
                        if (popupData.controllersList.length == 0) return ElMessage({
                            message: '该项目下暂无控制器',
                            type: 'error',
                            duration: 3 * 1000
                        })
                    }

                });
            }

        }
        // 控制器下拉
        const visibleControllerList = () => {

            controllersListRequest(popupData.Request).then((res) => {
                store.commit('controllersListData', res.data.items)
                popupData.controllersList = res.data.items
            });
        }
        // 打开创建小区弹窗
        const openEstablishEstate = () => {
            if (props.popupType == 10) {
                popupData.establishEstateShow = true
            } else if (props.popupType == 14) {
                if (popupData.selectData == "") {
                    ElMessage({
                        message: '请选择项目',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else {
                    popupData.establishEstateShow = true
                }
            }
        }
        // 关闭创建小区弹窗
        const offEstablishEstateShow = () => {
            popupData.establishEstateShow = false
        }
        //创建小区
        const sureoffEstablishEstateShow = () => {
            let Request = {}
            // 判断是否为项目列表快捷创建 小区楼宇创建
            Request.name = popupData.newAreaName
            if (props.popupType == 10) {

                Request.project_id = popupData.popupFData.id
            } else if (props.popupType == 14) {

                if (popupData.selectData == "") {
                    ElMessage({
                        message: '请选择项目',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else {
                    Request.project_id = popupData.selectData
                }
            }
            newAreaRequest(Request).then((res) => {
                if (res.ok) {
                    ElMessage({
                        message: '小区信息保存成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    // 修改小区以后更新 小区列表
                    let Request = {
                        page: 0
                    }
                    popupData.establishEstateShow = false
                    // 小区列表
                    areaListRequest(Request).then((res) => {
                        store.commit('areaListData', res.data.items)
                    });
                    popupData.areaList = []
                    popupData.areaList = store.state.areaList
                    if (popupData.areaList) {
                        popupData.establishEstateShow = false
                        popupData.newAreaName = ""
                    }
                }
            });
        }
        // 修改小区
        const rempArea = () => {
            let data = {
                name: popupData.remopAreaName,
                area_id: popupData.popupFData.area_id
            }
            revampAreaRequest(data).then((res) => {
                if (res.ok) {
                    ElMessage({
                        message: '修改成功',
                        type: 'success',
                        duration: 3 * 1000
                    })
                    // 修改小区以后更新 小区列表
                    areaListRequest(popupData.Request).then((res) => {
                        store.commit('areaListData', res.data.items)
                    });
                }
            });
        }
        // 删除小区
        const deleteArea = () => {
            if (popupData.projectSelect == "") {
                ElMessage({
                    message: '请选择项目',
                    type: 'error',
                    duration: 3 * 1000
                })
            } else if (popupData.areaSlect == "") {
                ElMessage({
                    message: '请点击左侧选择一个小区',
                    type: 'error',
                    duration: 3 * 1000
                })
            } else {
                deleteAreaRequest(popupData.areaSlect).then((res) => {
                    if (res.ok) {

                        ElMessage({
                            message: '删除小区成功',
                            type: 'info',
                            duration: 3 * 1000
                        })
                        popupData.areaSlect = ""
                        areaListRequest(popupData.Request).then((res) => {
                            store.commit('areaListData', res.data.items)
                        });
                        popupData.areaList = []
                        popupData.areaList = store.state.areaList
                    }
                });
            }

        }
        // 关闭弹窗
        const offPopup = () => {
            context.emit('offPopup', false, 0);
            if (props.popupType == 1) {
                popupData.loginAccount = ""
                popupData.loginPassword = ""
            } else if (props.popupType == 6) {
                popupData.controllersSlect = ""
                popupData.loopSlect = ""
                popupData.partNumSlect = ""
                popupData.alarmsTypeSelsct = ""
                popupData.testRequest.pass_num = ""
                popupData.testRequest.note = ""

            } else if (props.popupType == 7) {
                popupData.addObjectData.name = "",//清空项目名称输入框
                    popupData.addObjectData.address = "",//清空项目地址输入框
                    popupData.addObjectData.mobile = ""//清空联系电话输入框
            } else if (props.popupType == 8) {
                popupData.userSelect = ""//清空项目人员多选
            } else if (props.popupType == 10 || props.popupType == 14) {
                popupData.areaSlect = "",//清空小区名称
                    popupData.newBuilding = ""//清空楼宇名称
                popupData.numOne = 0
                popupData.numTwo = 0
                popupData.switchValue = false
            } else if (props.popupType == 13) {
                popupData.remopAreaName = popupData.popupFData.area_name
                popupData.revampBuildName = ""
            } else if (props.popupType == 15) {
                popupData.areaSlect = ""
                popupData.buildingSlect = ""

            } else if (props.popupType == 16) {
                popupData.floorsName = popupData.popupFData.name//清空楼层选择
            } else if (props.popupType == 18) {
                popupData.controllerTypeSelect = ""
            } else if (props.popupType == 20) {
                popupData.addUsser = ""
                popupData.addPassword = ""
                popupData.selectData = ""
                popupData.userTypeSelect = ""
                popupData.addPasswordAgain = ""
            }
        }
        // 选择器
        const selectFun = (val, num) => {
            popupData.selectData = val
            // 当弹窗为 新建楼层时 选择小区以后根据小区id请求楼宇列表
            if (props.popupType == 15) {
                if (val) {
                    if(num==1){
                        popupData.buildingList = []
                    let data = {
                        page: 0,
                        area_id: val
                    }
                    buildingListRequest(data).then((res) => {
                        popupData.buildingList = res.data.items
                    });
                    }
                    
                }

            } else if (props.popupType == 14) {
                if (num == 1) {
                    popupData.areaSlect = ""
                }
            }
        }
        // 上传文件
        const onchange = (event) => {
            popupData.fileList = event.target.files
        }
        const sure = (val) => {
            if (props.popupType == 1) {
                if (popupData.loginAccount == "" || popupData.loginPassword == "") {
                    ElMessage({
                        message: '信息输入不完整',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else {
                    let data = {
                        user_name: popupData.loginAccount,
                        password: md5(popupData.loginPassword)
                    }
                    context.emit('sure', data, 1);
                }
            } else if (props.popupType == 2) {
                if (popupData.logout == "") return ElMessage({
                    message: '请输入超级密码',
                    type: 'error',
                    duration: 3 * 1000
                })
                let data = {
                    password: popupData.logout
                }
                context.emit('sure', data, props.popupType);
            } else if (props.popupType == 3) {
                if (popupData.shiftAccount == "" || popupData.shiftPassword == "") {
                    ElMessage({
                        message: '请填写完整信息',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else {
                    let data = {
                        user_name: popupData.shiftAccount,
                        password: popupData.shiftPassword
                    }
                    context.emit('sure', data, props.popupType);
                }
            } else if (props.popupType == 4) {
                offPopup()
                context.emit('sure', "", props.popupType);
            } else if (props.popupType == 5) {
                context.emit('sure', "", props.popupType);
            } else if (props.popupType == 6) {
                if (popupData.testRequest.controller_num == "") return ElMessage({
                    message: '请选择控制器',
                    type: 'error',
                    duration: 3 * 1000
                })
                if (popupData.testRequest.loop_num == "") return ElMessage({
                    message: '请选择回路',
                    type: 'error',
                    duration: 3 * 1000
                })
                if (popupData.testRequest.addr_num == "") return ElMessage({
                    message: '请选择地址号',
                    type: 'error',
                    duration: 3 * 1000
                })
                if (popupData.testRequest.alarm_type_id == "") return ElMessage({
                    message: '请选择模拟类型',
                    type: 'error',
                    duration: 3 * 1000
                })
                // popupData.testRequest.pass_num = parseInt(popupData.testRequest.pass_num)
                testRequest(popupData.testRequest).then((res) => {
                    if (res.ok) {
                        popupData.testShow = false
                        alarmsNumListRequest(popupData.Request).then((res) => {
                            store.commit('alarmsNumData', res.data)
                        });
                        if (popupData.routerData != "/") {
                            ElMessage({
                                message: '提交模拟报警成功,请返回首页查看',
                                type: 'success',
                                duration: 10 * 1000
                            })
                        }
                    }
                });
            } else if (props.popupType == 7) {
                if (popupData.addObjectData.name == "" || popupData.addObjectData.address == "") return ElMessage({
                    message: '请填写完整信息',
                    type: 'warning',
                })
                context.emit('sure', popupData.addObjectData, props.popupType);
            } else if (props.popupType == 9) {
                context.emit('sure', popupData.popupFData.id, props.popupType);
            } else if (props.popupType == 8) {
                let data = {
                    name: popupData.revampName,
                    mobile: popupData.revampMobile,
                    address: popupData.revampAddress,
                    project_id: popupData.popupFData.id,
                    is_active:popupData.objectTypeSelect
                }
                if (popupData.objectTypeSelect=="是") {
                    data.is_active = 1
                }
                context.emit('sure', data, props.popupType, popupData.selectData);
            } else if (props.popupType == 10 || props.popupType == 14) {
                if (popupData.numOne > popupData.numTwo) {
                    ElMessage({
                        message: '起始楼宇不能高于结束楼宇',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else if (popupData.areaSlect == "") {
                    ElMessage({
                        message: '请选择小区',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else if (popupData.switchValue == true && popupData.numOne == 0 && popupData.numTwo == 0) {
                    ElMessage({
                        message: '请选择楼宇编号',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else if (popupData.switchValue == false && popupData.newBuilding == "") {
                    ElMessage({
                        message: '请选择楼宇名称',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else if (popupData.switchValue == true && popupData.numOne == 0) {
                    ElMessage({
                        message: '起始楼宇不能为0',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else if (popupData.switchValue == true && (popupData.numOne < 0 || popupData.numTwo <= 0)) {
                    ElMessage({
                        message: '楼宇编号不能为负',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else {
                    if (popupData.switchValue == true) {
                        popupData.newBuilding = ""
                    } else if (popupData.switchValue == false) {
                        popupData.numOne = "",
                            popupData.numTwo = ""
                    }
                    let Data = {
                        areaID: popupData.areaSlect,
                        data: popupData.popupFData,
                        name: popupData.newBuilding,
                        file: popupData.fileList,
                        start: popupData.numOne,
                        end: popupData.numTwo
                    }
                    if (popupData.fileList == "") {
                        Data.file = ""
                    }
                    context.emit('sure', Data, props.popupType);
                    popupData.areaSlect = "",//清空小区名称
                        popupData.newBuilding = ""//清空楼宇名称
                    popupData.numOne = 0
                    popupData.numTwo = 0
                    popupData.fileList = ""
                    popupData.areaList = []
                }
            } else if (props.popupType == 11) {
                if (popupData.switchValue == true && popupData.floorStart > popupData.floorEnd) {
                    ElMessage({
                        message: '起始楼层不能高于结束楼层',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else if (popupData.switchValue == true && popupData.floorStart == 0 && popupData.floorEnd == 0) {
                    ElMessage({
                        message: '请选择楼层编号或输入楼层名称',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else if (popupData.switchValue == false && popupData.newFloors == "") {
                    ElMessage({
                        message: '请输入楼层名称',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else if (popupData.switchValue == true && popupData.floorStart == 0) {
                    ElMessage({
                        message: '起始楼层不能为0',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else if (popupData.fileList == "") {
                    ElMessage({
                        message: '请选择文件',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else {
                    if (popupData.switchValue == true) {
                        popupData.newFloors = ""
                    } else {
                        popupData.floorStart = ""
                        popupData.floorEnd = ""
                    }
                    let data = {
                        name: popupData.newFloors,
                        start: popupData.floorStart,
                        end: popupData.floorEnd,
                        file: popupData.fileList,
                        picture_type_id: 2,
                        area_id: popupData.popupFData.area_id,
                        build_id: popupData.popupFData.id
                    }

                    context.emit('sure', data, props.popupType);
                    popupData.areaSlect = ""//清空小区小区选择
                    popupData.buildingSlect = ""//清空楼宇选择
                    popupData.floorEnd = 0//清空楼宇选择
                    popupData.floorStart = 0//清空楼宇选择
                }
            } else if (props.popupType == 12) {
                context.emit('sure', popupData.popupFData.id, props.popupType);
            } else if (props.popupType == 13) {
                let data = {
                    build_id: popupData.popupFData.id,
                    name: popupData.revampBuildName,
                    file: popupData.fileList,
                    picture_type_id: 1
                }
                context.emit('sure', data, props.popupType);
                popupData.remopAreaName = popupData.popupFData.area_name
                popupData.revampBuildName = ""
            } else if (props.popupType == 15) {
                if (popupData.areaSlect == "") {
                    ElMessage({
                        message: '请选择小区',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else if (popupData.buildingSlect == "") {
                    ElMessage({
                        message: '请选择楼宇',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else if (popupData.fileList == "") {
                    ElMessage({
                        message: '请选择文件',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else if (popupData.switchValue == true && popupData.floorStart == 0 && popupData.floorEnd == 0) {
                    ElMessage({
                        message: '请选择楼层编号',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else if (popupData.switchValue == true && popupData.floorStart == 0) {
                    ElMessage({
                        message: '起始楼层不能为0',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else if (popupData.switchValue == false && popupData.newFloors == "") {
                    ElMessage({
                        message: '请输入楼层名称',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else if (popupData.switchValue == true && popupData.floorStart > popupData.floorEnd) {
                    ElMessage({
                        message: '起始楼层不能高于结束楼层',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else {
                    if (popupData.switchValue == true) {
                        popupData.newFloors = ""
                    } else {
                        popupData.floorStart = ""
                        popupData.floorEnd = ""
                    }
                    let data = {
                        name: popupData.newFloors,
                        start: popupData.floorStart,
                        end: popupData.floorEnd,
                        file: popupData.fileList,
                        picture_type_id: 2,
                        area_id: popupData.areaSlect,
                        build_id: popupData.buildingSlect
                    }
                    context.emit('sure', data, props.popupType);
                    popupData.areaSlect = ""//清空小区小区选择
                    popupData.buildingSlect = ""//清空楼宇选择
                    popupData.floorEnd = 0//清空楼宇选择
                    popupData.floorStart = 0//清空楼宇选择
                }

            } else if (props.popupType == 16) {
                let data = {
                    floor_id: popupData.popupFData.id,
                    name: popupData.floorsName,
                    file: popupData.fileList,
                    picture_type_id: 2,
                }
                context.emit('sure', data, props.popupType);
                popupData.floorsName = popupData.popupFData.name//清空楼层选择

            } else if (props.popupType == 17) {
                context.emit('sure', popupData.popupFData.id, props.popupType);
            } else if (props.popupType == 18) {
                if (popupData.controllerName == "" || popupData.controllersetupdate == "" || popupData.controllerType == "" || popupData.controllerManufacturer == "" || popupData.controllerCode == "") return ElMessage({
                    message: '请填写完整信息',
                    type: 'error',
                    duration: 3 * 1000
                })
                let data = {
                    name: popupData.controllerName,
                    code: popupData.controllerCode,
                    controller_id: popupData.popupFData.id,
                    setup_date: popupData.controllersetupdate,
                    model: popupData.controllerType,
                    manufacturer: popupData.controllerManufacturer,
                    controller_type: popupData.controllerTypeSelect
                }
                if (popupData.controllerCode == popupData.popupFData.code) {
                    data.code = ""
                }
                if (popupData.controllerTypeSelect == "主机") {
                    data.controller_type = 1
                } else if (popupData.controllerTypeSelect == "从机") {
                    data.controller_type = 2
                }
                context.emit('sure', data, props.popupType);
            } else if (props.popupType == 19) {
                let data = {
                    device_type_id: popupData.selectData,
                    psn: popupData.devicePsn,
                    device_id: popupData.popupFData.id,
                    description: popupData.deviceDescription
                }
                if (popupData.devicePsn == popupData.popupFData.psn) {
                    data.psn = ""
                }
                context.emit('sure', data, props.popupType);
            } else if (props.popupType == 20) {
                if (popupData.selectData == "" || popupData.addUsser == "" || popupData.addPassword == "" || popupData.addPasswordAgain == "") {
                    ElMessage({
                        message: '请填写完整信息',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else if (popupData.addPassword != popupData.addPasswordAgain) {
                    ElMessage({
                        message: '两次密码输入不一致',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else {
                    let data = {
                        user_name: popupData.addUsser,
                        password: md5(popupData.addPassword),
                        role_id: popupData.selectData
                    }
                    context.emit('sure', data, props.popupType);
                }
            } else if (props.popupType == 21) {
                let user_id = popupData.popupFData.id
                context.emit('sure', user_id, props.popupType);
            } else if (props.popupType == 22) {
                if (popupData.selectData == "" && popupData.popupFData.role_id) {
                    popupData.selectData = popupData.popupFData.role_id
                }
                if (popupData.addPassword == "" || popupData.addPasswordAgain == "") {
                    ElMessage({
                        message: '请填写完整信息',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else if (popupData.addPassword != popupData.addPasswordAgain) {
                    ElMessage({
                        message: '两次密码输入不一致',
                        type: 'error',
                        duration: 3 * 1000
                    })
                } else {
                    let data = {
                        // user_name: popupData.addUsser || popupData.popupFData.user_name,
                        password: md5(popupData.addPassword),
                        role_id: popupData.selectData,
                        user_id: popupData.popupFData.id
                    }
                    context.emit('sure', data, props.popupType);
                }
            } else if (props.popupType == 23) {
                if (popupData.projectSelect == "" || popupData.fileList == "") return ElMessage({
                    message: '请填写完整信息',
                    type: 'error',
                    duration: 3 * 1000
                })
                let data = {
                    project_id: popupData.selectData,
                    file: popupData.fileList,
                }
                context.emit('sure', data, props.popupType, val);
            } else if (props.popupType == 24) {
                if (popupData.selectData == "" || popupData.fileList == "") return ElMessage({
                    message: '请填写完整信息',
                    type: 'error',
                    duration: 3 * 1000
                })
                let num = 0
                popupData.controllersList.forEach((item) => {
                    if (item.id == popupData.selectData) {
                        num = item.code
                    }
                })
                let data = {
                    controller_id: popupData.selectData,
                    controller_num: num,
                    file: popupData.fileList,
                }
                context.emit('sure', data, props.popupType);
                popupData.loading = true
            } else if (props.popupType == 25) {
                context.emit('sure', popupData.popupFData.id, props.popupType);
            }
        }
        const sureLogin = () => {
            let data = {
                user_name: "superadmin",
                password: md5("qqqqq")
            }
            context.emit('sure', data, 1);
        }
        // 模拟测试
        const testSelectFun = (val, type) => {
            if (type == 1) {

                popupData.testRequest.controller_num = val

                // 选择控制器时 清空回路号和地址号选择器
                popupData.loopSlect = ""
                popupData.testRequest.loop_num = ""
                popupData.loopList = []
                popupData.partNumSlect = ""
                popupData.partNumList = []
                popupData.testRequest.addr_num = ""
                if (val != "") {
                    let loopRequest = {
                        page: 0,
                        controller_num: val
                    }
                    inquireLoopRequest(loopRequest).then((res) => {
                        popupData.loopList = res.data.loops
                    });
                }
            } else if (type == 2) {
                if (val != "") {
                    popupData.testRequest.loop_num = val//回路号
                    popupData.partNumSlect = ""
                    popupData.testRequest.addr_num = ""
                    popupData.partNumList = []
                    let deviceRequest = {
                        controller_num: popupData.controllersSlect,
                        loop_num: val,
                        page: 0,
                    }
                    deviceListRequest(deviceRequest).then((res) => {
                        popupData.partNumList = res.data.items
                    });
                } else {
                    popupData.partNumList = []
                    popupData.partNumSlect = ""
                }
            } else if (type == 3) {
                popupData.testRequest.addr_num = val
            } else if (type == 4) {
                popupData.testRequest.alarm_type_id = val
            } else if (type == 5) {
                popupData.controllersSlect = ""
                popupData.controllersList = []
                popupData.loopSlect = ""
                popupData.testRequest.loop_num = ""
                popupData.loopList = []
                popupData.partNumSlect = ""
                popupData.partNumList = []
                popupData.testRequest.addr_num = ""
            }
        }
        const nameBlur = () => {
            let name = document.getElementById('refname').value
            popupData.loginAccount = name
        }
        const passBlur = () => {
            let name = document.getElementById('refpass').value
            popupData.loginPassword = name
        }
        // 换班
        const newnameBlur = () => {
            let name = document.getElementById('newname').value
            popupData.shiftAccount = name
        }
        const newpasswordBlur = () => {
            let name = document.getElementById('newpassword').value
            popupData.shiftPassword = name
        }
        // 退出登录
        const outloginBlur = () => {
            let name = document.getElementById('outlogin').value
            popupData.logout = name
        }

        watch(() => popupData.areaSlect, (newvalue, oldvalue) => {
            if (newvalue != oldvalue) {
                popupData.buildingSlect = ""
            }
        })

        // 监听父组件传递的props的值 用来判断显示哪一个弹窗
        watch(props, (newProps) => {
            popupData.userList = store.state.userList
            popupData.userTypeList = store.state.userType
            popupData.areaList = store.state.areaList
            popupData.projectList = store.state.projectList
            popupData.deviceTypeList = store.state.deviceTypeList
            popupData.popupFData = props.popupData
            if (newProps.popupType == 1 || newProps.popupType == 3) {
                popupData.loginShow = true
            } else if (newProps.popupType == 6) {
                popupData.testShow = true
                let Request = {
                    page: 0,
                }
                // 模拟测试判断是否展示多项目选择器
                projectListRequest(Request).then((res) => {
                    popupData.projectList = res.data.items
                    if (popupData.projectList.length == 0) {
                        ElMessage({
                            message: '请先创建项目',
                            type: 'info',
                            duration: 3 * 1000
                        })
                    } else if (popupData.projectList.length == 1) {
                        popupData.testObjectState = false
                    } else {
                        popupData.testObjectState = true
                    }
                });
            } else if (newProps.popupType == 7 || newProps.popupType == 20 || newProps.popupType == 23 || newProps.popupType == 24) {
                popupData.newObjectShow = true
            } else if (newProps.popupType == 8 || newProps.popupType == 13 || newProps.popupType == 16 || newProps.popupType == 22) {
                popupData.redactObjectShow = true
                if (newProps.popupType == 8) {
                    popupData.revampName = props.popupData.name
                    popupData.revampAddress = props.popupData.address
                    popupData.revampMobile = props.popupData.mobile
                    if (props.popupData.is_active==1) {
                        popupData.objectTypeSelect = "是"
                    }else{
                        popupData.objectTypeSelect = "否"
                    }
                } else if (newProps.popupType == 13) {
                    popupData.remopAreaName = popupData.popupFData.area_name
                    popupData.revampBuildName = popupData.popupFData.name
                } else if (newProps.popupType == 16) {
                    popupData.floorsName = popupData.popupFData.name
                }
            } else if (newProps.popupType == 2 || newProps.popupType == 4 || newProps.popupType == 5 || newProps.popupType == 9 || newProps.popupType == 12 || newProps.popupType == 17 || newProps.popupType == 21 || newProps.popupType == 25) {
                popupData.deleteObjectShow = true
            } else if (newProps.popupType == 10 || newProps.popupType == 11 || newProps.popupType == 14 || newProps.popupType == 15) {
                popupData.fastEstablishShow = true
                if (newProps.popupType == 10 || newProps.popupType == 14) {
                    popupData.areaList = []
                }
            } else if (newProps.popupType == 18 || newProps.popupType == 19) {
                popupData.controllerShow = true
                if (newProps.popupType == 18) {
                    popupData.controllerCode = props.popupData.code
                    popupData.controllerName = props.popupData.name
                    popupData.controllersetupdate = props.popupData.setup_date
                    if (props.popupData.controller_type == 1) {
                        popupData.controllerTypeSelect = "主机"
                    } else if (props.popupData.controller_type == 2) {
                        popupData.controllerTypeSelect = "从机"
                    } else {
                        popupData.controllerTypeSelect = ""
                    }
                    popupData.controllerManufacturer = props.popupData.manufacturer
                    popupData.controllerType = props.popupData.model

                }
                if (newProps.popupType == 19) {
                    popupData.deviceDescription = props.popupData.description
                    popupData.devicePsn = props.popupData.psn
                }
            }
            else if (newProps.popupType == 0) {
                popupData.loginShow = false
                popupData.testShow = false
                popupData.newObjectShow = false
                popupData.redactObjectShow = false
                popupData.deleteObjectShow = false
                popupData.fastEstablishShow = false
                popupData.controllerShow = false
            }
        }
        );
        watch(() => popupData.loginShow, (oldvalue, newvalue) => {
            if (newvalue == true) {
                context.emit('offPopup', false, 0);
                popupData.loginAccount = ""
                popupData.loginPassword = ""
                popupData.shiftAccount = ""
                popupData.shiftPassword = ""
            }
        })
        // 监听模拟测试弹窗的显示状态
        watch(() => popupData.testShow, (oldvalue, newvalue) => {
            if (newvalue == true) {
                context.emit('offPopup', false, 0);

                popupData.testOnjectSelsct = ""
                popupData.controllersList = []
                popupData.controllersSlect = ""
                popupData.loopSlect = ""
                popupData.partNumSlect = ""
                popupData.alarmsTypeSelsct = ""
                popupData.loopList = []
                popupData.partNumList = []
                popupData.testRequest.pass_num = ""
                popupData.testRequest.controller_num = ""
                popupData.testRequest.loop_num = ""
                popupData.testRequest.addr_num = ""
                popupData.testRequest.alarm_type_id = ""
                popupData.testRequest.note = ""
                popupData.testRequest.project_id = ""
            }
        })
        // 
        watch(() => popupData.newObjectShow, (oldvalue, newvalue) => {
            if (newvalue == true) {
                popupData.areaSlect = ""//清空小区名称
                popupData.buildingSlect = ""
                popupData.projectSelect = ""//清空项目选择器
                popupData.controllersSlect = "",//清空控制器选择器
                    popupData.selectData = ""
                popupData.addObjectData.name = "",//清空项目名称输入框
                    popupData.addObjectData.address = "",//清空项目地址输入框
                    popupData.addObjectData.mobile = "",//清空联系电话输入框
                    popupData.addUsser = ""
                popupData.addPassword = ""
                popupData.userTypeSelect = ""
                popupData.addPasswordAgain = ""
                context.emit('offPopup', false, 0);
                popupData.fileList = []
                popupData.loading = false
            }
        })
        // 监听修改项目 修改楼宇 修改楼层弹窗的显示状态
        watch(() => popupData.redactObjectShow, (oldvalue, newvalue) => {
            if (newvalue == true) {
                context.emit('offPopup', false, 0);
                if (props.popupType == 8) {
                    popupData.userSelect = ""
                    popupData.popupFData.revampName = ""
                    popupData.popupFData.revampAddress = ""
                    popupData.popupFData.revampMobile = ""
                    popupData.popupFData.revampMobile = ""
                    popupData.popupFData.is_active = ""
                    popupData.objectTypeSelect = ""
                }
                else if (props.popupType == 13) {
                    popupData.remopAreaName = popupData.popupFData.area_name
                    popupData.revampBuildName = ""
                }
                else if (props.popupType == 16) {
                    popupData.floorsName = popupData.popupFData.name
                }
            }
        })

        // 监听注销 消音/复位 打印 删除项目 删除楼宇 删除楼层 弹窗的显示状态
        watch(() => popupData.deleteObjectShow, (oldvalue, newvalue) => {
            if (newvalue == true) {
                context.emit('offPopup', false, 0);
            }
        })
        // 监听控制器编辑 设备编辑弹窗的显示状态
        watch(() => popupData.controllerShow, (newvalue, oldvalue) => {
            if (oldvalue == true) {
                context.emit('offPopup', false, 0)
                popupData.controllerTypeSelect = ""
                popupData.deviceTypeSlect = ""
            }
        })

        // 监听快捷创建项目弹窗的显示状态
        watch(() => popupData.fastEstablishShow, (oldvalue, newvalue) => {
            if (newvalue == true) {
                context.emit('offPopup', false, 0);
                popupData.areaSlect = "",//清空小区名称
                    popupData.buildingSlect = "",//清空楼宇选择
                    popupData.switchValue = false,//开关
                    popupData.fileList = [],//文件
                    popupData.areaList = []
                // 创建楼宇
                popupData.projectSelect = "",//清空项目选择器
                    popupData.newBuilding = "",//清空楼宇名称
                    popupData.numOne = 0,//清空楼宇编号
                    popupData.numTwo = 0,//清空楼宇编号
                    // 创建楼层
                    popupData.floorEnd = 0//清空楼层编号
                popupData.floorStart = 0//清空楼层编号
                popupData.newFloors = ""//清空楼层名称输入框

            }
        })
        watch(() => router.currentRoute.value.path, (newValue, oldValue) => {
            popupData.routerData = newValue
            if (newValue == "/") {

            }
        }, { immediate: true })

        return {
            popupData,
            offPopup,
            openEstablishEstate,
            offEstablishEstateShow,
            sureoffEstablishEstateShow,
            sure,
            sureLogin,
            selectFun,
            visible,
            visibleNewFloors,
            rempArea,
            onchange,
            visibleFast,
            testSelectFun,
            testvisibleControllerList,
            visibleControllerList,
            deleteArea,
            visibleUser,
            nameBlur,
            newnameBlur,
            newpasswordBlur,
            outloginBlur,
            passBlur,
            visibleObject,

        }
    }
}
</script>
<style scoped lang="scss">
.popupBox {
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
            font-size: 18px;
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

        .account {
            width: 500px;
            height: 44px;
        }

        .password {
            width: 500px;
            height: 44px;
            margin-top: 50px;
        }

        .changeBox {
            margin-top: 36px;
        }

        .testMsgBox {
            width: 560px;
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

        .areaBoxDetail {
            width: 500px;
            display: flex;

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
                top: 190px;
                right: 200px;
                cursor: pointer;
            }
        }

        .newUserBox {
            width: 500px;
            height: 44px;
            display: flex;
            margin-top: 50px;

            .text {
                width: 120px;
                height: 44px;
            }

            .input {
                width: 320px;
                height: 44px;

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
            }
        }

        .newUserBox:nth-child(1) {
            margin-top: 20px;
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

    // 控制器上传弹窗
    .controllerUploadingBox {
        width: 1000px;
        height: 430px;
        font-size: 22px;
        font-weight: 500;

        .objectSelectBox {
            width: 1000px;
            height: 430px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;

            .selectBox {
                width: 400px;
                height: 44px;

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
            }

            .fileBox {
                width: 400px;
                height: 44px;
                margin-top: 30px;
            }

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

        .inputSlect {

            :deep(.el-input) {
                width: 320px;
                height: 36px;
                background-color: #fff;
            }

            :deep(.el-input__wrapper) {
                width: 320px;
                height: 36px;
                color: #4A5CD5;
                background-color: #F7F8FC;
                border: none !important;
                box-shadow: none !important;
            }
        }
    }

    // 模拟测试弹窗
    .testBox {
        width: 1000px;
        height: 430px;
        display: flex;
        flex-wrap: wrap;

        .testMsgBox {
            width: 490px;
            height: 44px;
            display: flex;
            margin-top: 36px;

            .testTextBox {
                width: 120px;
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
                margin-left: 18px;
            }
        }

        .remarkBox {
            width: 1000px;
            height: 100px;
            display: flex;
            flex-direction: row;
            margin-left: 20px;

            .remarkText {
                width: 120px;
                height: 100px;
                font-size: 22px;
                font-weight: 500;
                color: #000000;
                letter-spacing: 1.1px;
                display: flex;
                justify-content: right;
            }

            .remarkInput {
                width: 750px;
                height: 120px;
                margin-left: 18px;

                .explaininput {
                    border: none;
                    width: 750px;
                    height: 100px;
                    border-radius: 3px;
                    font-size: 14px;
                    color: rgb(0, 0, 0);
                    resize: none;
                    padding-left: 15px;
                    padding-top: 10px;
                    background-color: #F7F8FC;
                }
            }
        }
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

    .fastEstablish {
        :deep(.el-dialog) {
            display: flex;
            flex-direction: column;
            margin: 0 !important;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            height: 600px;
            width: 1200px;
            border-radius: 8px;

            .headerBox {
                width: 1200px;
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
                font-size: 18px;
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

        // 选择器
        :deep(.el-select) {
            width: 320px;
            height: 44px;
            color: #4A5CD5;
        }

        :deep(.el-input) {
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



        .fastEstablishMsg {
            width: 1200px;
            height: 430px;
            font-size: 22px;
            font-weight: 500;
            color: #000000;
            letter-spacing: 1.1px;
            display: flex;
            flex-direction: column;


            .fastBox {
                display: flex;
                align-items: center;
                margin-top: 50px;
                margin-left: 137px;

                :deep(.el-switch) {
                    padding-bottom: 7px;
                    height: 44px;
                }

                :deep(.el-switch__label *) {
                    font-size: 23px;
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
                    margin-left: 16px;
                    cursor: pointer;
                }

                .inputSlect {
                    margin-left: 10px;

                    :deep(.el-input) {
                        width: 320px;
                        height: 36px;
                        background-color: #fff;
                    }

                    :deep(.el-input__wrapper) {
                        width: 320px;
                        height: 36px;
                        color: #4A5CD5;
                        background-color: #F7F8FC;
                        border: none !important;
                        box-shadow: none !important;
                    }
                }

                .numberSlect {
                    margin-left: 10px;

                    :deep(.el-input-number) {
                        width: 120px;
                        height: 36px;
                        // font-size: 20px;

                        .el-input-number__decrease,
                        .el-input-number__increase {
                            width: 36px;
                            height: 36px;
                            background: #4a5cd5;
                            border-radius: 1px;
                            color: #fff;

                        }

                        .el-input__wrapper {
                            height: 36px;
                            background-color: #fff;
                        }
                    }

                    :deep(.el-input) {
                        width: 120px;
                        height: 36px;
                        // font-size: 20px;
                        background-color: #fff;
                    }

                }

            }
        }

        .sureBox {
            width: 1200px;
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
    }

    // 控制器编辑弹窗
    .controllerBox {
        :deep(.el-dialog) {
            display: flex;
            flex-direction: column;
            margin: 0 !important;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            height: 600px;
            width: 1500px;
            border-radius: 8px;

            .headerBox {
                width: 1500px;
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
                font-size: 18px;
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

        // 选择器
        :deep(.el-select) {
            width: 320px;
            height: 44px;
            color: #4A5CD5;
        }

        :deep(.el-input) {
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

        .sureBox {
            width: 1500px;
            height: 80px;
            display: flex;
            flex-direction: row-reverse;
            align-items: center;
            border-top: 1px solid #eaeaf1;

            .sureBtn {
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

            .sureLoginBtn {
                width: 170px;
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

        .controllerMsg {
            width: 1500px;
            height: 430px;
            font-size: 22px;
            font-weight: 500;
            color: #000000;
            letter-spacing: 1.1px;
            display: flex;
            flex-direction: column;

            .controllerBox {
                display: flex;
                align-items: center;
                margin-top: 36px;
                margin-left: 91px;
            }

            .controllerBox:first-child {
                margin-top: 81px;
            }

            .remarkBox {
                width: 1400px;
                height: 100px;
                display: flex;
                flex-direction: row;
                margin-top: 36px;
                margin-left: 30px;

                .remarkText {
                    width: 150px;
                    height: 100px;
                    font-size: 22px;
                    font-weight: 500;
                    color: #000000;
                    letter-spacing: 1.1px;
                    display: flex;
                    justify-content: right;
                }

                .remarkInput {
                    width: 1267px;
                    height: 120px;


                    .explaininput {
                        border: none;
                        width: 1267px;
                        height: 100px;
                        border-radius: 3px;
                        font-size: 14px;
                        color: rgb(0, 0, 0);
                        resize: none;
                        padding-left: 15px;
                        padding-top: 10px;
                        background-color: #F7F8FC;
                    }
                }
            }
        }


        .deviceMsg {
            width: 1500px;
            height: 430px;
            font-size: 22px;
            font-weight: 500;
            color: #000000;
            letter-spacing: 1.1px;
            display: flex;
            flex-direction: column;

            .deviceBox {
                display: flex;
                align-items: center;
                margin-top: 36px;
                margin-left: 102px;

                .deviceInput {
                    width: 320px;
                    height: 44px;
                    border-radius: 4px;
                    border: none;
                    padding-left: 10px;
                    outline: none;
                }
            }

            .deviceBox:first-child {
                margin-top: 41px;
            }

            .deviceBox:nth-child(3) {
                margin-left: 79px;
            }

            .deviceRemark {
                margin-top: 36px;
                margin-left: 79px;
                display: flex;

                .deviceImg {
                    width: 100px;
                    height: 100px;
                    margin-right: 320px;

                    .deviceimg {
                        width: 100px;
                        height: 100px;
                    }
                }

                .remarkInput {
                    width: 750px;
                    height: 100px;


                    .explaininput {
                        border: none;
                        width: 750px;
                        height: 100px;
                        border-radius: 3px;
                        font-size: 14px;
                        color: rgb(0, 0, 0);
                        resize: none;
                        padding-left: 15px;
                        padding-top: 10px;
                        background-color: #F7F8FC;
                    }
                }
            }
        }
    }

}

.avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.avatar-uploader .el-upload:hover {
    border-color: #409EFF;
}

.avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
}

.avatar {
    width: 178px;
    height: 178px;
    display: block;
}
</style>