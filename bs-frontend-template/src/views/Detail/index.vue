<template>
  <div v-if="detail" style="padding: 30px">
    <h1 class="main-title">{{ detail.title }}</h1>
    <div class="desc">
      <el-button
        @click="viewCommentDetail(detail.text, detail.subject)"
        type="primary"
        size="mini"
        >内容分析
      </el-button>
      <span title="点击率">
        <svg-icon
          class-name="svg-icon"
          icon-class="svg-eye-open"
          style="display: inline"
        />
        {{ detail.view_count }}
      </span>
      <span>
        {{ detail.intime }}
      </span>
      <span>
        {{ detail.media_name }}
      </span>
      <span v-if="detail.keywords">
        <el-tag
          v-for="t in detail.keywords.split(',')"
          :key="t"
          type="info"
          style="margin: 0 5px 5px 0; cursor: pointer"
          effect="plain"
          >{{ t }}</el-tag
        >
      </span>
    </div>
    <div v-html="detail.html" />
  </div>
</template>

<script>
import request from "/@/utils/request";
export default {
  props: ["id"],
  created() {
    request.post("/news/detail/", { id: this.id }).then((res) => {
      this.detail = res.data;
    });
  },
  data() {
    return {
      detail: null,
    };
  },
  methods: {
    jsonify(text) {
      return JSON.parse(text);
    },
    viewCommentDetail(text, subject) {
      localStorage.setItem("text", text.trim());
      this.$router.push({ name: "AnalyseList", params: { subject } });
    },
  },
};
</script>

<style lang="postcss" scoped>
.main-title {
  font-size: 38px;
  color: #4d4f53;
  line-height: 38px;
  padding: 40px 0;
  font-weight: bold;
  text-align: center;
}

.desc {
  height: 64px;
  border: 1px solid #e5e5e5;
  border-width: 1px 0;
  width: 100%;
  background: #f0f2f4;
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  padding: 0 30px;
  flex-direction: row-reverse;

  span {
    margin-right: 20px;
  }
}
</style>
<style>
.img_wrapper {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  text-align: center;
}
</style>