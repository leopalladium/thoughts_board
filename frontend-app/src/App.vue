<script setup>
import { ref, reactive, onMounted, nextTick, onUnmounted } from 'vue';
import axios from 'axios';

// --- State ---
const thoughts = ref([]);
const newThought = ref('');
const error = ref('');
const isLoading = ref(false);

// Холст и панорамирование/зум
const canvasRef = ref(null);
const sidebarWidth = 370;
const zoom = ref(1);
const pan = reactive({ x: 0, y: 0 });
const draggingCanvas = ref(false);
const dragStart = reactive({ x: 0, y: 0 });
const panStart = reactive({ x: 0, y: 0 });

// Позиции карточек
const positions = reactive({});
const draggingCardId = ref(null);
const dragCardOffset = reactive({ x: 0, y: 0 });

const backendUrl = 'https://api.klimentsi.live';

// --- Utils ---
function getRandomPosition() {
  const padding = 60;
  const w = window.innerWidth - sidebarWidth - 340 - padding;
  const h = window.innerHeight - 180 - padding;
  return {
    x: Math.random() * w + sidebarWidth + padding / 2,
    y: Math.random() * h + padding / 2,
  };
}

// --- API ---
async function fetchThoughts() {
  isLoading.value = true;
  error.value = '';
  try {
    // Corrected the URL to include the /thoughts/ endpoint
    const response = await axios.get(`${backendUrl}/thoughts/`);
    thoughts.value = response.data;
    await nextTick();
    for (const t of thoughts.value) {
      if (!positions[t.id]) positions[t.id] = getRandomPosition();
    }
  } catch (err) {
    error.value = 'Ошибка загрузки мыслей';
  } finally {
    isLoading.value = false;
  }
}

async function addThought() {
  if (!newThought.value.trim()) return;
  isLoading.value = true;
  error.value = '';
  try {
    const response = await axios.post(`${backendUrl}/thoughts/`, {
      content: newThought.value
    });
    thoughts.value.push(response.data);
    positions[response.data.id] = getRandomPosition();
    newThought.value = '';
    await nextTick();
    scrollToLastThought();
  } catch (err) {
    error.value = 'Ошибка добавления мысли';
  } finally {
    isLoading.value = false;
  }
}

function scrollToLastThought() {
  const lastId = thoughts.value[thoughts.value.length - 1]?.id;
  if (!lastId) return;
  const el = document.getElementById('thought-' + lastId);
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
  }
}


// --- Card Drag ---
function onCardMouseDown(e, id) {
  draggingCardId.value = id;
  const pos = positions[id];
  dragCardOffset.x = e.clientX - pos.x;
  dragCardOffset.y = e.clientY - pos.y;
  window.addEventListener('mousemove', onCardMouseMove);
  window.addEventListener('mouseup', onCardMouseUp);
  document.body.style.userSelect = 'none';
}
function onCardMouseMove(e) {
  if (draggingCardId.value !== null) {
    const id = draggingCardId.value;
    positions[id].x = (e.clientX - dragCardOffset.x);
    positions[id].y = (e.clientY - dragCardOffset.y);

    // --- Repulsion logic ---
    const minDist = 140; // минимальное расстояние между центрами карточек
    const repulseStrength = 0.18; // сила отталкивания

    const thisPos = positions[id];
    const thisRect = {
      x: thisPos.x,
      y: thisPos.y,
      w: 320,
      h: 120
    };
    for (const otherId in positions) {
      if (otherId == id) continue;
      const otherPos = positions[otherId];
      const otherRect = {
        x: otherPos.x,
        y: otherPos.y,
        w: 320,
        h: 120
      };
      // Центры карточек
      const cx1 = thisRect.x + thisRect.w / 2;
      const cy1 = thisRect.y + thisRect.h / 2;
      const cx2 = otherRect.x + otherRect.w / 2;
      const cy2 = otherRect.y + otherRect.h / 2;
      const dx = cx1 - cx2;
      const dy = cy1 - cy2;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < minDist && dist > 1) {
        // Смещаем другую карточку в сторону от текущей
        const overlap = minDist - dist;
        const nx = dx / dist;
        const ny = dy / dist;
        positions[otherId].x -= nx * overlap * repulseStrength;
        positions[otherId].y -= ny * overlap * repulseStrength;
      }
    }
  }
}
function onCardMouseUp() {
  draggingCardId.value = null;
  window.removeEventListener('mousemove', onCardMouseMove);
  window.removeEventListener('mouseup', onCardMouseUp);
  document.body.style.userSelect = '';
}

// --- Canvas Drag ---
function onCanvasMouseDown(e) {
  // Не начинать drag, если клик по карточке
  if (e.target.closest('article')) return;
  draggingCanvas.value = true;
  dragStart.x = e.clientX;
  dragStart.y = e.clientY;
  panStart.x = pan.x;
  panStart.y = pan.y;
  window.addEventListener('mousemove', onCanvasMouseMove);
  window.addEventListener('mouseup', onCanvasMouseUp);
  document.body.style.cursor = 'grabbing';
}
function onCanvasMouseMove(e) {
  if (draggingCanvas.value) {
    pan.x = panStart.x + (e.clientX - dragStart.x);
    pan.y = panStart.y + (e.clientY - dragStart.y);
  }
}
function onCanvasMouseUp() {
  draggingCanvas.value = false;
  window.removeEventListener('mousemove', onCanvasMouseMove);
  window.removeEventListener('mouseup', onCanvasMouseUp);
  document.body.style.cursor = '';
}

// --- Zoom ---
function onCanvasWheel(e) {
  if (e.ctrlKey || e.metaKey) return;
  e.preventDefault();
  const prevZoom = zoom.value;
  let delta = e.deltaY < 0 ? 1.1 : 0.9;
  let newZoom = Math.max(0.5, Math.min(2, zoom.value * delta));
  const mouseX = e.clientX - sidebarWidth;
  const mouseY = e.clientY;
  const wx = (mouseX - pan.x) / zoom.value;
  const wy = (mouseY - pan.y) / zoom.value;
  pan.x -= (newZoom - prevZoom) * wx;
  pan.y -= (newZoom - prevZoom) * wy;
  zoom.value = newZoom;
}

// --- Enter to send ---
function onTextareaKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey && !e.altKey && !e.metaKey) {
    e.preventDefault();
    addThought();
  }
}

// --- Автообновление мыслей ---
let refreshInterval = null;
onMounted(() => {
  fetchThoughts();
  refreshInterval = setInterval(fetchThoughts, 15000); // 15 секунд
});
onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval);
});

</script>

<template>
  <div class="flex h-screen w-screen overflow-hidden font-sans bg-gradient-to-br from-indigo-50 via-blue-50 to-white space-mono">
    <!-- Sidebar -->
    <aside class="w-[370px] min-w-[260px] max-w-full bg-white/90 border-r border-gray-200 shadow-lg flex flex-col px-8 py-8 z-20 fixed top-0 left-0 bottom-0 h-full">
      <header class="mb-8 border-b border-gray-200 pb-3">
        <h1 class="text-4xl font-extrabold text-indigo-700 leading-tight tracking-tight drop-shadow-sm select-none poiret lowercase">
          you'll<br>never<br>read
        </h1>
      </header>
      <form @submit.prevent="addThought" class="flex flex-col gap-4 mt-2">
        <textarea
          v-model="newThought"
          placeholder="your thought..."
          rows="3"
          required
          @keydown="onTextareaKeydown"
          class="resize-none rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-base text-gray-800 focus:outline-none focus:ring-2 focus:ring-indigo-200 shadow space-mono"
        ></textarea>
        <div class="flex gap-2 w-full">
          <button
            type="submit"
            :disabled="isLoading"
            class="rounded-xl bg-gradient-to-r from-indigo-400 to-indigo-200 text-white font-bold py-2.5 px-6 shadow hover:from-indigo-500 transition disabled:opacity-60 space-mono flex-1"
            style="min-width: 0;"
          >
            {{ isLoading ? '...' : 'send' }}
          </button>
          <button
            @click="fetchThoughts"
            :disabled="isLoading"
            class="rounded-xl bg-gradient-to-r from-indigo-200 to-indigo-400 text-white font-bold p-0 flex items-center justify-center shadow hover:from-indigo-300 transition disabled:opacity-60 space-mono"
            title="refresh"
            type="button"
            style="width:48px; min-width:48px; height:48px;"
          >
            <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M480-160q-134 0-227-93t-93-227q0-134 93-227t227-93q69 0 132 28.5T720-690v-110h80v280H520v-80h168q-32-56-87.5-88T480-720q-100 0-170 70t-70 170q0 100 70 170t170 70q77 0 139-44t87-116h84q-28 106-114 173t-196 67Z"/></svg>
          </button>
        </div>
      </form>
      <div v-if="error" class="text-red-600 text-center mt-4 text-base space-mono">
        <small>{{ error }}</small>
      </div>
      <div class="mt-10 pt-4 border-t border-dashed border-gray-200 text-gray-400 text-sm leading-relaxed select-none space-mono">
        <b>zoom:</b> mouse wheel<br>
        <b>canvas panning:</b> lmb on the empty space<br>
        <b>moving:</b> drad the cards <br>
        <br>
        <b>why?</b> for thoughts that can't be spoken directly, for messages that can't be sent. if you have something you need to say to someone, but the words won't reach them, share it here. this is a safe space for your true feelings. they'll never read it, but at least strangers will. <br>

      </div>
      <div class="mt-auto text-xs text-black pt-8 select-none space-mono">
        &copy; {{ new Date().getFullYear() }} you'll never read<br>

      </div>
    </aside>
    <!-- Canvas -->
    <main
      class="relative flex-1 h-screen overflow-hidden space-mono"
      ref="canvasRef"
      :style="{ width: `calc(100vw - ${sidebarWidth}px)` }"
      @wheel.passive="onCanvasWheel"
      style="overflow: hidden;"
    >
      <div
        class="absolute top-0 left-0 w-full h-full"
        style="overflow: visible; cursor: grab;"
        :style="{
          transform: `translate(${pan.x}px,${pan.y}px) scale(${zoom})`,
          transformOrigin: '0 0'
        }"
        @mousedown="onCanvasMouseDown"
      >
        <transition-group name="thought-card-animation" tag="div">
          <article
            v-for="(thought, idx) in thoughts"
            :key="thought.id"
            :id="'thought-' + thought.id"
            class="absolute rounded-2xl bg-white/95 shadow-2xl p-6 flex flex-col justify-between transition duration-200 ease-in-out cursor-grab select-none border border-indigo-100 space-mono"
            :class="[
              'hover:shadow-3xl hover:-translate-y-1 hover:scale-[1.03]',
              draggingCardId === thought.id ? 'z-30 ring-2 ring-indigo-300' : 'z-10'
            ]"
            :style="{
              left: (positions[thought.id]?.x || sidebarWidth + 100) + 'px',
              top: (positions[thought.id]?.y || 100) + 'px',
              minWidth: '260px',
              maxWidth: '420px',
              width: 'auto',
              minHeight: '80px',
              maxHeight: '400px',
              '--thought-idx': idx,
              '--thought-total': thoughts.length
            }"
            @mousedown.stop="onCardMouseDown($event, thought.id)"
          >
            <p class="mb-2 text-lg text-gray-800 font-medium break-words leading-snug w-full space-mono">
              {{ thought.content }}
            </p>
            <footer class="text-right mt-auto space-mono">
              <small class="text-gray-400 text-xs">{{ new Date(thought.created_at).toLocaleString() }}</small>
            </footer>
          </article>
        </transition-group>
        <p v-if="thoughts.length === 0 && !isLoading && !error"
           class="text-gray-400 text-center text-lg mt-16 select-none space-mono">
          it's nothing here, be brave and first!
        </p>
        <p v-if="isLoading && thoughts.length === 0"
           class="text-gray-400 text-center text-lg mt-16 select-none space-mono">Загрузка...</p>
      </div>
    </main>
  </div>
</template>

<style scoped>
.thought-card-animation-enter-active,
.thought-card-animation-leave-active {
  transition:
    opacity 0.55s cubic-bezier(.4,2,.6,1),
    transform 0.55s cubic-bezier(.4,2,.6,1);
}
.thought-card-animation-enter-from {
  opacity: 0;
  transform:
    scale(0.85)
    translateY(60px)
    rotate(calc((var(--thought-idx, 0) - var(--thought-total, 0)/2) * 6deg));
  filter: blur(2px);
}
.thought-card-animation-enter-to {
  opacity: 1;
  transform: scale(1) translateY(0) rotate(0deg);
  filter: blur(0);
}
.thought-card-animation-leave-from {
  opacity: 1;
  transform: scale(1) translateY(0) rotate(0deg);
  filter: blur(0);
}
.thought-card-animation-leave-to {
  opacity: 0;
  transform:
    scale(0.85)
    translateY(-60px)
    rotate(calc((var (--thought-idx, 0) - var(--thought-total, 0)/2) * -6deg));
  filter: blur(2px);
}
.thought-card-animation-move {
  transition: transform 0.55s cubic-bezier(.4,2,.6,1);
}

/* Убираем скроллбары у body */
body {
  overflow: hidden !important;
}

.poiret {
  font-family: 'Poiret One', cursive, sans-serif !important;
  letter-spacing: 0.04em;
}
.lowercase {
  text-transform: lowercase !important;
}
.space-mono {
  font-family: 'Space Mono', monospace !important;
}

/* Кнопки в строке, разные размеры */
button[type="submit"] {
  /* send */
  min-width: 110px;
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}
button[title="refresh"] {
  /* refresh */
  min-width: 48px;
  min-height: 48px;
  width: 48px;
  height: 48px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Кнопки в строке, разные размеры и адаптивное заполнение */
form .flex.gap-2.w-full {
  width: 100%;
}
form .flex.gap-2.w-full > button[type="submit"] {
  flex: 1 1 0%;
  min-width: 0;
}
form .flex.gap-2.w-full > button[title="refresh"] {
  flex: 0 0 auto;
  width: 48px;
  min-width: 48px;
  height: 48px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

</style>

<style>
/* Убираем скроллбары у html и body глобально */
html, body {
  overflow: hidden !important;
  height: 100%;
  width: 100%;
}
</style>
