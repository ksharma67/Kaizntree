<template>
  <div>
    <div class="login-container">
      <img alt="Kaizntree" src="../assets/logo.png" class="logo">
      <h1>{{ msg }}</h1>
      <form @submit.prevent="login">
        <div class="form-group">
          <input type="text" id="username" v-model.trim="username" placeholder="Username" required>
        </div>
        <div class="form-group">
          <input type="password" id="password" v-model.trim="password" placeholder="Password" required>
        </div>
        <div class="form-group" style="padding-top: 15px;">
          <button type="button" class="v-btn v-size--default theme--light v-btn--has-bg" @click="showModal = true">Create Account</button>
          <button type="submit" class="v-btn v-size--default theme--light v-btn--has-bg">Login</button>
        </div>
      </form>
      <a href="#" @click="forgotPassword">Forgot Password?</a>
    </div>
    <dynamic-modal
      :visible="showModal"
      title="Create Account"
      @update:visible="showModal = $event"
      :onSubmit="createAccount"
    >
      <form @submit.prevent="createAccount">
        <input type="text" v-model="newAccount.username" placeholder="New Username" required>
        <input type="password" v-model="newAccount.password" placeholder="Password" required>
        <input type="password" v-model="newAccount.confirmPassword" placeholder="Confirm Password" required>
      </form>
    </dynamic-modal>
  </div>
</template>

<script>
import { userLogin, setAuthToken, registerUser } from '../services/apiService';
import DynamicModal from '../components/DynamicModal.vue';

export default {
  name: 'AppLogin',
  components: {
    DynamicModal
  },
  props: {
    msg: String
  },
  data() {
    return {
      username: '',
      password: '',
      showModal: false,
      newAccount: {
        username: '',
        password: '',
        confirmPassword: ''
      }
    };
  },
  methods: {
    async login() {
  try {
    const response = await userLogin(this.username, this.password);
    const token = response.data.token;
    localStorage.setItem('user-token', token);
    setAuthToken(token);

    // Navigate to 'Item Dashboard' route and pass the token as a meta field
    this.$router.push({ name: 'Item Dashboard', params: { token: token } });
  } catch (error) {
    console.error('Error logging in:', error.response.data);
    alert('Failed to login: ' + error.response.data.error);
    this.username = '';
    this.password = '';
  }
},
    async createAccount() {
      // Basic checks for empty fields
    if (!this.newAccount.username || !this.newAccount.password || !this.newAccount.confirmPassword) {
      alert('Please fill in all fields.');
      return;
    }
    // Check for password match
    if (this.newAccount.password !== this.newAccount.confirmPassword) {
      alert('Passwords do not match!');
      return;
    }
    // Example of adding a simple password complexity check
    if (this.newAccount.password.length < 8) {
      alert('Password must be at least 8 characters long.');
      return;
    }
    // Regular expression for password complexity: must contain letters and numbers
    if (!/(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}/.test(this.newAccount.password)) {
      alert('Password must contain at least one number, one lowercase and one uppercase letter.');
      return;
    }
    try {
      // Attempt to register the user
      await registerUser(this.newAccount.username, this.newAccount.password);
      alert('Registration successful! Please log in.');
      this.showModal = false;
      this.newAccount = { username: '', password: '', confirmPassword: '' };
      // Optionally redirect to login or other component
      this.$router.push('/login');
      } catch (error) {
        console.error('Registration failed:', error.response.data);
        alert('Failed to register: ' + (error.response && error.response.data.error ? error.response.data.error : 'Unknown error'));
      }
    },
    forgotPassword() {
      this.$router.push('/forgot-password');
    }
  }
}
</script>

<style scoped>
.login-container {
  font-family: Roboto, sans-serif !important;
  max-width: 400px;
  margin: 0 auto;
}
.logo {
  margin-top: 20px;
  max-width: 94%;
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}
h1 {
  margin-bottom: 20px;
}
.form-group {
  margin-bottom: 15px;
  display: flex;
  justify-content: space-between;
}
/* Base styles for text and password input fields */
input[type="text"],
input[type="password"] {
  width: calc(50% - 10px);
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  max-height: 32px;
  flex: 1 1 auto;
  line-height: 20px;
  font: inherit;
  appearance: auto;
}

/* Styles for focused text and password input fields */
input[type="text"]:focus,
input[type="password"]:focus {
  outline: none;
  border: 0.5px solid #000;
  border-radius: 4px;
  /* Add thicker bottom border */
  border-bottom: 3px solid #007bff; /* Start with thin bottom border */
  position: relative;
  transition: border-color 0.5s ease-in-out; /* Apply transition to border-color only */
}

/* Add pseudo-element for the bottom border animation */
input[type="text"]:focus::after,
input[type="password"]:focus::after {
  content: ""; /* Ensure content is not null */
  position: absolute;
  bottom: -1px; /* Adjust to position the border correctly */
  left: 0;
  right: 0;
  width: 100%; /* Full width */
  height: 3px; /* Height of the bottom border */
  background-color: #007bff; /* Color of the bottom border */
  transform: scaleX(0); /* Start with scale 0 */
  transition: transform 0.5s ease-in-out; /* Apply transition to transform for animation */
  z-index: -1; /* Ensure it does not overlay the text field */
}

/* Adjust pseudo-element width when focused */
input[type="text"]:focus::after,
input[type="password"]:focus::after {
  width: 100%; /* Full width when focused */
  left: 0; /* Align to the left */
  transform: scaleX(1); /* Center horizontally */
}

.v-btn {
  height: 36px;
  font-family: Montserrat !important;
  min-width: 40%;
  padding: 0 16px;
  font: inherit;
  letter-spacing: 10% !important;
  font-size: .875rem;
  color: rgba(0, 0, 0, .87);
  border-radius: 4px;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  text-transform: uppercase;
  background-color: #f5f5f5;
  border: none;
  cursor: pointer;
  transition-duration: .28s;
  transition-property: box-shadow, transform, opacity;
  transition-timing-function: cubic-bezier(.4, 0, .2, 1);
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  vertical-align: middle;
  white-space: nowrap;
  box-shadow: 0 3px 6px 0 rgba(0, 0, 0, .15);
}
.v-btn:hover {
  box-shadow: 0 3px 1px -2px rgba(0, 0, 0, .2), 0 2px 2px 0 rgba(0, 0, 0, .14), 0 1px 5px 0 rgba(0, 0, 0, .12);
}
.v-btn:before {
  background-color: currentColor;
  border-radius: inherit;
  bottom: 0;
  color: inherit;
  content: "";
  left: 0;
  opacity: 0;
  pointer-events: none;
  position: absolute;
  right: 0;
  top: 0;
  transition: opacity .2s cubic-bezier(.4, 0, .6, 1);
}
.v-btn--is-elevated {
  box-shadow: 0 3px 1px -2px rgba(0, 0, 0, .2), 0 2px 2px 0 rgba(0, 0, 0, .14), 0 1px 5px 0 rgba(0, 0, 0, .12);
}
.theme--light.v-btn {
  color: rgba(0, 0, 0, .87);
}
.v-btn--is-elevated:active {
  box-shadow: 0 5px 5px -3px rgba(0, 0, 0, .2), 0 8px 10px 1px rgba(0, 0, 0, .14), 0 3px 14px 2px rgba(0, 0, 0, .12);
}
a {
  font-family: Montserrat !important;
  color: #007bff; 
  padding-top: 15px;
  text-decoration: none;
  cursor: pointer;
  float: left;
  line-height: 1.5px;
  text-decoration-line: underline;
}
</style>
