import axios from 'axios';

// Base URL for the API
const API_URL = 'http://127.0.0.1:8000/api/';

// Create an Axios instance with default configuration
const instance = axios.create({
  baseURL: API_URL, // Base URL for all requests
  timeout: 1000, // Timeout for requests (in milliseconds)
  headers: {'Content-Type': 'application/json'} // Default header for requests
});

// Function to set the auth token for any request
export const setAuthToken = (token) => {
  instance.defaults.headers.common['Authorization'] = `Token ${token}`; // Set the authorization header with the token
};

// Function to handle user login
export const userLogin = (username, password) => {
  return instance.post('login/', {username, password}); // Send a POST request to the 'login/' endpoint with the username and password
};

// Function to register a new user
export const registerUser = (username, password) => {
  return instance.post('register/', {username, password}); // Send a POST request to the 'register/' endpoint with the username and password
};

// Functions for Categories
export const createCategory = (data) => {
  return instance.post('categories/', data); // Send a POST request to the 'categories/' endpoint with the category data
};

export const getCategories = () => {
  return instance.get('categories/'); // Send a GET request to the 'categories/' endpoint to retrieve all categories
};

export const updateCategory = (id, data) => {
  return instance.put(`categories/${id}/`, data); // Send a PUT request to the 'categories/{id}/' endpoint with the category data to update
};

export const deleteCategory = (id) => {
  return instance.delete(`categories/${id}/`); // Send a DELETE request to the 'categories/{id}/' endpoint to delete the category
};

// Functions for Items
export const createItem = (data) => {
  return instance.post('items/', data); // Send a POST request to the 'items/' endpoint with the item data
};

export const getItems = () => {
  return instance.get('items/'); // Send a GET request to the 'items/' endpoint to retrieve all items
};

export const updateItem = (id, data) => {
  return instance.put(`items/${id}/`, data); // Send a PUT request to the 'items/{id}/' endpoint with the item data to update
};

export const deleteItem = (id) => {
  return instance.delete(`items/${id}/`); // Send a DELETE request to the 'items/{id}/' endpoint to delete the item
};

// Functions for Tags
export const createTag = (data) => {
  return instance.post('tags/', data); // Send a POST request to the 'tags/' endpoint with the tag data
};

export const getTags = () => {
  return instance.get('tags/'); // Send a GET request to the 'tags/' endpoint to retrieve all tags
};

export const updateTag = (id, data) => {
  return instance.put(`tags/${id}/`, data); // Send a PUT request to the 'tags/{id}/' endpoint with the tag data to update
};

export const deleteTag = (id) => {
  return instance.delete(`tags/${id}/`); // Send a DELETE request to the 'tags/{id}/' endpoint to delete the tag
};

// Functions for Stock Statuses
export const createStockStatus = (data) => {
  return instance.post('stockstatuses/', data); // Send a POST request to the 'stockstatuses/' endpoint with the stock status data
};

export const getStockStatuses = () => {
  return instance.get('stockstatuses/'); // Send a GET request to the 'stockstatuses/' endpoint to retrieve all stock statuses
};

export const updateStockStatus = (id, data) => {
  return instance.put(`stockstatuses/${id}/`, data); // Send a PUT request to the 'stockstatuses/{id}/' endpoint with the stock status data to update
};

export const deleteStockStatus = (id) => {
  return instance.delete(`stockstatuses/${id}/`); // Send a DELETE request to the 'stockstatuses/{id}/' endpoint to delete the stock status
};
