<template>
  <div id="app">
    <NavBar />
    <ChannelList />
    <VoDList />
  </div>
</template>

<script>
// import VoDList from './components/VoDList.vue'
import NavBar from "./components/NavBar.vue";
import ChannelList from "./components/ChannelList.vue";
export default {
  name: "App",
  components: {
    // VoDList,
    NavBar,
    ChannelList
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
}
</style>
