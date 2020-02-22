<template>
  <div class="app-container">
    <el-button size="mini" @click="cancel">返回</el-button>
    <el-button v-if="!isPreview" type="primary" size="mini" @click="submit">提交</el-button>
    <br><br>
    <!-- Note that row-key is necessary to get a correct row order. -->
    {{ qu.qu_name }}<br><br>
    <div class="editor-content" v-html="qu.qu_text" /><br>
    <el-form ref="form" v-loading="listLoading" :model="qu_data">
      <el-form-item v-for="(v, i) in qu.qu_info" :key="i">
        {{ i + 1 + '.（' + v.type + '）' + v.title }}<br>
        <el-radio-group v-if="v.type==='单选'" v-model="qu_data[i]">
          <el-radio v-for="(opt, j) in v.options" :key="j" :label="j+1" style="width: 100%">{{ opt }}<br><br><br></el-radio>
        </el-radio-group>
        <el-checkbox-group v-if="v.type==='多选'" v-model="qu_data[i]">
          <el-checkbox v-for="(opt, j) in v.options" :key="j" :label="j+1" style="width: 100%">{{ opt }}</el-checkbox>
        </el-checkbox-group>
        <el-input v-if="v.type==='简答'" v-model="qu_data[i]" type="textarea" autosize>{{ qu_data[i] }}</el-input>
      </el-form-item>
    </el-form>
    <el-button @click="cancel">返回</el-button>
    <el-button v-if="!isPreview" type="primary" @click="submit">提交</el-button>

    <el-dialog title="提示" :visible.sync="dialogVisible">
      <span>返回后已填信息将丢失</span>
      <span slot="footer" class="dialog-footer">
        <el-button style="max-width: 40%;" @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" style="max-width: 40%;" @click="cancel_do">确定</el-button>
      </span>
    </el-dialog>
    <br><br>
    <div v-if="this.$route.query.dev === '1'">
      <el-alert>json格式数据：<br>{{ qu_data }}</el-alert>
    </div>
  </div>
</template>

<script>
import { getQuInfo, setQuData, getQuData } from '@/api/questionnair'

export default {
  name: 'QuDo',
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      listLoading: true,
      qu: {
        qu_name: null,
        qu_info: [],
        qu_text: null
      },
      userid: this.$route.query.userid,
      qu_id: this.$route.query.qu_id,
      qu_data: null,
      isPreview: false,
      dialogVisible: false,
      isQuDataChanged: null
    }
  },
  watch: {
    qu_data: {
      handler() {
        if (this.isQuDataChanged === null) {
          this.isQuDataChanged = false
        } else if (!this.isQuDataChanged) {
          this.isQuDataChanged = true
        }
      },
      deep: true
    }
  },
  created() {
    this.listLoading = true
    this.isPreview = this.$route.query.isPreview === '1'
    this.getList()
  },
  methods: {
    async getList() {
      // this.qu_name = 'XXX问卷'
      // this.qu_info = [{ type: '单选', title: '第一道题', options: ['选项1', '选项2', '选项3'] },
      //   { type: '多选', title: '第二道题', options: ['选项a', '选项b'] },
      //   { type: '简答', title: '第三道题' }]
      await getQuInfo({ 'qu_id': this.qu_id }).then(response => {
        this.qu = response.data.qu
      })
      await getQuData({ 'qu_id': this.qu_id, 'userid': this.userid }).then(response => {
        this.qu_data = response.data.qu_data
      })
      if (!this.qu_data) {
        this.qu_data = this.qu.qu_info.map(v => [])
      }
      this.listLoading = false
    },
    submit() {
      const undoList = []
      for (let i = 0; i < this.qu_data.length; i++) {
        if (this.qu_data[i].length === 0) {
          undoList.push(i + 1)
        }
      }
      if (undoList.length > 0) {
        this.$message.warning('有题目未填：' + undoList)
      } else {
        setQuData({ 'qu_id': this.qu_id, 'qu_data': this.qu_data, 'userid': this.userid }).then(response => {
          this.isQuDataChanged = false
          this.$message.success('提交成功')
        })
      }
    },
    cancel() {
      if (this.isPreview) {
        this.cancel_do()
        // this.$router.push('/manage/manage_qu')
      } else {
        if (this.isQuDataChanged) {
          this.dialogVisible = true
        } else {
          this.cancel_do()
        }
      }
    },
    cancel_do() {
      this.$router.go(-1)
    }
  }
}
</script>
