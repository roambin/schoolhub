<template>
  <div class="app-container">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>备份与恢复</span>
        <el-button type="primary" size="medium" @click="backup_dump()">新增备份</el-button>
      </div>
      <el-table v-loading="listLoading" :data="backup.dumps" border fit highlight-current-row style="width: 100%;">
        <el-table-column label="时间" align="center">
          <template slot-scope="{row}">
            <span>{{ row.replace(/_/g, ' ').replace(/\./g, ':') }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="{row, $index}">
            <el-button type="warning" size="medium" @click="backup_restore(row)">回滚</el-button>
            <el-button type="danger" size="medium" @click="backup_delete(row, $index)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <br><br>
    <pay-pic />
  </div>
</template>

<script>
import { backup_list, backup_delete, backup_dump, backup_restore } from '@/api/system'
import PayPic from './pay_pic';
export default {
  name: 'System',
  components: {PayPic},
  data() {
    return {
      listLoading: false,
      backup: {
        dumps: []
      }
    }
  },
  created() {
    this.backup_list()
  },
  methods: {
    backup_list() {
      this.listLoading = true
      backup_list().then(response => {
        this.backup.dumps = response.data.dumps
        this.listLoading = false
      })
    },
    backup_delete(row, index) {
      this.listLoading = true
      backup_delete({ dump_name: row }).then(response => {
        if (response.msg) {
          this.$message.error(response.msg)
        } else {
          this.backup.dumps.splice(index, 1)
          this.$message.success('操作成功')
        }
        this.listLoading = false
      })
    },
    backup_dump() {
      this.listLoading = true
      backup_dump().then(response => {
        if (response.msg) {
          this.$message.error(response.msg)
        } else {
          this.$message.success('操作成功')
        }
        this.backup_list()
        this.listLoading = false
      })
    },
    backup_restore(row) {
      this.listLoading = true
      backup_restore({ dump_name: row }).then(response => {
        if (response.msg) {
          this.$message.error(response.msg)
        } else {
          this.$message.success('操作成功')
        }
        this.listLoading = false
      })
    }
  }
}
</script>
