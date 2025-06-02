<script setup>
import { computed } from 'vue';
import { useDrag } from 'vue3-dnd';

// Определяем props
const props = defineProps({
  thought: {
    type: Object,
    required: true,
  },
  // Позиция будет передаваться от родителя
  left: { type: Number, required: true },
  top: { type: Number, required: true },
});

// Уникальный идентификатор для типа перетаскиваемого элемента
const ItemTypes = {
  THOUGHT: 'thought',
};

// --- Логика vue3-dnd ---
const [collect, drag] = useDrag(() => ({
  type: ItemTypes.THOUGHT,
  // В "item" мы передаем данные, которые будут доступны при перетаскивании
  item: { id: props.thought.id, left: props.left, top: props.top },
  collect: (monitor) => ({
    isDragging: monitor.isDragging(), // Узнаем, перетаскивается ли элемент прямо сейчас
  }),
}));

const formattedDate = computed(() => {
  return new Date(props.thought.created_at).toLocaleString();
});

// Динамические стили для позиционирования и отображения перетаскивания
const style = computed(() => ({
  position: 'absolute',
  left: `${props.left}px`,
  top: `${props.top}px`,
  cursor: 'move',
  // Делаем элемент полупрозрачным, когда его тащат
  opacity: collect.value.isDragging ? 0.5 : 1,
}));
</script>

<template>
  <div
      :ref="drag"
      :style="style"
      class="bg-white/10 p-4 rounded-lg shadow-lg text-left transition-all w-64"
  >
    <p class="text-gray-200 text-lg">{{ thought.content }}</p>
    <p class="text-xs text-gray-400 mt-2 text-right">{{ formattedDate }}</p>
  </div>
</template>