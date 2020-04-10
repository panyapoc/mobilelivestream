<template>
  <div id="ChannelList">
    <h1>Video Ondemand</h1>
    <b-table :items="items" :fields="fields" :sort-by.sync="sortBy" :sort-desc.sync="sortDesc" responsive="sm">
      <template v-slot:cell(VoDEndpoint)="data">
        <b-button :href="data.value" variant="success">Play <b-icon icon="play-fill"></b-icon></b-button>
      </template>
      <template v-slot:cell(StartTime)="data">
        <span>{{ timeConverter(data.value) }}</span>
      </template>
      <template v-slot:cell(EndTime)="data">
        <span>{{ timeConverter(data.value) }}</span>
      </template>
    </b-table>
    <div>
      <!-- Sorting By: <b>{{ sortBy }}</b>, Sort Direction: -->
      <!-- <b>{{ sortDesc ? 'Descending' : 'Ascending' }}</b> -->
    </div>
  </div>
</template>

<script>
import axios from "axios";

const rootapi = process.env.VUE_APP_AWS_APIGATEWAY_ENDPOINT

console.log(rootapi)

export default {
  data() {
    return {
      sortBy: "STATE",
      sortDesc: false,
      fields: [
        { key: "VoDID", sortable: true , label: "VOD ID"},
        { key: "ChannelId", sortable: true, label: "ChannelId"},
        { key: "StartTime", sortable: true, label: "Start Time"},
        { key: "EndTime", sortable: true, label: "End Time"},
        { key: "VoDEndpoint", sortable: false, label: "Player"}
      ],
      items: []
    };
  },
  created() {
    axios
      .get(`${rootapi}/vod`)
      .then(response => {
        // JSON responses are automatically parsed.


        let channels = response.data


        // channels.forEach((channel,index) => {
        //     channels[index]['Player']=
        // });

        console.table(channels)
        this.items = channels;
      })
      .catch(e => {
        this.errors.push(e);
      });

    // async / await version (created() becomes async created())
    //
    // try {
    //   const response = await axios.get(`http://jsonplaceholder.typicode.com/posts`)
    //   this.posts = response.data
    // } catch (e) {
    //   this.errors.push(e)
    // }
  },
  methods: {
    timeConverter(UNIX_timestamp){
      if(!UNIX_timestamp)
        return "Stream Still RUNNING"
      else{
        var a = new Date(UNIX_timestamp * 1000);
        return a.toLocaleDateString() + ' ' + a.toLocaleTimeString()
      }

      // var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
      // var year = a.getFullYear();
      // var month = a.getMonth()
      // var date = a.getDate();
      // var hour = a.getHours();
      // var min = a.getMinutes();
      // var sec = a.getSeconds();
      // var time = `${date}/${month}/${year} ${hour}:${min}:${sec}`;
      // return time;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#ChannelList {
  /* font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50; */
  max-width: 75rem;
  margin: 50px auto auto auto;
}
h1 {
    margin-bottom: 20px;
}
</style>
