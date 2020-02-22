<template>
  <div class="app-container">
    <report-mbti v-if="qu_id==='5e495cc421a85ca33b638d94'" />
    <el-card v-else>
      <span>暂无报告</span>
    </el-card>
  </div>
</template>

<script>
import ReportMbti from './component/report_mbti'

export default {
  name: 'GenerateReport',
  components: { ReportMbti },
  data() {
    return {
      userid: this.$route.query.userid,
      qu_id: this.$route.query.qu_id
    }
  },
  created() {
  }
}
</script>
