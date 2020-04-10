<template>
  <div id="app">
    <NavBar/>
    <ChannelList/>
    <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import NavBar from './components/NavBar.vue'
import ChannelList from './components/ChannelList.vue'
export default {
  name: 'App',
  components: {
    // HelloWorld,
    NavBar,
    ChannelList
  }
}
</script>

<style>
/* #app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
} */
</style>
