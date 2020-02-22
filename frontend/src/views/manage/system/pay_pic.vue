<template>
  <div>
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>付款二维码</span>
      </div>
      <el-upload
        class="upload-demo"
        drag
        :action="base_url + '/uploadFilesAdmin?token=' + token"
        :data="{filename: 'public/pay_pic'}"
        :show-file-list="false"
        :on-success="handleAvatarSuccess"
        :before-upload="beforeAvatarUpload"
        multiple
      >
        <i class="el-icon-upload" />
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
      </el-upload>
    </el-card>
  </div>
</template>

<script>
import { getToken } from '@/utils/auth'
export default {
  name: 'PayPic',
  data() {
    return {
      base_url: process.env.VUE_APP_BASE_API,
      token: getToken()
    }
  },
  methods: {
    handleAvatarSuccess(res, file) {
      this.$message.success({ message: '修改成功', duration: 1000 })
    },
    beforeAvatarUpload(file) {
      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isLt2M) {
        this.$message.error('上传文件大小不能超过 2MB!')
      }
      return isLt2M
    }
  }
}
</script>
