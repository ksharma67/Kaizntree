<template>
  <div class="sidebar-menu" :class="{ 'open': isMenuOpen }">
    <!-- Toggle button for hamburger menu -->
    <div class="menu-toggle" @click="toggleMenu">
      <div class="hamburger">
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
      </div>
    </div>
    <!-- Hamburger menu, visible only when isMenuOpen is true -->
    <ul v-if="isMenuOpen" class="hamburger-menu">
      <li v-for="(item, index) in menuItems" :key="index">
        <template v-if="item.spacer">
          <!-- Render a spacer if item.spacer is true -->
          <div class="spacer"></div>
        </template>
        <template v-else>
          <!-- Render a router link for non-spacer items -->
          <router-link :to="item.route" class="menu-item" :class="{ 'active': $route.path === item.route }" exact>
            <div class="menu-icon-wrapper">
              <img :src="requireIcon(item.icon)" class="menu-icon" alt="Menu Icon">
            </div>
            <span class="menu-label">{{ item.label }}</span>
          </router-link>
        </template>
      </li>
    </ul>
    <!-- Main menu, visible on larger screens -->
    <ul class="main-menu">
      <li v-for="(item, index) in menuItems" :key="index">
        <template v-if="item.spacer">
          <div class="spacer"></div>
        </template>
        <template v-else>
          <router-link :to="item.route" class="menu-item" :class="{ 'active': $route.path === item.route }" exact>
            <div class="menu-icon-wrapper">
              <img :src="requireIcon(item.icon)" class="menu-icon" alt="Menu Icon">
            </div>
            <span class="menu-label">{{ item.label }}</span>
          </router-link>
        </template>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'SidebarMenu',
  data() {
    return {
      // Array of menu items with id, label, route, icon, and optional spacer
      menuItems: [
        {id: 1, label: 'Home', route: '/dashboard', icon: 'home.png'},
        {id: 2, label: 'Items', route: '/items', icon: 'items.png'},
        {id: 3, label: 'Stock', route: '/stock', icon: 'stock.png'},
        {id: 4, label: 'Build', route: '/build', icon: 'build.png'},
        {id: 5, label: 'Customers', route: '/customers', icon: 'customers.png'},
        {id: 6, label: 'Sales Orders', route: '/salesorders', icon: 'salesorders.png'},
        {id: 7, label: 'Suppliers', route: '/suppliers', icon: 'suppliers.png'},
        {id: 8, label: 'Manufacturers', route: '/manufacturers', icon: 'manufacturers.png'},
        {id: 9, label: 'Purchase Orders', route: '/purchaseorders', icon: 'purchaseorders.png'},
        {id: 10, label: 'Reports', route: '/reports', icon: 'reports.png'},
        { spacer: true },
        {id: 11, label: 'Help', route: '/help', icon: 'help.png'},
        {id: 12, label: 'Integrations', route: '/integrations', icon: 'integrations.png'},
        {id: 13, label: 'Logout', route: '/', icon: 'logout.png'},
        {id: 14, label: 'My Profile', route: '/myprofile', icon: 'myprofile.png'}
          // Add more menu items as needed
      ],
      isMenuOpen: false // Flag to control the visibility of the hamburger menu
    };
  },
  methods: {
    // Method to load icons dynamically
    requireIcon(icon) {
      return require(`@/assets/${icon}`);
    },
    // Method to toggle the visibility of the hamburger menu
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
    // Method to handle logout (if applicable)
    logout() {
      localStorage.removeItem('user-token'); // Remove the token from localStorage
      this.$router.push('/login'); // Redirect to login page
    }
  }
}
</script>

<style scoped>
/* Styles for the sidebar menu */
.sidebar-menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 200px; /* Adjust the width for sidebar menu */
  height: 100%;
  background-color: #ffffff; /* Sidebar background color */
  transition: transform 0.3s ease-in-out;
  overflow-y: auto; /* Enable scrolling */
  z-index: 999; /* Ensure sidebar is above other content */
  border-right: 5px solid #007bff;
}

/* Styles for menu lists */
.sidebar-menu ul {
  list-style-type: none;
  padding: 0;
  padding-left: 10px;
}

.sidebar-menu ul li {
  margin-bottom: 2%;
}

/* Styles for menu items */
.sidebar-menu ul li a {
  font-family: Montserrat, sans-serif !important;
  text-decoration: none;
  color: #373737;
  font-weight: 500;
  display: flex; /* Align items horizontally */
  align-items: center; /* Center align items vertically */
  padding: 5px 5px;
}

/* Styles for active menu items */
.sidebar-menu ul li a.active {
  background-color: #bbbaba;
  color: #000;
  border-radius: 5px;
}

/* Styles for menu icons */
.sidebar-menu ul li a .menu-icon {
  width: 30px; /* Adjust the width as needed */
  height: 30px; /* Adjust the height as needed */
  margin-right: 10px;
}

/* Styles for menu toggle (hamburger icon) */
.menu-toggle {
  position: absolute;
  top: 20px;
  right: 20px;
  cursor: pointer;
  z-index: 1000; /* Ensure toggle is above other content */
}

/* Styles for spacer */
.spacer {
  height: 40px; /* Adjust the height for the desired spacing */
}

/* Styles for hamburger menu */
.hamburger-menu {
  list-style-type: none;
  padding: 0;
}

.hamburger-menu li {
  margin-bottom: 15px;
}

.hamburger-menu li a {
  font-family: Montserrat, sans-serif !important;
  text-decoration: none;
  color: #333;
  font-weight: 500;
  display: flex;
  align-items: center;
  padding: 5px 5px;
}

.hamburger-menu li a.active {
  background-color: #bbbaba;
  color: #000;
  border-radius: 5px;
}

.hamburger-menu li a .menu-icon {
  width: 30px;
  height: 30px;
  margin-right: 10px;
}

/* Styles for hamburger icon */
.hamburger {
  width: 30px;
  height: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.bar {
  width: 100%;
  height: 3px;
  background-color: #333;
}

/* Media queries for responsive layout */
@media screen and (min-width: 769px) {
  .menu-toggle {
    display: none; /* Hide menu toggle on larger screens */
  }

  .hamburger-menu {
    display: none; /* Hide hamburger menu on larger screens */
  }

  .sidebar-menu.open .hamburger-menu {
    display: block; /* Show hamburger menu when sidebar is open */
  }
}

@media screen and (max-width: 768px) {
  .sidebar-menu {
    border-right: none; /* Remove right border on smaller screens */
  }
  .main-menu {
    display: none; /* Hide main menu on smaller screens */
  }

  .sidebar-menu.open .main-menu {
    display: block; /* Show main menu when sidebar is open */
  }
}
</style>
