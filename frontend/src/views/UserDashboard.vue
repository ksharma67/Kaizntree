<template>
    <div>
      <div class="sidebar" :class="{ 'open': isMenuOpen }">
        <SidebarMenu @menuItemSelected="updateDashboardTitle" />
      </div>
      <div class="main-content">
        <h1>{{ dashboardTitle }}</h1>
        <!-- Other content of the dashboard goes here -->
      </div>
    </div>
  </template>
  
  <script>
  import SidebarMenu from '@/components/SidebarMenu.vue';
  
  export default {
    components: {
      SidebarMenu
    },
    data() {
      return {
        dashboardTitle: 'Dashboard',
        isMenuOpen: false
      };
    },
    methods: {
      updateDashboardTitle(selectedMenuItemLabel) {
        this.dashboardTitle = selectedMenuItemLabel;
      }
    }
  };
  </script>
  
  <style scoped>
  /* Your existing styles */
  
  .sidebar {
    width: 200px;
    background-color: #ffffff;
    position: fixed;
    top: 0;
    left: -200px; /* Move sidebar off the screen by default */
    transition: left 0.3s ease-in-out; /* Add transition for smooth animation */
  }
  
  .sidebar.open {
    left: 0; /* Move sidebar to the left when opened */
  }
  
  .main-content {
    margin-left: 220px; /* Adjust margin to accommodate opened sidebar */
  }
  
  .main-content h1 {
    font-size: 34px;
    color: #333;
    padding-top: 25px;
    text-align: left;
  }
  
  /* Media query for tablet and mobile */
  @media screen and (max-width: 768px) {
    .sidebar {
      width: 200px; /* Reset width */
      right: 0; /* Move sidebar to the right */
      left: auto; /* Reset left positioning */
    }
  
    .main-content {
      margin-right: 0px; /* Adjust margin to accommodate opened sidebar */
      margin-left: 220px; /* Reset margin for smaller screens */
    }
  
    .sidebar.open {
      left: auto; /* Reset left positioning when opened */
      right: 0; /* Move sidebar to the right when opened */
    }
  }
  </style>
  