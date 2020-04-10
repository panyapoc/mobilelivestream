<template>
  <div id="ChannelList">
    <b-table
      :items="items"
      :fields="fields"
      :sort-by.sync="sortBy"
      :sort-desc.sync="sortDesc"
      responsive="sm"
    ></b-table>

    <div>
      <!-- Sorting By: <b>{{ sortBy }}</b>, Sort Direction: -->
      <!-- <b>{{ sortDesc ? 'Descending' : 'Ascending' }}</b> -->
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    const Channel = [
      {
        isActive: true,
        age: 40,
        first_name: "Dickerson",
        last_name: "Macdonald"
      },
      { isActive: false, age: 21, first_name: "Larsen", last_name: "Shaw" },
      { isActive: false, age: 89, first_name: "Geneva", last_name: "Wilson" },
      { isActive: true, age: 38, first_name: "Jami", last_name: "Carney" }
    ];
    return {
      sortBy: "age",
      sortDesc: false,
      fields: [
        { key: "last_name", sortable: true },
        { key: "first_name", sortable: true },
        { key: "age", sortable: true }
      ],
      items: Channel
    };
  },
  reated() {
    axios
      .get(`http://jsonplaceholder.typicode.com/posts`)
      .then(response => {
        // JSON responses are automatically parsed.
        this.posts = response.data;
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
