<template>
  <router-view></router-view>
</template>

<script>
export default {
  methods: {
    initializeLayout() {
    }
  },
  computed: {
      session () {
        return this.$store.state.session
      }
  },
  mounted() {
    this.initializeLayout();
  }
};
</script>
