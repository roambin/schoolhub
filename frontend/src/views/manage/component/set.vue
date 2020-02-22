<template>
  <div class="app-container">
    <qu-do v-if="component === 'qu_do'"/>
    <personal-info v-if="component === 'personal_info'"/>
    <change-password v-if="component === 'change_password'"/>
  </div>
</template>

<script>
import QuDo from '@/views/questionnair/questionnair_do/qu_do.vue'
import PersonalInfo from '@/views/personal/personal_info/index.vue'
import ChangePassword from '@/views/personal/change_password/index.vue'

export default {
  components: { QuDo, PersonalInfo, ChangePassword },
  data() {
    return {
      component: this.$route.query.component
    }
  }
}
</script>
