<template>
  <div class="app-container">
    <div class="filter-container">
      <el-form>
        <el-form-item>
          <el-select v-model="cur_table_name" placeholder="表格" size="medium" style="max-width: 200px" @change="handleSel">
            <el-option v-for="v in table_infos" :key="v.table_name" :label="v.table_name" :value="v.table_name" />
          </el-select>
          <el-button v-if="$minRole(3)" type="primary" size="medium" @click="userSetSel">保存修改</el-button>
          <el-button v-if="$minRole(3)" v-waves class="filter-item" size="medium" type="danger" @click="handleDelete">清空</el-button>
          <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" size="medium" plain icon="el-icon-upload2" @click="handleDownload">导出excel</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-table ref="table" v-loading="listLoading" :data="cur_table_data" max-height="1000" border fit highlight-current-row style="width: 100%;">
      <el-table-column v-for="(v, k) in table_infos_map[cur_table_name]" :key="k" :label="v.item_name" align="center" min-width="80" class-name="small-padding fixed-width">
        <template slot-scope="{row, $index}">
          <el-input v-if="v.item_type==='txt'" v-model="row[v.item_name]" size="mini" />
          <div v-if="v.item_type==='file'">
            <el-image :src="base_url + '/showFiles?token=' + token + '&userid=' + userid + '&filename=' + row[v.item_name]" fit="contain">
              <div slot="error" class="image-slot">
                <i class="el-icon-picture-outline" />
              </div>
            </el-image>
            <br>
            <el-button v-if="$minRole(3)" type="primary" size="mini" @click="handleUpload(row, v, $index)">上传</el-button>
          </div>
        </template>
      </el-table-column>
      <el-table-column v-if="$minRole(3)" label="管理" align="center" min-width="80" class-name="small-padding fixed-width">
        <template slot-scope="{$index}">
          <el-button type="danger" size="mini" round plain @click="cur_table_data.splice($index, 1)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-button v-if="$minRole(3)" type="primary" size="medium" round plain @click="handleAdd">+</el-button>

    <el-dialog title="上传" :visible.sync="dialogUploadVisible" :show-close="false">
      <el-upload
        class="upload-demo"
        drag
        :action="base_url + '/uploadFiles?token=' + token"
        :data="{filename: filename, userid: userid}"
        :show-file-list="false"
        :on-success="handleAvatarSuccess"
        :before-upload="beforeAvatarUpload"
        multiple
      >
        <i class="el-icon-upload" />
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button @click="handleCancel()">取消</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import waves from '@/directive/waves' // waves directive
import { userGetSel, userSetSel } from '@/api/user'
import { org_list } from '@/api/organization'
import { getToken } from '@/utils/auth'

export default {
  name: 'UserDataPersonal',
  directives: { waves },
  data() {
    return {
      base_url: process.env.VUE_APP_BASE_API,
      token: getToken(),
      listLoading: true,
      downloadLoading: false,
      table_infos: [],
      table_infos_map: {},
      userid: this.$route.query.userid,
      user: null,
      cur_table_name: null,
      cur_table_data: [],
      filename: null,
      cur_index: { index: null, label: null },
      tmp_url: null,
      dialogUploadVisible: false
    }
  },
  created() {
    this.getOrgs()
    this.getList()
  },
  methods: {
    handleAvatarSuccess(res, file) {
      this.cur_table_data[this.cur_index.index][this.cur_index.label] = null
      this.$message.success({ message: '修改成功', duration: 1000 })
    },
    beforeAvatarUpload(file) {
      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isLt2M) {
        this.$message.error('上传文件大小不能超过 2MB!')
      }
      return isLt2M
    },
    handleUpload(row, v, index) {
      if (!row[v.item_name]) {
        row[v.item_name] = this.$guid()
      }
      const data_set = {}
      data_set['user_data.table_datas.' + this.cur_table_name] = this.cur_table_data
      userSetSel({ 'userids': [this.userid], 'data_set': [data_set] }).then(response => {
        this.filename = row[v.item_name]
        this.cur_index.index = index
        this.cur_index.label = v.item_name
        this.tmp_url = this.cur_table_data[this.cur_index.index][this.cur_index.label]
        this.dialogUploadVisible = true
      })
    },
    handleCancel() {
      this.cur_table_data[this.cur_index.index][this.cur_index.label] = this.tmp_url
      this.dialogUploadVisible = false
    },
    getList() {
      userGetSel({ 'userid': this.userid, 'data_sel': { '_id': 0, 'user_info': 1, 'user_data.table_datas': 1 }}).then(response => {
        const user = response.data.user
        if (!user.user_data) {
          user.user_data = {}
        }
        if (!user.user_data.table_datas) {
          user.user_data.table_datas = {}
        }
        this.user = user
      })
      setTimeout(() => {
        this.listLoading = false
      }, 0.3 * 1000)
    },
    getOrgs() {
      org_list().then(response => {
        const orgs = response.data.orgs
        const org_name = this.$route.query.org_name
        for (const i in orgs) {
          if (orgs[i].org_name === org_name) {
            this.table_infos = orgs[i].table_infos
            const table_infos_map = {}
            for (const j in this.table_infos) {
              const table_info = this.table_infos[j]
              table_infos_map[table_info.table_name] = table_info.table_items
            }
            this.table_infos_map = table_infos_map
          }
        }
      })
    },
    userSetSel() {
      const data_set = {}
      data_set['user_data.table_datas.' + this.cur_table_name] = this.cur_table_data
      userSetSel({ 'userids': [this.userid], 'data_set': [data_set] }).then(response => {
        this.$message.success({ message: '修改成功', duration: 1000 })
      })
    },
    handleSel() {
      this.cur_table_data = this.user.user_data.table_datas[this.cur_table_name] || []
    },
    handleAdd() {
      if (!this.cur_table_name) {
        this.$message.warning({ message: '请选择表格', duration: 1000 })
        return
      }
      const line = {}
      const items = this.table_infos_map[this.cur_table_name]
      for (const i in items) {
        line[items[i].item_name] = null
      }
      this.cur_table_data.push(line)
    },
    handleDelete() {
      this.cur_table_data = []
    },
    handleDownload() {
      this.downloadLoading = true
        import('@/vendor/Export2Excel').then(excel => {
          const tHeader = []
          const infos = this.table_infos_map[this.cur_table_name]
          for (const i in infos) {
            if (infos[i].item_type !== 'file') {
              tHeader.push(infos[i].item_name)
            }
          }
          const data = this.formatJson(tHeader)
          excel.export_json_to_excel({
            header: tHeader,
            data,
            filename: this.cur_table_name
          })
          this.downloadLoading = false
        })
    },
    formatJson(filterVal) {
      return this.cur_table_data.map(v => filterVal.map(j => {
        return v[j]
      }))
    }
  }
}
</script>
