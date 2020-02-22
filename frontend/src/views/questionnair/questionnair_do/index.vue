<template>
  <div class="app-container">
    <router-link :to="{path: '/report/general_report'}">
      <el-button type="primary">综合报告</el-button>
    </router-link>
    <br><br>
    <el-table :key="tableKey" v-loading="listLoading" :data="list" border fit highlight-current-row style="width: 100%;">
      <el-table-column label="问卷名" prop="qu_name" align="center" min-width="80">
        <template slot-scope="{row}">
          <span>{{ row.qu_name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" min-width="100" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <router-link :to="{path: '/questionnair/qu_do', query: {qu_id: row.qu_id, isPreview: '0'}}">
            <el-button type="primary" size="mini">做问卷</el-button>
          </router-link>
          <router-link :to="{path: '/report/generate_report', query: {qu_id: row.qu_id}}">
            <el-button size="mini">查看报告</el-button>
          </router-link>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />
  </div>
</template>

<script>
import { getQuList } from '@/api/questionnair'
import waves from '@/directive/waves' // waves directive
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

export default {
  name: 'QuestionnairDoIndex',
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 100000,
        qu_name: undefined
      }
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
      }, 0.6 * 1000)
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    }
  }
}
</script>
