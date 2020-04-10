<template>
  <div>
    <NavBar />
    <div id="metadata">
      <b-row>
        <b-col class="text-left"><h3>{{ TypeTitle }}</h3></b-col>
        <b-col class="text-right"><h3>{{ id }}</h3></b-col>
      </b-row>
    </div>
    <video-player :options="videoOptions"/>
  </div>

</template>

<script>
import NavBar from "@/components/NavBar.vue";
import VideoPlayer from "@/components/VideoPlayer.vue";

export default {
	name: "Video",
	components: {
    VideoPlayer,
    NavBar,
  },
  props: ['type','id','url'],
	data() {
		return {
      TypeTitle : null,

			videoOptions: {
        aspectRatio: "16:9",
				autoplay: true,
				controls: true,
				sources: [
					{
            // src: `${cloudfront}/vod/${this.id}/index.m3u8`,
            src: this.url,
            type: "application/x-mpegURL"
					}
				]
			}
    };
  },
  created() {
    if (this.type === 'vod'){
      this.TypeTitle = 'Video On-Demand'
    } else if (this.type === 'live'){
      this.TypeTitle = 'Live'
    }
  }
};
</script>

<style scoped>
#metadata {
    max-width: 75rem;
    margin: 10px auto 10px auto;
}

.title {
    max-width: 75rem;
    padding: 20px auto 10rem auto ;
}
</style>