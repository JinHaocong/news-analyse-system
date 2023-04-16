<template>
  <el-tag v-text="val[0]" style="margin-right: 10px; margin-top: 5px" :title="value.name" :color="value.color"
    effect="dark" type="info"></el-tag>
</template>

<script>
export const tp = [
  {
    name: "人名",
    expression: /^nr/i,
    color: "#50c6fb",
  },
  {
    name: "地名",
    expression: /^ns/i,
    color: "#d07f7f",
  },
  {
    name: "组织",
    expression: /^nt/i,
    color: "#8e8b8b",
  },
  {
    name: "字符串",
    expression: /^nx/i,
    color: "#96dbf8",
  },
  {
    name: "专有名词",
    expression: /^nz/i,
    color: "#8bc3f5",
  },
  {
    name: "名词",
    expression: /^n/i,
    color: "#488fce",
  },
  {
    name: "电话号码",
    expression: /^tel/i,
    color: "#184",
  },
  {
    name: "时间词",
    expression: /^t/i,
    color: "#c7aee7",
  },
  {
    name: "处所词",
    expression: /^s/i,
    color: "#cee887",
  },
  {
    name: "方位词",
    expression: /^f/i,
    color: "#c9aaca",
  },
  {
    name: "动词",
    expression: /^v/i,
    color: "#ffcb99",
  },
  {
    name: "形容词",
    expression: /^a/i,
    color: "#67ccaa",
  },
  {
    name: "区别词",
    expression: /^b/i,
    color: "#67a6d9",
  },
  {
    name: "状态词",
    expression: /^z/i,
    color: "#f3e988",
  },
  {
    name: "代词",
    expression: /^r/i,
    color: "#9acccd",
  },
  {
    name: "数词",
    expression: /^m/i,
    color: "#986699",
  },
  {
    name: "量词",
    expression: /^q/i,
    color: "#ff9899",
  },
  {
    name: "副词",
    expression: /^d/i,
    color: "#ffcccb",
  },
  {
    name: "介词",
    expression: /^p/i,
    color: "#99cc67",
  },
  {
    name: "连词",
    expression: /^c/i,
    color: "#8ea4de",
  },
  {
    name: "网页链接",
    expression: /^url/i,
    color: "#680",
  },
  {
    name: "助词",
    expression: /^u/i,
    color: "#4dd9e6",
  },
  {
    name: "电子邮件",
    expression: /^email/i,
    color: "#694",
  },
  {
    name: "叹词",
    expression: /^e/i,
    color: "#d7acd7",
  },
  {
    name: "语气词",
    expression: /^y/i,
    color: "#f48363",
  },
  {
    name: "拟声词",
    expression: /^o/i,
    color: "#f2d404",
  },
  {
    name: "前缀",
    expression: /^h/i,
    color: "#30aadd",
  },
  {
    name: "身份证号",
    expression: /^id/i,
    color: "#691",
  },
  {
    name: "IP地址",
    expression: /^ip/i,
    color: "#846",
  },
  {
    name: "后缀",
    expression: /^k/i,
    color: "#806",
  },
  {
    name: "标点符号",
    expression: /^w/i,
    color: "#946",
  },
  {
    name: "成语",
    expression: /^i/i,
    color: "#f3f",
  },
  {
    name: "简称略语",
    expression: /^j/i,
    color: "#13c",
  },
];
export default {
  props: ["val"],
  computed: {
    value() {
      for (let i of tp) {
        if (i.expression.test(this.val[1])) {
          return i;
        }
      }
      console.log(this.val)
      return {
        name: '未知',
        color: 'red'
      }
    },
  },
};
</script>