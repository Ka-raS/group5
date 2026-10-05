<script setup lang="ts">
import { computed, ref } from 'vue'

// Câu hỏi trắc nghiệm: bấm một đáp án để xem đúng (xanh) hay sai (đỏ); được chọn lại cho tới khi đúng.
// q, options, explain nhận HTML (dùng <sub>, <i>…) vì KaTeX không render bên trong props.
const props = defineProps<{
  n: number
  q: string
  options: string[]
  answer: number
  explain?: string
}>()

const tried = ref<number[]>([])
const solved = computed(() => tried.value.includes(props.answer))
function pick(k: number) {
  if (!solved.value && !tried.value.includes(k)) tried.value.push(k)
}
function state(k: number) {
  if (!tried.value.includes(k)) return solved.value ? 'dim' : ''
  return k === props.answer ? 'ok' : 'bad'
}
</script>

<template>
  <div class="quiz" data-no-nav>
    <div class="q">
      <span><b>{{ n }}.</b> <span v-html="q" /></span>
      <button v-if="tried.length" class="reset" @click="tried = []">làm lại</button>
    </div>
    <div class="opts">
      <button v-for="(o, k) in options" :key="k" :class="state(k)" @click="pick(k)">
        <span class="key">{{ 'ABCD'[k] }}</span>
        <span v-html="o" />
        <span class="mark">{{ state(k) === 'ok' ? '✓' : state(k) === 'bad' ? '✗' : '' }}</span>
      </button>
    </div>
    <div v-if="solved && explain" class="explain" v-html="explain" />
  </div>
</template>

<style scoped>
.quiz { border: 1px solid #cbd5e1; border-radius: 10px; padding: .45rem .6rem; font-size: .75rem; background: #f8fafc; }
.q { display: flex; align-items: flex-start; gap: .5rem; margin-bottom: .3rem; line-height: 1.3; }
.opts { display: grid; grid-template-columns: 1fr 1fr; gap: .25rem; }
.opts button { display: flex; align-items: center; gap: .35rem; text-align: left; padding: .2rem .4rem; border: 1px solid #cbd5e1; border-radius: 6px; background: #fff; line-height: 1.25; transition: background .2s, border-color .2s; }
.opts button:hover { border-color: #2563eb; }
.key { font-weight: 700; color: #64748b; }
.mark { margin-left: auto; font-weight: 800; }
.opts button.ok { background: #dcfce7; border-color: #16a34a; color: #166534; }
.opts button.bad { background: #fee2e2; border-color: #dc2626; color: #991b1b; }
.opts button.dim { opacity: .45; }
.explain { margin-top: .3rem; color: #166534; line-height: 1.3; }
.reset { margin-left: auto; flex: none; font-size: .65rem; color: #64748b; text-decoration: underline; }
</style>
