<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-upload2" @click="handleDownload">
        导出excel
      </el-button>
      <router-link to="/manage/manage_qu/qu_edit">
        <el-button type="primary">添加</el-button>
      </router-link>
    </div>
    <br>
    <el-table :key="tableKey" v-loading="listLoading" :data="list" border fit highlight-current-row style="width: 100%;">
      <el-table-column label="问卷名" prop="qu_name" align="center" min-width="80">
        <template slot-scope="{row}">
          <span>{{ row.qu_name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="编辑问卷" align="center" min-width="100" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <router-link :to="{path: '/manage/manage_qu/qu_do', query: {qu_id: row.qu_id, isPreview: '1'}}">
            <el-button size="mini">浏览</el-button>
          </router-link>
          <router-link :to="{path: '/manage/manage_qu/qu_edit', query: {qu_id: row.qu_id}}">
            <el-button type="primary" size="mini">编辑</el-button>
          </router-link>
          <router-link :to="{path: '/manage/manage_qu/qu_edit_report', query: {qu_id: row.qu_id}}">
            <el-button type="primary" size="mini">报告编辑</el-button>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column label="删除问卷" align="center" min-width="100" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button size="mini" type="danger" @click="handleDelete(row,$index)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import { getQuList, delQu } from '@/api/questionnair'

export default {
  name: 'ManageQu',
  directives: { waves },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      downloadLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    async getList() {
      this.listLoading = true
      // this.list = [{ qu_id: 1, qu_name: 'a' },
      //   { qu_id: 2, qu_name: 'b' },
      //   { qu_id: 3, qu_name: 'c' }]
      await getQuList().then(response => {
        this.list = response.list
      })
      this.total = this.list.length
      setTimeout(() => {
        this.listLoading = false
      }, 0.3 * 1000)
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleDelete(row, index) {
      delQu({ 'qu_id': row.qu_id }).then(response => {
        this.$notify.success({ title: '删除成功', message: '问卷已删除', showClose: false, duration: 1000 })
        this.list.splice(index, 1)
      })
    },
    handleDownload() {
      this.downloadLoading = true
        import('@/vendor/Export2Excel').then(excel => {
          const tHeader = ['问卷名']
          const filterVal = ['qu_name']
          const data = this.formatJson(filterVal)
          excel.export_json_to_excel({
            header: tHeader,
            data,
            filename: 'questionnairs'
          })
          this.downloadLoading = false
        })
    },
    formatJson(filterVal) {
      return this.list.map(v => filterVal.map(j => {
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    }
  }
}
</script>
