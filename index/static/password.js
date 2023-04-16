const PasswordView = (() => {
    const template = `
        <div style="padding:20px;">
            <h1>修改密码</h1>
            <el-form>
                <el-form-item label="原密码">
                    <el-input style="width:300px;" v-model="profile.password" clearable show-password></el-input>
                </el-form-item>
                <el-form-item label="新密码">
                    <el-input style="width:300px;" v-model="profile.npassword" clearable show-password></el-input>
                </el-form-item>
                <el-form-item label="确认密码">
                    <el-input style="width:300px;" v-model="profile.npassword2" clearable show-password></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="doSave">修改</el-button>
                </el-form-item>
            </el-form>
        </div>
    `
    return {
        template,
        data() {
            return {
                profile: {
                    password: null,
                    npassword: null,
                    npassword2: null,
                },
            }
        },
        methods: {
            doSave() {
                axios.post('/user/change_password/', this.profile).then(res => {
                    let {
                        code,
                        message
                    } = res.data
                    if (code != 0) {
                        this.$message.error(message)
                    } else {
                        this.$message.success("修改成功，请重新登录")
                        window.location.replace("/")
                    }
                })
            }
        }
    }
})()