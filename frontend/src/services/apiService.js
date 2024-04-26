import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/';

const instance = axios.create({
  baseURL: API_URL,
  timeout: 1000,
  headers: {'Content-Type': 'application/json'}
});

// Function to set the auth token for any request
export const setAuthToken = (token) => {
  instance.defaults.headers.common['Authorization'] = `Token ${token}`;
};

export const userLogin = (username, password) => {
  return instance.post('login/', {username, password});
};

export const registerUser = (username, password) => {
  return instance.post('register/', {username, password});
};

// Functions for Categories
export const createCategory = (data) => {
  return instance.post('categories/', data);
};

export const getCategories = () => {
  return instance.get('categories/');
};

export const updateCategory = (id, data) => {
  return instance.put(`categories/${id}/`, data);
};

export const deleteCategory = (id) => {
  return instance.delete(`categories/${id}/`);
};

// Functions for Items
export const createItem = (data) => {
  return instance.post('items/', data);
};

export const getItems = () => {
  return instance.get('items/');
};

export const updateItem = (id, data) => {
  return instance.put(`items/${id}/`, data);
};

export const deleteItem = (id) => {
  return instance.delete(`items/${id}/`);
};

// Functions for Tags
export const createTag = (data) => {
  return instance.post('tags/', data);
};

export const getTags = () => {
  return instance.get('tags/');
};

export const updateTag = (id, data) => {
  return instance.put(`tags/${id}/`, data);
};

export const deleteTag = (id) => {
  return instance.delete(`tags/${id}/`);
};

// Functions for Stock Statuses
export const createStockStatus = (data) => {
  return instance.post('stockstatuses/', data);
};

export const getStockStatuses = () => {
  return instance.get('stockstatuses/');
};

export const updateStockStatus = (id, data) => {
  return instance.put(`stockstatuses/${id}/`, data);
};

export const deleteStockStatus = (id) => {
  return instance.delete(`stockstatuses/${id}/`);
};
