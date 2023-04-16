const ProfileView = (() => {
    const template = `
        <div style="padding:20px;">
            <h1>个人信息</h1>
            <el-form :inline="true">
                <el-form-item label="姓名">
                    <el-input  style="width:300px;" v-model="profile.name" clearable></el-input>
                </el-form-item>
                <el-form-item label="学历">
                    <el-select clearable style="width:300px;" v-model="profile.degree">
                        <el-option v-for="value in degree" :key="value" :value="value" :label="value"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="工作经验">
                    <el-select style="width: 300px;" clearable v-model="profile.workyear">
                        <el-option v-for="value in workyear" :key="value" :value="value" :label="value"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="意向城市">
                    <el-input  style="width:300px;" v-model="profile.workarea" clearable></el-input>
                </el-form-item>
                <el-form-item label="意向岗位">
                    <el-input  style="width:300px;" v-model="profile.job_name" clearable></el-input>
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
                    name: null,
                    degree: null,
                    workyear: null,
                    workarea: null,
                    job_name: null,
                },
                degree: {
                    "1": "初中及以下",
                    "2": "高中",
                    "3": "中技",
                    "4": "中专",
                    "5": "大专",
                    "6": "本科",
                    "7": "硕士",
                    "8": "博士",
                    "": "无学历要求"
                },
                workyear: {
                    "1": "在校生/应届生",
                    "3": "1年经验",
                    "4": "2年经验",
                    "5": "3-4年经验",
                    "6": "5-7年经验",
                    "7": "8-9年经验",
                    "8": "10年以上经验",
                    "10": "无需经验",
                },
            }
        },
        beforeMount() {
            this.getProfile()
        },
        methods: {
            getProfile() {
                axios.get('/user/get_profile/').then(res => {
                    Object.assign(this.profile, res.data)
                })
            },
            doSave() {
                axios.post('/user/save_profile/', this.profile).then(res => {
                    this.$message.success("修改成功")
                })
            }
        }
    }
})()