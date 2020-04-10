<template>
  <div class="NavBar">
    <div>
      <b-navbar toggleable="lg" type="dark" variant="primary">
        <b-navbar-brand href="#">Mobile Live Streaming</b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
        <b-collapse id="nav-collapse" is-nav>
          <!-- <b-navbar-nav>
            <b-nav-item href="#">Link</b-nav-item>
            <b-nav-item href="#" disabled>Disabled</b-nav-item>
          </b-navbar-nav> -->
          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">
            <b-nav-item href="#" disabled>README</b-nav-item>
            <b-nav-item
              target="_blank"
              rel="noopener noreferrer"
              href="https://github.com/panyapoc/mobilelivestream"
              >GitHub</b-nav-item
            >
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>
  </div>
</template>

<script>
export default {
  name: "NavBar"
  // props: {
  //   msg: String
  // }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
