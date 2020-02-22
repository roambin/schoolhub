<template>
  <div class="app-container">
    {{ org }}
<!--    <component :is="currentRole" />-->
  </div>
</template>

<script>
import { getInfo } from '@/api/user'
export default {
  name: 'Home',
  data() {
    return {
      loading: false,
      org: null,
      currentRole: 'adminDashboard'
    }
  },
  created() {
    getInfo().then(response => {
      this.org = response.data.user_info.org
    })
  },
  methods: {

  }
}
</script>
