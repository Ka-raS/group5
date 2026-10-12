<script setup lang="ts">
import { computed, ref } from 'vue'

// Tín hiệu lỗi (gradient) đi ngược từ cuối câu về đầu câu, mỗi bước bị nhân với một hệ số:
//   RNN: hệ số mỗi bước (phụ thuộc trọng số và hàm tanh) → còn lại hệ số^số bước
//   LSTM (đường bộ nhớ): mỗi bước nhân với cổng quên → còn lại cổng quên^số bước
const props = withDefaults(defineProps<{ lstm?: boolean }>(), { lstm: false })

const gamma = ref(0.9)
const T = ref(50)
const f = ref(0.99)

const W = 560, H = 230, PL = 56, PB = 34, PT = 10
const LOGMIN = -12, LOGMAX = 4
const xs = (k: number) => PL + (k / T.value) * (W - PL - 10)
const ys = (v: number) => {
  const l = Math.min(LOGMAX, Math.max(LOGMIN, Math.log10(Math.max(v, 1e-300))))
  return PT + ((LOGMAX - l) / (LOGMAX - LOGMIN)) * (H - PT - PB)
}
const path = (base: number) => {
  let d = ''
  for (let k = 0; k <= T.value; k++) d += `${k ? 'L' : 'M'}${xs(k).toFixed(1)},${ys(Math.pow(base, k)).toFixed(1)}`
  return d
}
const ticks = [
  { v: 1e4, l: '×10 000' }, { v: 1, l: '100%' }, { v: 1e-4, l: '0.01%' }, { v: 1e-8, l: '10⁻⁶ %' }, { v: 1e-12, l: '10⁻¹⁰ %' },
]
// Đọc kết quả thành câu dễ hiểu: phần trăm còn lại, hoặc "phình to gấp … lần"
const say = (v: number) => {
  if (v >= 1.05) return `phình to gấp ${v >= 1e4 ? v.toExponential(1) : v.toFixed(1)} lần (bùng nổ)`
  const p = 100 * v
  if (p >= 1) return `còn ${p.toFixed(1)}%`
  if (p >= 1e-3) return `chỉ còn ${p.toPrecision(2)}%`
  return `gần như bằng 0 (${p.toExponential(1)}%)`
}
const rnnEnd = computed(() => Math.pow(gamma.value, T.value))
const lstmEnd = computed(() => Math.pow(f.value, T.value))
</script>

<template>
  <div class="gd" data-no-nav>
    <svg :viewBox="`0 0 ${W} ${H}`" class="plot">
      <g v-for="t in ticks" :key="t.v">
        <line :x1="PL" :x2="W - 10" :y1="ys(t.v)" :y2="ys(t.v)" class="grid" />
        <text :x="PL - 6" :y="ys(t.v) + 4" class="tick" text-anchor="end">{{ t.l }}</text>
      </g>
      <line :x1="PL" :x2="W - 10" :y1="ys(1)" :y2="ys(1)" class="one" />
      <text :x="W - 12" :y="ys(1) - 6" class="tick" text-anchor="end">tín hiệu nguyên vẹn (100%)</text>
      <text :x="(PL + W) / 2" :y="H - 4" class="tick" text-anchor="middle">số bước đi ngược về quá khứ (0 → {{ T }})</text>
      <path :d="path(gamma)" class="rnn" />
      <path v-if="props.lstm" :d="path(f)" class="lstm" />
    </svg>
    <div class="ctrl">
      <label>Số bước cần nhớ lại = <b>{{ T }}</b>
        <span class="sub">khoảng cách từ chữ "Pháp" tới chỗ trống</span>
        <input type="range" min="1" max="100" step="1" v-model.number="T"></label>
      <label class="crnn">RNN: mỗi bước, tín hiệu × <b>{{ gamma.toFixed(2) }}</b>
        <span class="sub">hệ số do trọng số và hàm tanh quyết định; khó giữ đúng bằng 1</span>
        <input type="range" min="0.5" max="1.2" step="0.01" v-model.number="gamma"></label>
      <label v-if="props.lstm" class="clstm">LSTM: mỗi bước, tín hiệu × cổng quên = <b>{{ f.toFixed(3) }}</b>
        <span class="sub">mạng tự học giữ cổng quên gần 1 khi cần nhớ</span>
        <input type="range" min="0.5" max="1" step="0.001" v-model.number="f"></label>
      <div class="out">
        <div>Sau {{ T }} bước, tín hiệu lỗi:</div>
        <div class="crnn">RNN: <b>{{ say(rnnEnd) }}</b></div>
        <div v-if="props.lstm" class="clstm">LSTM: <b>{{ say(lstmEnd) }}</b></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.gd { display: grid; grid-template-columns: 1.6fr 1fr; gap: 1rem; align-items: center; }
.plot { width: 100%; }
.grid { stroke: #e2e8f0; }
.one { stroke: #94a3b8; stroke-dasharray: 4 4; }
.tick { font-size: 11px; fill: #64748b; }
.rnn { fill: none; stroke: #ea580c; stroke-width: 3; }
.lstm { fill: none; stroke: #2563eb; stroke-width: 3; }
.ctrl { font-size: .8rem; }
.ctrl label { display: block; margin-bottom: .5rem; }
.ctrl .sub { display: block; font-size: .68rem; opacity: .7; color: #334155; }
.ctrl input { width: 100%; display: block; }
.out { font-size: .82rem; margin-top: .3rem; line-height: 1.4; }
.crnn { color: #ea580c; } .clstm { color: #2563eb; }
</style>
