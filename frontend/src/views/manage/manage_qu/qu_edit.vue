<template>
  <div class="app-container">
    <el-button size="mini" @click="clickCancel">返回</el-button>
    <el-button type="primary" size="mini" @click="submit">提交</el-button>
    <br><br>
    <!-- Note that row-key is necessary to get a correct row order. -->
    问卷名：<el-input v-model="qu.qu_name" maxlength="30" size="medium" style="width: 80%" /><br><br>
<!--    问卷说明：<el-input v-model="qu_text" type="textarea" autosize>{{ qu_text }}</el-input><br><br>-->
    问卷说明：<br><br><tinymce v-model="qu.qu_text" :height="300" /><br><br>
    题目：<br><br>
    <el-table ref="dragTable" v-loading="listLoading" :data="qu.qu_info" :show-header="false" border fit highlight-current-row style="width: 100%">
      <el-table-column min-width="300px" label="内容">
        <template slot-scope="{row,$index}">
          题目：
          <el-select v-model="row.type" size="mini" placeholder="问卷类型">
            <el-option v-for="item in ['单选', '多选', '简答']" :key="item" :label="item" :value="item" />
          </el-select>
          <el-input v-model="row.title" size="small" />
          <div v-if="row.type !== '简答'">
            选项：
            <div v-for="(u,i) in row.options" :key="i">
              <el-input v-model="row.options[i]" size="small" style="width: 90%" />
              <el-button size="mini" type="danger" style="max-width: 5%" round plain @click="delOption($index, i)">-</el-button>
            </div>
            <el-button type="primary" size="mini" round plain @click="addOption($index)">+</el-button>
          </div>
        </template>
      </el-table-column>

      <el-table-column align="center" label="删除" width="80">
        <template slot-scope="{row,$index}">
          <el-button type="danger" icon="el-icon-delete" circle plain @click="delQuestion($index)" />
        </template>
      </el-table-column>
    </el-table>
    <br>
    添加：
    <el-button type="primary" size="small" round plain @click="addQuestion('单选')">单选</el-button>
    <el-button type="primary" size="small" round plain @click="addQuestion('多选')">多选</el-button>
    <el-button type="primary" size="small" round plain @click="addQuestion('简答')">简答</el-button>
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
      <el-input v-model="dev.qu_info" type="textarea" autosize style="font-size: 70%" @change="qu.qu_info = JSON.parse(dev.qu_info)"/>
      <el-alert>{{ qu_id }}<br>问卷名：{{ qu.qu_name }}<br>json格式数据：<br>{{ qu }}</el-alert>
    </div>
  </div>
</template>

<script>
import { getQuInfo, setQuInfo } from '@/api/questionnair'
import Tinymce from '@/components/Tinymce'

export default {
  name: 'QuEdit',
  components: { Tinymce },
  data() {
    return {
      qu_id: null,
      qu: {
        qu_name: null,
        qu_info: [],
        qu_text: null
      },
      isQuInfoChanged: null,
      listLoading: true,
      dialogVisible: false,
      dev: { qu_info: null }
    }
  },
  watch: {
    list: {
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
      // this.qu_name = ''
      // this.qu.qu_info = [{ type: '单选', title: 'a', options: ['1', '2'] },
      //   { type: '多选', title: 'b', options: ['11', '22'] },
      //   { type: '简答', title: 'c' }]
      getQuInfo({ 'qu_id': this.qu_id }).then(response => {
        this.qu = response.data.qu
        this.listLoading = false
      })
    },
    addOption(i_q) {
      this.qu.qu_info[i_q].options.push(null)
    },
    delOption(i_q, i_o) {
      this.qu.qu_info[i_q].options.splice(i_o, 1)
    },
    addQuestion(type) {
      const elem = { type: type, title: null }
      if (type !== '简答') {
        elem.options = [null]
      }
      this.qu.qu_info.push(elem)
    },
    delQuestion(i_q) {
      this.qu.qu_info.splice(i_q, 1)
    },
    submit() {
      setQuInfo({
        'qu_id': this.qu_id,
        'qu': this.qu
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
