<template>
  <div id="ChannelList">
    <b-table :items="items" :fields="fields" :sort-by.sync="sortBy" :sort-desc.sync="sortDesc" responsive="sm">
      <template v-slot:cell(MediaPackageHLSEndpoint)="data">
        <div>
          <b-button :href="data.value" variant="success">Play</b-button>
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

const rootapi = process.env.VUE_APP_AWS_APIGATEWAY_ENDPOINT

console.log(rootapi)

export default {
  data() {
    return {
      sortBy: "STATE",
      sortDesc: false,
      fields: [
        { key: "ChannelID", sortable: true },
        { key: "MediaPackageHLSEndpoint", sortable: false, label: "Player"},
        { key: "State", sortable: true }
      ],
      items: []
    };
  },
  created() {
    axios
      .get(`${rootapi}/channel`)
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
  margin: 0 auto;
}
</style>
