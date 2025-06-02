<script setup>
import { useDrop } from 'vue3-dnd';
import ThoughtItem from './ThoughtItem.vue';

// Определяем props и emits
const props = defineProps({
  thoughts: { type: Array, required: true },
  positions: { type: Object, required: true },
});
const emit = defineEmits(['thought-moved']);

const ItemTypes = {
  THOUGHT: 'thought',
};

// --- Логика vue3-dnd для drop-зоны ---
const [, drop] = useDrop(() => ({
  accept: ItemTypes.THOUGHT, // Принимаем только элементы типа 'thought'
  drop(item, monitor) {
    // Вычисляем новую позицию элемента
    const delta = monitor.getDifferenceFromInitialOffset();
    const left = Math.round(item.left + delta.x);
    const top = Math.round(item.top + delta.y);

    // Отправляем событие наверх, чтобы App.vue обновил позицию
    emit('thought-moved', { id: item.id, left, top });

    // Возвращаем undefined, как требует документация, чтобы useDrag().drop() не сработал
    return undefined;
  },
}));
</script>

<template>
  <div ref="drop" class="relative w-full h-full">
    <ThoughtItem
        v-for="thought in thoughts"
        :key="thought.id"
        :thought="thought"
        :left="positions[thought.id]?.left || 50"
        :top="positions[thought.id]?.top || 50"
    />
  </div>
</template>