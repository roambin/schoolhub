<template>
  <div class="login-container">
    <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" auto-complete="on" label-position="left">

      <div class="title-container">
        <h3 class="title">{{ isLogin ? '登入' : '注册' }}</h3>
        <div class="tips">
          <span style="cursor:pointer;user-select:none;" @click="switch_login">切换为{{ !isLogin ? '登入' : '注册' }}</span>
        </div>
      </div>

      <el-form-item v-show="!isLogin" prop="user_info.org">
        <el-select ref="org" v-model="loginForm.user_info.org" placeholder="机构" clearable style="width: 100%" @change="loginForm.user_info.sub_org=[]">
          <el-option v-for="v in orgs" :key="v.org_name" :label="v.org_name" :value="v.org_name" />
        </el-select>
      </el-form-item>
      <el-form-item v-show="!isLogin">
        <el-select v-model="loginForm.user_info.sub_org" placeholder="班级" multiple clearable style="width: 100%">
          <el-option v-for="v in orgs_map[loginForm.user_info.org]" :key="v" :label="v" :value="v" />
        </el-select>
      </el-form-item>
      <el-form-item prop="user_info.username">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          ref="username"
          v-model="loginForm.user_info.username"
          placeholder="用户名"
          name="username"
          type="text"
          tabindex="1"
          auto-complete="on"
        />
      </el-form-item>

      <el-form-item prop="password">
        <span class="svg-container">
          <svg-icon icon-class="password" />
        </span>
        <el-input
          :key="passwordType"
          ref="password"
          v-model="loginForm.password"
          :type="passwordType"
          placeholder="密码"
          name="password"
          tabindex="2"
          auto-complete="on"
          @keyup.enter.native="handleLogin"
        />
        <span class="show-pwd" @click="showPwd">
          <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
        </span>
      </el-form-item>

      <el-form-item v-show="!isLogin" prop="password_confirm">
        <span class="svg-container">
          <svg-icon icon-class="password" />
        </span>
        <el-input
          :key="passwordType"
          ref="password_confirm"
          v-model="loginForm.password_confirm"
          :type="passwordType"
          placeholder="确认密码"
          name="password_confirm"
          tabindex="2"
          @keyup.enter.native="handleLogin"
        />
      </el-form-item>

      <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:30px;" @click.native.prevent="handleLogin">登入</el-button>

    </el-form>
  </div>
</template>

<script>
import { org_list_name } from '@/api/organization'

export default {
  name: 'Login',
  data() {
    const validateUsername = (rule, value, callback) => {
      if (value.length === 0 || value.length > 30) {
        callback(new Error('用户名长度为1到30个字符'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('密码不能低于6位'))
      } else {
        callback()
      }
    }
    const validatePasswordConfirm = (rule, value, callback) => {
      if (!this.isLogin && value !== this.loginForm.password) {
        callback(new Error('两次密码不一致'))
      } else {
        callback()
      }
    }
    const validateNotEmpty = (rule, value, callback) => {
      if (!this.isLogin && !value) {
        callback(new Error('不可为空'))
      } else {
        callback()
      }
    }
    return {
      isLogin: true,
      loginForm: {
        user_info: { sub_org: [] },
        password: '',
        password_confirm: ''
      },
      loginRules: {
        user_info: {
          username: [{ required: true, trigger: 'blur', validator: validateUsername }]
          // org: [{ required: true, rigger: 'blur', validator: validateNotEmpty }]
        },
        password: [{ required: true, trigger: 'blur', validator: validatePassword }],
        password_confirm: [{ required: true, trigger: 'blur', validator: validatePasswordConfirm }]
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined,
      orgs: [],
      orgs_map: {}
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  created() {
    this.getOrgs()
  },
  methods: {
    getOrgs() {
      org_list_name().then(response => {
        this.orgs = response.data.orgs
        this.orgs_map = response.data.orgs_map
      })
    },
    switch_login() {
      this.isLogin = !this.isLogin
    },
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store.dispatch(this.isLogin ? 'user/login' : 'user/register', this.loginForm).then(() => {
            this.$message.success(this.isLogin ? '登入成功' : '注册成功')
            this.$router.push({ path: this.redirect || '/' })
            this.loading = false
          }).catch(() => {
            this.loading = false
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg:#283443;
$light_gray:#fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg:#2d3a4b;
$dark_gray:#889aa4;
$light_gray:#eee;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
}
</style>
