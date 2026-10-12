<script setup lang="ts">
import { computed, ref } from 'vue'
import LstmCell from './LstmCell.vue'

// Một ô LSTM thu nhỏ: bộ nhớ chỉ là MỘT con số, nên tính tay được.
// Trọng số đặt sẵn (không học) để đầu vào có ý nghĩa dễ hiểu:
//   +2 = "thông tin quan trọng, hãy ghi nhớ"   0 = "từ bình thường"   −2 = "hết ngữ cảnh, hãy xóa"
// cổng quên = σ(0.5h + 3x + 3)   cổng ghi = σ(0.5h + 4x − 3)   nội dung mới = tanh(0.5h + 2x)   cổng đọc = σ(0.5h + x + 1)
const sig = (z: number) => 1 / (1 + Math.exp(-z))

const x = ref(2)
const hPrev = ref(0)
const cPrev = ref(0)
const manual = ref(false)
const fM = ref(0.9)
const iM = ref(0.5)
const oM = ref(0.8)

const sequence = [2, 0, 0, 0, -2, 0]
const meaning = (v: number) => (v >= 1 ? 'quan trọng → ghi nhớ' : v <= -1 ? 'hết ngữ cảnh → xóa' : 'từ bình thường')
const stepIdx = ref(0)
const history = ref<{ x: number; f: number; i: number; c: number }[]>([])

const r = computed(() => {
  const h0 = hPrev.value, x0 = x.value
  const f = manual.value ? fM.value : sig(0.5 * h0 + 3 * x0 + 3)
  const i = manual.value ? iM.value : sig(0.5 * h0 + 4 * x0 - 3)
  const g = Math.tanh(0.5 * h0 + 2 * x0)
  const o = manual.value ? oM.value : sig(0.5 * h0 + x0 + 1)
  const c = f * cPrev.value + i * g
  const h = o * Math.tanh(c)
  return { x: x0, hPrev: h0, cPrev: cPrev.value, f, i, g, o, c, h }
})

// Câu tóm tắt việc ô LSTM đang làm ở bước này
const action = computed(() => {
  const { f, i } = r.value
  if (i > 0.5 && f > 0.5) return { text: 'GHI thêm thông tin mới, vẫn giữ bộ nhớ cũ', cls: 'ci' }
  if (i > 0.5) return { text: 'XÓA bộ nhớ cũ, GHI thông tin mới vào', cls: 'ci' }
  if (f < 0.5) return { text: 'XÓA bộ nhớ', cls: 'cf' }
  return { text: 'GIỮ bộ nhớ, gần như không ghi gì mới', cls: 'cs' }
})

function step() {
  if (stepIdx.value >= sequence.length) return
  if (stepIdx.value > 0) { hPrev.value = r.value.h; cPrev.value = r.value.c }
  x.value = sequence[stepIdx.value]
  stepIdx.value++
  const s = r.value
  history.value.push({ x: s.x, f: s.f, i: s.i, c: s.c })
}
function reset() {
  stepIdx.value = 0; history.value = []
  x.value = 2; hPrev.value = 0; cPrev.value = 0; manual.value = false
}
const f2 = (n: number) => n.toFixed(2)
const pct = (n: number) => `${Math.round(100 * n)}%`
</script>

<template>
  <div class="sim" data-no-nav>
    <div class="left">
      <LstmCell :values="r" />
      <div class="act">Ở bước này ô LSTM đang: <b :class="action.cls">{{ action.text }}</b></div>
      <div class="eqs">
        <div><b class="cf">Cổng quên</b> = {{ f2(r.f) }} → giữ lại {{ pct(r.f) }} bộ nhớ cũ</div>
        <div><b class="ci">Cổng ghi</b> = {{ f2(r.i) }} → ghi vào {{ pct(r.i) }} nội dung mới (nội dung mới = {{ f2(r.g) }})</div>
        <div><b class="cs">Bộ nhớ mới</b> = {{ f2(r.f) }} × {{ f2(r.cPrev) }} + {{ f2(r.i) }} × {{ f2(r.g) }} = <b class="cs">{{ f2(r.c) }}</b></div>
        <div><b class="co">Cổng đọc</b> = {{ f2(r.o) }} → đầu ra = <b class="co">{{ f2(r.h) }}</b></div>
      </div>
    </div>
    <div class="right">
      <div class="hint">Ô LSTM thu nhỏ: bộ nhớ chỉ là <b>1 con số</b>. Trọng số đặt sẵn để đầu vào có nghĩa:
        <b>+2</b> = thông tin quan trọng, <b>0</b> = từ bình thường, <b>−2</b> = hết ngữ cảnh</div>
      <label>Đầu vào lúc này = {{ f2(x) }} <span class="mean">({{ meaning(x) }})</span>
        <input type="range" min="-2" max="2" step="0.1" v-model.number="x"></label>
      <label>Bộ nhớ đang có = {{ f2(cPrev) }}<input type="range" min="-2" max="2" step="0.05" v-model.number="cPrev"></label>
      <label class="chk"><input type="checkbox" v-model="manual"> Tự chỉnh các cổng bằng tay</label>
      <template v-if="manual">
        <label class="cf">Cổng quên = {{ f2(fM) }}<input type="range" min="0" max="1" step="0.01" v-model.number="fM"></label>
        <label class="ci">Cổng ghi = {{ f2(iM) }}<input type="range" min="0" max="1" step="0.01" v-model.number="iM"></label>
        <label class="co">Cổng đọc = {{ f2(oM) }}<input type="range" min="0" max="1" step="0.01" v-model.number="oM"></label>
      </template>
      <div class="btns">
        <button @click="step" :disabled="stepIdx >= sequence.length">Bước tiếp ▶ ({{ stepIdx }}/{{ sequence.length }})</button>
        <button @click="reset">Làm lại</button>
      </div>
      <div class="seq">Chuỗi chạy thử: [{{ sequence.join(', ') }}] = ghi · 3 từ bình thường · xóa · bình thường</div>
      <table v-if="history.length"><tbody>
        <tr><th>bước</th><th>đầu vào</th><th class="cf">quên</th><th class="ci">ghi</th><th class="cs">bộ nhớ</th></tr>
        <tr v-for="(s, k) in history" :key="k">
          <td>{{ k + 1 }}</td><td>{{ s.x }}</td><td>{{ f2(s.f) }}</td><td>{{ f2(s.i) }}</td><td><b>{{ f2(s.c) }}</b></td>
        </tr>
      </tbody></table>
    </div>
  </div>
</template>

<style scoped>
.sim { display: grid; grid-template-columns: 1.5fr 1fr; gap: 1rem; font-size: 0.8rem; }
.act { margin-top: .2rem; font-size: .8rem; }
.eqs { font-size: 0.72rem; line-height: 1.45; margin-top: .2rem; }
.hint { font-size: .72rem; line-height: 1.35; background: #f1f5f9; border-radius: 6px; padding: .3rem .45rem; margin-bottom: .4rem; }
.mean { opacity: .7; }
.right label { display: block; margin-bottom: .35rem; }
.right input[type=range] { width: 100%; display: block; }
.chk { margin-top: .4rem; }
.btns { display: flex; gap: .5rem; margin: .5rem 0 .3rem; }
button { padding: .2rem .7rem; border-radius: 6px; background: #2563eb; color: white; }
button:disabled { opacity: .4; }
button + button { background: #64748b; }
.seq { font-size: .68rem; opacity: .8; }
table { font-size: .7rem; margin-top: .3rem; }
td, th { padding: 1px 6px !important; }
.cf { color: #dc2626; } .ci { color: #16a34a; } .co { color: #7c3aed; } .cs { color: #2563eb; }
</style>
