<template>
  <div id="Video">
    <NavBar />
    <h1>This is an about page</h1>
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
	data() {
		return {
			videoOptions: {
        aspectRatio: "16:9",
				autoplay: true,
				controls: true,
				sources: [
					{
            // src: "https://d3btskzrn2dzma.cloudfront.net/vod/c53860f6-1175-46ea-a3f5-78887cb3f81b/index.m3u8",
            type: "application/x-mpegURL"
					}
				]
			}
		};
	}
};
</script>

