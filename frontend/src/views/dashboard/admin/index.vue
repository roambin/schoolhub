<template>
  <div class="dashboard-editor-container">
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <line-chart :chart-data="data"/>
    </el-row>
  </div>
</template>

<script>
import LineChart from '@/components/Charts/LineChart'
import RaddarChart from '@/components/Charts/RaddarChart'
import PieChart from '@/components/Charts/PieChart'
import BarChart from '@/components/Charts/BarChart'

export default {
  name: 'DashboardAdmin',
  components: {
    LineChart,
    RaddarChart,
    PieChart,
    BarChart
  },
  data() {
    return {
      data: [1, 2]
    }
  }
}
</script>
