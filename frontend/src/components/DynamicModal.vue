<template>
  <!-- The modal overlay is shown when the `visible` prop is true -->
  <div v-if="visible" class="modal-overlay">
    <div class="modal-window">
      <div class="modal-header">
        <!-- The modal title is displayed using the `title` prop -->
        <h5>{{ title }}</h5>
        <!-- Button to close the modal -->
        <button @click="closeModal">X</button>
      </div>
      <div class="modal-body">
        <!-- Slot for the modal content -->
        <slot></slot>
      </div>
      <div class="modal-footer">
        <!-- Button to save/submit the modal -->
        <button @click="handleSave">Save</button>
        <!-- Button to cancel/close the modal -->
        <button @click="closeModal">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DynamicModal',
  props: {
    // Prop to control the visibility of the modal
    visible: {
      type: Boolean,
      required: true
    },
    // Prop for the modal title
    title: {
      type: String,
      default: 'Modal Title'
    },
    // Prop to pass a function to be executed when the modal is submitted
    onSubmit: {
      type: Function,
      required: true
    }
  },
  methods: {
    // Method to close the modal and emit an event to update the parent component
    closeModal() {
      this.$emit('update:visible', false);
    },
    // Method to handle the save/submit action of the modal
    handleSave() {
      // Check if the `onSubmit` prop is a function
      if (typeof this.onSubmit === 'function') {
        // Call the function passed as `onSubmit`
        this.onSubmit();
      } else {
        // Log an error if `onSubmit` is not a function or not provided
        console.error('onSubmit is not a function or not provided');
      }
    }
  }
}
</script>

<style scoped>
/* Styles for the modal overlay */
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

/* Styles for the modal window */
.modal-window {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0,0,0,0.25);
  width: 90%;
  max-width: 500px;
}

/* Styles for the modal header */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h5 {
  margin: 0;
}

/* Styles for the modal body */
.modal-body {
  margin-top: 20px;
}

/* Styles for the modal footer */
.modal-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

/* Styles for the modal footer buttons */
.modal-footer button {
  margin-left: 10px;
}
</style>
