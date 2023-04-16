const template4 = `<div style="padding:20px;">
<el-form v-model="queryForm" :inline="true" size="mini">
<el-form-item label="职位名称">
    <el-input v-model="queryForm.job_name__icontains" style="max-width: 300px;" clearable
        @change="queryForm.page=1;doSearch()">
    </el-input>
</el-form-item>
<el-form-item label="工作地区">
    <el-input v-model="queryForm.workarea_text__icontains" style="max-width: 300px;" clearable
        @change="queryForm.page=1;doSearch()">
    </el-input>
</el-form-item>
<el-form-item label="工作经验">
    <el-select v-model="queryForm.workyear_text" style="max-width: 300px;" clearable
        @change="queryForm.page=1;doSearch()">
        <el-option v-for="value in workyear" :key="value" :value="value" :label="value"></el-option>
    </el-select>
</el-form-item>
<el-form-item label="学历要求">
    <el-select v-model="queryForm.degreefrom_text" style="max-width: 300px;" clearable
        @change="queryForm.page=1;doSearch()">
        <el-option v-for="value in degree" :key="value" :value="value" :label="value"></el-option>
    </el-select>
</el-form-item>
<el-form-item label="薪资范围">
    <el-select v-model="queryForm.providesalary" style="max-width: 300px;" clearable
        @change="queryForm.page=1;doSearch()">
        <el-option v-for="value in salary" :key="value" :value="value" :label="value"></el-option>
    </el-select>
</el-form-item>
<el-form-item>
    <el-button type="primary" @click="queryForm.page=1;doSearch()">搜索</el-button>
</el-form-item>
</el-form>
<vue-echarts :options="degree_chart"></vue-echarts>
</div>
`
var DegreeView = {
    template: template4,
    data() {
        return {
            queryForm: {
                job_name__icontains: null,
                company_name__icontains: null,
                workarea_text__icontains: null,
                workyear_text: null,
                degreefrom_text: null,
                providesalary: null,
                total: 0,
                page: 1,
                pagesize: 12
            },
            salary: ["面议", "3K以下", "3-5K", "5-10K", "10-15K", "15-20K", "20-30K", "30-50K", "50K以上"],
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
            workyear_chart: {},
            workarea_chart: {},
            providesalary_chart: {},
            degree_chart: {},
        }
    },
    beforeMount() {
        this.doSearch()
    },
    methods: {
        handleClick() {
            this.doSearch()
        },
        handleCommand(cmd) {
            if (cmd === 'gotoAdmin') {
                window.location.href = "/admin"
            } else if (cmd === 'logout') {
                window.location.href = "/user/logout"
            }
        },
        doSearch() {
            axios.post('/ajax/chart/degree/', this.queryForm).then(res => {
                this.degree_chart = res.data
            })
        },
        handleCurrentChange(page) {
            this.queryForm.page = page
            this.doSearch()
        }
    },
    components: {
        'vue-echarts': {
            props: ['options'],
            watch: {
                options(newOption, oldOption) {
                    if (newOption !== null) {
                        let chart = echarts.init(this.$el, 'white', {
                            renderer: 'canvas'
                        })
                        chart.setOption(newOption)
                    }
                }
            },
            template: `<div class="chart-container" style="width:900px; height:500px;margin-bottom:50px;"></div>`,
        }
    }
}