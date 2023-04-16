<template>
    <div style='padding: 30px'>
        <el-row justify='center' type='flex'>
            <el-form :inline='true' :model='commentForm'>
                <el-form-item label='标题'>
                    <el-input
                        v-model='commentForm._title__icontains'
                        clearable
                        @change='search'
                    />
                </el-form-item>
                <el-form-item label='内容'>
                    <el-input
                        v-model='commentForm._text__icontains'
                        clearable
                        @change='search'
                    />
                </el-form-item>
                <el-form-item label='标签'>
                    <el-input
                        v-model='commentForm._keywords__icontains'
                        clearable
                        @change='search'
                    />
                </el-form-item>
                <el-form-item label='来源媒体'>
                    <el-input
                        v-model='commentForm._media_name__icontains'
                        clearable
                        @change='search'
                    />
                </el-form-item>
                <el-form-item>
                    <el-button type='primary' @click='search'>搜索</el-button>
                </el-form-item>
            </el-form>
        </el-row>
        <el-table :data='commentList' style='width: 100%; margin: 20px 10px'>
            <el-table-column align='center' label='封面' prop='img' width='180'>
                <template #default='{ row }'>
                    <el-link
                        :underline='false'
                        type='primary'
                        @click='viewNewsDetail(row.id)'
                    >
                        <el-image
                            :src='jsonify(row.img).u'
                            style='width: 180px; height: 150px'
                        >
                            <template #error>
                                <div class='image-slot'>暂无封面图</div>
                            </template>
                        </el-image>
                    </el-link>
                </template>
            </el-table-column>
            <el-table-column align='center' label='标题' prop='title' sortable>
                <template #default='{ row }'>
                    <el-link
                        :underline='false'
                        type='primary'
                        @click='viewNewsDetail(row.id)'
                    >
                        {{ row.title }}
                    </el-link>
                </template>
            </el-table-column>
            <el-table-column label='简介' prop='intro' sortable>
                <template #default='{ row }'>
                    <el-link :underline='false' type='info' @click='showDl(row.intro)'>
                        {{ ellipsis(row.intro) }}
                    </el-link>
                </template>
            </el-table-column>
            <el-table-column label='标签' prop='keywords' sortable width='180'>
                <template #default='{ row }'>
                    <template v-if='row.keywords'>
                        <el-tag
                            v-for='t in row.keywords.split(",")'
                            :key='t'
                            effect='plain'
                            size='mini'
                            style='margin: 0 5px 5px 0; cursor: pointer'
                            type='info'
                            @click='
                                commentForm._keywords__icontains = t;
                                search();
                            '
                        >{{ t }}
                        </el-tag>
                    </template>
                </template>
            </el-table-column>
            <el-table-column
                label='来源媒体'
                prop='media_name'
                sortable
                width='150'
            />
            <el-table-column label='发布日期' prop='intime' sortable width='150' />
            <el-table-column label='点击率' prop='view_count' sortable width='150' />
            <el-table-column align='center' label='操作' sortable width='180'>
                <template #default='scope'>
                    <el-button
                        size='mini'
                        type='primary'
                        @click='viewCommentDetail(scope.row.text, scope.row.subject)'
                    >内容分析
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-row justify='center' style='margin-top: 30px' type='flex'>
            <!--            <el-pagination-->
            <!--                :current-page='commentForm.page'-->
            <!--                :page-size='commentForm.pagesize'-->
            <!--                layout='prev, pager, next, jumper, total'-->
            <!--                :total='commentForm.total'-->
            <!--                background-->
            <!--                @current-change='handleCurrentChange'-->
            <!--            />-->
            <el-pagination
                :current-page='commentForm.page'
                :page-size='commentForm.pagesize'
                :page-sizes='pagesize'
                :total='commentForm.total'
                layout='sizes, prev, pager, next, jumper, total'
                @size-change='handleSizeChange'
                @current-change='handleCurrentChange'
            />
        </el-row>
        <el-dialog
            v-model='centerDialogVisible'
            center
            destroy-on-close
            title='简介'
            width='70%'
        >
            <el-card
                shadow='always'
                style='margin-bottom: 20px; background-color: #f6f6f6'
            >
                <div v-html='highlight()' />
            </el-card>
        </el-dialog>
    </div>
</template>

<script>
import request from '/@/utils/request'

export default {
    data() {
        return {
            text: '',
            pagesize: [10, 20, 50, 100],
            commentList: [],
            commentForm: {
                _txts__icontains: null,
                _positive: null,
                total: 0,
                page: 1,
                pagesize: 20
            },
            centerDialogVisible: false
        }
    },
    beforeMount() {
        this.search()
    },
    methods: {
        jsonify(text) {
            return JSON.parse(text)
        },
        highlight() {
            if (this.commentForm._txts__icontains) {
                const txt = this.commentForm._txts__icontains
                const reg = new RegExp(this.commentForm._txts__icontains, 'ig')
                return this.text.replace(
                    reg,
                    `<span style='color:red;font-weight:bold;'>${txt}</span>`
                )
            }
            return this.text
        },
        ellipsis(text, max = 50) {
            return text.length > max ? `${text.substring(0, max)}...` : text
        },
        showDl(text) {
            this.text = text
            this.centerDialogVisible = true
        },
        viewNewsDetail(id) {
            this.$router.push({ name: 'Detail', params: { id } })
        },
        viewCommentDetail(text, subject) {
            localStorage.setItem('text', text.trim())
            this.$router.push({ name: 'AnalyseList', params: { subject } })
        },
        handleCurrentChange(page) {
            this.commentForm.page = page
            this.getlist()
        },
        handleSizeChange(val) {
            this.commentForm.pagesize = val
            this.getlist()
        },
        search() {
            this.commentForm.page = 1
            this.getlist()
        },
        getlist() {
            request.post('/news/', this.commentForm)
                .then((res) => {
                    this.commentList = res.data.result
                    this.commentForm.total = res.data.total
                })
        }
    }
}
</script>


<style lang='postcss' scoped>
.image-slot {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    background: var(--el-fill-color-light);
    color: var(--el-text-color-secondary);
    font-size: 30px;
}
</style>
