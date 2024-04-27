<template>
  <div>
    <div class="sidebar" :class="{ 'open': isMenuOpen }">
      <!-- Sidebar menu component -->
      <SidebarMenu @menuItemSelected="updateDashboardTitle" />
    </div>
    <div class="main-content">
      <div class="dashboard-header">
        <h1>{{ dashboardTitle }}</h1>
        <!-- Check if the search is inactive and then display "All Items" -->
        <div v-if="!isSearchActive" class="all-items-label">All Items</div>
        <div class="summary-section">
          <!-- Summary section with total categories and total items -->
          <div class="summary-item">
            <i class="material-icons">category</i>
            <div class="summary-text">
              <h2>Total Categories</h2>
              <span>{{ totalCategories }}</span>
            </div>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-item">
            <i class="material-icons">inventory_2</i>
            <div class="summary-text">
              <h2>Total Items</h2>
              <span>{{ totalItems }}</span>
            </div>
          </div>
        </div>
      </div>
      <div class="item-dashboard">
        <div class="dashboard-controls">
          <!-- Button to open the new category modal -->
          <button class="new-category-btn" @click="openNewCategoryModal">NEW ITEM CATEGORY</button>
        </div>
        <!-- Modal component for creating a new category -->
        <dynamic-modal
            title="Create New Category"
            :visible="showNewCategoryModal"
            @update:visible="showNewCategoryModal = $event"
            :onSubmit="submitNewCategory">
            <form @submit.prevent="submitNewCategory">
              <label for="category-name">Category Name:</label>
              <input id="category-name" v-model="newCategoryName" type="text" placeholder="Enter category name" required>
              <div class="modal-footer">
                <button type="submit">Save</button>
                <button type="button" @click="closeNewCategoryModal">Cancel</button>
              </div>
            </form>
          </dynamic-modal>
        <div class="subcategory-section">
          <!-- Section for displaying subcategories -->
          <div class="category-header" @click="toggleSubcategories">
            <span>{{ totalCategories }} Subcategories</span>
            <span class="category-arrow">▶</span>
          </div>
          <div :class="{ 'active': showSubcategories }" v-show="showSubcategories" class="subcategories-container">
            <span v-for="category in categories" :key="category.id" class="subcategory">
              {{ category.name }}
            </span>
          </div>
        </div>
        <div class="dashboard-controls">
          <!-- Button to open the new item modal -->
          <button class="new-item-btn" @click="openNewItemModal">NEW ITEM</button>
            <!-- Modal component for creating a new item -->
            <dynamic-modal
              title="Create New Item"
              :visible="showNewItemModal"
              @update:visible="showNewItemModal = $event"
              :onSubmit="submitNewItem"
            >
              <form @submit.prevent="submitNewItem">
                <label for="item-name">Item Name:</label>
                <input id="item-name" v-model="newItem.name" type="text" placeholder="Enter item name" required>

                <label for="item-sku">SKU:</label>
                <input id="item-sku" v-model="newItem.sku" type="text" placeholder="Enter SKU" required>

                <label for="item-category">Category:</label>
                <select id="item-category" v-model="newItem.categoryId" required>
                  <option v-for="category in categories" :value="category.id" :key="category.id">
                    {{ category.name }}
                  </option>
                </select>
                <label for="item-tags">Tags:</label>
                <input id="item-tags" v-model="newItem.tags" type="text" placeholder="Enter tags, comma separated">

                <label for="item-stock">Available Stock:</label>
                <input id="item-stock" v-model="newItem.availableStock" type="number" placeholder="Enter available stock" required>

                <div class="modal-footer">
                  <button type="submit">Save</button>
                  <button type="button" @click="closeNewItemModal">Cancel</button>
                </div>
              </form>
            </dynamic-modal>
          <button class="new-options-btn" @click="openNewItemModal">OPTIONS ▼</button>
          <!-- Search box for filtering items -->
          <div class="search-box">
            <input type="text" v-model="searchQuery" placeholder="Search">
          </div>
          <!-- Controls for toggling between grid and list view -->
          <div v-if="currentView === 'grid'" class="view-controls">
                <button @click="toggleView('grid')"><i class="material-icons">view_column</i></button>
            </div>
            <div v-else class="view-controls">
                <button @click="toggleView('list')"><i class="material-icons">list</i></button>
            </div>
          <!-- Filter controls -->
          <div class="filter-controls">
            <!-- Filter Toggle Button -->
              <button @click="toggleFilters">
                <i class="material-icons">filter_alt</i>
              </button>
          </div>
          <!-- Additional filter inputs -->
          <div v-if="showFilters" class="filter-controls">
            <input type="date" v-model="filterStartDate" placeholder="Start Date">
            <input type="date" v-model="filterEndDate" placeholder="End Date">
            <select v-model="filterStockStatus">
              <option value="">All</option>
              <option value="inStock">In Stock</option>
              <option value="outOfStock">Out of Stock</option>
            </select>
            <button @click="applyFilters">Apply Filters</button>
          </div>
        </div>
        <div class="table-wrapper">
          <!-- Grid view for displaying items -->
          <table v-if="currentView === 'grid'" class="grid-view">
            <thead>
              <tr>
                <th><input type="checkbox" @change="toggleSelectAll" v-model="allSelected" /></th>
                <th>SKU</th>
                <th>Name</th>
                <th>Tags</th>
                <th>Category</th>
                <th>In Stock</th>
                <th>Available Stock</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in filteredItems" :key="item.id">
                <td class="checkbox-cell"><input type="checkbox" v-model="item.selected" /></td>
                <td>{{ item.sku }}</td>
                <td>{{ item.name }}</td>
                <td>
                  <span v-for="tagId in item.tags" :key="tagId">
                    {{ formatTags(item.tags) }}
                  </span>
                </td>
                <td>{{ getCategoryName(item.category) }}</td>
                <td>{{ item.inStock ? 'Yes' : 'No' }}</td>
                <td>{{ item.available_stock }}</td>
              </tr>
            </tbody>
          </table>
          <!-- List view for displaying items -->
          <div v-else class="list-view">
              <div class="item-list">
                  <div class="item-title">SKU</div>
                  <div class="item-title">Name</div>
                  <div class="item-title">Tags</div>
                  <div class="item-title">Category</div>
                  <div class="item-title">In Stock</div>
                  <div class="item-title">Available Stock</div>
                </div>
                <!-- List Items-->
                <div class="list-item" v-for="item in filteredItems" :key="item.id">
                  <input type="checkbox" v-model="item.selected" />
                  <div class="item-details">
                    <div>{{ item.sku }}</div>
                    <div>{{ item.name }}</div>
                    <div>
                      <span v-for="tagId in item.tags" :key="tagId">
                        {{ formatTags(item.tags) }}
                      </span>
                    </div>
                    <div>{{ getCategoryName(item.category) }}</div>
                    <div>{{ item.inStock ? 'Yes' : 'No' }}</div>
                    <div>{{ item.available_stock }}</div>
                  </div>
                </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import SidebarMenu from '@/components/SidebarMenu.vue';
import DynamicModal from '@/components/DynamicModal.vue';
import { getItems, getCategories, createCategory, createItem, getTags } from '@/services/apiService';

export default {
  components: {
    SidebarMenu,
    DynamicModal,
  },
  computed: {
    // Check if the search query is active
    isSearchActive() {
    return this.searchQuery.trim().length > 0;
  },
  // Filter items based on search query and filters
  filteredItems() {
    return this.items.filter(item => {
      const inDateRange = (!this.filterStartDate || new Date(item.date) >= new Date(this.filterStartDate)) &&
                          (!this.filterEndDate || new Date(item.date) <= new Date(this.filterEndDate));

      // Stock status is expected to be a string "Yes" or "No".
      const stockStatusMatch = !this.filterStockStatus || 
                               (this.filterStockStatus === 'inStock' && item.stock_status === 2) ||
                               (this.filterStockStatus === 'outOfStock' && item.stock_status === 1);

      const searchLower = this.searchQuery.toLowerCase();
      const nameMatch = item.name.toLowerCase().includes(searchLower);
      const skuMatch = item.sku.toLowerCase().includes(searchLower);
      const tagsMatch = item.tags.some(tagId => {
        const tagName = this.getTagName(tagId);
        return typeof tagName === 'string' && tagName.toLowerCase().includes(searchLower);
      });
      const categoryMatch = this.getCategoryName(item.category).toLowerCase().includes(searchLower);

      return inDateRange && stockStatusMatch && (nameMatch || skuMatch || tagsMatch || categoryMatch);
    });
  }
},
  data() {
    return {
      dashboardTitle: 'Item Dashboard',
      isMenuOpen: false,
      showNewItemModal: false,
      showNewCategoryModal: false,
      showSubcategories: false,
      totalCategories: 0,
      totalItems: 0,
      categoryId: null,
      items: [],
      tags: [],
      categories: [],
      subcategories: [], 
      newCategoryName: '',
      newItem: { name: '', sku: '', category: null, tags: [], availableStock: 0 },
      searchQuery: '',
      showFilters: false,
      filterStartDate: '',
      filterEndDate: '',
      filterStockStatus: '',
      currentView: 'grid',
    };
  },
  watch: {
    'items': {
      handler: function(newItems) {
        this.allSelected = newItems.every(item => item.selected);
      },
      deep: true
    }
  },
  methods: {
    // Toggle the sidebar menu
    toggleSubcategories() {
    this.showSubcategories = !this.showSubcategories;
    console.log("Toggled showSubcategories to: ", this.showSubcategories); // Debugging output
  },
  toggleFilters() {
    // Toggle the filter controls
    this.showFilters = !this.showFilters;
  },
  toggleSelectAll() {
    // Toggle select all items
      if(this.allSelected) {
        this.items.forEach(item => item.selected = true);
      } else {
        this.items.forEach(item => item.selected = false);
      }
    },
    // Toggle between grid and list view
    toggleView(viewType) {
      this.currentView = viewType === 'grid' ? 'list' : 'grid';
        console.log('View toggled to:', this.currentView); // Optional: for debugging
    },
    // Apply filters to the item list
    applyFilters() {
    this.updateFilteredItems(); // You might need to call this or directly manipulate the filtered list
  },
  // Update the filtered items based on the filter criteria
  updateFilteredItems() {
    this.filteredItems = this.items.filter((item) => {
      return (
        (this.filterStartDate ? new Date(item.date) >= new Date(this.filterStartDate) : true) &&
        (this.filterEndDate ? new Date(item.date) <= new Date(this.filterEndDate) : true) &&
        (this.filterStockStatus ? item.stockStatus === this.filterStockStatus : true)
      );
    });
  },
  // Update the dashboard title based on the selected menu item
    updateDashboardTitle(selectedMenuItemLabel) {
      this.dashboardTitle = selectedMenuItemLabel;
    },  
    // Fetch items from the API
    async fetchItems() {
      try {
        const response = await getItems();
        console.log("Items fetched:", response.data.results); // Add this log statement
        if (response.data && Array.isArray(response.data.results)) {
          this.items = response.data.results.map(item => ({
            ...item,
            selected: false,
            tags: item.tags || [] // Ensuring tags are always an array
          }));
          this.totalItems = response.data.count; // Use the count from the response
        } else {
          console.error('Expected an array in results but got:', response.data);
          this.items = []; // Fallback to an empty array
          this.totalItems = 0;
        }
      } catch (error) {
        console.error('Error fetching items:', error);
        alert('Failed to load items.');
      }
    },
    // Fetch categories from the API
    async fetchCategories() {
  try {
    const response = await getCategories();
    if (response.data && Array.isArray(response.data.results)) {
      this.categories = response.data.results;
      this.totalCategories = this.categories.length;
      console.log("Fetched categories: ", this.categories); // Debugging output
    } else {
      console.error('Data is not an array:', response.data);
      this.categories = [];
      this.totalCategories = 0;
    }
  } catch (error) {
    console.error('Failed to fetch categories:', error);
    this.categories = [];
    this.totalCategories = 0;
  }
},
// Fetch tags from the API
    async fetchTags() {
      try {
        const response = await getTags();
        console.log("API Response:", response.data); // Log the entire API response
        if (response.data && Array.isArray(response.data.results)) {
          this.tags = response.data.results;
        } else {
          console.error('Data is not an array:', response.data);
          this.tags = [];
        }
      } catch (error) {
        console.error('Failed to fetch tags:', error);
        this.tags = [];
      }
    },
    // Get the tag name based on the tag ID
    getTagName(tagId) {
      const tag = this.tags.find(tag => tag.id === tagId);
      console.log("Tag:", tag);
      return tag ? tag.name : 'Tag not found';
    },
    // Format tags for display
    formatTags(tagIds) {
    return tagIds.map(tagId => this.getTagName(tagId)).join(', ');
    },
    // Get the category name based on the category ID
    getCategoryName(categoryId) {
      console.log("Category ID:", categoryId); // Add this log statement
      const categoriesArray = Array.from(this.categories); // Convert proxy array to a regular array
      console.log("Categories Array:", categoriesArray); // Add this log statement
      const category = categoriesArray.find(cat => cat.id === categoryId);
      console.log("Category:", category); // Add this log statement
      return category ? category.name : 'Category not found';
    },
    // Create a new category
    async handleNewCategory() {
      if (!this.newCategoryName) {
        alert('Category name cannot be empty.');
        return;
      }
      try {
        const response = await createCategory({ name: this.newCategoryName });
        this.categories.push(response.data);
        this.newCategoryName = '';
        alert('Category added successfully!');
      } catch (error) {
        console.error('Failed to create category:', error);
        alert('Failed to add category.');
      }
    },
    // Create a new item
    async handleNewItem() {
      this.showNewItemModal = true; // Open the modal for new item
    },
    // Close the new category modal
    closeNewCategoryModal() {
      this.showNewCategoryModal = false;
    },
    // Close the new item modal
    closeNewItemModal() {
      this.showNewItemModal = false;
    },
    // Submit the new category form
    submitNewCategory() {
      if (!this.newCategoryName.trim()) {
        alert('Category name cannot be empty.');
        return;
      }
      // Call the API to create the new category
      createCategory({ name: this.newCategoryName }).then(response => {
        this.categories.push(response.data);
        this.closeNewCategoryModal(); // Close the modal on successful submission
        alert('Category added successfully!');
      }).catch(error => {
        console.error('Failed to create category:', error);
        alert('Failed to add category.');
      });
    },
    // Submit the new item form
    submitNewItem() {
  console.log("Submitting new item");
  if (!this.newItem.name || !this.newItem.sku || !this.newItem.categoryId) {
    alert('Name, SKU, and Category cannot be empty.');
    return;
  }

  // Check if the category ID is defined
  if (!this.newItem.categoryId) {
    console.error('Category ID is not defined');
    alert('Category is required.');
    return;
  }

  // Convert categories Proxy array to a regular array
  const categoriesArray = Array.from(this.categories);

  // Check if the category with the selected ID exists in the categories array
  const selectedCategory = categoriesArray.find(cat => cat.id === this.newItem.categoryId);
  if (!selectedCategory) {
    console.error('Category not found for categoryId:', this.newItem.categoryId);
    alert('Selected category does not exist.');
    return;
  }

  // Set the category name to newItem.category
  this.newItem.category = selectedCategory.name;

  // Call the API to create the new item
  createItem(this.newItem)
    .then(response => {
      this.items.push(response.data);
      this.closeNewItemModal(); // Close the modal on successful submission
      alert('Item added successfully!');
    })
    .catch(error => {
      console.error('Failed to create item:', error);
      alert('Failed to add item.');
    });
},
  },
  mounted() {
    console.log("Component mounted");
    this.fetchItems();
    this.fetchCategories().then(() => {
      console.log("Categories loaded", this.categories);
    });
    this.fetchTags();
    console.log("Tags fetched:", this.tags); // Log the fetched tags
    console.log("Tag IDs:", this.tags.map(tag => tag.id)); // Log the IDs of fetched tags
  },
  openNewCategoryModal() {
    console.log('Opening new category modal');
    this.showNewCategoryModal = true;
  },
  openNewItemModal() {
    console.log('Opening new item modal');
    this.showNewItemModal = true;
  }
};
</script>
  
  <style scoped>
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
    flex-grow: 1;
    padding: 20px;
  }
  .main-content h1 {
    font-size: 34px;
    color: #333;
    /* Removed padding-top to align with summary */
    text-align: left;
  }

  .checkbox-cell {
  width: 10px;
  text-align: center; /* Centers the checkbox horizontally */
  vertical-align: middle; /* Centers the checkbox vertically */
  align-items: center; /* Aligns the checkbox with the text */
  }

  .dashboard-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .dashboard-stats {
  display: flex;
  margin-bottom: 20px;
}

.all-items-label {
  /* Adjust the style to match your design */
  font-size: 20px; /* Adjust as needed */
  color: #666; /* Adjust as needed */
  margin-top: 10px; /* Space from the title */
  padding-left: 20px; /* Align with the title if it has padding */
}

.stats-card {
  display: flex;
  align-items: center;
  padding: 10px;
  margin-right: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stats-icon {
  margin-right: 10px;
  /* Add styles for icon size, etc. */
}

.stats-info > p {
  margin: 0;
  padding: 0;
  color: #333;
}

.stats-number {
  font-size: 24px;
  font-weight: bold;
}
  
  .main-content h1 {
    font-size: 34px;
    color: #333;
    text-align: left;
  }

  .summary-section {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    background-color: #fff; /* Or any color that matches your design */
    font-size: 10px;
  }

  .summary-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px; /* Adjust the space between the icon-text block and divider */
}
.summary-text {
  margin-left: 8px; /* Space between icon and text */
}

.item-list {
  display: list-item;
  align-items: center;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-weight: bold;
}
.list-item {
  display:list-item;
  align-items: center;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.summary-divider {
  width: 100%;
  height: 1px;
  background-color: #ccc; /* Divider color */
  margin-bottom: 5px; /* Space below the divider, same as above */
}

.summary-section .material-icons {
  /* Size of the icon */
  font-size: 24px; /* Adjust as needed */
  /* If you want to change the color of the icon */
  color: #666; /* Icon color, change as needed */
}

.new-category-btn {
  background-color: #4CAF50; /* Green background */
  color: white; /* White text */
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.new-category-btn:hover {
  background-color: #45a049; /* Darker green on hover */
}

.dashboard-controls {
  display: flex; /* Aligns all child elements in a row */
  align-items: center; /* Centers the buttons vertically */
  gap: 10px; /* Adds space between the elements */
  margin-bottom: 20px; /* Provides space below the controls */
}

.control-btn {
  background-color: #f7f7f7; /* Light grey background */
  border: 1px solid #ccc; /* Subtle border */
  border-radius: 4px;
  padding: 10px 15px;
  cursor: pointer;
  font-size: 16px; /* Adjust as needed */
  transition: background-color 0.2s ease-in-out;
}

.control-btn:hover {
  background-color: #e0e0e0; /* Darker shade on hover */
}

.control-input input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
  width: 100%; /* Allows the input to fill the space */
}

.total-categories, .total-items {
    margin-right: 400px; /* Adjust as needed */
    text-align: center;
  }

  .category-arrow {
  cursor: pointer;
}

.category-arrow span:first-child {
  margin-right: 5px;
}

.category-arrow span:last-child {
  color: blue; /* Or any color you prefer */
}

.subcategory-section {
  margin-top: 10px; /* Adjust spacing to match your layout */
  margin-bottom: 15px;
}

.category-arrow {
  cursor: pointer;
  user-select: none;
}

.category-arrow span:first-child {
  display: inline-block;
  transition: transform 0.3s;
}

.category-arrow[aria-expanded="true"] span:first-child {
  transform: rotate(90deg); /* Rotates the arrow when subcategories are shown */
}

.subcategory-section {
  background-color: #f0f0f0; /* Light grey background */
  border: 1px solid #ddd; /* Optional: adds a subtle border */
  border-radius: 5px;
}

.category-header {
  padding: 10px 15px;
  display: flex;
  justify-content: space-between; /* Positions the arrow to the right */
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.category-arrow {
  transition: transform 0.3s ease-in-out;
}

.subcategory-section .subcategories-container {
  display: none; /* This will start off hidden because `showSubcategories` is initially false */
  padding: 10px;
  background-color: #f9f9f9; /* Slightly different grey for contrast */
}

.subcategories-container .subcategory {
  display: block; /* Stack categories vertically */
  padding: 5px 0; /* Spacing above and below subcategory name */
  cursor: pointer;
}

.subcategories-container .subcategory:not(:last-child) {
  border-bottom: 1px solid #eaeaea; /* Adds a divider between subcategories */
}

.subcategory-section .subcategories-container.active {
    display: block; /* Active state */
}

/* Style to rotate the arrow when subcategories are shown */
.category-header[aria-expanded="true"] .category-arrow {
  transform: rotate(90deg);
}

.new-item-btn{
  background-color: #4CAF50; /* Green background */
  color: white; /* White text */
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-left: 15px;
  transition: background-color 0.3s ease;
}

.new-options-btn{
  background-color: #f0f0f0; 
  padding-left: 10px;
  color: black;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}
.search-box{
  display: flex;
  align-items: center;
  margin-left: auto; /* Pushes the search box to the right */
  border: none; /* Removes all borders */
  border-bottom: 2px solid #ccc;
}
.search-box input {
  padding: 10px;
  border: none;
  border-radius: 4px;
  margin-right: 10px; /* Spacing between search box and buttons */
  font-size: 16px; /* Adjust as needed */
}

.search-box input:focus {
  outline: none; /* Remove default focus outline */
  border-bottom: 2px solid #007bff; /* Blue bottom border on focus */
}

.view-controls button {
  background-color: #f7f7f7; /* Light grey background */
  border: 1px solid #ccc; /* Subtle border to enhance visibility */
  border-radius: 4px;
  padding: 10px 15px;
  margin-right: 5px; /* Spacing between buttons */
  cursor: pointer;
  font-size: 16px; /* Adjust as needed */
  transition: background-color 0.2s ease-in-out, transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* Soft shadow for depth */
}

.view-controls button:hover {
  background-color: #e0e0e0; /* Slightly darker on hover */
  transform: translateY(-2px); /* Slight lift effect on hover */
  box-shadow: 0 4px 6px rgba(0,0,0,0.15); /* Increased shadow on hover for more depth */
}

.view-controls button.active, .view-controls button:active {
  background-color: #4CAF50; /* Green background for active state */
  color: white; /* White text for active state */
  box-shadow: 0 1px 3px rgba(0,0,0,0.2); /* Subtle shadow for pressed effect */
}

.filter-controls {
  border-radius: 4px;
  padding: 10px 15px;
  cursor: pointer;
  font-size: 16px; /* Adjust as needed */
  transition: background-color 0.2s ease-in-out, transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.filter-controls:hover {
  background-color: #e0e0e0; /* Slightly darker on hover */
  transform: translateY(-2px); /* Slight lift effect on hover */
  box-shadow: 0 4px 6px rgba(0,0,0,0.15); /* Increased shadow on hover for more depth */
}

.filter-controls.active, .filter-controls:active {
  background-color: #4CAF50; /* Green background for active state */
  color: white; /* White text for active state */
  box-shadow: 0 1px 3px rgba(0,0,0,0.2); /* Subtle shadow for pressed effect */
}

.filter-controls input,
.filter-controls select {
  padding: 8px;
  margin-bottom: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.filter-controls button {
  padding: 10px 20px;
  background-color: #a2ada2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

/* Additional styling for dropdown or other filter components goes here */
.options-dropdown {
  /* Dropdown styling */
  display: inline-block; /* Adjust as needed for your layout */
  margin-left: 10px; /* Space from the search box or other elements */
}

/* Style specific to the dropdown trigger button */
.options-dropdown button {
  background-color: #f7f7f7; /* Light grey background */
  border: none;
  border-radius: 4px;
  padding: 10px 15px;
  cursor: pointer;
  font-size: 16px; /* Adjust as needed */
  transition: background-color 0.2s ease-in-out;
}

.options-dropdown button:hover {
  background-color: #e0e0e0; /* Slightly darker on hover */
}

.item-dashboard table {
  width: 100%;
  border-collapse: collapse;
  /* Other table styles */
}

.item-dashboard th, .item-dashboard td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.in-stock {
  color: green;
}

.out-of-stock {
  color: red;
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
    .dashboard-stats {
    flex-direction: column;
  }

  .stats-card {
    width: 100%;
    margin-bottom: 10px;
  }
  }
  </style>
  
