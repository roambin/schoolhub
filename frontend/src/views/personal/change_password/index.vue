<template>
  <div class="app-container">
    <el-form ref="form" :model="data" :rules="rules">
      <h3 class="title">修改密码</h3>
      <el-form-item v-if="!$route.query.userid" label="旧密码" prop="pwd_old" style="max-width: 500px">
        <el-input v-model="data.pwd_old" type="password" />
      </el-form-item>
      <el-form-item label="新密码" prop="pwd_new" style="max-width: 500px">
        <el-input v-model="data.pwd_new" type="password" />
      </el-form-item>
      <el-form-item label="确认密码" prop="pwd_confirm" style="max-width: 500px">
        <el-input v-model="data.pwd_confirm" type="password" />
      </el-form-item>
      <el-button @click="back">返回</el-button>
      <el-button type="primary" @click="submit">修改</el-button>
    </el-form>
  </div>
</template>

<script>
import { resetPwd } from '@/api/user'
import { encrypt } from '@/utils/rsa'

export default {
  name: 'ChangePassword',
  data() {
    const validatePwdOld = (rule, value, callback) => {
      if (value.length === 0 || value.length > 30) {
        callback(new Error('用户名长度为1到30个字符'))
      } else {
        callback()
      }
    }
    const validatePwdNew = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('密码不能低于6位'))
      } else {
        callback()
      }
    }
    const validatePwdConfirm = (rule, value, callback) => {
      if (value !== this.data.pwd_new) {
        callback(new Error('两次密码不一致'))
      } else {
        callback()
      }
    }
    return {
      data: {
        pwd_old: '',
        pwd_new: '',
        pwd_confirm: ''
      },
      rules: {
        pwd_old: [{ required: true, trigger: 'blur', validator: validatePwdOld }],
        pwd_new: [{ required: true, trigger: 'blur', validator: validatePwdNew }],
        pwd_confirm: [{ required: true, trigger: 'blur', validator: validatePwdConfirm }]

      }
    }
  },
  methods: {
    submit() {
      this.$refs.form.validate(valid => {
        if (valid) {
          const data = { pwd_old: encrypt(this.data.pwd_old), pwd_new: encrypt(this.data.pwd_new), userid: this.$route.query.userid }
          resetPwd(data).then(response => {
            this.$message.success('密码修改成功')
          })
          return true
        } else {
          return false
        }
      })
    },
    back() {
      this.$router.go(-1)
    }
  }
}
</script>
