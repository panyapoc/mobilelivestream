import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import Player from '../views/Player.vue';

Vue.use(VueRouter);

  const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/player/:type/:id/:url',
    name: 'Player',
    component: Player,
    props: true
  }
];

const router = new VueRouter({
  routes
});

export default router;
