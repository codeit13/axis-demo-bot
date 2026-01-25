<template>
  <aside class="sidebar" :class="{ 'sidebar-open': isOpen, 'sidebar-closed': !isOpen }">
    <div class="sidebar-header">
      <div class="logo">
        <div class="logo-icon">
          <span style="position: relative; z-index: 1;">+</span>
        </div>
        <span class="logo-text">Axis Neo</span>
      </div>
      <button class="close-button" @click="$emit('close')">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>
    <nav class="sidebar-nav">
      <router-link to="/" class="nav-item" :class="{ active: $route.path === '/' }">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="3" width="7" height="7"></rect>
          <rect x="14" y="3" width="7" height="7"></rect>
          <rect x="14" y="14" width="7" height="7"></rect>
          <rect x="3" y="14" width="7" height="7"></rect>
        </svg>
        <span>Overview</span>
      </router-link>
      <router-link to="/service-lifecycle" class="nav-item" :class="{ active: $route.path === '/service-lifecycle' }">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path>
        </svg>
        <span>Service Lifecycle</span>
      </router-link>
      <router-link to="/agent-hub" class="nav-item" :class="{ active: $route.path === '/agent-hub' || $route.path.startsWith('/agent-hub') }">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
          <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
        </svg>
        <span>Agent Hub</span>
      </router-link>
      <router-link to="/security" class="nav-item" :class="{ active: $route.path === '/security' }">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
        </svg>
        <span>Security Guardrails</span>
      </router-link>
      <router-link to="/settings" class="nav-item" :class="{ active: $route.path === '/settings' }">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="3"></circle>
          <path d="M12 1v6m0 6v6M5.64 5.64l4.24 4.24m4.24 4.24l4.24 4.24M1 12h6m6 0h6M5.64 18.36l4.24-4.24m4.24-4.24l4.24-4.24"></path>
        </svg>
        <span>Settings</span>
      </router-link>
    </nav>
    <div class="sidebar-footer">
      <div class="user-profile">
        <div class="avatar">PC</div>
        <div class="user-info">
          <div class="user-name">Piyush Chordia</div>
          <div class="user-title">Vice President</div>
        </div>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </div>
    </div>
  </aside>
</template>

<script>
export default {
  name: 'Sidebar',
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close']
}
</script>

<style scoped>
.sidebar {
  width: 260px;
  background: #97144D;
  color: white;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  overflow: hidden;
  height: 100%;
  position: fixed;
  left: 0;
  top: 73px;
  z-index: 999;
  transform: translateX(0);
  transition: transform 0.3s ease;
}

.sidebar-closed {
  transform: translateX(-100%);
}

.close-button {
  display: none;
  background: none;
  border: none;
  color: white;
  padding: 0.5rem;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s;
  margin-left: auto;
}

.close-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

@media (max-width: 1023px) {
  .close-button {
    display: flex;
    align-items: center;
    justify-content: center;
  }
}

@media (min-width: 1024px) {
  .sidebar {
    position: relative;
    top: 0;
    transform: translateX(0) !important;
  }
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
  color: white;
  position: relative;
}

.logo-icon::before {
  content: '+';
  position: absolute;
  top: -4px;
  left: -4px;
  font-size: 10px;
  color: white;
}

.logo-icon::after {
  content: '+';
  position: absolute;
  bottom: -4px;
  right: -4px;
  font-size: 10px;
  color: white;
}

.logo-text {
  font-size: 1.125rem;
  font-weight: 600;
  color: white;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
  overflow-y: auto;
  overflow-x: hidden;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.2s;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-item.active {
  background-color: rgba(255, 255, 255, 0.15);
  color: white;
  border-left-color: white;
  font-weight: 500;
}

.sidebar-footer {
  padding: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.user-profile:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
}

.user-info {
  flex: 1;
}

.user-name {
  font-weight: 500;
  font-size: 0.875rem;
}

.user-title {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.7);
}
</style>
