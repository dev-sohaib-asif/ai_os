<script setup lang="ts">
import { computed } from 'vue'
import type { EmoExpression } from '@/lib/emo-personality'

const props = defineProps<{
  expression: EmoExpression
}>()

// SVG values for different expressions
const eyes = computed(() => {
  switch (props.expression) {
    case 'happy':
      return { 
        left: 'M 30 45 Q 40 35 50 45', 
        right: 'M 70 45 Q 80 35 90 45',
        mouth: 'M 45 70 Q 60 85 75 70'
      }
    case 'sad':
      return { 
        left: 'M 30 50 Q 40 45 50 50', 
        right: 'M 70 50 Q 80 45 90 50',
        mouth: 'M 45 80 Q 60 70 75 80'
      }
    case 'angry':
      return { 
        left: 'M 30 45 L 50 55', 
        right: 'M 70 55 L 90 45',
        mouth: 'M 50 80 L 70 80'
      }
    case 'surprised':
      return { 
        left: 'circle(5 at 40 45)', 
        right: 'circle(5 at 80 45)',
        mouth: 'M 55 75 Q 60 85 65 75'
      }
    case 'love':
      return { 
        left: 'M 30 45 Q 40 30 50 45 Q 40 60 30 45', 
        right: 'M 70 45 Q 80 30 90 45 Q 80 60 70 45',
        mouth: 'M 45 75 Q 60 90 75 75'
      }
    case 'dead':
      return { 
        left: 'M 35 40 L 45 50 M 45 40 L 35 50', 
        right: 'M 75 40 L 85 50 M 85 40 L 75 50',
        mouth: 'M 50 80 L 70 80'
      }
    case 'cool':
      return { 
        left: 'rect(30, 40, 20, 10)', 
        right: 'rect(70, 40, 20, 10)',
        mouth: 'M 50 80 Q 60 75 70 80'
      }
    case 'sleepy':
      return { 
        left: 'M 30 50 L 50 50', 
        right: 'M 70 50 L 90 50',
        mouth: 'M 55 75 Q 60 78 65 75'
      }
    case 'snarky':
      return { 
        left: 'M 30 45 Q 40 40 50 45', 
        right: 'M 70 45 L 90 40',
        mouth: 'M 60 80 Q 70 78 75 80'
      }
    case 'thinking':
      return { 
        left: 'M 30 40 Q 40 38 50 40', 
        right: 'M 70 50 Q 80 48 90 50',
        mouth: 'M 50 85 Q 60 85 70 85'
      }
    case 'laughter':
      return {
        left: 'M 30 45 Q 40 35 50 45', 
        right: 'M 70 45 Q 80 35 90 45',
        mouth: 'M 40 75 Q 60 95 80 75 L 40 75'
      }
    case 'bored':
      return {
        left: 'M 30 45 L 50 45', 
        right: 'M 70 45 L 90 45',
        mouth: 'M 50 85 L 70 85'
      }
    case 'excited':
      return {
        left: 'M 30 40 L 40 30 L 50 40', 
        right: 'M 70 40 L 80 30 L 90 40',
        mouth: 'M 40 75 Q 60 95 80 75'
      }
    case 'confused':
      return {
        left: 'M 30 45 Q 40 40 50 50', 
        right: 'M 70 50 Q 80 40 90 45',
        mouth: 'M 55 85 Q 60 80 65 85'
      }
    case 'nervous':
      return {
        left: 'M 35 45 Q 40 42 45 45', 
        right: 'M 75 45 Q 80 42 85 45',
        mouth: 'M 45 80 L 50 85 L 55 80 L 60 85 L 65 80 L 70 85 L 75 80'
      }
    case 'ghost':
      return {
        left: 'M 30 45 Q 40 45 50 45', 
        right: 'M 70 45 Q 80 45 90 45',
        mouth: 'M 45 75 Q 60 100 75 75'
      }
    case 'newspaper':
      return {
        left: 'M 30 45 L 45 45 L 45 55 L 30 55 Z',
        right: 'M 75 45 L 90 45 L 90 55 L 75 55 Z',
        mouth: 'M 50 80 L 70 80'
      }
    case 'headphones':
      return {
        left: 'M 35 45 Q 40 35 45 45', 
        right: 'M 75 45 Q 80 35 85 45',
        mouth: 'M 50 80 Q 60 90 70 80'
      }
    case 'celebration':
      return {
        left: 'M 35 40 L 45 40', 
        right: 'M 75 40 L 85 40',
        mouth: 'M 40 80 Q 60 100 80 80'
      }
    case 'smart':
      return {
        left: 'M 30 40 L 50 40 L 50 50 L 30 50 Z', 
        right: 'M 70 40 L 90 40 L 90 50 L 70 50 Z',
        mouth: 'M 55 80 L 65 80'
      }
    case 'neutral':
    default:
      return { 
        left: 'M 35 50 Q 40 48 45 50', 
        right: 'M 75 50 Q 80 48 85 50',
        mouth: 'M 55 80 L 65 80'
      }
  }
})

const color = computed(() => {
  if (props.expression === 'angry') return 'text-red-500'
  if (props.expression === 'love') return 'text-pink-500'
  if (props.expression === 'sleepy') return 'text-blue-200'
  if (props.expression === 'dead') return 'text-gray-500'
  if (props.expression === 'ghost') return 'text-purple-400'
  return 'text-cyan-400'
})

const bgGlow = computed(() => {
   if (props.expression === 'angry') return 'bg-red-500/20'
   if (props.expression === 'love') return 'bg-pink-500/20'
   return 'bg-cyan-500/20'
})

</script>

<template>
  <div class="relative flex items-center justify-center aspect-square w-full max-w-[300px] mx-auto group">
    <!-- Glow Effect -->
    <div :class="['absolute inset-0 rounded-3xl blur-3xl transition-all duration-500', bgGlow]"></div>
    
    <!-- Robot Head Frame -->
    <div class="relative w-full h-full bg-slate-900 rounded-[40px] border-4 border-slate-800 shadow-2xl overflow-hidden p-8 flex items-center justify-center">
      <!-- Screen Background -->
      <div class="absolute inset-2 bg-black rounded-[32px] overflow-hidden">
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(0,255,255,0.05)_0%,transparent_100%)]"></div>
        <div class="absolute inset-0 grid grid-cols-[repeat(20,minmax(0,1fr))] opacity-[0.03]">
          <div v-for="i in 400" :key="i" class="border-[0.5px] border-white/20 aspect-square"></div>
        </div>
      </div>

      <!-- Eyes and Mouth SVG -->
      <svg viewBox="0 0 120 120" class="relative w-full h-full drop-shadow-[0_0_8px_currentColor]" :class="color">
        <!-- Left Eye -->
        <template v-if="expression === 'surprised'">
          <circle cx="40" cy="45" r="5" fill="currentColor" />
        </template>
        <template v-else-if="expression === 'smart' || expression === 'newspaper' || expression === 'cool'">
           <path v-if="expression === 'cool'" d="M 25 40 L 55 40 L 55 55 L 25 55 Z" fill="currentColor" />
           <path v-else :d="eyes.left" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" />
        </template>
        <path v-else :d="eyes.left" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" />

        <!-- Right Eye -->
        <template v-if="expression === 'surprised'">
          <circle cx="80" cy="45" r="5" fill="currentColor" />
        </template>
        <template v-else-if="expression === 'smart' || expression === 'newspaper' || expression === 'cool'">
           <path v-if="expression === 'cool'" d="M 65 40 L 95 40 L 95 55 L 65 55 Z" fill="currentColor" />
           <path v-else :d="eyes.right" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" />
        </template>
        <path v-else :d="eyes.right" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" />

        <!-- Mouth -->
        <path :d="eyes.mouth" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />
        
        <!-- Accessories -->
        <!-- Headphones -->
        <template v-if="expression === 'headphones'">
           <path d="M 15 60 Q 15 10 60 10 Q 105 10 105 60" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" class="opacity-50" />
           <rect x="5" y="55" width="15" height="30" rx="4" fill="currentColor" class="opacity-50" />
           <rect x="100" y="55" width="15" height="30" rx="4" fill="currentColor" class="opacity-50" />
        </template>
        
        <!-- Celebration Hat -->
        <template v-if="expression === 'celebration'">
           <path d="M 40 20 L 60 0 L 80 20 Z" fill="currentColor" class="opacity-50" />
        </template>

        <!-- Ghost trail -->
        <template v-if="expression === 'ghost'">
           <circle cx="60" cy="60" r="45" fill="currentColor" class="opacity-10 animate-pulse" />
        </template>
      </svg>
    </div>
    
    <!-- Ears/Sensors -->
    <div class="absolute -left-4 top-1/2 -translate-y-1/2 w-8 h-12 bg-slate-800 rounded-l-lg border-y-2 border-l-2 border-slate-700"></div>
    <div class="absolute -right-4 top-1/2 -translate-y-1/2 w-8 h-12 bg-slate-800 rounded-r-lg border-y-2 border-r-2 border-slate-700"></div>
  </div>
</template>

<style scoped>
svg path {
  transition: d 0.3s ease-in-out, stroke 0.3s ease-in-out;
}
</style>
