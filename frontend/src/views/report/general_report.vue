<template>
  <div class="app-container">
    <el-card>
      <span>暂无报告</span>
    </el-card>
  </div>
</template>

<script>
import ReportMbti from './generate_report/component/report_mbti'

export default {
  name: 'GeneralReport',
  components: { ReportMbti },
  data() {
    return {
      userid: this.$route.query.userid
    }
  },
  created() {
  }
}
</script>
