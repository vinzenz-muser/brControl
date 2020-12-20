<template>
  <router-view></router-view>
</template>

<script>
export default {
  methods: {
    initializeLayout() {
      if (!this.$rtl.isRTL) {
        // Just make sure rtl css is off when we are not on rtl
        this.$rtl.disableRTL();
      }
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
