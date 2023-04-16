const template11 = `<div style="padding:20px;">
<h1>推荐岗位</h1>
<el-card v-if="records.length===0">
    <span style="color:red;font-size:20px;">
    暂无适合您个人信息的岗位推荐，请完善或修改您的个人信息
    </span>
</el-card>
<el-card shadow="hover" style="margin-top:10px;cursor: pointer;" v-for="job in records"
:key="job.jobid" @click.native="viewDetail(job.jobid)">
<el-row type="flex" justify="space-between" style="margin-bottom: 10px;">
    <el-col :span="8">
        <el-link type="primary" :underline="false" style="font-size: 17px;">{{job.job_name}}
        </el-link>
    </el-col>
    <el-col :span="8">
        <el-link type="primary" :underline="false" style="font-size: 17px;">{{job.company_name}}
        </el-link>
    </el-col>
</el-row>
<el-row type="flex" justify="space-between" style="margin-bottom: 10px;">
    <el-col :span="10">
        <span
            style="font-size:16px;color:darksalmon;margin-right:10px;">{{job.providesalary_text || '面议'}}</span>
        <span style="color:#61687c">{{job.attribute}}</span>
    </el-col>
    <el-col :span="8">
        <span style="color:#61687c;margin-right:5px;">{{job.companytype_text}}</span>
        <span style="color:#61687c">{{job.companysize_text}}</span>
    </el-col>
</el-row>
<el-row type="flex" justify="space-between" style="margin-bottom: 5px;">
    <el-col :span="10">
        <el-tag v-for="welf in job.jobwelf.split(' ')" :key="welf" style="margin:0 5px 5px 0;"
            size="mini" type="info" plain v-show="welf">
            {{welf}}</el-tag>
    </el-col>
    <el-col :span="8">
        <span style="color:#61687c">{{job.companyind_text}}</span>
    </el-col>
</el-row>
</el-card>
<el-row type="flex" justify="center" style="margin-top:20px">
<el-pagination @current-change="handleCurrentChange" :current-page="queryForm.page"
    :page-size="queryForm.pagesize" layout="prev, pager, next, jumper, total"
    :total="queryForm.total" background>
</el-pagination>
</el-row>
</div>
`
var RecommandView = {
    template: template11,
    data() {
        return {
            queryForm: {
                total: 0,
                page: 1,
                pagesize: 12
            },
            records: [],
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
        }
    },
    beforeMount() {
        this.doSearch()
    },
    methods: {
        viewDetail(jobid) {
            window.open(`/detail/${jobid}`)
        },
        handleClick() {
            this.doSearch()
        },
        doSearch() {
            axios.post('/ajax/recommand/', this.queryForm).then(res => {
                this.records = res.data.content.results
                this.queryForm.total = res.data.content.total
            })
        },
        handleCurrentChange(page) {
            this.queryForm.page = page
            this.doSearch()
        }
    },
}