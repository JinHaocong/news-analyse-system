<template>
  <div class="chart-container" style="margin-bottom: 50px; width: 100%; height: 500px" ref="el"></div>
</template>

<script lang="ts" setup>
import { onMounted, ref, watch } from "vue";
import request from "/@/utils/request";
const props = defineProps(["api", "option"]);
const el = ref(null);
let chart: any = null;
const load = () => {
  if (props.api) {
    request.get(props.api).then((res) => {
      if (typeof res.data === "string") {
        let no = eval("(" + res.data + ")");
        chart.clear()
        chart.setOption(no);
      } else {
        chart.clear()
        chart.setOption(res.data);
      }
      chart.resize();
    });
  } else {
    if (typeof props.option === "string") {
      let no = eval("(" + props.option + ")");
      chart.clear()
      chart.setOption(no);
    } else {
      if (props.option) {
        chart.clear()
        chart.setOption(props.option);
        setTimeout(chart.resize, 100)
      }
    }
  }
};
watch(
  () => props.api,
  () => {
    load();
  }
);
watch(
  () => props.option,
  () => {
    load();
  },
  {
    deep: true
  }
);
onMounted(() => {
  chart = echarts.init(el.value as unknown as HTMLElement, "white", {
    renderer: "canvas",
  });
  window.addEventListener("resize", () => {
    chart.resize();
  });
  load();
});
</script>