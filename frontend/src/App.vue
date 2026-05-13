<script setup>
import { ref, markRaw, nextTick } from 'vue'
import { VueFlow, useVueFlow } from '@vue-flow/core'
import '@vue-flow/core/dist/style.css'

import SkillNode from './components/SkillNode.vue'
import SkillSidebar from './components/SkillSidebar.vue'
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const { fitView } = useVueFlow()

const nodes = ref([])
const edges = ref([])
const xp = ref(0)
const subject = ref('')
const isLoading = ref(false)
const selectedNode = ref(null)

const nodeTypes = {
  skill: markRaw(SkillNode)
}

function calculateLayout(rawNodes) {
  // Simple depth-based layout
  const nodeMap = new Map(rawNodes.map(n => [n.id, n]))
  const depths = new Map()

  function getDepth(id) {
    if (depths.has(id)) return depths.get(id)
    const node = nodeMap.get(id)
    if (!node || !node.prerequisites || node.prerequisites.length === 0) {
      depths.set(id, 0)
      return 0
    }
    const d = Math.max(...node.prerequisites.map(p => getDepth(p))) + 1
    depths.set(id, d)
    return d
  }

  rawNodes.forEach(n => getDepth(n.id))

  const depthGroups = {}
  rawNodes.forEach(n => {
    const d = depths.get(n.id)
    if (!depthGroups[d]) depthGroups[d] = []
    depthGroups[d].push(n)
  })

  return rawNodes.map(node => {
    const d = depths.get(node.id)
    const indexInDepth = depthGroups[d].indexOf(node)
    return {
      id: node.id,
      type: 'skill',
      position: {
        x: d * 400 + 50,
        y: indexInDepth * 300 + 100
      },
      data: {
        label: node.title,
        description: node.description,
        status: node.prerequisites.length === 0 ? 'available' : 'locked',
        prerequisites: node.prerequisites
      }
    }
  })
}

function onNodeClick(event) {
  selectedNode.value = event.node
}

function completeNode() {
  if (!selectedNode.value) return

  selectedNode.value.data.status = 'completed'
  xp.value += 50

  // Unlock logic
  nodes.value.forEach((node) => {
    if (node.data.status === 'locked') {
      const allCompleted = node.data.prerequisites.every((preId) => {
        const preNode = nodes.value.find((n) => n.id === preId)
        return preNode && preNode.data.status === 'completed'
      })
      if (allCompleted) {
        node.data.status = 'available'
      }
    }
  })
}

async function generateTree() {
  if (!subject.value) return
  isLoading.value = true
  
  try {
    const response = await fetch('http://localhost:8000/generate-skill-tree', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ subject: subject.value })
    })

    const data = await response.json()
    nodes.value = calculateLayout(data.nodes)
    
    edges.value = []
    data.nodes.forEach((node) => {
      node.prerequisites.forEach((pre) => {
        edges.value.push({
          id: `e${pre}-${node.id}`,
          source: pre,
          target: node.id,
          animated: true
        })
      })
    })

    await nextTick()
    setTimeout(() => fitView(), 100)
  } catch (err) {
    console.error("Failed to generate tree:", err)
    alert("Error generating roadmap. Check backend console.")
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="container">
    <div class="flow-area">
      <div class="xp-bar">
        <span class="label">RANK: NOVICE</span>
        <div class="xp-val">{{ xp }} XP</div>
      </div>
      
      <div class="top-bar">
        <div class="search-box">
          <input
            v-model="subject"
            placeholder="What do you want to learn?"
            @keyup.enter="generateTree"
          />
          <button @click="generateTree" :disabled="isLoading">
            <span v-if="isLoading">GENERATING...</span>
            <span v-else>GENERATE ROADMAP</span>
          </button>
        </div>
      </div>

      <VueFlow
        :nodes="nodes"
        :edges="edges"
        :node-types="nodeTypes"
        fit-view-on-init
        @node-click="onNodeClick"
      >
        <template #background>
          <div class="custom-bg"></div>
        </template>
      </VueFlow>
    </div>

    <SkillSidebar
      :node="selectedNode"
      @complete="completeNode"
    />
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

.container {
  display: flex;
  width: 100vw;
  height: 100vh;
  background: #0a0a0f;
  font-family: 'Inter', sans-serif;
}

.flow-area {
  flex: 1;
  position: relative;
}

.xp-bar {
  position: absolute;
  top: 30px;
  left: 10px;
  z-index: 1000;
  background: rgba(17, 24, 39, 0.8);
  backdrop-filter: blur(10px);
  padding: 15px 25px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.xp-bar .label {
  font-size: 0.65rem;
  font-weight: 800;
  color: #64748b;
  letter-spacing: 2px;
  display: block;
  margin-bottom: 4px;
}

.xp-bar .xp-val {
  color: #39ff14;
  font-weight: 800;
  font-size: 1.4rem;
  text-shadow: 0 0 10px rgba(57, 255, 20, 0.3);
}

.top-bar {
  position: absolute;
  top: 30px;
  right: 10px;
  z-index: 1000;
}

.search-box {
  display: flex;
  gap: 10px;
  background: rgba(17, 24, 39, 0.8);
  backdrop-filter: blur(10px);
  padding: 8px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.search-box input {
  padding: 12px 20px;
  width: 300px;
  background: transparent;
  border: none;
  color: white;
  font-weight: 600;
  outline: none;
}

.search-box button {
  padding: 12px 25px;
  border: none;
  border-radius: 12px;
  background: #bc13fe;
  color: white;
  font-weight: 800;
  font-size: 0.8rem;
  letter-spacing: 1px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 0 15px rgba(188, 19, 254, 0.3);
}

.search-box button:hover:not(:disabled) {
  background: #d437ff;
  transform: translateY(-2px);
  box-shadow: 0 0 25px rgba(188, 19, 254, 0.5);
}

.search-box button:disabled {
  opacity: 0.5;
  cursor: wait;
}

.custom-bg {
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(circle at 2px 2px, rgba(255,255,255,0.05) 1px, transparent 0);
  background-size: 40px 40px;
}
</style>