<template>
  <div id="app">
    <NavBar />
      <b-alert
      :show="dismissCountDown"
      dismissible
      :variant="alertType"
      @dismissed="dismissCountDown=0"
      @dismiss-count-down="countDownChanged"
    >
      {{ alertMsg }}
    </b-alert>
    <!-- <b-button @click="onShowAlert" variant="info" class="m-1">
      Show alert with count-down timer
    </b-button> -->
    <ChannelList v-on:showAlert="onShowAlert"/>
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
  },
  data() {
    return {
      dismissSecs: 5,
      alertType : 'green',
      alertMsg : 'Test',
      dismissCountDown: 0
    }
  },
  methods: {
    countDownChanged: function (dismissCountDown) {
      this.dismissCountDown = dismissCountDown
    },
    onShowAlert: function (alertMsg,alertType) {
      this.alertMsg = alertMsg
      this.alertType = alertType
      this.dismissCountDown = this.dismissSecs
    }
  }
}
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


.table td{
  vertical-align: middle !important;
}
</style>
