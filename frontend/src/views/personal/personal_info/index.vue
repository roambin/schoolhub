<template>
  <div class="app-container">
    <el-form ref="form" :model="user_info" label-width="80px">
      <h3 class="title">个人信息</h3>
      <el-form-item label="用户名">
        <el-input v-model="user_info.username" :disabled="!$minRole(3)" style="max-width: 200px" />
      </el-form-item>
      <el-form-item label="机构">
        <el-select v-model="user_info.org" placeholder="机构" :disabled="!$minRole(3)" clearable>
          <el-option v-for="v in orgs" :key="v.org_name" :label="v.org_name" :value="v.org_name" />
        </el-select>
      </el-form-item>
      <el-form-item label="班级">
        <el-select v-model="user_info.sub_org" placeholder="班级" :disabled="userid && !$minRole(3)" multiple clearable>
          <el-option v-for="v in orgs_map[user_info.org]" :key="v" :label="v" :value="v" />
        </el-select>
      </el-form-item>
      <el-form-item label="生日">
        <el-date-picker v-model="user_info.birthday" type="date" value-format="yyyy-MM-dd" placeholder="选择日期" :disabled="userid && !$minRole(3)" style="max-width: 500px" />
      </el-form-item>
    </el-form>
    <el-button @click="back">返回</el-button>
    <el-button type="primary" @click="submit">提交</el-button>
  </div>
</template>

<script>
import { setUserInfo, getUserInfo } from '@/api/user'
import { org_list } from '@/api/organization'

export default {
  name: 'PersonalInfo',
  data() {
    return {
      user_info: null,
      userid: null,
      orgs: [],
      orgs_map: {}
    }
  },
  created() {
    this.userid = this.$route.query.userid
    this.getList()
    this.getOrgs()
  },
  methods: {
    getList() {
      getUserInfo({ userid: this.userid }).then(response => {
        this.user_info = response.data.user_info
      })
    },
    getOrgs() {
      org_list().then(response => {
        this.orgs = response.data.orgs
        this.orgs_map = response.data.orgs_map
      })
    },
    submit() {
      const data = { user_infos: [this.user_info] }
      data['userids'] = this.userid ? [this.userid] : null
      setUserInfo(data).then(response => {
        this.$message.success('编辑成功')
      })
    },
    back() {
      this.$router.go(-1)
    }
  }
}
</script>
