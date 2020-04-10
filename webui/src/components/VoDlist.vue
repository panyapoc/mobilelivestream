<template>
  <div id="ChannelList">
    <b-row>
      <b-col align-v="start" class="text-left"><h1>Video On-Demand</h1></b-col>
    </b-row>
    <b-table
      :items="items"
      :fields="fields"
      :sort-by.sync="sortBy"
      :sort-desc.sync="sortDesc"
      responsive="sm"
      borderless="borderless"
      v-if="items.length !=0"
    >
      <template v-slot:cell(VoDEndpoint)="data">
        <b-button :href="data.value" variant="primary"
          ><b-icon icon="play-fill"></b-icon
        ></b-button>
      </template>
      <template v-slot:cell(StartTime)="data">
        <span>{{ timeConverter(data.value) }}</span>
      </template>
      <template v-slot:cell(EndTime)="data">
        <span>{{ timeConverter(data.value) }}</span>
      </template>
    </b-table>
    <div v-else>
      No VOD avalible, please finish Streamming first.
    </div>
  </div>
</template>

<script>
const rootapi = process.env.VUE_APP_AWS_APIGATEWAY_ENDPOINT;

console.log(rootapi);

export default {
  data() {
    return {
      sortBy: "STATE",
      sortDesc: false,
      fields: [
        { key: "VoDID", sortable: true, label: "VOD ID" },
        { key: "ChannelId", sortable: true, label: "ChannelId" },
        { key: "StartTime", sortable: true, label: "Start Time" },
        { key: "EndTime", sortable: true, label: "End Time" },
        { key: "VoDEndpoint", sortable: false, label: "Player" }
      ],
      items: []
    };
  },
  created() {
    this.$http
      .get(`${rootapi}/vod`)
      .then(response => {
        // JSON responses are automatically parsed.

        let channels = response.data;

        // channels.forEach((channel,index) => {
        //     channels[index]['Player']=
        // });

        console.table(channels);
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
    timeConverter(UNIX_timestamp) {
      if (!UNIX_timestamp) return "Stream Still RUNNING";
      else {
        var a = new Date(UNIX_timestamp * 1000);
        return a.toLocaleDateString() + " " + a.toLocaleTimeString();
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
