<template>
  <div v-if="visible" class="modal-overlay">
    <div class="modal-window">
      <div class="modal-header">
        <h5>{{ title }}</h5>
        <button @click="closeModal">X</button>
      </div>
      <div class="modal-body">
        <slot></slot>
      </div>
      <div class="modal-footer">
        <button @click="handleSave">Save</button>
        <button @click="closeModal">Cancel</button>
      </div>
    </div>
  </div>
</template>
  
<script>
export default {
  name: 'DynamicModal',
  props: {
    visible: {
      type: Boolean,
      required: true
    },
    title: {
      type: String,
      default: 'Modal Title'
    },
    onSubmit: {
      type: Function,
      required: true
    }
  },
  methods: {
    closeModal() {
      this.$emit('update:visible', false);
    },
    handleSave() {
      if (typeof this.onSubmit === 'function') {
        this.onSubmit(); // Execute the function passed as onSubmit
      } else {
        console.error('onSubmit is not a function or not provided');
      }
    }
  }
}
</script>
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.6);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10;
  }
  
  .modal-window {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0,0,0,0.25);
    width: 90%;
    max-width: 500px;
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .modal-header h5 {
    margin: 0;
  }
  
  .modal-body {
    margin-top: 20px;
  }
  
  .modal-footer {
    display: flex;
    justify-content: flex-end;
    margin-top: 20px;
  }
  
  .modal-footer button {
    margin-left: 10px;
  }
  </style>
  