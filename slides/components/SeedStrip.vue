<script setup lang="ts">
import { computed, ref } from 'vue'
import data from '../data/lstm_vs_rnn.json'

// Kết quả từng seed của RNN và LSTM trên tập test (số liệu thật, sinh bởi experiment/lstm_*.ipynb + export_slide_data.py)
const props = defineProps<{ task: 'stock' | 'ecommerce', metrics: string[] }>()

const LOWER = ['MAE', 'RMSE', 'log loss']
const LABEL: Record<string, string> = {
  'MAE': 'MAE (điểm %)', 'RMSE': 'RMSE (điểm %)', 'R2 log': 'R² (thang log)', 'direction acc': 'Đúng hướng biến động',
  'accuracy': 'Accuracy', 'ROC-AUC': 'ROC-AUC', 'MCC': 'MCC', 'macro F1': 'Macro F1', 'recall refunded': 'Recall lớp refunded', 'log loss': 'Log loss',
}
const CELLS = ['RNN', 'LSTM'] as const

const d = computed(() => (data as any)[props.task])
const metric = ref(props.metrics[0])
const lower = computed(() => LOWER.includes(metric.value))
const values = (cell: string): number[] => d.value.per_seed[cell][metric.value]
const means = computed(() => Object.fromEntries(CELLS.map(c => [c, d.value.mean[c][metric.value]])))
const wins = computed(() => d.value.lstm_wins[metric.value])
const n = computed(() => d.value.seeds.length)

const W = 560, H = 150, PL = 60, PR = 20, ROW = { RNN: 45, LSTM: 95 } as Record<string, number>
const range = computed(() => {
  const all = CELLS.flatMap(c => values(c))
  const lo = Math.min(...all), hi = Math.max(...all), pad = (hi - lo) * 0.15 || 0.001
  return [lo - pad, hi + pad]
})
const xs = (v: number) => PL + ((v - range.value[0]) / (range.value[1] - range.value[0])) * (W - PL - PR)
const ticks = computed(() => {
  const [lo, hi] = range.value
  return [0, 1, 2, 3, 4].map(k => lo + ((hi - lo) * (k + 0.5)) / 5)
})
const digits = computed(() => (range.value[1] - range.value[0] < 0.02 ? 4 : 3))
</script>

<template>
  <div class="ss" data-no-nav>
    <div class="seg">
      <button v-for="m in props.metrics" :key="m" :class="{ sel: metric === m }" @click="metric = m">{{ LABEL[m] || m }}</button>
    </div>
    <svg :viewBox="`0 0 ${W} ${H}`" class="plot">
      <g v-for="t in ticks" :key="t">
        <line :x1="xs(t)" :x2="xs(t)" :y1="22" :y2="H - 28" class="grid" />
        <text :x="xs(t)" :y="H - 12" class="tick" text-anchor="middle">{{ t.toFixed(digits) }}</text>
      </g>
      <text :x="lower ? PL : W - PR" :y="12" class="tick" :text-anchor="lower ? 'start' : 'end'">
        {{ lower ? '← tốt hơn (thấp hơn)' : 'tốt hơn (cao hơn) →' }}</text>
      <g v-for="c in CELLS" :key="c">
        <text :x="PL - 10" :y="ROW[c] + 4" :class="c === 'RNN' ? 'crnn' : 'clstm'" class="lab" text-anchor="end">{{ c }}</text>
        <line :x1="xs(means[c])" :x2="xs(means[c])" :y1="ROW[c] - 15" :y2="ROW[c] + 15" :class="c === 'RNN' ? 'mrnn' : 'mlstm'" />
        <circle v-for="(v, k) in values(c)" :key="k" :cx="xs(v)" :cy="ROW[c]" r="6" :class="c === 'RNN' ? 'drnn' : 'dlstm'" />
      </g>
    </svg>
    <div class="note">
      Mỗi chấm = 1 seed, vạch = trung bình của {{ n }} seed ·
      RNN <b class="crnn">{{ means.RNN.toFixed(4) }}</b>, LSTM <b class="clstm">{{ means.LSTM.toFixed(4) }}</b> ·
      LSTM tốt hơn RNN cùng seed: <b>{{ wins }}/{{ n }}</b>
    </div>
  </div>
</template>

<style scoped>
.ss { font-size: .78rem; }
.plot { width: 100%; }
.grid { stroke: #e2e8f0; }
.tick { font-size: 11px; fill: #64748b; }
.lab { font-size: 13px; font-weight: 700; }
.drnn { fill: #ea580c; fill-opacity: .75; }
.dlstm { fill: #2563eb; fill-opacity: .75; }
.mrnn { stroke: #ea580c; stroke-width: 3; }
.mlstm { stroke: #2563eb; stroke-width: 3; }
.seg { display: flex; flex-wrap: wrap; gap: .3rem; margin-bottom: .2rem; }
.seg button { padding: .1rem .55rem; border-radius: 6px; border: 1px solid #94a3b8; }
.seg button.sel { background: #2563eb; color: #fff; border-color: #2563eb; }
.note { opacity: .85; }
.crnn { color: #ea580c; fill: #ea580c; } .clstm { color: #2563eb; fill: #2563eb; }
</style>
