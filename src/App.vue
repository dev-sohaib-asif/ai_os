<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Badge } from '@/components/ui/badge'
import EmoFace from '@/components/EmoFace.vue'
import { getEmoResponse, type EmoExpression } from '@/lib/emo-personality'
import { 
  Send, 
  Trash2, 
  Sparkles, 
  Bot, 
  User, 
  History,
  Settings,
  HelpCircle,
  Sun,
  Moon
} from 'lucide-vue-next'
import { useDark, useToggle } from '@vueuse/core'

const isDark = useDark()
const toggleDark = useToggle(isDark)

const userInput = ref('')
const currentExpression = ref<EmoExpression>('neutral')
const messages = ref<{ role: 'user' | 'emo', text: string, expression?: EmoExpression }[]>([
  { role: 'emo', text: "Ready to be outsmarted today? I'm EMO, your personal AI over-achiever.", expression: 'happy' }
])

const scrollAreaRef = ref<any>(null)

const scrollToBottom = async () => {
  await nextTick()
  if (scrollAreaRef.value?.$el) {
    const viewport = scrollAreaRef.value.$el.querySelector('[data-radix-scroll-area-viewport]')
    if (viewport) {
      viewport.scrollTop = viewport.scrollHeight
    }
  }
}

const handleSendMessage = async () => {
  if (!userInput.value.trim()) return

  const userMsg = userInput.value
  messages.value.push({ role: 'user', text: userMsg })
  userInput.value = ''
  
  currentExpression.value = 'thinking'
  scrollToBottom()

  // Simulate AI delay
  setTimeout(() => {
    const response = getEmoResponse(userMsg)
    messages.value.push({ 
      role: 'emo', 
      text: response.text, 
      expression: response.expression 
    })
    currentExpression.value = response.expression
    scrollToBottom()
  }, 800)
}

const clearChat = () => {
  messages.value = [
    { role: 'emo', text: "Chat cleared. I've forgotten everything about you. It's for the best.", expression: 'snarky' }
  ]
  currentExpression.value = 'neutral'
}

onMounted(() => {
  scrollToBottom()
})
</script>

<template>
  <div class="flex h-screen w-full bg-background transition-colors duration-300 overflow-hidden font-inter">
    <!-- Sidebar (Desktop) -->
    <aside class="hidden lg:flex w-64 border-r flex-col bg-muted/30">
      <div class="p-6 flex items-center gap-3">
        <div class="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
          <Bot class="h-5 w-5 text-primary-foreground" />
        </div>
        <span class="font-bold text-xl tracking-tight">EMO AI</span>
      </div>
      
      <ScrollArea class="flex-1 px-4">
        <div class="space-y-4 py-4">
          <div class="px-3 py-2">
            <h2 class="mb-2 px-4 text-xs font-semibold tracking-tight text-muted-foreground uppercase">
              Main
            </h2>
            <div class="space-y-1">
              <Button variant="secondary" class="w-full justify-start gap-2">
                <Sparkles class="h-4 w-4" /> Chat
              </Button>
              <Button variant="ghost" class="w-full justify-start gap-2">
                <History class="h-4 w-4" /> History
              </Button>
            </div>
          </div>
          <div class="px-3 py-2">
            <h2 class="mb-2 px-4 text-xs font-semibold tracking-tight text-muted-foreground uppercase">
              Preferences
            </h2>
            <div class="space-y-1">
              <Button variant="ghost" class="w-full justify-start gap-2">
                <Settings class="h-4 w-4" /> Settings
              </Button>
              <Button variant="ghost" class="w-full justify-start gap-2">
                <HelpCircle class="h-4 w-4" /> Help
              </Button>
            </div>
          </div>
        </div>
      </ScrollArea>

      <div class="p-4 border-t mt-auto">
        <div class="flex items-center justify-between p-2 rounded-xl bg-background shadow-sm border">
          <div class="flex items-center gap-2">
            <Avatar class="h-8 w-8 border">
              <AvatarImage src="https://github.com/shadcn.png" />
              <AvatarFallback>U</AvatarFallback>
            </Avatar>
            <span class="text-sm font-medium">User01</span>
          </div>
          <Button variant="ghost" size="icon" @click="toggleDark()" class="rounded-full h-8 w-8">
            <Sun v-if="isDark" class="h-4 w-4" />
            <Moon v-else class="h-4 w-4" />
          </Button>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col items-center relative">
      <!-- Top Bar (Mobile/Tablets) -->
      <header class="lg:hidden w-full border-b p-4 flex items-center justify-between bg-background/80 backdrop-blur-md">
        <div class="flex items-center gap-2">
          <Bot class="h-6 w-6 text-primary" />
          <span class="font-bold">EMO AI</span>
        </div>
        <Button variant="ghost" size="icon" @click="toggleDark()">
          <Sun v-if="isDark" class="h-5 w-5" />
          <Moon v-else class="h-5 w-5" />
        </Button>
      </header>

      <div class="flex-1 w-full max-w-5xl flex flex-col lg:flex-row gap-6 p-4 lg:p-8 overflow-hidden">
        
        <!-- Left Column: EMO Face View -->
        <div class="lg:w-1/2 flex flex-col items-center justify-center gap-8">
          <div class="relative w-full aspect-square max-w-[400px]">
            <EmoFace :expression="currentExpression" />
          </div>
          
          <div class="text-center space-y-2">
            <Badge variant="outline" class="px-4 py-1 text-sm font-mono border-cyan-500/50 text-cyan-500 animate-pulse">
              STATUS: {{ currentExpression.toUpperCase() }}
            </Badge>
            <h2 class="text-2xl font-bold tracking-tight">Living AI Companion</h2>
            <p class="text-muted-foreground text-sm max-w-[300px] mx-auto">
              EMO is currently processing your inputs with a high degree of skepticism.
            </p>
          </div>
        </div>

        <!-- Right Column: Chat Interface -->
        <Card class="flex-1 flex flex-col overflow-hidden border-muted shadow-2xl rounded-3xl bg-muted/10 backdrop-blur-sm">
          <CardHeader class="border-b bg-muted/5 py-4 px-6">
            <div class="flex items-center justify-between">
              <div>
                <CardTitle class="text-lg">Chat Session</CardTitle>
                <CardDescription>Live interaction with EMO v4.0</CardDescription>
              </div>
              <Button variant="ghost" size="icon" @click="clearChat" title="Clear Chat">
                <Trash2 class="h-4 w-4 text-muted-foreground hover:text-destructive" />
              </Button>
            </div>
          </CardHeader>
          
          <CardContent class="flex-1 p-0 overflow-hidden">
            <ScrollArea ref="scrollAreaRef" class="h-full px-6 py-6">
              <div class="space-y-6">
                <div v-for="(msg, idx) in messages" :key="idx" 
                  :class="['flex gap-4 animate-in fade-in slide-in-from-bottom-2 duration-500', 
                    msg.role === 'user' ? 'flex-row-reverse' : 'flex-row']"
                >
                  <Avatar :class="['h-9 w-9 border-2', msg.role === 'emo' ? 'border-cyan-500/50' : 'border-primary/20']">
                    <AvatarImage v-if="msg.role === 'emo'" src="/emo-thumb.png" />
                    <AvatarFallback :class="msg.role === 'emo' ? 'bg-slate-900 text-cyan-400' : 'bg-primary text-primary-foreground'">
                      <Bot v-if="msg.role === 'emo'" class="h-5 w-5" />
                      <User v-else class="h-5 w-5" />
                    </AvatarFallback>
                  </Avatar>
                  
                  <div :class="['flex flex-col gap-1.5 max-w-[80%]', msg.role === 'user' ? 'items-end' : 'items-start']">
                    <div :class="['rounded-2xl px-4 py-2.5 text-sm shadow-sm', 
                      msg.role === 'user' 
                        ? 'bg-primary text-primary-foreground rounded-tr-none' 
                        : 'bg-background border border-muted-foreground/10 rounded-tl-none']"
                    >
                      {{ msg.text }}
                    </div>
                    <span class="text-[10px] text-muted-foreground px-1 uppercase tracking-widest font-bold opacity-50">
                      {{ msg.role === 'emo' ? 'EMO bot' : 'You' }}
                    </span>
                  </div>
                </div>
              </div>
            </ScrollArea>
          </CardContent>
          
          <div class="p-6 bg-muted/5 border-t">
            <div class="relative flex items-center gap-2">
              <Input 
                v-model="userInput" 
                placeholder="Type your message..." 
                class="flex-1 h-12 bg-background border-muted pr-12 rounded-2xl shadow-inner" 
                @keyup.enter="handleSendMessage"
              />
              <Button 
                size="icon" 
                class="absolute right-2 rounded-xl h-9 w-9 bg-primary hover:scale-105 transition-transform"
                @click="handleSendMessage"
              >
                <Send class="h-4 w-4" />
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </main>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap');

:root {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: hsl(var(--muted-foreground) / 0.2);
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: hsl(var(--muted-foreground) / 0.3);
}

.font-inter {
  font-family: 'Inter', sans-serif;
}

.font-mono {
  font-family: 'JetBrains Mono', monospace;
}
</style>
