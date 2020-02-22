<template>
  <div class="app-container">
    <el-card v-if="!qu.qu_report" class="box-card">
      <span>暂无报告</span>
    </el-card>
    <div id="printTest">
      <div v-if="qu.qu_report">
        <div>
          <span v-if="user_info.org" style="margin-right: 40px">{{ '机构：' + user_info.org }}</span>
          <span v-if="user_info.sub_org.length > 0" style="margin-right: 40px">{{ '班级：' + user_info.sub_org }}</span>
          <span v-if="user_info.username" style="margin-right: 40px">{{ '姓名：' + user_info.username }}</span>
        </div><br>
        <el-divider />
        <span style="font-size: 40px;color: rgba(27,97,169,0.91)">你的MBTI人格为：{{ qu.qu_report.report_data.type }}</span><br><br>
        <div v-if="print" style="font-size: 20px;color: rgba(27,97,169,0.91)">
          <span style="margin-right: 40px">外倾E : {{ count['E'] }}，内倾I : {{ count['I'] }}</span>
          <br>
          <span style="margin-right: 40px">实感S : {{ count['S'] }}，直觉N : {{ count['N'] }}</span>
          <br>
          <span style="margin-right: 40px">思维T : {{ count['T'] }}，情感F : {{ count['F'] }}</span>
          <br>
          <span style="margin-right: 40px">判断J : {{ count['J'] }}，知觉P : {{ count['P'] }}</span>
          <br>
        </div>
        <div v-if="!print">
          <br>
          <el-row>
            <el-col :span="4" style="text-align: center">E ({{ count['E'] }})</el-col>
            <el-col :span="16"><el-progress :show-text="false" :stroke-width="26" :percentage="100*count['E']/(count['E'] + count['I'])" /></el-col>
            <el-col :span="4" style="text-align: center">I ({{ count['I'] }})</el-col>
          </el-row><br>
          <el-row>
            <el-col :span="4" style="text-align: center">S ({{ count['S'] }})</el-col>
            <el-col :span="16"><el-progress :show-text="false" :stroke-width="26" :percentage="100*count['S']/(count['S'] + count['N'])" /></el-col>
            <el-col :span="4" style="text-align: center">N ({{ count['N'] }})</el-col>
          </el-row><br>
          <el-row>
            <el-col :span="4" style="text-align: center">T ({{ count['T'] }})</el-col>
            <el-col :span="16"><el-progress :show-text="false" :stroke-width="26" :percentage="100*count['T']/(count['T'] + count['F'])" /></el-col>
            <el-col :span="4" style="text-align: center">F ({{ count['F'] }})</el-col>
          </el-row><br>
          <el-row>
            <el-col :span="4" style="text-align: center">J ({{ count['J'] }})</el-col>
            <el-col :span="16"><el-progress :show-text="false" :stroke-width="26" :percentage="100*count['J']/(count['J'] + count['P'])" /></el-col>
            <el-col :span="4" style="text-align: center">P ({{ count['P'] }})</el-col>
          </el-row><br>
        </div>
        <div class="editor-content" v-html="report_text" /><br>
      </div>
    </div>
    <br><br>
    <!--    <el-button v-if="$minRole(100) || qu.info.auth === 2" v-print="'#printTest'" type="primary" @click="ExportSavePdf(user_info.username,'的报告')">下载报告</el-button>-->
    <el-button v-if="$minRole(100) || qu.info.auth === 2" @click="doPrint3">下载报告</el-button>
    <el-button v-if="!$minRole(100) && qu.info.auth !== 2" @click="getFullReport">解锁完整报告</el-button>
    <el-dialog title="获得完整报告" :visible.sync="dialogFullReportVisible">
      <span>扫码付款后解锁完整报告</span><br><br>
      <el-image :src="base_url + '/showFilesCustom?filename=public/pay_pic'" fit="fill" />
    </el-dialog>
  </div>
</template>

<script>

import { getUserQu, downloadReport, getUserInfo, getReportText } from '@/api/user'
import { saveAs } from 'file-saver'
import { getToken } from '@/utils/auth'

export default {
  name: 'ReportMbti',
  data() {
    return {
      userid: this.$route.query.userid,
      qu_id: this.$route.query.qu_id,
      qu: null,
      count: null,
      dialogFullReportVisible: false,
      user_info: {},
      report_text: null,
      base_url: process.env.VUE_APP_BASE_API,
      token: getToken(),
      print: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      getUserQu({ userid: this.userid, qu_id: this.qu_id }).then(response => {
        if (response.data) {
          this.qu = response.data.qu || {}
          this.count = this.qu.qu_report.report_data.count

          getReportText({ qu_id: this.qu_id, download_info: { type: this.qu.qu_report.report_data.type }}).then(response => {
            this.report_text = response.data
          })
        }
      })
      getUserInfo({ userid: this.userid }).then(response => {
        this.user_info = response.data.user_info
      })
    },
    getFullReport() {
      this.dialogFullReportVisible = true
    },
    download_report() {
      downloadReport({ qu_id: this.qu_id, download_info: { type: this.qu.qu_report.report_data.type }}).then(response => {
        if (response.code === 40002) {
          this.$message.error({ message: '没有权限', duration: 1000 })
        } else {
          const blob = new Blob([response.data], { type: response.headers['content-type'] })
          saveAs(blob, this.qu.qu_report.report_data.type + '.pdf')
        }
      })
    },
    doPrint3() {
      this.print = true
      // 判断iframe是否存在，不存在则创建iframe
      var iframe = document.getElementById('print-iframe')
      if (!iframe) {
        var el = document.getElementById('printTest')
        iframe = document.createElement('IFRAME')
        var doc = null
        iframe.setAttribute('id', 'print-iframe')
        iframe.setAttribute('style', 'position:absolute;width:0px;height:0px;left:-500px;top:-500px;')
        document.body.appendChild(iframe)
        doc = iframe.contentWindow.document
        // 这里可以自定义样式
        // doc.write("<LINK rel="stylesheet" type="text/css" href="css/print.css">");
        doc.write('<div>' + el.innerHTML + '</div>')
        doc.close()
        iframe.contentWindow.focus()
      }
      iframe.contentWindow.print()
      if (navigator.userAgent.indexOf('MSIE') > 0) {
        document.body.removeChild(iframe)
      }
      this.print = false
    }
  }
}
</script>
