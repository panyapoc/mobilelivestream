<template>
  <div id="ChannelList">
    <h1>Live Channel</h1>
    <b-table
      :items="items"
      :fields="fields"
      :sort-by.sync="sortBy"
      :sort-desc.sync="sortDesc"
      responsive="sm"
    >
      <template v-slot:cell(StartChannel)="data">
        <div>
          <b-button :disabled="data.item.State == STREAMRUNNING" variant="success" @click="startChannel()">Start <b-icon icon="play-fill"></b-icon></b-button>
        </div>
      </template>
      <template v-slot:cell(RTMPEndpoint)="data">
        <div>
          <b-button-group>
          <b-button
            v-b-tooltip.hover
            :title="data.value"
            v-clipboard:copy="data.value"
            v-clipboard:success="onCopy"
            v-clipboard:error="onError"
          > Full <b-icon icon="file-earmark" aria-hidden="true"></b-icon>
          </b-button>
                    <b-button
            v-b-tooltip.hover
            :title="getRTMPEndpoint(data.value)"
            v-clipboard:copy="getRTMPEndpoint(data.value)"
            v-clipboard:success="onCopy"
            v-clipboard:error="onError"
          > RTMP <b-icon icon="file-earmark" aria-hidden="true"></b-icon>
          </b-button>
                    <b-button
            v-b-tooltip.hover
            :title="getStreamKey(data.value)"
            v-clipboard:copy="getStreamKey(data.value)"
            v-clipboard:success="onCopy"
            v-clipboard:error="onError"
          > Stream key <b-icon icon="file-earmark" aria-hidden="true"></b-icon>
          </b-button>
          </b-button-group>
        </div>
      </template>
        <template v-slot:cell(MediaPackageHLSEndpoint)="data">
        <div>
          <b-button :disabled="data.item.State != STREAMRUNNING" :href="data.value" variant="success">Play <b-icon icon="play-fill"></b-icon></b-button>
        </div>
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

const rootapi = process.env.VUE_APP_AWS_APIGATEWAY_ENDPOINT;

console.log(rootapi);

export default {
  data() {
    return {
      STREAMRUNNING : "RUNNING",
      sortBy: "STATE",
      sortDesc: false,
      fields: [
        { key: "ChannelID", sortable: true },
        { key: "State", sortable: true },
        { key: "StartChannel", sortable: false, label: "Start Channel" },
        { key: "RTMPEndpoint", sortable: false, label: "RTMP" },
        { key: "MediaPackageHLSEndpoint", sortable: false, label: "Player" },
      ],
      items: []
    };
  },
  created() {
    axios
      .get(`${rootapi}/channel`)
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
  },
  methods: {
    onCopy: function (e) {
      alert('You just copied: ' + e.text)
    },
    onError: function (e) {
      alert('Failed to copy texts' + e.text)
    },
    getRTMPEndpoint : function (RTMPEndpoint) {
      // eslint-disable-next-line no-unused-vars
      let comp = RTMPEndpoint.split('/');
      return `${comp[0]}//${comp[2]}`
    },
    getStreamKey : function (RTMPEndpoint) {
      // eslint-disable-next-line no-unused-vars
      let comp = RTMPEndpoint.split('/');
      return comp[3]
    },
    startChannel: function (){
      axios.post(`${rootapi}/channel/startChannel`)
      .then(function (response) {
        console.log(response);
        this.$emit('showAlert','response','success');
      })
      .catch(function (error) {
        console.log(error);
        this.$emit('showAlert','Error','danger');
      });
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
