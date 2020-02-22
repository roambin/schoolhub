<template>
  <div class="app-container">
    <upload-excel-component :on-success="handleSuccess" :before-upload="beforeUpload" />
    <br>
    <el-form ref="form" :model="uploadForm" :rules="uploadFormRules" label-width="120px">
      <el-form-item label="问卷" prop="qu_id">
        <el-select v-model="uploadForm.qu_id" placeholder="选择问卷">
          <el-option v-for="item in quOptions" :key="item.qu_id" :label="item.qu_name" :value="item.qu_id" />
        </el-select>
      </el-form-item>
      <el-form-item label="用户名列" prop="name">
        <el-select v-model="uploadForm.name" placeholder="输入数字">
          <el-option v-for="i in tableHeader.length" :key="i-1" :label="i" :value="i-1" />
        </el-select>
      </el-form-item>
      <el-form-item label="数据列区间" prop="area">
        <el-select ref="low" v-model="uploadForm.low" placeholder="输入数字">
          <el-option v-for="i in tableHeader.length" :key="i-1" :label="i" :value="i-1" />
        </el-select>
        -
        <el-select ref="high" v-model="uploadForm.high" placeholder="输入数字">
          <el-option v-for="i in tableHeader.length" :key="i-1" :label="i" :value="i-1" />
        </el-select>
      </el-form-item>
      <el-button :loading="loading" type="primary" @click="submit">上传</el-button>
    </el-form>
    <el-table :data="tableData" border highlight-current-row style="width: 100%;margin-top:20px;">
      <el-table-column v-for="item of tableHeader" :key="item" :prop="item" :label="item" />
    </el-table>
  </div>
</template>

<script>
import UploadExcelComponent from '@/components/UploadExcel/index.vue'
import { uploadQuData, getQuList, getQuInfo } from '@/api/questionnair'

export default {
  name: 'UploadExcel',
  components: { UploadExcelComponent },
  data() {
    const validateLargeThanLow = (rule, value, callback) => {
      if (this.uploadForm.low === null || this.uploadForm.high === null || this.uploadForm.low > this.uploadForm.high) {
        callback(new Error('无效的数据区间'))
      } else {
        callback()
      }
    }
    return {
      loading: false,
      tableData: [],
      tableHeader: [],
      quOptions: [],
      uploadForm: {
        qu_id: null,
        name: null,
        low: null,
        high: null
      },
      qu_info: null,
      uploadFormRules: {
        qu_id: [{ required: true, message: '不可为空' }],
        name: [{ required: true, message: '不可为空' }],
        area: [{ validator: validateLargeThanLow }]
      }
    }
  },
  created() {
    getQuList().then(response => {
      this.quOptions = response.list
    })
  },
  methods: {
    beforeUpload(file) {
      const isLt1M = file.size / 1024 / 1024 < 100
      if (isLt1M) {
        return true
      }
      this.$message({
        message: '上传文件不可大于100M，请分批上传',
        type: 'warning'
      })
      return false
    },
    handleSuccess({ results, header }) {
      this.tableData = results
      this.tableHeader = header
      this.uploadForm.name = 0
      this.uploadForm.low = 1
      this.uploadForm.high = header.length - 1
    },
    submit() {
      this.$refs.form.validate(valid => {
        if (valid) {
          this.uploadqu_datas()
        } else {
          return false
        }
      })
    },
    async uploadqu_datas() {
      await getQuInfo({ 'qu_id': this.uploadForm.qu_id }).then(response => {
        this.qu_info = response.data.qu.qu_info
      })
      const dataColNum = this.uploadForm.high - this.uploadForm.low + 1
      if (dataColNum !== this.qu_info.length) {
        this.$message.warning('上传数据有' + dataColNum + '列，而问卷有' + this.qu_info.length + '题，请确保数据一致')
        this.loading = false
        return false
      }
      const usernames = this.tableData.map(o => o[this.tableHeader[this.uploadForm.name]])
      const qu_datas = this.tableData.map(o => {
        const tmpList = []
        for (let i = this.uploadForm.low; i <= this.uploadForm.high; i++) {
          const iq = i - this.uploadForm.low
          let item = o[this.tableHeader[i]]
          if (this.qu_info[iq].type === '单选') {
            item = Number(item)
          } else if (this.qu_info[iq].type === '多选') {
            item = item.toString().split(',').map(e => Number(e))
          } else if (this.qu_info[iq].type === '简答') {
            item = item.toString()
          }
          tmpList.push(item)
        }
        return tmpList
      })
      uploadQuData({ qu_id: this.uploadForm.qu_id, usernames: usernames, qu_datas: qu_datas }).then(() => {
        this.$message.success('上传成功')
        this.loading = false
      }).catch(() => {
        this.loading = false
      })
    }
  }
}
</script>
