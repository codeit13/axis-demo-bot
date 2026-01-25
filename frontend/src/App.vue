<template>
  <div id="app">
    <Topbar @toggle-sidebar="toggleSidebar" />
    <div class="main-layout">
      <Sidebar :is-open="sidebarOpen" @close="closeSidebar" />
      <div v-if="sidebarOpen" class="sidebar-overlay" @click="closeSidebar"></div>
      <main class="main-content" :class="{ 'content-shifted': sidebarOpen }">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
import Topbar from './components/Topbar.vue'
import Sidebar from './components/Sidebar.vue'

export default {
  name: 'App',
  components: {
    Topbar,
    Sidebar
  },
  data() {
    return {
      sidebarOpen: false
    }
  },
  methods: {
    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen
    },
    closeSidebar() {
      this.sidebarOpen = false
    }
  },
  watch: {
    '$route'() {
      // Close sidebar on route change for mobile
      if (window.innerWidth < 1024) {
        this.sidebarOpen = false
      }
    }
  },
  mounted() {
    // Check if we're on desktop on mount
    if (window.innerWidth >= 1024) {
      this.sidebarOpen = true
    }
    
    // Handle window resize
    window.addEventListener('resize', () => {
      if (window.innerWidth >= 1024) {
        this.sidebarOpen = true
      } else {
        this.sidebarOpen = false
      }
    })
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background-color: #f5f5f5;
  color: #333;
}

#app {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.main-layout {
  display: flex;
  flex: 1;
  overflow: hidden;
  min-height: 0;
  position: relative;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  background-color: #f5f5f5;
  min-height: 0;
  transition: margin-left 0.3s ease;
}

.sidebar-overlay {
  position: fixed;
  top: 73px;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 998;
  display: none;
}

@media (max-width: 1023px) {
  .sidebar-overlay {
    display: block;
  }
  
  .content-shifted {
    margin-left: 0;
  }
}
</style>
