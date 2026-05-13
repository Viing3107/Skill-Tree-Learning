<script setup>
defineProps({
  node: Object
})
defineEmits(['complete'])
</script>

<template>
  <div class="sidebar" :class="{ active: node }">
    <div v-if="node" class="sidebar-content">
      <div class="category">SKILL DETAILS</div>
      <h1>{{ node.data.label }}</h1>
      
      <div class="status-badge" :class="node.data.status">
        {{ node.data.status.toUpperCase() }}
      </div>

      <p class="description">
        {{ node.data.description || 'No description available for this skill.' }}
      </p>

      <div class="meta">
        <div class="meta-item">
          <span class="label">REWARD:</span>
          <span class="value">+50 XP</span>
        </div>
      </div>

      <button
        v-if="node.data.status === 'available'"
        class="btn-complete"
        @click="$emit('complete')"
      >
        MARK AS COMPLETED
      </button>
      
      <div v-else-if="node.data.status === 'locked'" class="locked-msg">
        ⚠️ Complete prerequisites to unlock this skill.
      </div>

      <div v-else-if="node.data.status === 'completed'" class="completed-msg">
        ✨ You have mastered this skill!
      </div>
    </div>

    <div v-else class="empty-state">
      <div class="icon">🔍</div>
      <h2>Select a Node</h2>
      <p>Click on a skill to view details and track your progress.</p>
    </div>
  </div>
</template>

<style scoped>
.sidebar {
  width: 380px;
  height: 100vh;
  background: rgba(17, 17, 29, 0.95);
  backdrop-filter: blur(20px);
  border-left: 1px solid rgba(255, 255, 255, 0.1);
  padding: 40px 30px;
  box-sizing: border-box;
  color: white;
  z-index: 100;
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.sidebar-content {
  animation: slide-in 0.4s ease-out;
}

.category {
  color: var(--neon-cyan);
  font-size: 0.8rem;
  letter-spacing: 3px;
  margin-bottom: 10px;
  font-weight: 800;
}

h1 {
  margin: 0 0 20px 0;
  font-size: 2.2rem;
  line-height: 1.1;
  background: linear-gradient(to right, #fff, #94a3b8);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 800;
  margin-bottom: 30px;
  border: 1px solid currentColor;
}

.status-badge.available { color: #00f2ff; background: rgba(0, 242, 255, 0.1); }
.status-badge.completed { color: #39ff14; background: rgba(57, 255, 20, 0.1); }
.status-badge.locked { color: #ef4444; background: rgba(239, 68, 68, 0.1); }

.description {
  color: #94a3b8;
  font-size: 1.8rem;
  line-height: 1.7;
  font-size: 1.05rem;
  margin-bottom: 40px;
}

.meta {
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  padding-top: 20px;
  margin-bottom: 40px;
}

.meta-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.meta-item .label { color: #4b5563; font-weight: 700; font-size: 0.8rem; }
.meta-item .value { color: #39ff14; font-weight: 700; }

.btn-complete {
  width: 100%;
  padding: 18px;
  border: none;
  border-radius: 12px;
  background: var(--neon-cyan);
  color: #000;
  font-weight: 800;
  font-size: 0.9rem;
  letter-spacing: 1px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 0 20px rgba(0, 242, 255, 0.4);
}

.btn-complete:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 30px rgba(0, 242, 255, 0.6);
}

.locked-msg, .completed-msg {
  padding: 20px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
  text-align: center;
  font-weight: 600;
  color: #94a3b8;
}

.empty-state {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  color: #4b5563;
}

.empty-state .icon { font-size: 4rem; margin-bottom: 20px; opacity: 0.2; }
.empty-state h2 { color: #334155; }

@keyframes slide-in {
  from { transform: translateX(30px); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}
</style>