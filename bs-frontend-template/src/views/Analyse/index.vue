<template>
  <div class="analyse">
    <div class="wrap">
      <div class="top">
        {{ text }}
        <!-- <el-input type="textarea" :rows="8" placeholder="在这输入文本..." v-model="text" /> -->
        <!-- <el-button style="float:right;margin-top:20px;" @click="analyse" type="primary" :disabled="text.length === 0">
          提交文本
        </el-button> -->
      </div>
      <div class="main-title">
        <span class="dot-line-gray"></span>
        <span class="title">分析结果</span>
      </div>
      <el-tabs tab-position="left" type="border-card" style="min-height:500px;flex:1" v-model="currentTab">
        <el-tab-pane label="主题分析">
          <div style="display:flex;justify-content:center;height:200px;align-items:center">
            <el-radio-group v-model="subject" size="large">
              <el-radio-button :label="c" v-for="c in chans" :key="c" :disabled="subject != c" />
            </el-radio-group>
          </div>
        </el-tab-pane>
        <el-tab-pane label="摘要分析">
          <p v-for="s in summary" :key="s" style="margin-bottom:20px;color:#488fce;">
            {{ s }}
          </p>
        </el-tab-pane>
        <el-tab-pane label="关键词分析" name="keywords">
          <vue-echarts :option="wordcloud" style="heigth:500px;" v-if="currentTab == 'keywords'"></vue-echarts>
        </el-tab-pane>
        <el-tab-pane label="情感分析" name="sentiment">
          <template>
            <p style="text-align:center;display:flex;align-items:center;">
              <span style="margin-right:20px;">
                判断为:
              </span>
              <template v-if="sentiment">
                <el-tag effect="dark" v-if="sentiment[0] >= 0.5" type="success">正面</el-tag>
                <el-tag effect="dark" v-else type="danger">负面</el-tag>
              </template>
            </p>
          </template>
          <vue-echarts :option="pie" style="heigth:300px;" v-if="currentTab == 'sentiment'"></vue-echarts>
        </el-tab-pane>
        <el-tab-pane label="词性分析">
          <div class="flex">
            <div style="max-width:80%;min-width: 80%;">
              <my-tag v-for="tag, idx in tags" :val="tag" :key="idx" />
            </div>
            <div>
              <p style="margin-bottom: 22px;height: 45px;line-height: 45px;font-size: 16px;color: #979797;">词性类别图示:</p>
              <el-tag v-text="value.name" style="margin-right: 10px; margin-top: 5px" v-for="value in tp"
                :key="value.name" :color="value.color" effect="dark" type="info"></el-tag>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import request from "/@/utils/request";
import MyTag from "./my-tag.vue";
import { tp } from "./my-tag.vue";
export default {
  props: ['subject'],
  data() {
    return {
      tp,
      chans: ['国内', '国际', '体育', '娱乐', '军事', '科技', '财经', '股市', '美股', '社会'],
      currentTab: 0,
      text: "",
      pie: null,
      wordcloud: null,
      sentiment: null,
      summary: null,
      tags: [],
    };
  },
  mounted() {
    var text = localStorage.getItem("text")
    if (text) {
      this.text = text
      this.analyse();
    }
  },
  methods: {
    async analyse() {
      let { data: sentiment } = await request.post('/sentiment/', { text: this.text })
      this.sentiment = sentiment

      let { data: pie } = await request.post('/pie/', { text: this.text })
      this.pie = pie

      let { data: tags } = await request.post('/tag/', { text: this.text })
      this.tags = tags

      let { data: wordcloud } = await request.post('/keywords/', { text: this.text })
      this.wordcloud = wordcloud

      let { data: summary } = await request.post('/summary/', { text: this.text })
      this.summary = summary
    }
  },
  components: {
    MyTag,
  },
};
</script>

<style lang="postcss" scoped>
.analyse {
  display: flex;
  padding: 30px;
  justify-content: center;

  .wrap {
    width: 80%;
    display: flex;
    flex-direction: column;

    .top {
      border-radius: 5px;
      overflow: hidden;
      padding: 20px;
      background-color: rgb(246, 246, 246);
      box-shadow: #999 1px 1px 5px;
    }

    .main-title {
      position: relative;
      margin: 28px 0 22px 0;
      height: 32px;
      font-size: 24px;
      line-height: 32px;
      color: #565656;

      .dot-line-gray {
        position: absolute;
        top: 15px;
        left: 0;
        right: 0;
        z-index: 0;
        height: 1px;
        border: 1px dashed #888;
      }

      .title {
        position: absolute;
        padding-right: 26px;
        background-color: #f0f2f5;
        z-index: 1;
      }
    }
  }
}
</style>