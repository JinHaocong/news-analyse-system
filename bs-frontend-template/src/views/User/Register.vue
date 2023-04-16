<template>
  <div class="w-screen h-screen bg-gray-200 flex justify-center items-center">
    <div class="layout-login" @keyup="enterSubmit">
      <h3 class="text-2xl font-semibold text-gray-700 text-center mb-6">
        {{ ImportMetaEnv.VITE_APP_TITLE }}
      </h3>
      <el-form
        ref="ruleForm"
        label-position="right"
        label-width="80px"
        :model="form"
        :rules="rules"
      >
        <el-form-item class="mb-6 -ml-20" prop="name">
          <el-input
            v-model="form.name"
            placeholder="请输入用户名"
            prefix-icon="el-icon-user"
          />
        </el-form-item>
        <el-form-item class="mb-6 -ml-20" prop="pwd">
          <el-input
            v-model="form.pwd"
            placeholder="请输入密码"
            prefix-icon="el-icon-lock"
            show-password
          />
        </el-form-item>
        <el-form-item class="mb-6 -ml-20" prop="pwd2">
          <el-input
            v-model="form.pwd2"
            placeholder="请再次输入密码"
            prefix-icon="el-icon-lock"
            show-password
          />
        </el-form-item>
        <el-form-item class="mb-6 -ml-20">
          <el-button type="primary" class="w-full" @click="onSubmit"
            >注册</el-button
          >
        </el-form-item>
        <el-link
          type="info"
          :underline="false"
          class="text-xs"
          @click="toPage('Login')"
          >已有帐号? 立即登录</el-link
        >
      </el-form>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from "vue";
import { useLayoutStore } from "/@/store/modules/layout";
import { ElNotification } from "element-plus";
import { validate } from "/@/utils/formExtend";

const formRender = () => {
  const { register } = useLayoutStore();
  let form = reactive({
    name: "",
    pwd: "",
    pwd2: "",
  });
  const ruleForm = ref(null);
  const enterSubmit = (e: KeyboardEvent) => {
    if (e.key === "Enter") {
      onSubmit();
    }
  };
  const onSubmit = async () => {
    let { name, pwd, pwd2 } = form;
    if (!(await validate(ruleForm))) return;
    await register({ username: name, password: pwd, password2: pwd2 });
    ElNotification({
      title: "提示",
      message: "注册成功",
      type: "success",
    });
  };
  const rules = reactive({
    name: [
      {
        validator: (
          rule: any,
          value: any,
          callback: (arg0?: Error | undefined) => void
        ) => {
          if (!value) {
            return callback(new Error("用户名不能为空"));
          }
          callback();
        },
        trigger: "blur",
      },
    ],
    pwd: [
      {
        validator: (
          rule: any,
          value: any,
          callback: (arg0?: Error | undefined) => void
        ) => {
          if (!value) {
            return callback(new Error("密码不能为空"));
          }
          callback();
        },
        trigger: "blur",
      },
    ],
    pwd2: [
      {
        required: true,
        message: "确认密码不能为空",
        trigger: "blur",
      },
      {
        validator: (
          rule: any,
          value: string,
          callback: (arg0?: Error | undefined) => void
        ) => {
          if(value!==form.pwd){
              callback(new Error("两次密码不一致"))
          }
          callback();
        },
        trigger: "blur",
      },
    ],
  });
  return {
    form,
    onSubmit,
    enterSubmit,
    rules,
    ruleForm,
  };
};
export default defineComponent({
  name: "Login",
  setup() {
    return {
      labelCol: { span: 4 },
      wrapperCol: { span: 14 },
      ...formRender(),
    };
  },
});
</script>

<style lang='postcss' scoped>
.layout-login {
  width: 450px;
  padding: 60px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 12px 0 rgb(0 0 0 / 10%);

  /* ::v-deep(.el-input__inner) {
    border: 1px solid hsla(0, 0%, 100%, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #ddd;
  } */
}
</style>