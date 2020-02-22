<template>
  <div class="root-container">
    loading...<i class="el-icon-loading" />
  </div>
</template>

<script>
export default {
  name: 'Root',
  created() {
    const role = this.$store.getters.role
    if (role > 1) {
      this.$router.push('/manage/home')
    } else {
      this.$router.push('/questionnair')
    }
  }
}
</script>
