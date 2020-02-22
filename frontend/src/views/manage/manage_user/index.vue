<template>
  <div class="app-container">
    <div class="filter-container">
      <el-form>
        <el-form-item>
          <el-input v-model="data_filter.user_info.username" placeholder="用户名" size="medium" clearable style="max-width: 200px" class="filter-item" @keyup.enter.native="handleFilter" />
          <el-select v-model="data_filter.user_info.role" placeholder="权限" size="medium" clearable class="filter-item">
            <el-option v-for="(v,k) in roleMap" :key="k" :label="v" :value="Number(k)" />
          </el-select>
          <el-select v-model="data_filter.user_info.org" placeholder="机构" size="medium" clearable style="max-width: 200px" @change="data_filter.user_info.sub_org=[]">
            <el-option v-for="v in orgs" :key="v.org_name" :label="v.org_name" :value="v.org_name" />
          </el-select>
          <el-select v-model="data_filter.user_info.sub_org" placeholder="班级" size="medium" multiple clearable style="max-width: 200px">
            <el-option v-for="v in orgs_map[data_filter.user_info.org]" :key="v" :label="v" :value="v" />
          </el-select>
          <el-button v-waves class="filter-item" size="medium" type="primary" round icon="el-icon-search" @click="handleFilter" />
        </el-form-item>
        <el-form-item>
          <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" size="medium" plain icon="el-icon-upload2" @click="handleDownload">导出excel</el-button>
          <el-button v-if="$minRole(3)" type="primary" size="medium" @click="batchSet('dialogQuAuthVisible')">问卷授权</el-button>
          <el-button type="primary" size="medium" @click="batchSet('dialogClassVisible')">机构班级</el-button>
          <el-button v-if="$minRole(3)" type="primary" size="medium" @click="dialogAddUserVisible = true">添加用户</el-button>
          <el-button type="primary" size="medium" plain round @click="manageVisible = !manageVisible">{{ manageVisible ? '折叠' : '展开' }}</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-table
      ref="table"
      :key="tableKey"
      v-loading="listLoading"
      row-key="_id"
      :data="users"
      max-height="1000"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" :reserve-selection="true" align="center" min-width="20" />
      <el-table-column label="用户" prop="username" align="center" min-width="80" fixed>
        <template slot-scope="{row}">
          <span>{{ row.user_info.username }}</span>
        </template>
      </el-table-column>
      <el-table-column label="机构" min-width="100" align="center">
        <template slot-scope="{row}">
          <el-select v-model="row.user_info.org" size="medium" placeholder="无" clearable style="width: 100%" :disabled="!$minRole(100)" @change="setSubOrgsOne(row, true)">
            <el-option v-for="v in orgs" :key="v.org_name" :label="v.org_name" :value="v.org_name" />
          </el-select>
        </template>
      </el-table-column>
      <el-table-column label="班级" min-width="120" align="center">
        <template slot-scope="{row}">
          <el-select v-model="row.user_info.sub_org" size="medium" placeholder="无" multiple clearable style="width: 100%" @change="setSubOrgsOne(row, false)">
            <el-option v-for="v in orgs_map[row.user_info.org]" :key="v" :label="v" :value="v" />
          </el-select>
        </template>
      </el-table-column>
      <el-table-column label="权限" min-width="130" align="center">
        <template slot-scope="{row}">
          <el-select v-model="row.user_info.role" size="medium" placeholder="权限" @change="resetUserInfo([row['_id']], [row.user_info])">
            <el-option v-for="(v,k) in roleMap" :key="k" :label="v" :value="Number(k)" />
          </el-select>
        </template>
      </el-table-column>
      <el-table-column v-if="manageVisible && $minRole(2)" label="个人信息" align="center" min-width="100" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <router-link :to="{path: '/manage/manage_user/set', query: {component: 'personal_info',userid: row['_id']}}">
            <el-button size="mini" type="primary">修改</el-button>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column v-if="manageVisible && $minRole(3)" label="密码重置" align="center" min-width="100" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <router-link :to="{path: '/manage/manage_user/set', query: {component: 'change_password',userid: row['_id']}}">
            <el-button size="mini" type="primary">重置</el-button>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column v-if="manageVisible && $minRole(101)" label="一次授权" align="center" min-width="100" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-checkbox-group v-model="row.user_info.auth" @change="resetUserInfo([row['_id']], [row.user_info])">
            <el-checkbox v-for="item in ['备份', '回滚']" :label="item" :value="item" style="width: 100%" />
          </el-checkbox-group>
        </template>
      </el-table-column>
      <el-table-column v-if="manageVisible && $minRole(4)" label="删除用户" align="center" min-width="100" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-popconfirm title="确认删除用户" @onConfirm="handleDelete(row,$index)">
            <el-button slot="reference" size="mini" type="danger">删除</el-button>
          </el-popconfirm>
        </template>
      </el-table-column>
      <el-table-column v-if="manageVisible" label="综合报告" align="center" min-width="100" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <router-link :to="{path: '/report/general_report', query: { userid: row['_id'] }}">
            <el-button size="mini" type="primary">查看</el-button>
          </router-link>
        </template>

      </el-table-column>
      <el-table-column v-for="qu in qus" :key="qu['_id']" :label="qu.qu_name" align="center" min-width="120" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <span :style="'color:'+(row.qus[qu.qu_id] === undefined ? (row.user_info.role < 100 ? '#909399' : '#F56C6C') : (row.qus[qu.qu_id].qu_report ? '#67C23A' : '#F56C6C'))+';font-weight: bold;'">
            {{ row.qus[qu.qu_id] === undefined ? (row.user_info.role < 100 ? '未授权' : '未完成') : (row.qus[qu.qu_id].qu_report ? '已完成' : '未完成') }}
          </span>
          <span>{{ row.qus[qu.qu_id] ? (row.qus[qu.qu_id].qu_report ? row.qus[qu.qu_id].qu_report.report_preview : null) : null }}</span>
          <br>
          <el-popover placement="bottom" width="200" trigger="click">
            <el-button slot="reference" size="mini">更多</el-button>
            <router-link :to="{path: '/manage/manage_user/set', query: { component: 'qu_do', userid: row['_id'], qu_id: qu.qu_id }}">
              <el-button size="mini">回答</el-button>
            </router-link>
            <router-link :to="{path: '/report/generate_report', query: { userid: row['_id'], qu_id: qu.qu_id}}">
              <el-button size="mini">报告</el-button>
            </router-link>
            <br><br>
            <el-button v-if="$minRole(100)" size="mini" :type="isPaid(row.qus[qu.qu_id]) ? 'success' : 'info'" @click="setUserQuInfo(row, qu.qu_id)">{{ isPaid(row.qus[qu.qu_id]) ? '已付费' : '未付费' }}</el-button>
          </el-popover>
        </template>
      </el-table-column>
    </el-table>

    <!--    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />-->

    <el-dialog title="问卷权限管理" :visible.sync="dialogQuAuthVisible">
      <el-form :model="cur_qus" label-position="left">
        <el-form-item label="选择问卷" prop="type">
          <el-select v-model="cur_qus.qu_ids" multiple class="filter-item" placeholder="选择">
            <el-option v-for="item in qus" :key="item.qu_id" :label="item.qu_name" :value="item.qu_id" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogQuAuthVisible = false">取消</el-button>
        <el-button type="primary" @click="setQuAuth(true)">添加权限</el-button>
        <el-button type="danger" @click="setQuAuth(false)">删除权限</el-button>
      </div>
    </el-dialog>

    <el-dialog title="机构班级重置" :visible.sync="dialogClassVisible">
      <el-form label-position="left">
        <el-form-item label="选择">
          <el-select v-model="cur_org" clearable class="filter-item" placeholder="机构" @change="cur_sub_orgs=[]">
            <el-option v-for="e in orgs" :key="e.org_name" :label="e.org_name" :value="e.org_name" />
          </el-select>
          <el-select v-model="cur_sub_orgs" multiple class="filter-item" placeholder="班级">
            <el-option v-for="e in orgs_map[cur_org]" :key="e" :label="e" :value="e" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogClassVisible = false">取消</el-button>
        <el-button type="primary" @click="setSubOrgs()">重置</el-button>
      </div>
    </el-dialog>

    <el-dialog title="添加用户" :visible.sync="dialogAddUserVisible">
      <el-form label-position="left">
        <el-form-item label="用户名">
          <el-input v-model="cur_add_user.user_info.username" minlength="1" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="cur_add_user.password" label="密码" minlength="6" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogAddUserVisible = false">取消</el-button>
        <el-button type="primary" @click="addUser()">添加</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import waves from '@/directive/waves' // waves directive
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import { getUserList, setUserInfo, setSubOrgs, delUser, setQuAuth, addUser, setUserQuInfo } from '@/api/user'
import { getQuList } from '@/api/questionnair'
import { org_list } from '@/api/organization'

const roleMap = { 1: '学生', 2: '任课老师', 3: '班主任', 4: '机构经理', 5: '机构管理员', 100: '系统管理员', 101: '最高管理员' }

export default {
  name: 'ManageUser',
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      tableKey: 0,
      listQuery: {
        page: 1,
        limit: 100000
      },
      total: 0,
      listLoading: true,
      pickRows: [],
      users: null,
      data_filter: {
        user_info: {}
      },
      roleMap: {},
      qus: [],
      cur_qus: {
        qu_ids: []
      },
      cur_add_user: {
        user_info: {
          username: null
        },
        password: 'aaaaaa'
      },
      manageVisible: true,
      dialogQuVisible: false,
      dialogQuAuthVisible: false,
      dialogClassVisible: false,
      dialogAuthVisible: false,
      dialogAddUserVisible: false,
      downloadLoading: false,
      orgs: [],
      orgs_map: {},
      cur_org: null,
      cur_sub_orgs: []
    }
  },
  created() {
    this.getRoleOptions()
    this.getQus()
    this.getOrgs()
    this.getList()
  },
  methods: {
    handleSelectionChange(rows) {
      this.pickRows = rows
    },
    getList() {
      this.listLoading = true
      getUserList({ 'data_filter': this.data_filter }).then(response => {
        const users = response.data.users.map(e => {
          if (!e.user_info.auth) {
            e.user_info.auth = []
          }
          return e
        })
        this.users = users
        this.total = this.users.length
        this.$refs.table.clearSelection()
      })
      setTimeout(() => {
        this.listLoading = false
      }, 0.3 * 1000)
    },
    getRoleOptions() {
      const role = this.$store.getters.role
      for (const k in roleMap) {
        if (k <= role) {
          this.roleMap[k] = roleMap[k]
        }
      }
    },
    getQus() {
      getQuList().then(response => {
        this.qus = response.list
      })
    },
    getOrgs() {
      org_list().then(response => {
        this.orgs = response.data.orgs
        this.orgs_map = response.data.orgs_map
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    resetUserInfo(userids, user_infos) {
      setUserInfo({ userids: userids, user_infos: user_infos }).then(response => {
        this.$message.success('修改成功')
      })
    },
    handleDelete(row, index) {
      delUser({ 'userids': [row['_id']] }).then(response => {
        this.$notify.success({ title: '删除成功', message: '用户已删除', showClose: false, duration: 1000 })
        this.$refs.table.clearSelection()
        this.users.splice(index, 1)
      })
    },
    setSubOrgs() {
      const data = { userids: this.pickRows.map(r => r['_id']), org: this.cur_org, sub_org: this.cur_sub_orgs }
      setSubOrgs(data).then(response => {
        this.$message.success('修改成功')
        this.getList()
        this.dialogClassVisible = false
      })
    },
    setSubOrgsOne(row, isSetOrg) {
      const data = { userids: [row['_id']], org: row.user_info.org, sub_org: row.user_info.sub_org }
      setSubOrgs(data).then(response => {
        this.$message.success('修改成功')
        if (isSetOrg) {
          row.user_info.sub_org = []
        }
        this.dialogClassVisible = false
      })
    },
    addUser() {
      addUser(this.cur_add_user).then(response => {
        this.$message.success('修改成功')
      })
    },
    setQuAuth(is_add) {
      const data = { userids: this.pickRows.map(r => r['_id']), qu_ids: this.cur_qus.qu_ids, is_add: is_add }
      setQuAuth(data).then(response => {
        this.$message.success('修改成功')
        this.getList()
        this.dialogQuAuthVisible = false
      })
    },
    isPaid(qu) {
      return qu && qu.info && qu.info.auth && qu.info.auth === 2
    },
    setUserQuInfo(row, qu_id) {
      if (!row.qus[qu_id]) {
        row.qus[qu_id] = {}
      }
      const info = row.qus[qu_id].info || {}
      if (info.auth === 2) {
        info.auth = 1
      } else {
        info.auth = 2
      }
      setUserQuInfo({ userid: row['_id'], qu_id: qu_id, info: info }).then(response => {
        this.$message.success('修改成功')
        this.getList()
      })
    },
    batchSet(name) {
      if (this.pickRows.length === 0) {
        this.$message.warning('请先勾选用户')
      } else {
        this[name] = true
      }
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['用户名', '机构', '班级', '权限']
        const filterVal = ['username', 'org', 'sub_org', 'role']
        const data = this.formatJson(filterVal)
        alert(JSON.stringify(data))
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'users'
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal) {
      return this.users.map(v => filterVal.map(j => {
        if (j === 'role') {
          return this.roleMap[v.user_info[j]]
        } else {
          return v.user_info[j]
        }
      }))
    }
  }
}
</script>
