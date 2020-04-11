<template>
  <div id="ChannelList">
    <b-row>
      <b-col class="text-left"><h1>Live Channel</h1></b-col>
      <b-col class="text-right">
        <b-button-group>
        <b-button variant="primary" @click="refreshChannel()"
          ><b-icon icon="arrow-clockwise"></b-icon
        ></b-button>
        <b-button variant="primary" @click="newChannel()"
          >New Channel <b-icon icon="file-plus"></b-icon
        ></b-button>
        </b-button-group>
      </b-col>
    </b-row>

    <b-table
      :items="items"
      :fields="fields"
      :sort-by.sync="sortBy"
      :sort-desc.sync="sortDesc"
      responsive="sm"
      borderless="borderless"
      v-if="items.length != 0"
    >
      <template v-slot:cell(StartChannel)="data">
        <b-button-group>
          <b-button
            :disabled="data.item.State != IDLE"
            variant="dark"
            @click="startChannel(data.index,data.item.ChannelId)"
            ><b-icon icon="camera-video"></b-icon
          ></b-button>
          <b-button
            :disabled="data.item.State != RUNNING"
            variant="dark"
            @click="stopChannel(data.item.ChannelId, data.index)"
            ><b-icon icon="stop"></b-icon
          ></b-button>
        </b-button-group>
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
            >
              FULL
              <!-- <b-icon icon="file-earmark" aria-hidden="true"></b-icon> -->
            </b-button>
            <b-button
              v-b-tooltip.hover
              :title="getRTMPEndpoint(data.value)"
              v-clipboard:copy="getRTMPEndpoint(data.value)"
              v-clipboard:success="onCopy"
              v-clipboard:error="onError"
            >
              RTMP
              <!-- <b-icon icon="file-earmark" aria-hidden="true"></b-icon> -->
            </b-button>
            <b-button
              v-b-tooltip.hover
              :title="getStreamKey(data.value)"
              v-clipboard:copy="getStreamKey(data.value)"
              v-clipboard:success="onCopy"
              v-clipboard:error="onError"
            >
              STREAM KEY
              <b-icon icon="file-earmark" aria-hidden="true"></b-icon>
            </b-button>
          </b-button-group>
        </div>
      </template>
      <template v-slot:cell(MediaPackageHLSEndpoint)="data">
        <div>
          <b-button
            :to="{
              name: 'Player',
              params: {
                id: data.item.ChannelId,
                type: 'live',
                url: data.item.MediaPackageHLSEndpoint
              }
            }"
            :disabled="data.item.State != RUNNING"
            variant="secondary"
            ><b-icon icon="play-fill"></b-icon
          ></b-button>
        </div>
      </template>
    </b-table>

    <div v-else>
      No Channel avalible, please create new Channel.
    </div>
  </div>
</template>

<script>
const rootapi = process.env.VUE_APP_AWS_APIGATEWAY_ENDPOINT;

console.log(rootapi);

export default {
  data() {
    return {
      IDLE: "IDLE",
      RUNNING: "RUNNING",
      sortBy: "STATE",
      sortDesc: false,
      fields: [
        { key: "ChannelId", sortable: true },
        { key: "State", sortable: true },
        { key: "StartChannel", sortable: false, label: "START/STOP" },
        { key: "RTMPEndpoint", sortable: false, label: "RTMP ENDPOINT" },
        { key: "MediaPackageHLSEndpoint", sortable: false, label: "Player" }
      ],
      items: []
    };
  },
  created() {
    this.$http
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
    onCopy: function(e) {
      alert("You just copied: " + e.text);
    },
    onError: function(e) {
      alert("Failed to copy texts" + e.text);
    },
    getRTMPEndpoint: function(RTMPEndpoint) {
      // eslint-disable-next-line no-unused-vars
      let comp = RTMPEndpoint.split("/");
      return `${comp[0]}//${comp[2]}`;
    },
    getStreamKey: function(RTMPEndpoint) {
      // eslint-disable-next-line no-unused-vars
      let comp = RTMPEndpoint.split("/");
      return comp[3];
    },
    startChannel: function(index,ChannelId) {
      let self = this;
      this.items[index]["State"] = "STARTING";
      this.$http
        .post(`${rootapi}/channel/startChannel`,{
          ChannelId : ChannelId
        })
        .then(function(response) {
          console.log("startChannel", response);
          self.$emit("showAlert", response.data.message, "success");
        })
        .catch(function(error) {
          console.log(error);
          self.$emit("showAlert", error, "danger");
        });
    },
    stopChannel: function(ChannelId, index) {
      let self = this;
      this.items[index]["State"] = "STOPPING";
      console.log(ChannelId);
      this.$http
        .post(`${rootapi}/channel/stopChannel`, {
          ChannelId: ChannelId
        })
        .then(function(response) {
          console.log("stopChannel", response);
          self.$emit("showAlert", response.data.message, "success");
        })
        .catch(function(error) {
          console.log(error);
          self.$emit("showAlert", error, "danger");
        });
    },
    newChannel: function() {
      let self = this;
      this.$http
        .post(`${rootapi}/channel/addChannel`)
        .then(function(response) {
          console.log("addChannel", response);
          self.$emit("showAlert", "Done", "success");
        })
        .catch(function(error) {
          console.log(error);
          self.$emit("showAlert", error.message, "danger");
        });
    },
    refreshChannel: function() {
      this.$http
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
