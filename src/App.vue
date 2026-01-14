<script setup lang="ts">
import { ref } from 'vue'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { 
  Rocket, 
  Shield, 
  Zap, 
  Menu, 
  X, 
  Github, 
  Twitter, 
  Linkedin, 
  ArrowRight,
  CheckCircle2,
  ChevronRight,
  Sun,
  Moon
} from 'lucide-vue-next'
import { useDark, useToggle } from '@vueuse/core'

const isDark = useDark()
const toggleDark = useToggle(isDark)

const isMenuOpen = ref(false)
const email = ref('')

const features = [
  {
    title: 'Modern Architecture',
    description: 'Built with Vue 3, Vite, and TypeScript for the best developer experience and performance.',
    icon: Rocket,
    color: 'text-blue-500'
  },
  {
    title: 'Ready for Production',
    description: 'Pre-configured with Tailwind CSS 3.4 and shadcn-vue for building stunning interfaces.',
    icon: Shield,
    color: 'text-green-500'
  },
  {
    title: 'Lightning Fast',
    description: 'Blazing fast HMR and optimized builds ensure your application stays snappy.',
    icon: Zap,
    color: 'text-yellow-500'
  }
]

const stats = [
  { label: 'Downloads', value: '2.5M+' },
  { label: 'GitHub Stars', value: '45K+' },
  { label: 'Contributors', value: '1.2K+' },
  { label: 'Projects Built', value: '100K+' }
]
</script>

<template>
  <div class="min-h-screen transition-colors duration-300">
    <!-- Navigation -->
    <nav class="sticky top-0 z-50 w-full border-b bg-background/80 backdrop-blur-md">
      <div class="container flex h-16 items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
            <Rocket class="h-5 w-5 text-primary-foreground" />
          </div>
          <span class="text-xl font-bold tracking-tight">ViteVue</span>
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center gap-8">
          <a href="#" class="text-sm font-medium hover:text-primary transition-colors">Features</a>
          <a href="#" class="text-sm font-medium hover:text-primary transition-colors">Solutions</a>
          <a href="#" class="text-sm font-medium hover:text-primary transition-colors">Pricing</a>
          <a href="#" class="text-sm font-medium hover:text-primary transition-colors">Documentation</a>
        </div>

        <div class="flex items-center gap-4">
          <Button variant="ghost" size="icon" @click="toggleDark()" class="rounded-full">
            <Sun v-if="isDark" class="h-5 w-5" />
            <Moon v-else class="h-5 w-5" />
          </Button>
          <div class="hidden md:flex gap-2">
            <Button variant="ghost">Sign In</Button>
            <Button>Get Started</Button>
          </div>
          <Button variant="ghost" size="icon" class="md:hidden" @click="isMenuOpen = !isMenuOpen">
            <Menu v-if="!isMenuOpen" class="h-6 w-6" />
            <X v-else class="h-6 w-6" />
          </Button>
        </div>
      </div>

      <!-- Mobile Menu -->
      <div v-if="isMenuOpen" class="md:hidden border-t bg-background p-4 flex flex-col gap-4 animate-in slide-in-from-top duration-300">
        <a href="#" class="text-lg font-medium">Features</a>
        <a href="#" class="text-lg font-medium">Solutions</a>
        <a href="#" class="text-lg font-medium">Pricing</a>
        <a href="#" class="text-lg font-medium">Documentation</a>
        <hr />
        <Button variant="outline" class="w-full">Sign In</Button>
        <Button class="w-full">Get Started</Button>
      </div>
    </nav>

    <main>
      <!-- Hero Section -->
      <section class="relative py-20 overflow-hidden lg:py-32">
        <div class="absolute inset-0 -z-10 h-full w-full bg-background bg-[linear-gradient(to_right,#8080800a_1px,transparent_1px),linear-gradient(to_bottom,#8080800a_1px,transparent_1px)] bg-[size:14px_24px]">
          <div class="absolute left-0 right-0 top-0 -z-10 m-auto h-[310px] w-[310px] rounded-full bg-primary/20 opacity-20 blur-[100px]"></div>
        </div>
        
        <div class="container flex flex-col items-center text-center gap-8">
          <div class="inline-flex items-center rounded-full border bg-muted/50 px-3 py-1 text-sm font-medium animate-in fade-in zoom-in duration-1000">
            <span class="flex h-2 w-2 rounded-full bg-primary mr-2"></span>
            Exciting News: v4.0 is now in beta
            <ChevronRight class="ml-1 h-4 w-4" />
          </div>
          
          <h1 class="text-4xl font-extrabold tracking-tight sm:text-6xl md:text-7xl lg:text-8xl">
            Build <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600 dark:from-blue-400 dark:to-indigo-400">Faster</span> <br />
            Ship <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-pink-600 dark:from-purple-400 dark:to-pink-400">Better</span>
          </h1>
          
          <p class="max-w-[700px] text-lg text-muted-foreground sm:text-xl">
            The ultimate starter toolkit for building high-performance web applications with Vue, Tailwind CSS, and shadcn-ui. Fully responsive, accessible, and ready to go.
          </p>
          
          <div class="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
            <Button size="lg" class="px-8 flex gap-2">
              Start Building Now <ArrowRight class="h-4 w-4" />
            </Button>
            <Button variant="outline" size="lg" class="px-8 flex gap-2">
              <Github class="h-4 w-4" /> View on GitHub
            </Button>
          </div>

          <!-- Feature Cards -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16 w-full">
            <Card v-for="(feature, index) in features" :key="index" class="relative overflow-hidden group hover:shadow-lg transition-all border-muted">
              <div class="absolute top-0 right-0 p-4 transform translate-x-2 -translate-y-2 opacity-10 group-hover:translate-x-0 group-hover:translate-y-0 transition-transform duration-500">
                <component :is="feature.icon" class="h-16 w-16" />
              </div>
              <CardHeader>
                <div :class="['p-2 w-fit rounded-lg bg-muted', feature.color]">
                  <component :is="feature.icon" class="h-6 w-6" />
                </div>
                <CardTitle class="text-xl mt-4">{{ feature.title }}</CardTitle>
                <CardDescription class="text-base mt-2">
                  {{ feature.description }}
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      <!-- Stats Section -->
      <section class="border-y bg-muted/30 py-12">
        <div class="container">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div v-for="stat in stats" :key="stat.label" class="flex flex-col items-center gap-1">
              <span class="text-3xl font-bold tracking-tight">{{ stat.value }}</span>
              <span class="text-sm text-muted-foreground uppercase tracking-wider">{{ stat.label }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <section class="py-20 lg:py-32">
        <div class="container">
          <Card class="bg-primary text-primary-foreground overflow-hidden relative">
            <div class="absolute inset-0 -z-0 opacity-10">
              <div class="absolute right-0 top-0 h-64 w-64 rounded-full bg-white blur-[80px]"></div>
              <div class="absolute left-0 bottom-0 h-64 w-64 rounded-full bg-white blur-[80px]"></div>
            </div>
            
            <CardContent class="flex flex-col md:flex-row items-center justify-between gap-12 p-8 md:p-16 relative z-10">
              <div class="flex flex-col gap-4 text-center md:text-left max-w-[600px]">
                <h2 class="text-3xl font-bold tracking-tight sm:text-4xl md:text-5xl">Ready to transform your workflow?</h2>
                <p class="text-lg opacity-80 decoration-white/20 underline underline-offset-4 decoration-dotted">Join thousands of developers building amazing products every day.</p>
              </div>
              
              <div class="flex flex-col gap-4 w-full sm:w-[400px]">
                <div class="flex flex-col gap-2">
                  <Label for="email" class="text-primary-foreground">Email Address</Label>
                  <div class="flex gap-2">
                    <Input id="email" v-model="email" placeholder="you@example.com" class="bg-primary-foreground text-primary border-none focus-visible:ring-offset-primary" />
                    <Button variant="secondary" class="shrink-0">Subscribe</Button>
                  </div>
                </div>
                <p class="text-xs opacity-60 flex items-center gap-1 justify-center md:justify-start">
                  <CheckCircle2 class="h-3 w-3" /> No credit card required. Cancel anytime.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer class="border-t py-12 md:py-20">
      <div class="container grid grid-cols-1 md:grid-cols-4 gap-12">
        <div class="flex flex-col gap-4">
          <div class="flex items-center gap-2">
            <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
              <Rocket class="h-5 w-5 text-primary-foreground" />
            </div>
            <span class="text-xl font-bold tracking-tight">ViteVue</span>
          </div>
          <p class="text-sm text-muted-foreground max-w-[200px]">
            Building the future of the web, one component at a time.
          </p>
          <div class="flex gap-4">
            <Twitter class="h-5 w-5 text-muted-foreground hover:text-primary cursor-pointer transition-colors" />
            <Github class="h-5 w-5 text-muted-foreground hover:text-primary cursor-pointer transition-colors" />
            <Linkedin class="h-5 w-5 text-muted-foreground hover:text-primary cursor-pointer transition-colors" />
          </div>
        </div>
        
        <div class="flex flex-col gap-4">
          <h4 class="font-bold">Product</h4>
          <ul class="flex flex-col gap-2 text-sm text-muted-foreground">
            <li><a href="#" class="hover:text-primary transition-colors">Features</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Integrations</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Pricing</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Changelog</a></li>
          </ul>
        </div>

        <div class="flex flex-col gap-4">
          <h4 class="font-bold">Company</h4>
          <ul class="flex flex-col gap-2 text-sm text-muted-foreground">
            <li><a href="#" class="hover:text-primary transition-colors">About</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Blog</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Careers</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Contact</a></li>
          </ul>
        </div>

        <div class="flex flex-col gap-4">
          <h4 class="font-bold">Legal</h4>
          <ul class="flex flex-col gap-2 text-sm text-muted-foreground">
            <li><a href="#" class="hover:text-primary transition-colors">Privacy Policy</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Terms of Service</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Cookie Policy</a></li>
          </ul>
        </div>
      </div>
      <div class="container border-t mt-12 pt-8 flex items-center justify-between text-xs text-muted-foreground">
        <p>© 2026 ViteVue Inc. All rights reserved.</p>
        <p>Made with ❤️ in New York City</p>
      </div>
    </footer>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
}
</style>
