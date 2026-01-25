<template>
  <header class="header">
    <div class="header-left">
      <button class="hamburger-button" @click="$emit('toggle-sidebar')">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
      </button>
      <div class="logo">
        <div class="logo-icon">
          <span style="position: relative; z-index: 1;">+</span>
        </div>
        <span class="logo-text">Axis Neo Agentic Microservices</span>
      </div>
    </div>
    <div class="header-right">
      <div class="search-bar">
        <input type="text" placeholder="Search services, APIs, or agents" class="search-input" />
      </div>
      <button class="icon-button">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <path d="M12 16v-4M12 8h.01"></path>
        </svg>
      </button>
      <button class="icon-button">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"></path>
          <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
        </svg>
      </button>
      <div class="status-indicator">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polyline>
        </svg>
        <span class="status-text">11 Agents Operational</span>
      </div>
      <div class="user-avatar">PC</div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Topbar',
  emits: ['toggle-sidebar']
}
</script>

<style scoped>
.header {
  background: white;
  border-bottom: 1px solid #e5e5e5;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.hamburger-button {
  display: none;
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  color: #6b7280;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.hamburger-button:hover {
  background-color: #f3f4f6;
}

@media (max-width: 1023px) {
  .hamburger-button {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .logo-text {
    display: none;
  }
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
  color: #97144D;
  position: relative;
}

.logo-icon::before {
  content: '+';
  position: absolute;
  top: -4px;
  left: -4px;
  font-size: 10px;
  color: #97144D;
}

.logo-icon::after {
  content: '+';
  position: absolute;
  bottom: -4px;
  right: -4px;
  font-size: 10px;
  color: #97144D;
}

.logo-text {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.search-bar {
  position: relative;
}

.search-bar::before {
  content: '🔍';
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.875rem;
  z-index: 1;
  pointer-events: none;
}

.search-input {
  padding: 0.5rem 1rem;
  padding-left: 2.5rem;
  border: 1px solid #e5e5e5;
  border-radius: 6px;
  width: 300px;
  font-size: 0.875rem;
  background-color: #f9fafb;
}

@media (max-width: 768px) {
  .search-input {
    width: 200px;
  }
  
  .status-indicator .status-text {
    display: none;
  }
}

@media (max-width: 640px) {
  .search-bar {
    display: none;
  }
  
  .status-indicator {
    display: none;
  }
}

.search-input:focus {
  outline: none;
  border-color: #97144D;
}

.icon-button {
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  color: #6b7280;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.icon-button:hover {
  background-color: #f3f4f6;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #f3f4f6;
  border-radius: 6px;
  font-size: 0.875rem;
  color: #374151;
  font-weight: 500;
}

.status-indicator svg {
  color: #10b981;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #fbbf24;
  color: #1f2937;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.user-avatar:hover {
  transform: scale(1.05);
}
</style>
