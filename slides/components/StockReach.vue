<script setup lang="ts">
import { computed, ref } from 'vue'
import data from '../data/lstm_vs_rnn.json'

// Mô hình dùng thông tin xa tới đâu? (cổ phiếu, số liệu thật từ experiment/lstm_stock.ipynb, mục 7 và 9)
const s = (data as any).stock
const CELLS = ['RNN', 'LSTM'] as const
const view = ref<'sens' | 'cut' | 'window'>('sens')

const W = 560, H = 250, PL = 58, PR = 16, PT = 14, PB = 38
const K = Object.keys(s.mae_by_k.RNN).map(Number)
const mean = (a: number[]) => a.reduce((x, y) => x + y, 0) / a.length

const cfg = computed(() => {
  if (view.value === 'sens') {
    const lmin = -4.5, lmax = 0
    return {
      xlab: 'ngày trong cửa sổ (60 = hôm nay)', ylab: 'độ nhạy (so với ngày 60)',
      x: (v: number) => PL + ((v - 1) / 59) * (W - PL - PR),
      y: (v: number) => PT + ((lmax - Math.log10(v)) / (lmax - lmin)) * (H - PT - PB),
      xt: [1, 10, 20, 30, 40, 50, 60].map(v => [v, String(v)]),
      yt: [1, 1e-1, 1e-2, 1e-3, 1e-4].map(v => [v, v === 1 ? '1' : `1e${Math.log10(v)}`]),
      lines: Object.fromEntries(CELLS.map(c => [c, s.sensitivity_rel[c].map((v: number, i: number) => [i + 1, v])])),
      dots: {} as Record<string, number[][]>,
    }
  }
  if (view.value === 'cut') {
    const lo = 0.70, hi = 0.88
    return {
      xlab: 'chỉ giữ k ngày gần nhất (thang log)', ylab: 'MAE test (seed 42)',
      x: (v: number) => PL + (Math.log(v) / Math.log(60)) * (W - PL - PR),
      y: (v: number) => PT + ((hi - v) / (hi - lo)) * (H - PT - PB),
      xt: K.map(v => [v, String(v)]),
      yt: [0.70, 0.74, 0.78, 0.82, 0.86].map(v => [v, v.toFixed(2)]),
      lines: Object.fromEntries(CELLS.map(c => [c, K.map(k => [k, s.mae_by_k[c][String(k)]])])),
      dots: {} as Record<string, number[][]>,
    }
  }
  const ws = s.window_sweep.windows as number[], lo = 0.700, hi = 0.740
  const xi = (v: number) => ws.indexOf(v)
  return {
    xlab: 'độ dài cửa sổ (ngày giao dịch)', ylab: `MAE test (${s.window_sweep.seeds.length} seed)`,
    x: (v: number) => PL + 40 + (xi(v) / (ws.length - 1)) * (W - PL - PR - 80),
    y: (v: number) => PT + ((hi - v) / (hi - lo)) * (H - PT - PB),
    xt: ws.map(v => [v, String(v)]),
    yt: [0.70, 0.71, 0.72, 0.73, 0.74].map(v => [v, v.toFixed(2)]),
    lines: Object.fromEntries(CELLS.map(c => [c, ws.map((w, i) => [w, mean(s.window_sweep.mae[c][i])])])),
    dots: Object.fromEntries(CELLS.map(c => [c, ws.flatMap((w, i) => s.window_sweep.mae[c][i].map((v: number) => [w, v]))])),
  }
})
const path = (pts: number[][]) => pts.map((p, k) => `${k ? 'L' : 'M'}${cfg.value.x(p[0]).toFixed(1)},${cfg.value.y(p[1]).toFixed(1)}`).join('')
const pct = (v: number) => `${(100 * v).toFixed(1)}%`
const sci = (v: number) => v.toExponential(1)
const sweepMean = (c: string, i: number) => mean(s.window_sweep.mae[c][i]).toFixed(4)
</script>

<template>
  <div class="sr" data-no-nav>
    <div>
      <div class="seg">
        <button :class="{ sel: view === 'sens' }" @click="view = 'sens'">① Độ nhạy theo ngày</button>
        <button :class="{ sel: view === 'cut' }" @click="view = 'cut'">② Chỉ giữ k ngày gần nhất</button>
        <button :class="{ sel: view === 'window' }" @click="view = 'window'">③ Độ dài cửa sổ</button>
      </div>
      <svg :viewBox="`0 0 ${W} ${H}`" class="plot">
        <g v-for="[v, l] in cfg.yt" :key="'y' + v">
          <line :x1="PL" :x2="W - PR" :y1="cfg.y(v)" :y2="cfg.y(v)" class="grid" />
          <text :x="PL - 6" :y="cfg.y(v) + 4" class="tick" text-anchor="end">{{ l }}</text>
        </g>
        <text v-for="[v, l] in cfg.xt" :key="'x' + v" :x="cfg.x(v)" :y="H - PB + 15" class="tick" text-anchor="middle">{{ l }}</text>
        <text :x="(PL + W) / 2" :y="H - 4" class="tick" text-anchor="middle">{{ cfg.xlab }}</text>
        <text :x="12" :y="(H - PB) / 2" class="tick" text-anchor="middle" :transform="`rotate(-90 12 ${(H - PB) / 2})`">{{ cfg.ylab }}</text>
        <g v-for="c in CELLS" :key="c">
          <circle v-for="(p, k) in cfg.dots[c] || []" :key="k" :cx="cfg.x(p[0]) + (c === 'RNN' ? -6 : 6)" :cy="cfg.y(p[1])" r="3.5" :class="c === 'RNN' ? 'drnn' : 'dlstm'" />
          <path :d="path(cfg.lines[c])" :class="c === 'RNN' ? 'rnn' : 'lstm'" />
          <template v-if="view !== 'sens'">
            <circle v-for="(p, k) in cfg.lines[c]" :key="'m' + k" :cx="cfg.x(p[0])" :cy="cfg.y(p[1])" r="4" :class="c === 'RNN' ? 'mrnn' : 'mlstm'" />
          </template>
        </g>
        <g :transform="`translate(${view === 'sens' ? PL + 10 : W - PR - 120},${view === 'window' ? H - PB - 8 : PT + 12})`">
          <text x="0" y="0" class="crnn lab">— RNN</text>
          <text x="60" y="0" class="clstm lab">— LSTM</text>
        </g>
      </svg>
    </div>
    <div class="side">
      <table v-if="view === 'sens'"><tbody>
        <tr><th></th><th class="crnn">RNN</th><th class="clstm">LSTM</th></tr>
        <tr><td>ngày 1 / ngày 60</td><td>{{ sci(s.reach.RNN['day 1 / day 60 (median)']) }}</td><td>{{ sci(s.reach.LSTM['day 1 / day 60 (median)']) }}</td></tr>
        <tr><td>ngày 30 / ngày 60</td><td>{{ sci(s.reach.RNN['day 30 / day 60 (median)']) }}</td><td>{{ sci(s.reach.LSTM['day 30 / day 60 (median)']) }}</td></tr>
        <tr><td>phần ở 20 ngày cuối</td><td>{{ pct(s.reach.RNN['share in last 20 days']) }}</td><td>{{ pct(s.reach.LSTM['share in last 20 days']) }}</td></tr>
        <tr><td>phần ở 40 ngày đầu</td><td><b>{{ pct(s.reach.RNN['share in days 1-40']) }}</b></td><td><b>{{ pct(s.reach.LSTM['share in days 1-40']) }}</b></td></tr>
      </tbody></table>
      <table v-else-if="view === 'cut'"><tbody>
        <tr><th>giữ k ngày</th><th class="crnn">RNN</th><th class="clstm">LSTM</th></tr>
        <tr v-for="k in [5, 10, 20, 60]" :key="k"><td>k = {{ k }}</td><td>{{ s.mae_by_k.RNN[String(k)].toFixed(4) }}</td><td>{{ s.mae_by_k.LSTM[String(k)].toFixed(4) }}</td></tr>
      </tbody></table>
      <table v-else><tbody>
        <tr><th>cửa sổ</th><th class="crnn">RNN</th><th class="clstm">LSTM</th></tr>
        <tr v-for="(w, i) in s.window_sweep.windows" :key="w"><td>{{ w }} ngày</td><td>{{ sweepMean('RNN', i) }}</td><td>{{ sweepMean('LSTM', i) }}</td></tr>
      </tbody></table>
      <div class="hint" v-if="view === 'sens'">|∂ŷ / ∂x<sub>t</sub>| trên 512 cửa sổ test, chia cho giá trị ở ngày 60 (seed 42; tỉ số: trung vị 5 seed)</div>
      <div class="hint" v-else-if="view === 'cut'">Các ngày cũ hơn k đặt về 0 (= trung bình train). RNN: từ k = 20 trở đi MAE không đổi. LSTM: bỏ ngày cũ thì sai số tăng mạnh → LSTM thật sự dùng các ngày đó</div>
      <div class="hint" v-else>Cùng một tập mẫu cho cả 3 độ dài. RNN: cửa sổ 120 cho kết quả trùng với 60</div>
    </div>
  </div>
</template>

<style scoped>
.sr { display: grid; grid-template-columns: 1.75fr 1fr; gap: 1rem; align-items: center; }
.plot { width: 100%; }
.grid { stroke: #e2e8f0; }
.tick { font-size: 11px; fill: #64748b; }
.lab { font-size: 12px; font-weight: 700; }
.rnn { fill: none; stroke: #ea580c; stroke-width: 2.5; }
.lstm { fill: none; stroke: #2563eb; stroke-width: 2.5; }
.mrnn { fill: #ea580c; } .mlstm { fill: #2563eb; }
.drnn { fill: #ea580c; fill-opacity: .3; } .dlstm { fill: #2563eb; fill-opacity: .3; }
.seg { display: flex; flex-wrap: wrap; gap: .3rem; margin-bottom: .3rem; font-size: .75rem; }
.seg button { padding: .1rem .55rem; border-radius: 6px; border: 1px solid #94a3b8; }
.seg button.sel { background: #2563eb; color: #fff; border-color: #2563eb; }
.side { font-size: .78rem; }
table { font-size: .75rem; }
td, th { padding: 2px 6px !important; }
td:nth-child(n+2) { text-align: right; font-family: ui-monospace, monospace; }
.hint { font-size: .68rem; opacity: .7; margin-top: .4rem; line-height: 1.3; }
.crnn { color: #ea580c; fill: #ea580c; } .clstm { color: #2563eb; fill: #2563eb; }
</style>
