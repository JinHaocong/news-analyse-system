const template22 = `<div style="padding:20px;">
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
<el-form-item>
    <el-button type="primary" @click="queryForm.page=1;doSearch()">预测</el-button>
</el-form-item>
</el-form>
<h1>预测结果</h1>
<div v-if="data">
    <span>最低薪资：<strong>{{data.min.toFixed(1)}} 千/月</strong></span><br/><br/>
    <span>最高薪资：<strong>{{data.max.toFixed(1)}} 千/月</strong></span><br/><br/>
    <span>平均薪资：<strong>{{data.avg.toFixed(1)}} 千/月</strong></span><br/><br/>
</div>
</div>
`
var PredictView = {
    template: template22,
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
            data: null,
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
        this.doSearch()
    },
    methods: {
        handleClick() {
            this.doSearch()
        },
        doSearch() {
            axios.post('/ajax/predict/', this.queryForm).then(res => {
                this.data = res.data
            })
        },
        handleCurrentChange(page) {
            this.queryForm.page = page
            this.doSearch()
        }
    },
}