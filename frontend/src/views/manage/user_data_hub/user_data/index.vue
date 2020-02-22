<template>
  <div class="app-container">
    <div class="filter-container">
      <el-alert>提示：选择问卷后，点击表头可排序</el-alert>
      <el-form>
        <el-form-item>
          <el-select v-model="data_filter.user_info.org" placeholder="机构" size="medium" style="max-width: 200px" @change="handleChangeOrg">
            <el-option v-for="v in orgs" :key="v.org_name" :label="v.org_name" :value="v.org_name" />
          </el-select>
          <el-select v-model="data_filter.user_info.sub_org" placeholder="班级" size="medium" multiple clearable style="max-width: 200px">
            <el-option v-for="v in orgs_map[data_filter.user_info.org]" :key="v" :label="v" :value="v" />
          </el-select>
          <el-select v-model="data_filter.user_info.role" placeholder="权限" size="medium" clearable class="filter-item">
            <el-option v-for="(v,k) in roleMap" :key="k" :label="v" :value="Number(k)" />
          </el-select>
          <el-input v-model="data_filter.user_info.username" placeholder="用户名" size="medium" clearable style="max-width: 200px" class="filter-item" @keyup.enter.native="handleFilter" />
          <el-button v-waves class="filter-item" size="medium" type="primary" round icon="el-icon-search" @click="handleFilter" />
        </el-form-item>
        <el-form-item>
          <el-select v-model="cur_exam.subject_name" placeholder="科目" size="medium" clearable style="max-width: 200px" @change="cur_exam.exam_name=null">
            <el-option v-for="v in subjects" :key="v.subject_name" :label="v.subject_name" :value="v.subject_name" />
          </el-select>
          <el-select v-model="cur_exam.exam_name" placeholder="试卷" size="medium" multiple clearable style="max-width: 200px">
            <el-option v-for="v in subjects_map[cur_exam.subject_name]" :key="v" :label="v" :value="v" />
          </el-select>
          <el-button-group>
            <el-button size="medium" @click="handleChangeExams(true)">添加</el-button>
            <el-button size="medium" @click="handleChangeExams(false)">移除</el-button>
          </el-button-group>
        </el-form-item>
        <el-form-item>
          <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" size="medium" plain icon="el-icon-upload2" @click="handleDownload">导出excel</el-button>
          <el-button type="primary" size="medium" plain round @click="manageVisible = !manageVisible">{{ manageVisible ? '折叠' : '展开' }}</el-button>
          <el-button type="primary" size="medium" @click="userSetSel">保存修改</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-table ref="table" v-loading="listLoading" :data="users" border fit highlight-current-row max-height="1000" style="width: 100%;" @selection-change="handleSelectionChange" @header-click="handleCellClick">
      <el-table-column type="selection" :reserve-selection="true" align="center" min-width="20" />
      <el-table-column label="用户" prop="username" align="center" min-width="80" fixed>
        <template slot-scope="{row}">
          <span>{{ row.user_info.username }}</span>
        </template>
      </el-table-column>
      <el-table-column v-if="manageVisible" label="个人数据" align="center" min-width="80" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <router-link :to="{path: '/manage/user_data_hub/user_data_personal', query: { userid: row['_id'], org_name: row.user_info.org }}">
            <el-button size="mini" type="primary">查看</el-button>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column v-if="manageVisible" label="统计" align="center" min-width="80" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button size="mini" type="primary" @click="handleChart(row, 'line')">折线图</el-button>
          <el-button size="mini" type="primary" @click="handleChart(row, 'bar')">柱状图</el-button>
        </template>
      </el-table-column>
      <el-table-column v-for="v in cur_exams" :key="v" :label="v" align="center" min-width="60" class-name="small-padding fixed-width" :sortable="sortColLabel===v" :sort-method="sortGrade">
        <template slot-scope="{row}">
          <el-input v-model="row['exams_map'][v]" />
        </template>
      </el-table-column>
      <el-table-column v-if="cur_exams.length > 0" label="平均分" align="center" min-width="60" class-name="small-padding fixed-width" sortable :sort-method="sortAvgGrade">
        <template slot-scope="{row}">
          {{ statisticMap[row['_id']].avg.toFixed(2) }}
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="图表" :visible.sync="dialogChartVisible" :show-close="false">
      <line-chart v-if="dialogChartVisible && chartConf.chartType==='line'" :chart-label="cur_exams" :chart-data="chartConf.chartData" :chart-type="chartConf.chartType"/>
      <bar-chart v-if="dialogChartVisible && chartConf.chartType==='bar'" :chart-label="cur_exams" :chart-data="chartConf.chartData" :chart-type="chartConf.chartType"/>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogChartVisible = false">取消</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import waves from '@/directive/waves' // waves directive
import { userListSel, userSetSel } from '@/api/user'
import { org_list } from '@/api/organization'
import LineChart from '@/components/Charts/LineChart'
import BarChart from '@/components/Charts/BarChart'

const roleMap = { 1: '学生', 2: '任课老师', 3: '班主任', 4: '机构经理', 5: '机构管理员', 100: '系统管理员', 101: '最高管理员' }

export default {
  name: 'UserData',
  components: {
    LineChart,
    BarChart
  },
  directives: { waves },
  data() {
    return {
      listLoading: true,
      downloadLoading: false,
      pickRows: [],
      users: null,
      data_filter: {
        user_info: { org: this.$store.getters.user_info.org, role: 1 }
      },
      cur_exams: [],
      cur_exam: { subject_name: null, exam_name: null },
      manageVisible: true,
      orgs: [],
      orgs_map: {},
      subjects: {},
      subjects_map: {},
      roleMap: roleMap,
      sortColLabel: null,
      statisticMap: {},
      dialogChartVisible: false,
      chartConf: {
        chartData: [],
        chartType: 'line'
      }
    }
  },
  created() {
    this.getOrgs()
    this.getList()
  },
  methods: {
    handleSelectionChange(rows) {
      this.pickRows = rows
    },
    handleFilter() {
      this.getList()
    },
    getList() {
      if (!this.data_filter.user_info.org) {
        this.$message.warning({ message: '请选择机构', duration: 1000 })
        this.listLoading = false
        return
      }
      this.listLoading = true
      userListSel({ 'data_filter': this.data_filter, 'data_sel': ['user_info', 'user_data'] }).then(response => {
        const users = response.data.users
        users.map(e => {
          if (!e.user_info.auth) {
            e.user_info.auth = []
          }
          if (!e.user_data) {
            e.user_data = {}
          }
          if (!e.user_data.exams) {
            e.user_data.exams = []
          }
          // grade
          const exams_map = {}
          const subjects = this.subjects
          for (const i in subjects) {
            const subject = subjects[i]
            const exams = subject.exams
            for (const j in exams) {
              const exam = exams[j]
              exams_map[subject.subject_name + '.' + exam] = 0
            }
          }
          const exams = e.user_data.exams || []
          for (const i in exams) {
            const exam = exams[i]
            if (exams_map[exam.exam_name] === 0) {
              exams_map[exam.exam_name] = Number(exam.exam_grade)
            }
          }
          e['exams_map'] = exams_map
          return e
        })
        this.users = users
        this.$refs.table.clearSelection()
      })
      setTimeout(() => {
        this.listLoading = false
      }, 0.3 * 1000)
    },
    getSubjects() {
      let org_name = this.$store.getters.user_info.org
      if (this.$store.getters.user_info.role >= 100) {
        org_name = this.data_filter.user_info.org
      }
      for (const i in this.orgs) {
        const org = this.orgs[i]
        if (org.org_name === org_name) {
          this.subjects = org.subjects
          const map = {}
          for (const i in this.subjects) {
            const v = this.subjects[i]
            map[v.subject_name] = v.exams
          }
          this.subjects_map = map
        }
      }
    },
    getOrgs() {
      org_list().then(response => {
        this.orgs = response.data.orgs
        this.orgs_map = response.data.orgs_map
        this.getSubjects()
      })
    },
    userSetSel() {
      const userids = []
      const data_set = []
      const rows = this.pickRows
      for (const i in rows) {
        const row = rows[i]
        const exams_map = row.exams_map
        const exams = []
        for (const k in exams_map) {
          exams.push({ 'exam_name': k, 'exam_grade': Number(exams_map[k]) })
        }
        row.user_data.exams = exams
        userids.push(row['_id'])
        data_set.push({ 'user_data.exams': row.user_data.exams })
      }
      userSetSel({ 'userids': userids, 'data_set': data_set }).then(response => {
        this.$message.success({ message: '修改成功', duration: 1000 })
      })
    },
    handleChangeOrg() {
      this.cur_exams = []
      this.data_filter.user_info.sub_org = []
      this.getSubjects()
    },
    handleChangeExams(isAdd) {
      for (const k in this.cur_exam.exam_name) {
        const exam = this.cur_exam.subject_name + '.' + this.cur_exam.exam_name[k]
        if (isAdd) {
          this.cur_exams.push(exam)
        } else {
          for (const i in this.cur_exams) {
            if (this.cur_exams[i] === exam) {
              this.cur_exams.splice(i, 1)
            }
          }
        }
      }

      const statisticMap = {}
      const users = this.users
      for (const i in users) {
        const user = users[i]
        const statistic = { sum: 0, avg: 0 }
        const exams = this.cur_exams
        for (const j in exams) {
          statistic.sum += user.exams_map[exams[j]]
        }
        statistic.avg = statistic.sum / exams.length
        statisticMap[user['_id']] = statistic
      }
      this.statisticMap = statisticMap
    },
    handleDownload() {
      this.downloadLoading = true
        import('@/vendor/Export2Excel').then(excel => {
          const tHeader = this.cur_exams.slice()
          tHeader.push('平均分')
          const filterVal = this.cur_exams
          const data = this.formatJson(filterVal)
          excel.export_json_to_excel({
            header: tHeader,
            data,
            filename: 'users'
          })
          this.downloadLoading = false
        })
    },
    formatJson(filterVal) {
      return this.users.map(v => {
        const line = filterVal.map(j => {
          return v.exams_map[j]
        })
        line.push(this.statisticMap[v['_id']].avg)
        return line
      })
    },
    sortGrade(a, b) {
      const k = this.sortColLabel
      return a.exams_map[k] - b.exams_map[k]
    },
    sortAvgGrade(a, b) {
      return this.statisticMap[a['_id']].avg - this.statisticMap[b['_id']].avg
    },
    handleCellClick(column) {
      this.sortColLabel = column.label
    },
    handleChart(row, type) {
      this.chartConf.chartType = type
      this.chartConf.chartData = this.cur_exams.map(k => row.exams_map[k])
      this.dialogChartVisible = true
    }
  }
}
</script>
