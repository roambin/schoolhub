<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from './mixins/resize'

const animationDuration = 1500
const chartData = [100, 120, 161, 134, 105, 160, 165]
const chartLabel = ['a', 'b', 'c']

export default {
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '350px'
    },
    autoResize: {
      type: Boolean,
      default: true
    },
    chartData: {
      type: Object,
      default: chartData
    },
    chartLabel: {
      type: Array,
      default: chartLabel
    },
    chartType: {
      type: String,
      default: 'line'
    }
  },
  data() {
    return {
      chart: null
    }
  },
  watch: {
    chartData: {
      deep: true,
      handler(val) {
        this.setOptions(val)
      }
    },
    chartLabel: {
      deep: true,
      handler(val) {
        this.setOptions(val)
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart()
    })
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$el, 'macarons')
      this.setOptions({ chartData: this.chartData, chartLabel: this.chartLabel, chartType: this.chartType })
    },
    setOptions({ chartData, chartLabel, chartType } = {}) {
      this.chart.setOption({
        xAxis: {
          data: chartLabel,
          boundaryGap: true,
          axisTick: {
            show: false
          }
        },
        grid: {
          top: 50,
          left: '2%',
          right: '2%',
          bottom: '3%',
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          },
          padding: [5, 10]
        },
        yAxis: {
          axisTick: {
            show: false
          }
        },
        legend: {
          data: ['分数']
        },
        series: [{
          name: '分数',
          smooth: true,
          type: chartType,
          label: {
            show: true,
            position: 'top'
          },
          itemStyle: {
            normal: {
              color: '#FF005A',
              lineStyle: {
                color: '#FF005A',
                width: 2
              }
              // areaStyle: {
              //   color: '#f3f8ff'
              // }
            }
          },
          data: chartData,
          animationDuration: animationDuration,
          animationEasing: 'cubicInOut'
        }]
      })
    }
  }
}
</script>
