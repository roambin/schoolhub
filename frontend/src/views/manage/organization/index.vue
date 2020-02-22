<template>
  <div class="app-container">
    <el-button v-if="$minRole(100)" type="primary" @click="handleCreate()">添加+</el-button>
    <el-button type="primary" size="medium" plain round @click="manageVisible = !manageVisible">{{ manageVisible ? '折叠' : '展开' }}</el-button>
    <br><br>
    <el-table :key="tableKey" :data="orgs" border fit highlight-current-row style="width: 100%;">
      <el-table-column label="机构名" prop="org_name" align="left" min-width="100" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-input v-model="row.org_name" size="mini" /><br><br>
          <el-button size="mini" type="primary" @click="setOrg(row)">修改</el-button>
        </template>
      </el-table-column>
      <el-table-column label="班级管理" align="center" min-width="150" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <div v-for="(v,k) in row.sub_orgs" :key="k" style="text-align: left">
            <el-input v-model="row.sub_orgs[k]" size="mini" style="max-width: 70%" />
            <el-button size="mini" type="danger" plain circle @click="row.sub_orgs.pop(k)">-</el-button>
          </div>
          <div style="text-align: left">
            <el-button size="mini" type="primary" plain circle @click="row.sub_orgs.push('')">+</el-button>
            <br><br>
            <el-button size="mini" type="primary" @click="setOrg(row)">修改</el-button>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="试卷" align="center" min-width="150" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <div v-for="(v,k) in row.subjects" :key="'subject'+k" style="text-align: left">
            <span v-if="!manageVisible">科目</span>
            <el-input v-if="!manageVisible" v-model="row.subjects[k].subject_name" size="mini" style="max-width: 70%" />
            <el-button v-if="!manageVisible" size="mini" type="danger" plain circle @click="row.subjects.pop(k)">-</el-button>

            <el-card v-if="manageVisible" class="box-card" body-style="padding:10px">
              <div slot="header" class="clearfix">
                <span>科目</span>
                <el-input v-model="row.subjects[k].subject_name" size="mini" style="max-width: 70%" />
                <el-button size="mini" type="danger" plain circle @click="row.subjects.pop(k)">-</el-button>
              </div>
              <div>
                <div><span>试卷</span></div>
                <div v-for="(v1,k1) in row.subjects[k].exams" :key="'exam'+k1" style="text-align: left">
                  <el-input v-model="row.subjects[k].exams[k1]" size="mini" style="max-width: 70%" />
                  <el-button size="mini" type="danger" plain circle @click="row.subjects[k].exams.pop(k1)">-</el-button>
                </div>
                <el-button size="mini" type="primary" plain circle @click="row.subjects[k].exams.push('')">+</el-button>
              </div>
            </el-card><br>
          </div>
          <div style="text-align: left">
            <el-button size="mini" type="primary" plain circle @click="row.subjects.push({'subject_name': '', 'exams': []})">+</el-button>
            <br><br>
            <el-button size="mini" type="primary" @click="setOrg(row)">修改</el-button>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="表格" align="center" min-width="150" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <div v-for="(v,k) in row.table_infos" :key="'table_info'+k" style="text-align: left">
            <span v-if="!manageVisible">表格</span>
            <el-input v-if="!manageVisible" v-model="row.table_infos[k].table_name" size="mini" style="max-width: 70%" />
            <el-button v-if="!manageVisible" size="mini" type="danger" plain circle @click="row.table_infos.pop(k)">-</el-button>

            <el-card v-if="manageVisible" class="box-card" body-style="padding:10px">
              <div slot="header" class="clearfix">
                <span>表格</span>
                <el-input v-model="row.table_infos[k].table_name" size="mini" style="max-width: 70%" />
                <el-button size="mini" type="danger" plain circle @click="row.table_infos.pop(k)">-</el-button>
              </div>
              <div>
                <div><span>列</span></div>
                <div v-for="(v1,k1) in row.table_infos[k].table_items" :key="'table_items'+k1" style="text-align: left">
                  <el-input v-model="row.table_infos[k].table_items[k1].item_name" placeholder="名称" size="mini" style="max-width: 70%" />
                  <el-select v-model="row.table_infos[k].table_items[k1].item_type" placeholder="类型" size="mini">
                    <el-option label="值" value="txt" />
                    <el-option label="文件" value="file" />
                  </el-select>
                  <el-button size="mini" type="danger" plain circle @click="row.table_infos[k].table_items.pop(k1)">-</el-button><br><br>
                </div>
                <el-button size="mini" type="primary" plain circle @click="row.table_infos[k].table_items.push({'item_name': '', 'item_type': 'txt'})">+</el-button>
              </div>
            </el-card><br>
          </div>
          <div style="text-align: left">
            <el-button size="mini" type="primary" plain circle @click="row.table_infos.push({'table_name': '', 'table_items': []})">+</el-button>
            <br><br>
            <el-button size="mini" type="primary" @click="setOrg(row)">修改</el-button>
          </div>
        </template>
      </el-table-column>
      <el-table-column v-if="false" label="机构问卷" align="center" min-width="100" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button size="mini" type="primary" @click="handleQuAuth(row)">编辑</el-button>
        </template>
      </el-table-column>
      <el-table-column v-if="$minRole(100)" label="删除机构" align="center" min-width="100" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button size="mini" type="danger" @click="handleDelete(row,$index)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="问卷权限管理" :visible.sync="dialogQuAuthVisible">
      <el-checkbox-group v-model="cur_org.qus">
        <el-checkbox v-for="e in qus" :key="e.qu_id" :label="e.qu_name" :value="e.qu_id" style="width: 100%" />
      </el-checkbox-group>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogQuAuthVisible = false">取消</el-button>
        <el-button type="primary" @click="setOrg(cur_org)">修改</el-button>
      </div>
    </el-dialog>

    <el-dialog title="添加机构" :visible.sync="dialogOrgVisible">
      <el-form>
        <el-form-item label="名称">
          <el-input v-model="cur_org.org_name" />
        </el-form-item>
        <el-form-item v-if="false" label="授权问卷">
          <el-checkbox-group v-model="cur_org.qus">
            <el-checkbox v-for="e in qus" :key="e.qu_id" :label="e.qu_name" :value="e.qu_id" style="width: 100%" />
          </el-checkbox-group>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogOrgVisible = false">取消</el-button>
        <el-button type="primary" @click="addOrg">添加</el-button>
      </div>
    </el-dialog>

    <el-dialog title="班级管理" :visible.sync="dialogClassesVisible">
      <manage-classes />
    </el-dialog>

  </div>
</template>

<script>
import waves from '@/directive/waves' // waves directive
import { org_list, org_add, org_set, org_del } from '@/api/organization'
import { getQuList } from '@/api/questionnair'

export default {
  name: 'ManageQu',
  directives: { waves },
  data() {
    return {
      tableKey: 0,
      orgs: [],
      qus: [],
      cur_org: {},
      cur_sub_org: '',
      dialogQuAuthVisible: false,
      dialogOrgVisible: false,
      dialogClassesVisible: false,
      manageVisible: true
    }
  },
  created() {
    this.getList()
    this.getQus()
  },
  methods: {
    getList() {
      org_list().then(response => {
        this.orgs = response.data.orgs.map(e => {
          if (!e.table_infos) {
            e.table_infos = []
          }
          return e
        })
      })
    },
    getQus() {
      getQuList().then(response => {
        this.qus = response.list
      })
    },
    handleDelete(row, index) {
      org_del({ 'org_id': row['_id'] }).then(response => {
        this.$message.success('操作成功')
        this.orgs.splice(index, 1)
      })
    },
    addOrg() {
      org_add({ 'org': this.cur_org }).then(response => {
        if (response.msg) {
          this.$message.error(response.msg)
        } else {
          this.$message.success('操作成功')
          this.getList()
        }
      })
    },
    handleQuAuth(row) {
      this.cur_org = row
      this.dialogQuAuthVisible = true
    },
    handleCreate(row) {
      this.cur_org = { qus: [], sub_orgs: [], subjects: [] }
      this.dialogOrgVisible = true
    },
    setOrg(org) {
      org_set({ 'org_id': org['_id'], 'org': org }).then(response => {
        this.$message.success('操作成功')
      })
    }
  }
}
</script>
