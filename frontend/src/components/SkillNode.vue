<script setup>
import { Handle, Position } from '@vue-flow/core'

defineProps({
  data: Object
})
</script>

<template>
  <div
    class="skill-node"
    :class="data.status"
  >
    <Handle type="target" :position="Position.Top" />
    
    <div class="glow-layer"></div>
    <div class="content">
      <div class="status-icon" v-if="data.status === 'completed'">✓</div>
      <div class="status-icon" v-else-if="data.status === 'locked'">🔒</div>
      <div class="label">{{ data.label }}</div>
    </div>

    <Handle type="source" :position="Position.Bottom" />
  </div>
</template>

<style scoped>
.skill-node {
  min-width: 160px;
  padding: 20px;
  border-radius: 16px;
  text-align: center;
  position: relative;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  background: rgba(17, 24, 39, 0.8);
  backdrop-filter: blur(8px);
  border: 2px solid rgba(255, 255, 255, 0.1);
  color: white;
  cursor: pointer;
  overflow: visible;
}

.glow-layer {
  position: absolute;
  inset: -2px;
  border-radius: 16px;
  z-index: -1;
  opacity: 0;
  transition: opacity 0.3s;
}

.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.label {
  font-weight: 700;
  font-size: 1.1rem;
}

.status-icon {
  font-size: 1.2rem;
}

/* States */
.locked {
  filter: grayscale(1);
  opacity: 0.5;
  cursor: not-allowed;
}

.available {
  border-color: #00f2ff;
  box-shadow: 0 0 15px rgba(0, 242, 255, 0.3), inset 0 0 10px rgba(0, 242, 255, 0.2);
}
.available .label {
  color: #00f2ff;
  text-shadow: 0 0 8px rgba(0, 242, 255, 0.5);
}
.available .glow-layer {
  opacity: 1;
  background: radial-gradient(circle at center, rgba(0, 242, 255, 0.15) 0%, transparent 70%);
}

.completed {
  border-color: #39ff14;
  box-shadow: 0 0 20px rgba(57, 255, 20, 0.4), inset 0 0 15px rgba(57, 255, 20, 0.2);
}
.completed .label {
  color: #39ff14;
  text-shadow: 0 0 8px rgba(57, 255, 20, 0.5);
}
.completed .status-icon {
  color: #39ff14;
}

.skill-node:hover:not(.locked) {
  transform: translateY(-5px) scale(1.05);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
}

.available:hover {
  box-shadow: 0 0 30px rgba(0, 242, 255, 0.6);
}

.completed:hover {
  box-shadow: 0 0 35px rgba(57, 255, 20, 0.7);
}

/* Vue Flow Handles */
:deep(.vue-flow__handle) {
  width: 8px;
  height: 8px;
  background: #4b5563;
  border: 2px solid #1f2937;
}

.available :deep(.vue-flow__handle) { background: #00f2ff; }
.completed :deep(.vue-flow__handle) { background: #39ff14; }
</style>