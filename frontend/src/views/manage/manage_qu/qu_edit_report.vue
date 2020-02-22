<template>
  <div class="app-container">
    <el-button size="mini" @click="clickCancel">返回</el-button>
    <el-button type="primary" size="mini" @click="submit">提交</el-button>
    <br><br>
    <el-input v-model="cur_label" placeholder="选择或输入报告标签，点击切换" class="input-with-select" style="max-width: 300px">
      <el-select slot="prepend" v-model="cur_label">
        <el-option v-for="v in labels" :key="v" :label="v" :value="v" />
      </el-select>
    </el-input>
    <el-button type="primary" round plain @click="handleChange">切换</el-button>
    <el-button type="danger" round plain @click="delOption">删除</el-button>
    <br><br>
    {{ cur_label }}报告：<br><br>
    <div v-for="v in labels" :key="'f'+v">
      <tinymce v-if="cur_label === v" :key="v" v-model="qu.qu_report_map[v]" :height="500" />
    </div>
    <br><br>
    <el-button @click="clickCancel">返回</el-button>
    <el-button type="primary" @click="submit">提交</el-button>

    <el-dialog title="提示" :visible.sync="dialogVisible">
      <span>返回后未提交的信息将丢失</span>
      <span slot="footer" class="dialog-footer">
        <el-button style="max-width: 40%;" @click="dialogVisible = false">取消</el-button>
        <el-button style="max-width: 40%;" type="primary" @click="cancel">确定</el-button>
      </span>
    </el-dialog>
    <br><br>
    <div v-if="this.$route.query.dev === '1'">
      <el-input v-model="dev.info" type="textarea" autosize style="font-size: 70%" @change="qu.qu_report_map[cur_label] = dev.info"/>
      <el-alert>{{ qu_id }}<br>问卷名：{{ qu.qu_name }}<br>json格式数据：<br>{{ qu }}</el-alert>
    </div>
  </div>
</template>

<script>
import { quGet, quSet } from '@/api/questionnair'
import Tinymce from '@/components/Tinymce'

export default {
  name: 'QuEditReport',
  components: { Tinymce },
  data() {
    return {
      qu_id: null,
      qu: {
        qu_name: null,
        qu_report_map: {}
      },
      add_label: null,
      cur_label: null,
      labels: null,
      isQuInfoChanged: null,
      listLoading: true,
      dialogVisible: false,
      dev: { info: null }
    }
  },
  watch: {
    qu: {
      handler() {
        if (this.isQuInfoChanged === null) {
          this.isQuInfoChanged = false
        } else if (!this.isQuInfoChanged) {
          this.isQuInfoChanged = true
        }
      },
      deep: true
    }
  },
  created() {
    this.listLoading = true
    this.qu_id = this.$route.query.qu_id
    if (this.qu_id) {
      this.getQu()
    } else {
      this.listLoading = false
    }
  },
  methods: {
    getQu() {
      quGet({ 'qu_id': this.qu_id, data_sel: ['qu_name', 'qu_report_map'] }).then(response => {
        const qu = response.data.qu
        if (!qu.qu_report_map) {
          qu.qu_report_map = {}
        }
        const labels = []
        for (const i in qu.qu_report_map) {
          labels.push(i)
        }
        this.qu = qu
        this.labels = labels
        this.listLoading = false
      })
    },
    delOption() {
      for (const i in this.labels) {
        if (this.labels[i] === this.cur_label) {
          this.labels.splice(i, 1)
        }
      }
      this.cur_label = null
      delete this.qu.qu_report_map[this.cur_label]
    },
    handleChange() {
      if (this.cur_label) {
        for (const i in this.labels) {
          if (this.labels[i] === this.cur_label) {
            return
          }
        }
        this.labels.push(this.cur_label)
      }
    },
    submit() {
      quSet({
        'qu_id': this.qu_id,
        'data_set': { 'qu_report_map': this.qu.qu_report_map }
      }).then(response => {
        this.$message.success('提交成功')
        this.isQuInfoChanged = false
      })
    },
    clickCancel() {
      if (this.isQuInfoChanged) {
        this.dialogVisible = true
      } else {
        this.cancel()
      }
    },
    cancel() {
      this.$router.go(-1)
    }
  }
}
</script>
