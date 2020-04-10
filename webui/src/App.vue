<template>
  <div id="app">
    <NavBar />
    <ChannelList />
    <hr class="my-4">
    <VoDList />
  </div>
</template>

<script>
// import VoDList from './components/VoDList.vue'
import NavBar from "./components/NavBar.vue";
import ChannelList from "./components/ChannelList.vue";
import VoDList from "./components/VoDList.vue";

export default {
  name: "App",
  components: {
    VoDList,
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
