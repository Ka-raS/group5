---
theme: default
title: LSTM — Long Short-Term Memory
info: Thuyết trình LSTM, 45 phút, 4 người
colorSchema: light
highlighter: shiki
lineNumbers: false
mdc: true
transition: slide-left
fonts:
  sans: Be Vietnam Pro
  mono: JetBrains Mono
layout: cover
class: text-center
clicks: 2
---

# LSTM
## Long Short-Term Memory

<div class="mt-10 text-xl hook">
<span>"Tôi lớn lên ở </span><span class="key" :class="{ fade: $clicks >= 2 }">Pháp</span><span>, </span>
<span v-click="1" class="mid">… học tiểu học, chuyển nhà ba lần, chơi bóng đá, mê truyện tranh, làm quen bạn mới …</span>
<span>, nên tôi nói thành thạo tiếng </span><span class="blank">___</span>"
</div>

<div class="abs-b mb-8 w-full text-sm opacity-70">
<div class="font-bold">Nhóm 5</div>
<div>Nguyễn Phú Đại · Trần Vũ Tiến Minh · Trần Đình Hiếu · Phạm Thanh An</div>
</div>

<style>
.hook .key { color: #2563eb; font-weight: 800; transition: opacity 2.5s; }
.hook .key.fade { opacity: .12; }
.hook .mid { opacity: .6; font-style: italic; }
.hook .blank { color: #dc2626; font-weight: 800; }
</style>

<!--
**[Người 1 · ~1 phút]**

Xin chào thầy và các bạn. Hôm nay nhóm mình trình bày về LSTM, viết tắt của Long Short-Term Memory.

Trước khi vào bài, mời các bạn đọc câu này: "Tôi lớn lên ở Pháp, nên tôi nói thành thạo tiếng ___". Ai cũng điền được ngay: tiếng Pháp.

[click] Nếu chèn vào giữa câu khoảng 30 từ không liên quan, thì để điền được chỗ trống, mô hình phải **giữ thông tin "Pháp" qua khoảng 30 bước thời gian**.

[click] Với RNN cơ bản, ảnh hưởng của từ "Pháp" lên trạng thái ở cuối câu gần như bằng 0. Bài hôm nay trả lời ba câu hỏi: vì sao RNN không học được phụ thuộc xa, LSTM khắc phục bằng cơ chế nào, và vì sao về mặt toán học cơ chế đó hiệu quả.
-->

---
layout: center
---

# Vị trí của LSTM trong các kiến trúc mạng nơ-ron

<svg viewBox="0 0 760 330" class="w-full fam" style="max-height: 360px">
  <defs><marker id="a2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2563eb"/></marker></defs>
  <g v-click="1">
    <rect x="10" y="10" width="225" height="110" rx="10" fill="#f1f5f9" stroke="#475569" stroke-width="2"/>
    <text x="122" y="40" class="t1">MLP</text>
    <text x="122" y="64" class="t2">Dữ liệu: vector kích thước cố định</text>
    <text x="122" y="84" class="t2">Không chia sẻ trọng số</text>
    <text x="122" y="106" class="t3">mạng kết nối đầy đủ (fully connected)</text>
  </g>
  <g v-click="2">
    <rect x="250" y="10" width="225" height="110" rx="10" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
    <text x="362" y="40" class="t1">CNN</text>
    <text x="362" y="64" class="t2">Dữ liệu: dạng lưới (ảnh)</text>
    <text x="362" y="84" class="t2">Chia sẻ trọng số theo không gian</text>
    <text x="362" y="106" class="t3">cùng một kernel tại mọi vị trí</text>
  </g>
  <g v-click="3">
    <rect x="490" y="10" width="260" height="250" rx="12" fill="#fff7ed" stroke="#ea580c" stroke-width="2"/>
    <text x="620" y="38" class="t1">Họ RNN</text>
    <text x="620" y="60" class="t2">Dữ liệu: chuỗi, độ dài thay đổi</text>
    <text x="620" y="78" class="t2">Chia sẻ trọng số theo thời gian</text>
    <text x="620" y="100" class="t2" font-style="italic">h<tspan dy="4" class="sub">t</tspan><tspan dy="-4"> = F(h</tspan><tspan dy="4" class="sub">t−1</tspan><tspan dy="-4">, x</tspan><tspan dy="4" class="sub">t</tspan><tspan dy="-4">)</tspan></text>
    <rect x="510" y="114" width="220" height="50" rx="8" fill="#ffedd5" stroke="#ea580c" stroke-width="1.5"/>
    <text x="620" y="135" class="t4">RNN cơ bản (Elman, 1990)</text>
    <text x="620" y="154" class="t3">F: một lớp tanh</text>
    <text x="250" y="150" class="t2" fill="#475569">MLP, CNN, RNN: ba họ kiến trúc song song, khác nhau</text>
    <text x="250" y="168" class="t2" fill="#475569">ở giả định về cấu trúc của dữ liệu đầu vào</text>
  </g>
  <g v-click="4">
    <rect x="510" y="174" width="220" height="70" rx="10" fill="#dbeafe" stroke="#2563eb" stroke-width="3"/>
    <text x="620" y="200" class="t1" fill="#1d4ed8">LSTM (1997)</text>
    <text x="620" y="220" class="t3">F: cell state c + 3 cổng</text>
    <text x="620" y="236" class="t3">(forget, input, output)</text>
    <rect x="20" y="192" width="445" height="112" rx="10" fill="#eff6ff" stroke="#2563eb" stroke-dasharray="5 4"/>
    <text x="34" y="216" class="t4 l" fill="#1d4ed8">LSTM là một mô hình thuộc họ RNN:</text>
    <text x="34" y="240" class="t2 l">• cùng phép truy hồi; F dùng chung trọng số ở mọi bước</text>
    <text x="34" y="262" class="t2 l">• cùng huấn luyện bằng lan truyền ngược theo thời gian (BPTT)</text>
    <text x="34" y="284" class="t2 l">• khác RNN cơ bản ở hàm F: thêm cell state c và 3 cổng</text>
    <line x1="465" y1="230" x2="506" y2="212" stroke="#2563eb" stroke-width="2" marker-end="url(#a2)"/>
  </g>
</svg>

<style>
.fam text { text-anchor: middle; font-size: 13px; }
.fam .t1 { font-size: 20px; font-weight: 700; }
.fam .t3 { font-size: 12px; fill: #475569; }
.fam .t4 { font-size: 14px; font-weight: 700; }
.fam .sub { font-size: 9px; }
.fam text.l { text-anchor: start; }
</style>

<!--
**[Người 1 · ~1.5 phút]**

Trước khi vào LSTM, mình xác định vị trí của nó so với các kiến trúc mà lớp đã học.

[click] **MLP** là mạng kết nối đầy đủ: đầu vào là một vector có kích thước cố định, mỗi trọng số gắn với một vị trí đầu vào cố định. MLP không khai thác cấu trúc không gian hay thời gian của dữ liệu.

[click] **CNN**, các bạn đã làm ở assignment trước, dành cho dữ liệu dạng lưới như ảnh. Cùng một kernel được áp dụng tại mọi vị trí, tức là **chia sẻ trọng số theo không gian**.

[click] **RNN** dành cho dữ liệu chuỗi. Cùng một bộ trọng số được áp dụng ở mọi bước thời gian, tức là **chia sẻ trọng số theo thời gian**. Trạng thái ẩn được cập nhật theo phép truy hồi h t bằng F(h t trừ 1, x t). Lưu ý: MLP, CNN và RNN là **ba họ kiến trúc song song**, mỗi họ ứng với một giả định về cấu trúc dữ liệu; không họ nào được suy ra từ họ nào.

[click] LSTM **không phải một họ mô hình mới, mà là một mô hình trong họ RNN**, giống RNN cơ bản. Nó dùng cùng phép truy hồi, cùng chia sẻ trọng số qua các bước, và cùng được huấn luyện bằng lan truyền ngược theo thời gian, viết tắt là BPTT. Điểm khác duy nhất là hàm F: RNN cơ bản dùng một lớp tanh, còn LSTM dùng thêm một cell state c t và ba cổng để điều khiển việc ghi, xóa và đọc cell state.
-->

---

# So sánh MLP · CNN · RNN · LSTM

<div class="cmp">

| | MLP | CNN | RNN | <span class="text-blue-600">LSTM</span> |
|---|---|---|---|---|
| **Dữ liệu** | vector cố định | dạng lưới (ảnh) | chuỗi | chuỗi |
| **Chia sẻ trọng số** | không | theo không gian | theo thời gian | theo thời gian |
| **Trạng thái** | không | không | $h_t$ | $h_t$ **và** $c_t$ |
| **Phạm vi ngữ cảnh** | toàn bộ vector | trường tiếp nhận | thực tế ~10 bước | > 1000 bước (thí nghiệm 1997) |
| **Số tham số¹** | — | — | 29,312 | 117,248 (×4) |
| **Ứng dụng điển hình** | dữ liệu bảng | phân loại ảnh | chuỗi ngắn | dịch máy, giọng nói, chuỗi thời gian |

</div>

<div class="text-xs opacity-70 mt-1">¹ Một lớp, kích thước đầu vào d = 100, kích thước trạng thái ẩn h = 128, một vector bias cho mỗi phép biến đổi.</div>

<div v-click class="mt-4 text-center text-lg">
LSTM giữ nguyên cơ chế truy hồi của RNN và khắc phục hạn chế chính: <b class="text-red-600">khó học phụ thuộc xa</b>.
</div>

<style>
.cmp table { font-size: .8rem; line-height: 1.3; }
.cmp th, .cmp td { padding: .35rem .5rem !important; }
.cmp td:first-child { white-space: nowrap; }
</style>

<!--
**[Người 1 · ~1 phút]**

Bảng này tóm tắt khác biệt giữa bốn mô hình. Mình lưu ý ba dòng.

Dòng **trạng thái**: MLP và CNN không có trạng thái, mỗi mẫu đầu vào được xử lý độc lập. RNN có một hidden state h t. LSTM có **hai** trạng thái: h t và cell state c t. Cell state c t là thành phần trung tâm của cả bài.

Dòng **phạm vi ngữ cảnh**: trên thực tế RNN cơ bản thường chỉ học được phụ thuộc trong khoảng 10 bước. Bài báo gốc năm 1997 cho thấy LSTM học được phụ thuộc cách nhau hơn 1000 bước.

Dòng **số tham số**: với cùng kích thước, LSTM có gấp 4 lần số tham số của RNN. Lát nữa bạn Hiếu sẽ giải thích vì sao đúng bằng 4.

[click] Tóm lại: LSTM giữ nguyên cơ chế truy hồi của RNN, và khắc phục hạn chế chính của RNN là khó học phụ thuộc xa.
-->

---

# Ôn lại RNN

<div class="grid grid-cols-[1fr_1.15fr] gap-4 items-center">
<div class="text-center text-xl">

$h_t = \tanh(W_h\, h_{t-1} + W_x\, x_t + b)$

$\tanh(z) = \dfrac{e^{z} - e^{-z}}{e^{z} + e^{-z}} \in (-1, 1)$

</div>
<div class="legend">

- $x_t \in \mathbb{R}^d$: vector đầu vào tại bước $t$
- $h_t \in \mathbb{R}^h$: trạng thái ẩn (hidden state) tại bước $t$, $h_0 = 0$
- $W_h \in \mathbb{R}^{h \times h}$: ma trận trọng số trạng thái ẩn → trạng thái ẩn
- $W_x \in \mathbb{R}^{h \times d}$: ma trận trọng số đầu vào → trạng thái ẩn
- $b \in \mathbb{R}^h$: vector bias; $\tanh$ tính theo từng phần tử

</div>
</div>

<svg viewBox="0 0 760 200" class="w-full" style="max-height: 175px">
  <defs>
    <marker id="a4" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#475569"/></marker>
    <marker id="a4o" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#ea580c"/></marker>
  </defs>
  <g v-click="1">
    <line x1="8" y1="90" x2="58" y2="90" stroke="#475569" stroke-width="2" marker-end="url(#a4)"/>
    <text x="14" y="82" style="font-size:14px;font-style:italic">h<tspan dy="4" style="font-size:10px">0</tspan></text>
    <rect x="60" y="60" width="110" height="60" rx="10" fill="#ffedd5" stroke="#ea580c" stroke-width="2"/>
    <text x="115" y="96" text-anchor="middle" style="font-size:18px">tanh</text>
    <line x1="115" y1="170" x2="115" y2="122" stroke="#475569" stroke-width="2" marker-end="url(#a4)"/>
    <text x="121" y="152" fill="#475569" style="font-size:12px">W<tspan dy="4" style="font-size:9px;font-style:italic">x</tspan></text>
    <text x="115" y="192" text-anchor="middle" style="font-size:16px;font-style:italic">x<tspan dy="4" style="font-size:11px;font-style:italic">1</tspan></text>
    <line x1="115" y1="60" x2="115" y2="20" stroke="#475569" stroke-width="2" marker-end="url(#a4)"/>
    <text x="135" y="22" style="font-size:16px;font-style:italic">h<tspan dy="4" style="font-size:11px;font-style:italic">1</tspan></text>
    <line x1="170" y1="90" x2="238" y2="90" stroke="#ea580c" stroke-width="2.5" marker-end="url(#a4o)"/>
    <text x="188" y="82" fill="#ea580c" style="font-size:12px">W<tspan dy="4" style="font-size:9px;font-style:italic">h</tspan></text>
  </g>
  <g v-click="2">
    <rect x="240" y="60" width="110" height="60" rx="10" fill="#ffedd5" stroke="#ea580c" stroke-width="2"/>
    <text x="295" y="96" text-anchor="middle" style="font-size:18px">tanh</text>
    <line x1="295" y1="170" x2="295" y2="122" stroke="#475569" stroke-width="2" marker-end="url(#a4)"/>
    <text x="301" y="152" fill="#475569" style="font-size:12px">W<tspan dy="4" style="font-size:9px;font-style:italic">x</tspan></text>
    <text x="295" y="192" text-anchor="middle" style="font-size:16px;font-style:italic">x<tspan dy="4" style="font-size:11px;font-style:italic">2</tspan></text>
    <line x1="295" y1="60" x2="295" y2="20" stroke="#475569" stroke-width="2" marker-end="url(#a4)"/>
    <text x="315" y="22" style="font-size:16px;font-style:italic">h<tspan dy="4" style="font-size:11px;font-style:italic">2</tspan></text>
    <line x1="350" y1="90" x2="418" y2="90" stroke="#ea580c" stroke-width="2.5" marker-end="url(#a4o)"/>
    <text x="368" y="82" fill="#ea580c" style="font-size:12px">W<tspan dy="4" style="font-size:9px;font-style:italic">h</tspan></text>
  </g>
  <g v-click="3">
    <rect x="420" y="60" width="110" height="60" rx="10" fill="#ffedd5" stroke="#ea580c" stroke-width="2"/>
    <text x="475" y="96" text-anchor="middle" style="font-size:18px">tanh</text>
    <line x1="475" y1="170" x2="475" y2="122" stroke="#475569" stroke-width="2" marker-end="url(#a4)"/>
    <text x="481" y="152" fill="#475569" style="font-size:12px">W<tspan dy="4" style="font-size:9px;font-style:italic">x</tspan></text>
    <text x="475" y="192" text-anchor="middle" style="font-size:16px;font-style:italic">x<tspan dy="4" style="font-size:11px;font-style:italic">3</tspan></text>
    <line x1="475" y1="60" x2="475" y2="20" stroke="#475569" stroke-width="2" marker-end="url(#a4)"/>
    <text x="495" y="22" style="font-size:16px;font-style:italic">h<tspan dy="4" style="font-size:11px;font-style:italic">3</tspan></text>
    <line x1="530" y1="90" x2="598" y2="90" stroke="#ea580c" stroke-width="2.5" marker-end="url(#a4o)"/>
    <text x="548" y="82" fill="#ea580c" style="font-size:12px">W<tspan dy="4" style="font-size:9px;font-style:italic">h</tspan> …</text>
  </g>
  <g v-click="4">
    <rect x="600" y="60" width="110" height="60" rx="10" fill="#ffedd5" stroke="#ea580c" stroke-width="2"/>
    <text x="655" y="96" text-anchor="middle" style="font-size:18px">tanh</text>
    <line x1="655" y1="170" x2="655" y2="122" stroke="#475569" stroke-width="2" marker-end="url(#a4)"/>
    <text x="661" y="152" fill="#475569" style="font-size:12px">W<tspan dy="4" style="font-size:9px;font-style:italic">x</tspan></text>
    <text x="655" y="192" text-anchor="middle" style="font-size:16px;font-style:italic">x<tspan dy="4" style="font-size:11px;font-style:italic">T</tspan></text>
    <line x1="655" y1="60" x2="655" y2="20" stroke="#475569" stroke-width="2" marker-end="url(#a4)"/>
    <text x="675" y="22" style="font-size:16px;font-style:italic">h<tspan dy="4" style="font-size:11px;font-style:italic">T</tspan></text>
  </g>
</svg>

<div v-click="5" class="text-center">

Cùng một bộ $W_h, W_x, b$ được dùng ở <b>mọi</b> bước → huấn luyện bằng <b>BPTT</b> (lan truyền ngược theo thời gian)

</div>

<!--
**[Người 1 · ~1.5 phút]**

Ôn lại nhanh RNN mà các bạn đã làm. Ở mỗi bước t, trạng thái ẩn mới h t được tính từ trạng thái ẩn trước h t trừ 1 và đầu vào x t: nhân h t trừ 1 với ma trận W h, nhân x t với ma trận W x, cộng bias b, rồi áp dụng tanh cho từng phần tử. Với d là kích thước đầu vào và h là kích thước trạng thái ẩn, W h có kích thước h nhân h, W x có kích thước h nhân d. Hàm tanh đưa giá trị về khoảng (trừ 1, 1).

[click] [click] [click] [click] Khi trải mạng theo thời gian (unrolling), ta được một chuỗi các ô nối tiếp nhau. Các mũi tên ngang màu cam là phép nhân với **cùng một ma trận W h** ở mọi bước; các mũi tên dọc là phép nhân với cùng một W x.

[click] Để huấn luyện, ta dùng lan truyền ngược theo thời gian (BPTT), tức là áp dụng backpropagation trên đồ thị đã trải theo thời gian. Vì W h xuất hiện ở mọi bước, gradient từ bước cuối truyền về bước đầu phải nhân qua W h nhiều lần. Đây là nguồn gốc của vấn đề ở slide tiếp theo.
-->

---

# Vấn đề: gradient biến mất / bùng nổ

<div class="text-center text-xl">

$$\frac{\partial h_T}{\partial h_k} \;=\; \prod_{t=k+1}^{T} \frac{\partial h_t}{\partial h_{t-1}} \;=\; \prod_{t=k+1}^{T} \operatorname{diag}\big(\tanh'(a_t)\big)\, W_h$$

</div>

<div class="legend text-center -mt-2 mb-1">

$a_t = W_h h_{t-1} + W_x x_t + b$ (giá trị trước kích hoạt) · $\tanh'(z) = 1 - \tanh^2(z) \in (0, 1]$ · $\gamma = \lVert W_h \rVert \cdot \max \tanh'$: cận trên chuẩn của mỗi thừa số

</div>

<div class="grid grid-cols-2 gap-4 text-center text-sm mb-1">
<div class="text-orange-600">γ &lt; 1 ⇒ ‖tích‖ ≤ γ<sup>T−k</sup> → 0: <b>gradient biến mất</b></div>
<div class="text-red-600">‖W<sub>h</sub>‖ &gt; 1 ⇒ tích có thể tăng theo hàm mũ: <b>gradient bùng nổ</b></div>
</div>

<GradientDecay />

<!--
**[Người 1 · ~2 phút]**

Đây là phần toán chính của phần mở đầu. Để biết lỗi ở bước cuối T ảnh hưởng thế nào tới trạng thái ở bước k, ta tính đạo hàm partial h T trên partial h k. Theo quy tắc chuỗi, đạo hàm này là **tích** của T trừ k ma trận Jacobian partial h t trên partial h t trừ 1. Mỗi Jacobian bằng ma trận đường chéo chứa đạo hàm tanh tại a t, nhân với W h; a t là giá trị bên trong tanh.

Đạo hàm của tanh bằng 1 trừ tanh mũ 2, luôn nằm trong khoảng (0, 1]. Gọi ga-ma là cận trên chuẩn của mỗi thừa số, bằng chuẩn của W h nhân với giá trị lớn nhất của tanh phẩy:
- nếu ga-ma nhỏ hơn 1, chuẩn của tích bị chặn bởi ga-ma mũ T trừ k, nên tiến về 0 theo hàm mũ: gradient biến mất;
- nếu chuẩn của W h lớn hơn 1, tích **có thể** tăng theo hàm mũ: gradient bùng nổ. Đây là điều kiện cần, không phải điều kiện đủ.

**(Demo)** Đồ thị dùng mô hình đơn giản hóa: mỗi thừa số có độ lớn đúng bằng ga-ma. Với ga-ma bằng 0.9 và T bằng 50 bước, ta được 0.9 mũ 50 xấp xỉ 0.005, tức là độ lớn gradient truyền từ bước 50 về bước đầu chỉ còn **0.5%**. Tăng T lên 100 thì còn khoảng 3 nhân 10 mũ trừ 5. Tăng ga-ma lên 1.1 thì đồ thị tăng theo hàm mũ: gradient bùng nổ.

Không thể giữ ga-ma đúng bằng 1 trong suốt quá trình huấn luyện, vì W h thay đổi sau mỗi lần cập nhật và tanh phẩy thay đổi theo dữ liệu. Đó là lý do RNN không học được phụ thuộc giữa từ "Pháp" và vị trí cần dự đoán ở slide đầu.
-->

---

# Lịch sử: phát hiện vấn đề và đề xuất LSTM

<div class="grid grid-cols-2 gap-6 mt-2">
<div v-click="1" class="card">

### 1991 · Sepp Hochreiter
Sinh viên **TU München**, luận văn tốt nghiệp (diploma thesis), người hướng dẫn **Jürgen Schmidhuber**

→ **Phân tích toán học đầu tiên** về hiện tượng gradient biến mất ở RNN (chính là tích Jacobian ở slide trước)

<span class="text-sm opacity-70">(Bengio, Simard, Frasconi công bố độc lập năm 1994)</span>

</div>
<div v-click="2" class="card">

### Ý tưởng
Gradient suy giảm vì bị **nhân lặp lại với hệ số khác 1**

→ Dùng một đơn vị nhớ $c_t$ có **liên kết tự hồi quy trọng số cố định = 1**, hàm kích hoạt **tuyến tính**

$$c_t = 1 \cdot c_{t-1} + (\text{đầu vào mới}) \;\Rightarrow\; \frac{\partial c_t}{\partial c_{t-1}} = 1$$

→ **Constant Error Carousel (CEC)**: tín hiệu lỗi truyền qua giữ nguyên độ lớn

</div>
</div>

<div v-click="3" class="card mt-3">

**Vấn đề mới:** mọi đầu vào đều được cộng vào $c_t$ → thêm **cổng (gate)** nhân vào đầu vào và đầu ra của CEC để điều khiển khi nào *ghi*, khi nào *đọc*.
**1997:** Hochreiter & Schmidhuber, *"Long Short-Term Memory"*, tạp chí **Neural Computation** (đã có technical report năm 1995).

</div>

<style>
.card { background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 12px; padding: .6rem 1rem; font-size: .85rem; }
.card h3 { margin-top: 0 !important; color: #1d4ed8; }
</style>

<!--
**[Người 1 · ~2 phút]**

Vậy ai là người đã nhìn ra vấn đề này và sửa nó?

[click] Năm 1991, Sepp Hochreiter, khi đó là **sinh viên** Đại học Kỹ thuật München, làm luận văn tốt nghiệp dưới sự hướng dẫn của Jürgen Schmidhuber. Trong luận văn này, ông đưa ra **phân tích toán học đầu tiên** giải thích vì sao RNN không học được phụ thuộc xa, chính là tích các ma trận Jacobian ở slide trước. Năm 1994, Bengio, Simard và Frasconi công bố độc lập kết quả tương tự.

[click] Hướng khắc phục suy ra trực tiếp từ công thức: gradient suy giảm vì bị nhân lặp lại với hệ số khác 1. Vì vậy ông dùng một đơn vị có **liên kết tự hồi quy với trọng số cố định bằng 1** và hàm kích hoạt tuyến tính. Khi đó đạo hàm của c t theo c t trừ 1 đúng bằng 1, nên tín hiệu lỗi truyền qua bao nhiêu bước cũng không đổi độ lớn. Ông gọi đơn vị này là **Constant Error Carousel**, viết tắt CEC.

[click] Cách làm này sinh ra vấn đề mới: mọi đầu vào đều được cộng trực tiếp vào c t, kể cả đầu vào không liên quan, nên nội dung đã lưu bị ghi đè. Giải pháp là thêm các **cổng**, là các hệ số nhân trong khoảng 0 đến 1, đặt ở đầu vào và đầu ra của CEC để điều khiển khi nào được ghi và khi nào được đọc. Kết quả được công bố trong bài báo "Long Short-Term Memory" năm 1997 trên tạp chí Neural Computation, một trong những bài báo được trích dẫn nhiều nhất của lĩnh vực học sâu.
-->

---

# Các mốc phát triển của LSTM

<div class="timeline">
  <div v-click class="ev"><b>1997</b><span>Bản gốc: chỉ có <b>input gate</b> và <b>output gate</b>, <span class="text-red-600">chưa có forget gate</span></span></div>
  <div v-click class="ev"><b>1999–2000</b><span>Gers, Schmidhuber, Cummins thêm <b class="text-red-600">forget gate</b> (<i>"Learning to Forget"</i>); Gers & Schmidhuber thêm kết nối peephole</span></div>
  <div v-click class="ev"><b>2005</b><span>Graves & Schmidhuber: huấn luyện bằng gradient BPTT đầy đủ (không cắt bớt), <b>Bidirectional LSTM</b></span></div>
  <div v-click class="ev"><b>2009</b><span>LSTM thắng các cuộc thi nhận dạng chữ viết tay</span></div>
  <div v-click class="ev"><b>2014</b><span><b>seq2seq</b> (Sutskever et al.): encoder–decoder LSTM cho dịch máy</span></div>
  <div v-click class="ev"><b>2015–2016</b><span>Nhận dạng giọng nói của Google (2015), Google Translate (GNMT, 2016) dùng LSTM</span></div>
  <div v-click class="ev"><b>2017</b><span><b>Transformer</b> ra đời và dần thay thế LSTM trong NLP</span></div>
</div>

<div v-click class="mt-4 text-center text-sm">
Tên gọi: <i>short-term memory</i> là giá trị kích hoạt (khác với <i>long-term memory</i> là trọng số); LSTM giữ short-term memory qua <b>nhiều bước</b> → <i>Long Short-Term Memory</i>
</div>

<style>
.timeline { border-left: 3px solid #2563eb; margin-left: 1rem; padding-left: 1rem; }
.ev { display: grid; grid-template-columns: 7rem 1fr; gap: .5rem; padding: .25rem 0; font-size: .9rem; position: relative; }
.ev::before { content: ''; position: absolute; left: -1.45rem; top: .6rem; width: .7rem; height: .7rem; border-radius: 50%; background: #2563eb; }
.ev b:first-child { color: #1d4ed8; }
</style>

<!--
**[Người 1 · ~1 phút]**

Điểm qua nhanh hành trình của LSTM.

[click] Bản gốc năm 1997 chỉ có hai cổng: input gate và output gate. **Chưa có forget gate**, nghĩa là cell state chỉ được cộng thêm, không có cơ chế xóa.

[click] Năm 1999–2000, Felix Gers, Schmidhuber và Cummins thêm **forget gate**, cho phép mạng học cách xóa nội dung trong cell state. LSTM dùng ngày nay, kể cả `nn.LSTM` trong PyTorch, là phiên bản có forget gate. Cũng năm 2000, Gers và Schmidhuber đề xuất kết nối peephole, cho các cổng đọc trực tiếp cell state; PyTorch không dùng peephole.

[click] Năm 2005, Alex Graves và Schmidhuber huấn luyện LSTM bằng gradient BPTT đầy đủ, thay vì gradient bị cắt bớt như bản 1997, và giới thiệu Bidirectional LSTM. [click] Năm 2009, LSTM thắng các cuộc thi nhận dạng chữ viết tay. [click] Năm 2014, Sutskever và cộng sự dùng hai LSTM làm encoder và decoder cho dịch máy, gọi là seq2seq. [click] Khoảng 2015–2016, nhận dạng giọng nói của Google và Google Translate chuyển sang LSTM. [click] Đến 2017, Transformer xuất hiện và dần thay thế LSTM trong xử lý ngôn ngữ.

[click] Về tên gọi: trong bài báo gốc, "short-term memory" là giá trị kích hoạt của mạng, phân biệt với "long-term memory" là các trọng số được học chậm qua huấn luyện. "Long short-term memory" nghĩa là giá trị kích hoạt đó được duy trì qua nhiều bước thời gian.
-->

---
layout: center
class: text-center
---

# Cấu trúc bên trong một ô LSTM

<div class="text-xl opacity-80 mt-4">CEC (cell state) + 3 cổng: input, output (1997) và forget (bổ sung năm 2000)</div>

<!--
**[Người 1 · ~0.5 phút]**

Tóm lại, RNN không học được phụ thuộc xa vì gradient bị nhân lặp lại qua W h và tanh phẩy, và Hochreiter khắc phục bằng một đơn vị tự hồi quy có trọng số bằng 1 (CEC) kết hợp với các cổng. Tiếp theo, mời bạn Minh trình bày cấu trúc bên trong ô LSTM và cách từng cổng hoạt động.
-->

---

# Hai trạng thái: hidden state và cell state

<div class="grid grid-cols-2 gap-6 items-center">
<div class="text-center">

**RNN: một trạng thái $h_t$**

<svg viewBox="0 0 260 180" style="width: 85%; margin: auto">
  <defs><marker id="a9" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#475569"/></marker></defs>
  <rect x="70" y="40" width="120" height="90" rx="14" fill="#ffedd5" stroke="#ea580c" stroke-width="2"/>
  <text x="130" y="92" text-anchor="middle" style="font-size:20px">tanh</text>
  <line x1="5" y1="85" x2="68" y2="85" stroke="#475569" stroke-width="2.5" marker-end="url(#a9)"/>
  <line x1="190" y1="85" x2="255" y2="85" stroke="#475569" stroke-width="2.5" marker-end="url(#a9)"/>
  <line x1="130" y1="178" x2="130" y2="132" stroke="#475569" stroke-width="2.5" marker-end="url(#a9)"/>
  <text x="8" y="75" style="font-style:italic">h<tspan dy="4" style="font-size:11px;font-style:italic">t-1</tspan></text><text x="215" y="75" style="font-style:italic">h<tspan dy="4" style="font-size:11px;font-style:italic">t</tspan></text><text x="140" y="172" style="font-style:italic">x<tspan dy="4" style="font-size:11px;font-style:italic">t</tspan></text>
</svg>

</div>
<div class="text-center">

**LSTM: thêm <span class="text-blue-600">cell state $c_t$</span>**

<LstmCell active="state" />

</div>
</div>

<div class="grid grid-cols-2 gap-4 mt-2 text-sm">
<div v-click class="p-2 rounded bg-blue-50">

<b class="text-blue-600">$c_t \in \mathbb{R}^h$, cell state</b>: chỉ được cập nhật bằng phép nhân từng phần tử và phép cộng, không qua ma trận trọng số → <b>bộ nhớ dài hạn</b> (tương ứng CEC)

</div>
<div v-click class="p-2 rounded bg-slate-100">

<b>$h_t \in \mathbb{R}^h$, hidden state</b>: đầu ra tại mỗi bước, tính từ $c_t$ qua output gate → <b>bộ nhớ ngắn hạn</b>

</div>
</div>

<!--
**[Người 2 · ~1 phút]**

Cảm ơn Đại. Chúng ta bắt đầu bằng hình ảnh tổng thể.

Bên trái là RNN: chỉ có **một trạng thái** h. Toàn bộ thông tin cần lưu phải nằm trong h, và ở mỗi bước h đều bị nhân với W h rồi đi qua tanh.

Bên phải là LSTM. Đường màu xanh nằm ngang phía trên là **cell state c t**, một vector cùng kích thước h với hidden state.

[click] Trên đường đi từ c t trừ 1 đến c t chỉ có một phép nhân từng phần tử và một phép cộng, không có ma trận trọng số và không có hàm kích hoạt. Đây là Constant Error Carousel của Hochreiter, đóng vai trò bộ nhớ dài hạn.

[click] h t vẫn là đầu ra tại mỗi bước như ở RNN. Nó được tính từ c t thông qua output gate, đóng vai trò bộ nhớ ngắn hạn.

Ba cổng tiếp theo điều khiển ba thao tác trên cell state: xóa, ghi và đọc.
-->

---

# Cổng 1 · Forget gate: giữ lại bao nhiêu từ $c_{t-1}$?

<div class="grid grid-cols-[1.3fr_1fr] gap-6 items-center">
<LstmCell active="f" />
<div>

$$f_t = \sigma\big(W_f\,[h_{t-1}, x_t] + b_f\big)$$

<div class="legend mb-2">

- $\sigma(z) = \dfrac{1}{1 + e^{-z}} \in (0, 1)$: hàm sigmoid, tính theo từng phần tử
- $[h_{t-1}, x_t] \in \mathbb{R}^{h+d}$: ghép nối (concatenate) hai vector
- $W_f \in \mathbb{R}^{h \times (h+d)}$, $b_f \in \mathbb{R}^h$: trọng số và bias của forget gate

</div>

<div class="text-sm">

<v-clicks>

- $f_t \in (0, 1)^h$: một hệ số cho mỗi phần tử của $c_{t-1}$
- $f_t = 0$ → **xóa hoàn toàn** phần tử tương ứng của $c_{t-1}$
- $f_t = 1$ → **giữ nguyên** phần tử tương ứng của $c_{t-1}$
- Dùng **sigmoid** vì đầu ra nằm trong (0, 1): dùng làm **hệ số nhân** (gating)
- <span class="text-red-600">Không có trong bản 1997:</span> bản gốc tương đương $f \equiv 1$

</v-clicks>

</div>
</div>
</div>

<!--
**[Người 2 · ~1.5 phút]**

Cổng đầu tiên là **forget gate**, màu đỏ.

Đầu vào của cổng là hidden state trước h t trừ 1 và đầu vào hiện tại x t, ghép nối thành một vector kích thước h cộng d. Vector này được nhân với ma trận W f kích thước h nhân (h cộng d), cộng bias b f, rồi đi qua hàm sigmoid xích-ma(z) bằng 1 trên (1 cộng e mũ trừ z).

[click] Kết quả f t là một vector cùng kích thước với cell state, mỗi phần tử nằm trong khoảng 0 đến 1.

[click] Nếu một phần tử của f t bằng 0, phần tử tương ứng của c t trừ 1 bị nhân với 0, tức là bị **xóa hoàn toàn**. [click] Nếu bằng 1 thì phần tử đó được **giữ nguyên**.

[click] Lý do dùng sigmoid thay vì ReLU hay tanh: sigmoid cho đầu ra trong khoảng (0, 1), phù hợp để làm hệ số nhân: 0 chặn hoàn toàn, 1 cho qua hoàn toàn. ReLU không bị chặn trên, còn tanh cho giá trị âm.

[click] Như bạn Đại đã nói, cổng này **không có** trong bản gốc năm 1997. Bản gốc tương đương với f luôn bằng 1, nên cell state chỉ được cộng thêm mà không có cơ chế xóa. Ví dụ, khi văn bản chuyển sang một chủ đề khác, mạng cần xóa thông tin "Pháp" khỏi cell state. Forget gate cho phép mạng học khi nào cần xóa.
-->

---

# Cổng 2 · Input gate: ghi gì, ghi bao nhiêu?

<div class="grid grid-cols-[1.3fr_1fr] gap-6 items-center">
<LstmCell active="i,c" />
<div>

$$i_t = \sigma\big(W_i\,[h_{t-1}, x_t] + b_i\big)$$

$$\tilde c_t = \tanh\big(W_c\,[h_{t-1}, x_t] + b_c\big)$$

<div class="legend mb-2">

- $W_i, W_c \in \mathbb{R}^{h \times (h+d)}$, $b_i, b_c \in \mathbb{R}^h$: trọng số và bias của input gate và candidate
- $\tilde c_t$: giá trị ứng viên (candidate) để ghi vào cell state
- $\odot$: phép nhân từng phần tử (tích Hadamard)

</div>

<div class="text-sm">

<v-clicks>

- $\tilde c_t \in (-1, 1)^h$: **nội dung** cần ghi
- $i_t \in (0, 1)^h$: **tỉ lệ** được ghi cho mỗi phần tử
- Phần thực sự được ghi: $i_t \odot \tilde c_t$

</v-clicks>

</div>
</div>
</div>

<!--
**[Người 2 · ~1.5 phút]**

Cổng thứ hai, màu xanh lá, gồm hai thành phần có cùng dạng với forget gate, mỗi thành phần có ma trận trọng số và bias riêng.

Thành phần thứ nhất là **candidate** c̃ t, dùng hàm tanh. [click] Đây là **nội dung** mới cần ghi vào cell state. Vì dùng tanh nên giá trị nằm trong khoảng −1 đến 1, cho phép tăng hoặc giảm giá trị của cell state.

[click] Thành phần thứ hai là **input gate** i t, dùng sigmoid. Nó quyết định **tỉ lệ** được ghi cho từng phần tử: 0 là không ghi, 1 là ghi toàn bộ.

[click] Phần thực sự được ghi vào là tích từng phần tử i t nhân từng phần tử c̃ t. Ký hiệu hình tròn chấm là phép nhân từng phần tử của hai vector cùng kích thước.

Lý do tách thành hai thành phần: đây chính là vấn đề Hochreiter giải quyết bằng cổng, không phải đầu vào nào cũng cần được lưu. Với câu ví dụ, tại từ "Pháp", i gần 1 để ghi; tại các từ như "học tiểu học", "chơi bóng đá", i gần 0 để nội dung đã lưu không bị ghi đè.
-->

---

# Cập nhật cell state bằng phép cộng

<div class="grid grid-cols-[1.3fr_1fr] gap-6 items-center">
<LstmCell active="state,f,i,c" />
<div>

$$\boxed{\,c_t = \textcolor{#dc2626}{f_t} \odot c_{t-1} + \textcolor{#16a34a}{i_t \odot \tilde c_t}\,}$$

<div class="text-sm">

<v-clicks>

- <span class="text-red-600">Phần giữ lại từ $c_{t-1}$</span> **+** <span class="text-green-600">phần ghi mới</span>
- RNN: $h_t = \tanh(W_h h_{t-1} + \dots)$, trạng thái cũ bị **nhân với ma trận $W_h$ rồi qua tanh**
- LSTM: $c_{t-1}$ chỉ được **nhân từng phần tử với $f_t \in (0,1)^h$** rồi **cộng**
- Phép cộng này là cơ sở của phân tích gradient ở phần 3

</v-clicks>

</div>
</div>
</div>

<!--
**[Người 2 · ~1 phút]**

Bây giờ ghép hai cổng lại để cập nhật cell state. Công thức trong khung là công thức quan trọng nhất của LSTM.

[click] Diễn giải: cell state mới bằng phần được giữ lại từ cell state cũ, **cộng** với phần được ghi mới.

[click] So sánh với RNN: trạng thái cũ h t trừ 1 bị nhân với ma trận W h rồi đi qua tanh ở **mỗi bước**.

[click] Ở LSTM, c t trừ 1 chỉ được nhân từng phần tử với f t, có giá trị trong khoảng 0 đến 1, rồi **cộng** thêm phần ghi mới. Không có phép nhân ma trận, không có hàm kích hoạt.

[click] Lát nữa bạn Hiếu sẽ chứng minh chính phép cộng này giúp gradient không bị biến mất.
-->

---

# Cổng 3 · Output gate: đọc ra bao nhiêu?

<div class="grid grid-cols-[1.3fr_1fr] gap-6 items-center">
<LstmCell active="o" />
<div>

$$o_t = \sigma\big(W_o\,[h_{t-1}, x_t] + b_o\big)$$

$$h_t = o_t \odot \tanh(c_t)$$

<div class="legend mb-2">

- $W_o \in \mathbb{R}^{h \times (h+d)}$, $b_o \in \mathbb{R}^h$: trọng số và bias của output gate

</div>

<div class="text-sm">

<v-clicks>

- $\tanh(c_t)$: đưa giá trị cell state về khoảng (−1, 1)
- $o_t \in (0,1)^h$: tỉ lệ **đọc ra** của từng phần tử ở bước này
- Cell state có thể **lưu** một thông tin qua nhiều bước mà **không ảnh hưởng** tới $h_t$ ở các bước đó

</v-clicks>

</div>
</div>
</div>

<!--
**[Người 2 · ~1 phút]**

Cổng cuối cùng là **output gate**, màu tím.

Cell state là trạng thái nội bộ của ô. Đầu ra h t được tính từ cell state qua hai bước. [click] Đầu tiên cho c t qua tanh để đưa giá trị về khoảng −1 đến 1. [click] Sau đó nhân từng phần tử với output gate o t, cũng là một sigmoid với trọng số W o và bias b o riêng, để quyết định tỉ lệ đọc ra của từng phần tử.

[click] Hệ quả: mạng có thể **lưu** thông tin "Pháp" trong cell state suốt 30 bước mà không ảnh hưởng tới các đầu ra ở giữa. Đến từ "tiếng", khi cần dự đoán tên ngôn ngữ, output gate mới mở để đọc thông tin đó ra h t.
-->

---
clicks: 4
---

# Tổng hợp: 6 phương trình của LSTM

<div class="grid grid-cols-[1.2fr_1fr] gap-6 items-center">
<LstmCell :active="['all', 'f', 'i,c', 'state,f,i,c', 'o'][$clicks] || 'all'" />
<div class="eqs">

<div :class="{ hl: $clicks === 1 }">

$f_t = \sigma(W_f[h_{t-1}, x_t] + b_f)$

</div>
<div :class="{ hl: $clicks === 2 }">

$i_t = \sigma(W_i[h_{t-1}, x_t] + b_i)$

$\tilde c_t = \tanh(W_c[h_{t-1}, x_t] + b_c)$

</div>
<div :class="{ hl: $clicks === 3 }">

$c_t = f_t \odot c_{t-1} + i_t \odot \tilde c_t$

</div>
<div :class="{ hl: $clicks === 4 }">

$o_t = \sigma(W_o[h_{t-1}, x_t] + b_o)$

$h_t = o_t \odot \tanh(c_t)$

</div>
<div class="legend mt-2 px-2 opacity-80">

$\sigma$: sigmoid · $\odot$: nhân từng phần tử · $W_f, W_i, W_c, W_o \in \mathbb{R}^{h \times (h+d)}$ · $b_f, b_i, b_c, b_o \in \mathbb{R}^h$

</div>
</div>
</div>

<style>
.eqs > div { padding: .1rem .6rem; border-radius: 8px; transition: background .3s; }
.eqs .hl { background: #fef9c3; }
</style>

<!--
**[Người 2 · ~1 phút]**

Đây là toàn bộ LSTM trên một slide: sáu phương trình. Mình bấm lần lượt để đối chiếu từng phương trình với vị trí tương ứng trên sơ đồ.

[click] Forget gate. [click] Input gate và candidate. [click] Cập nhật cell state. [click] Output gate và đầu ra h t.

Để ý rằng bốn phương trình f, i, c̃, o có **cùng một dạng**: nhân ma trận với [h t trừ 1, x t], cộng bias, rồi cho qua sigmoid hoặc tanh. Điểm này rất quan trọng khi tính số tham số và khi xem cách PyTorch lưu trọng số. Bạn Hiếu sẽ quay lại điểm này.
-->

---

# Mô phỏng tính toán trong một ô LSTM

<LstmSimulator />

<!--
**[Người 2 · ~3 phút] — slide demo, nên để chủ động thời gian**

Bây giờ chúng ta chạy một LSTM có kích thước trạng thái ẩn bằng 1, nên mọi đại lượng đều là số vô hướng và có thể tính tay. Trọng số được đặt cố định như trong các phương trình bên dưới sơ đồ.

**Demo 1, kéo thanh trượt:**
- Đặt x t bằng 2: input gate i xấp xỉ 1, candidate c̃ xấp xỉ 1, nên cell state c tăng lên gần 1. Mạng **ghi** thông tin vào cell state.
- Đặt x t bằng trừ 2: forget gate f xấp xỉ 0, nên c bị **xóa**.

**Demo 2, bấm Reset rồi bấm Step liên tục.** Chuỗi đầu vào là [2, 0, 0, 0, −2, 0].
- Bước 1, x = 2: c xấp xỉ 0.99, mạng ghi thông tin.
- Bước 2 đến 4, x = 0: i xấp xỉ 0.06 nên gần như không ghi gì mới, còn f xấp xỉ 0.96 nên c giảm chậm: 0.98, 0.97, 0.95. Thông tin được **giữ**. Các bạn theo dõi bảng bên phải.
- Bước 5, x = −2: f xấp xỉ 0.06, c giảm về khoảng 0.06. Mạng **xóa** thông tin.

**Demo 3, bật "Chỉnh trực tiếp các cổng":** đặt f bằng 1, i bằng 0 thì c t bằng c t trừ 1 chính xác. Đây là trường hợp CEC của Hochreiter năm 1997.

Trong mạng thật, các trọng số này được **học** từ dữ liệu, chứ không phải do chúng ta đặt.
-->

---

# Ví dụ minh họa: giá trị các cổng trên câu mẫu

<div class="mt-4">
<GateHeatmap />
</div>

<v-clicks>

- Tại **"Pháp"**: <span class="text-green-600">i ≈ 1</span>, ghi thông tin "Pháp" vào $c_t$
- Ở các từ giữa: <span class="text-red-600">f ≈ 1</span>, giữ nguyên $c_t$; <span class="text-green-600">i ≈ 0</span>, không ghi đè
- Tại **"tiếng"**: <span class="text-purple-600">o ≈ 1</span>, đọc thông tin ra để dự đoán "Pháp"

</v-clicks>

<!--
**[Người 2 · ~1 phút]**

Quay lại câu ví dụ ở đầu bài. Bảng này minh họa giá trị của ba cổng tại từng từ mà ta mong muốn một mô hình đã huấn luyện tốt có được. Lưu ý đây là số liệu minh họa, không phải số đo từ một mô hình đã huấn luyện.

[click] Tại từ "Pháp", input gate gần 1 để ghi thông tin vào cell state.

[click] Ở các từ ở giữa, forget gate gần 1 để giữ cell state, input gate gần 0 để không ghi đè.

[click] Tại từ "tiếng", output gate gần 1 để đọc thông tin "Pháp" ra h t và dự đoán từ tiếp theo.

Đến đây là toàn bộ cơ chế lan truyền xuôi của LSTM. Câu hỏi còn lại: phép cộng trong cập nhật cell state có ý nghĩa gì về mặt toán? Mời bạn Hiếu.
-->

---

# Kích thước ma trận và số tham số

<div class="grid grid-cols-2 gap-6">
<div>

Với đầu vào $x_t \in \mathbb{R}^d$ và hidden $h_t \in \mathbb{R}^h$:

$$[h_{t-1}, x_t] \in \mathbb{R}^{h+d}, \qquad W_f, W_i, W_c, W_o \in \mathbb{R}^{h \times (h+d)}$$

Gộp **4 ma trận** thành 1, $W \in \mathbb{R}^{4h \times (h+d)}$, $b \in \mathbb{R}^{4h}$:

$$W\,[h_{t-1}, x_t] + b = \begin{bmatrix} z_i \\ z_f \\ z_c \\ z_o \end{bmatrix} \in \mathbb{R}^{4h}$$

<div class="legend">

$z_\ast$: giá trị trước kích hoạt của từng cổng; $i = \sigma(z_i)$, $f = \sigma(z_f)$, $\tilde c = \tanh(z_c)$, $o = \sigma(z_o)$

</div>

<div class="text-sm opacity-80">PyTorch lưu đúng như vậy: <code>weight_ih_l0</code> (4h × d), <code>weight_hh_l0</code> (4h × h), thứ tự các cổng là <b>i, f, g, o</b></div>

</div>
<div>

$$\#\text{params} = 4 \cdot \big[h(h+d) + h\big]$$

<div class="mt-6 text-lg">

❓ Với $d = 100$, $h = 128$?

</div>

<div v-click class="mt-2">

$4 \cdot [128 \cdot 228 + 128] = \mathbf{117{,}248}$

RNN: $128 \cdot 228 + 128 = 29{,}312$, nên **LSTM gấp 4 lần**

<div class="text-sm opacity-80 mt-2">

PyTorch dùng 2 vector bias (<code>b_ih</code>, <code>b_hh</code>) nên con số là $4 \cdot [h(h+d) + 2h] = 117{,}760$

</div>

</div>
</div>
</div>

<!--
**[Người 3 · ~1.5 phút]**

Cảm ơn Minh. Phần của mình đi vào toán, bắt đầu bằng một câu hỏi rất thực tế: một lớp LSTM có bao nhiêu tham số?

Gọi kích thước đầu vào là d, kích thước hidden là h. Vector ghép [h t trừ 1, x t] có kích thước h cộng d. Mỗi cổng cần một ma trận h nhân (h cộng d) và một bias h.

Như bạn Minh đã nói, bốn phương trình f, i, c̃, o có cùng dạng, nên ta có thể **gộp 4 ma trận thành một** ma trận 4h nhân (h cộng d), thực hiện một phép nhân rồi tách vector kết quả thành 4 đoạn, mỗi đoạn dài h, sau đó áp dụng sigmoid hoặc tanh cho từng đoạn. PyTorch cũng làm đúng như vậy: các bạn mở `weight_ih_l0` sẽ thấy nó có 4h hàng, theo thứ tự i, f, g, o, trong đó g là candidate.

Vậy số tham số là 4 nhân [h(h cộng d) cộng h]. Mời các bạn tính nhẩm với d = 100, h = 128.

[click] Kết quả là 117,248, đúng gấp 4 lần RNN. Lưu ý: PyTorch dùng hai vector bias riêng cho phần đầu vào và phần trạng thái ẩn, nên nếu đếm trong code sẽ ra 117,760. Tương tự, `nn.RNN` với cùng kích thước có 29,440 tham số. Đây là điểm hay gây nhầm lẫn khi làm bài.
-->

---

# Tính tay lan truyền xuôi qua 2 bước thời gian

<div class="text-sm mb-2">

LSTM vô hướng ở slide mô phỏng ($h = d = 1$): &nbsp; $f_t = \sigma(0.5h_{t-1} + 3x_t + 3)$ · $i_t = \sigma(0.5h_{t-1} + 4x_t - 3)$ · $\tilde c_t = \tanh(0.5h_{t-1} + 2x_t)$ · $o_t = \sigma(0.5h_{t-1} + x_t + 1)$ · khởi tạo $h_0 = c_0 = 0$

</div>

<div class="calc">

| Đại lượng | t = 1 &nbsp;($x_1 = 2$, $h_0 = 0$) | t = 2 &nbsp;($x_2 = 0$, $h_1 = 0.7225$) |
|---|---|---|
| $f_t$ | <span v-click="1">$\sigma(9) = 0.9999$</span> | <span v-click="4">$\sigma(3.361) = 0.9665$</span> |
| $i_t$ | <span v-click="1">$\sigma(5) = 0.9933$</span> | <span v-click="4">$\sigma(-2.639) = 0.0667$</span> |
| $\tilde c_t$ | <span v-click="1">$\tanh(4) = 0.9993$</span> | <span v-click="4">$\tanh(0.361) = 0.3463$</span> |
| $c_t = f_t c_{t-1} + i_t \tilde c_t$ | <span v-click="2">$0 + 0.9933 \cdot 0.9993 = \mathbf{0.9926}$</span> | <span v-click="5">$0.9665 \cdot 0.9926 + 0.0667 \cdot 0.3463 = \mathbf{0.9825}$</span> |
| $o_t$ | <span v-click="3">$\sigma(3) = 0.9526$</span> | <span v-click="6">$\sigma(1.361) = 0.7960$</span> |
| $h_t = o_t \tanh(c_t)$ | <span v-click="3">$0.9526 \cdot \tanh(0.9926) = \mathbf{0.7225}$</span> | <span v-click="6">$0.7960 \cdot \tanh(0.9825) = \mathbf{0.6003}$</span> |

</div>

<style>
.calc table { font-size: .8rem; }
.calc td, .calc th { padding: .25rem .6rem !important; }
</style>

<div v-click="7" class="mt-3 p-2 rounded bg-blue-50 text-center">

Ở bước 2, gần như không ghi thêm ($i_2$ ≈ 0.07) nhưng $c_2$ vẫn ≈ 0.98: giá trị của $c_1$ được <b>giữ lại</b> nhờ $f_2$ ≈ 0.97

</div>

<!--
**[Người 3 · ~2 phút]**

Để kiểm tra lại quá trình lan truyền xuôi, mình tính tay hai bước với LSTM vô hướng ở slide mô phỏng. Ban đầu h 0 bằng c 0 bằng 0.

**Bước 1, x = 2.** [click] Forget gate bằng sigmoid của 0.5 nhân 0 cộng 3 nhân 2 cộng 3 bằng 9, ra khoảng 0.9999. Input gate bằng sigmoid của 5, ra 0.9933. Candidate bằng tanh của 4, ra 0.9993.
[click] Cell state: c 0 bằng 0 nên chỉ còn phần ghi mới, 0.9933 nhân 0.9993 bằng 0.9926.
[click] Output gate bằng sigmoid của 3, ra 0.9526. Vậy h 1 bằng 0.9526 nhân tanh(0.9926) bằng 0.7225.

**Bước 2, x = 0.** Bây giờ h 1 bằng 0.7225, nên 0.5 h bằng 0.361.
[click] f bằng sigmoid của 3.361, ra 0.9665. i bằng sigmoid của −2.639, ra 0.0667, rất nhỏ. Candidate là 0.3463.
[click] Cell state: 0.9665 nhân 0.9926 cộng 0.0667 nhân 0.3463 bằng 0.9825.
[click] o là 0.796, và h 2 bằng 0.6003.

[click] Điểm cần thấy: ở bước 2 gần như không có gì mới được ghi, nhưng cell state vẫn giữ ở mức 0.98. Giá trị đã ghi ở bước 1 được giữ lại nhờ forget gate gần bằng 1.
-->

---
clicks: 3
---

# Lan truyền ngược: gradient qua cell state

<div v-click="1" class="text-sm">

**Công thức đầy đủ** ($c_{t-1}$ ảnh hưởng tới $c_t$ qua 2 đường):

$$
\frac{\partial c_t}{\partial c_{t-1}} =
\underbrace{\textcolor{#2563eb}{\operatorname{diag}(f_t)}}_{\text{trực tiếp}}
+
\underbrace{\textcolor{#94a3b8}{\Big[\operatorname{diag}(c_{t-1}\!\odot\!\sigma'_f)\,W_{fh} + \operatorname{diag}(\tilde c_t\!\odot\!\sigma'_i)\,W_{ih} + \operatorname{diag}(i_t\!\odot\!\tanh'_{\tilde c})\,W_{ch}\Big]\operatorname{diag}\big(o_{t-1}\!\odot\!\tanh'(c_{t-1})\big)}}_{\text{gián tiếp, đi qua } h_{t-1}\text{: có } W \text{ và đạo hàm, giống RNN}}
$$

<div class="legend opacity-80">

$W_{fh}, W_{ih}, W_{ch} \in \mathbb{R}^{h \times h}$: phần của $W_f, W_i, W_c$ nhân với $h_{t-1}$ (vì $W_f [h_{t-1}, x_t] = W_{fh} h_{t-1} + W_{fx} x_t$) · $\sigma'_f, \sigma'_i, \tanh'_{\tilde c}$: đạo hàm của hàm kích hoạt tại giá trị trước kích hoạt của $f_t, i_t, \tilde c_t$ · đường gián tiếp dùng $h_{t-1} = o_{t-1} \odot \tanh(c_{t-1})$

</div>

</div>

<div v-click="2" class="grid grid-cols-2 gap-4 mt-1">
<div class="p-2 rounded bg-orange-50 text-center">

**RNN**

$$\frac{\partial h_T}{\partial h_k} = \prod \operatorname{diag}(\tanh')\,W_h$$

ma trận $W_h$ nhân lặp lại → biến mất / bùng nổ

</div>
<div class="p-2 rounded bg-blue-50 text-center">

**LSTM, đường trực tiếp**

$$\frac{\partial c_T}{\partial c_k} \approx \prod_{t=k+1}^{T} \operatorname{diag}(f_t)$$

không có $W$, không có $\tanh'$; mạng **tự học** giữ $f \approx 1$

</div>
</div>

<div v-click="3" class="mt-2 text-center text-sm">
📜 Bản gốc 1997 <b>chủ động cắt bỏ</b> các số hạng gián tiếp khi tính gradient, chỉ giữ đường trực tiếp.
</div>

<!--
**[Người 3 · ~2.5 phút] — slide toán quan trọng nhất**

Đây là câu hỏi cốt lõi: khi lan truyền ngược, gradient đi từ c t về c t trừ 1 như thế nào?

[click] Nhìn lại công thức c t bằng f t nhân từng phần tử c t trừ 1 cộng i t nhân từng phần tử c̃ t. Biến c t trừ 1 ảnh hưởng tới c t qua **hai đường**.

- **Đường trực tiếp**, màu xanh: c t trừ 1 được nhân từng phần tử với f t. Đạo hàm theo đường này là ma trận đường chéo của f t.
- **Đường gián tiếp**, màu xám: c t trừ 1 tạo ra h t trừ 1 bằng o t trừ 1 nhân từng phần tử tanh(c t trừ 1), và h t trừ 1 là đầu vào của các cổng ở bước t. Đạo hàm theo đường này cho ra ba số hạng trong ngoặc vuông, ứng với f t, i t và c̃ t. W fh, W ih, W ch là phần của các ma trận trọng số nhân với h t trừ 1. Không cần nhớ chi tiết các số hạng này; điểm cần thấy là mỗi số hạng đều chứa **ma trận W** và **đạo hàm của sigmoid hoặc tanh**, tức là có cấu trúc giống RNN.

[click] Bây giờ đặt RNN và đường trực tiếp của LSTM cạnh nhau. Bên trái, RNN: tích của các ma trận đường chéo của tanh phẩy, nhân W h, nên biến mất hoặc bùng nổ. Bên phải, LSTM: chỉ là tích các hàm đường chéo của f t. **Không có ma trận trọng số, không có đạo hàm của hàm kích hoạt.** Hơn nữa, f t là đại lượng mạng **học** được: khi cần lưu thông tin, mạng học cách giữ f gần 1, và gradient truyền qua gần như không suy giảm.

Các số hạng gián tiếp vẫn có thể biến mất. Nhưng gradient toàn phần là tổng theo các đường, nên **chỉ cần đường trực tiếp còn thì gradient vẫn truyền về được**.

[click] Một chi tiết lịch sử: trong bài báo năm 1997, Hochreiter và Schmidhuber **chủ động cắt bỏ** các số hạng gián tiếp khi huấn luyện (truncated gradient), chỉ giữ đường trực tiếp. Phải đến năm 2005, Graves mới huấn luyện bằng gradient đầy đủ.
-->

---

# So sánh $\gamma^T$ (RNN) và $\prod f_t$ (LSTM)

<div class="mt-6">
<GradientDecay lstm />
</div>

<div class="mt-4 text-center text-sm opacity-80">Ví dụ: γ = 0.9, f<sub>t</sub> = 0.99 ở mọi bước, T = 100 → RNN: 0.9¹⁰⁰ ≈ 3·10⁻⁵, LSTM: 0.99¹⁰⁰ ≈ 0.37</div>

<!--
**[Người 3 · ~1 phút]**

Đây là đồ thị của bạn Đại ở slide 5, thêm đường màu xanh cho đường trực tiếp của LSTM, giả sử f t bằng nhau ở mọi bước.

**(Demo)** Đặt ga-ma = 0.9 cho RNN, f = 0.99 cho LSTM, T = 100. RNN còn khoảng 3 nhân 10 mũ trừ 5, LSTM còn khoảng 0.37, chênh nhau hơn **10 mũ 4 lần**.

Đặt f = 1: đường xanh nằm ngang, gradient không suy giảm. Đây là trường hợp CEC của bản 1997.

Khác biệt nằm ở chỗ ga-ma của RNN phụ thuộc vào W h và tanh phẩy, rất khó giữ gần 1, còn f t là đầu ra của một cổng mà mạng có thể học để đặt gần 1 khi cần lưu thông tin.
-->

---

# Liên hệ với ResNet

<div class="grid grid-cols-2 gap-6 mt-4">
<div class="p-4 rounded bg-amber-50">

### ResNet (2015)

$$x_{l+1} = x_l + F(x_l)$$

$$\frac{\partial x_{l+1}}{\partial x_l} = I + \frac{\partial F}{\partial x_l}$$

$x_l$: đầu ra lớp $l$ · $F$: khối residual (conv–BN–ReLU) · $I$: ma trận đơn vị

Skip connection theo **chiều sâu** (các lớp)

</div>
<div class="p-4 rounded bg-blue-50">

### LSTM (1997)

$$c_t = f_t \odot c_{t-1} + i_t \odot \tilde c_t$$

$$\frac{\partial c_t}{\partial c_{t-1}} \approx \operatorname{diag}(f_t)$$

Đường tương tự skip connection, theo **thời gian** (các bước); bằng $I$ khi $f_t = 1$

</div>
</div>

<div v-click class="mt-4 text-center">
Cùng một nguyên lý: <b>phép cộng</b> tạo một đường truyền gradient không đi qua ma trận trọng số.<br>
<span class="text-sm opacity-80">Highway Network (Srivastava, Greff, Schmidhuber 2015), tiền thân của ResNet, dùng cơ chế cổng của LSTM theo chiều sâu.</span>
</div>

<!--
**[Người 3 · ~1.5 phút]**

Slide này liên hệ với ResNet trong phần CNN các bạn đã học.

Bên trái là ResNet. Khối residual tính x l cộng 1 bằng x l cộng F(x l), với x l là đầu ra của lớp l và F là các lớp bên trong khối. Đạo hàm bằng ma trận đơn vị I cộng với Jacobian của F. Nhờ số hạng I, gradient luôn có một đường truyền thẳng qua các lớp. Đó là lý do ResNet huấn luyện được mạng hơn 100 lớp.

Bên phải là LSTM: c t bằng f t nhân từng phần tử c t trừ 1 cộng chấm chấm chấm. Đạo hàm theo đường trực tiếp là hàm đường chéo của f t. Khi f bằng 1 thì chính là ma trận đơn vị.

[click] Hai mô hình dùng **cùng một nguyên lý**: phép cộng tạo một đường truyền gradient không đi qua ma trận trọng số. ResNet áp dụng theo chiều sâu, LSTM áp dụng theo chiều thời gian, và LSTM ra đời trước ResNet 18 năm. Ngoài ra, Highway Network, tiền thân trực tiếp của ResNet, do nhóm của Schmidhuber đề xuất và dùng cơ chế cổng của LSTM theo chiều sâu.
-->

---

# Thí nghiệm 1: dữ liệu e-commerce (Olist)

<div class="small mb-1">

Dự báo số đơn hàng mỗi ngày, 15/01/2017 → 22/08/2018 (585 ngày) · đầu vào: cửa sổ 14 ngày, đầu ra: số đơn ngày kế tiếp · chia 80/20 theo thời gian · Min-Max (fit trên train) · hidden 64, batch 32, clip 1.0, early stopping theo validation

</div>

<div class="ecom">

| Mô hình | Huấn luyện | Tham số | RMSE ↓ | MAPE ↓ | R² ↑ |
|---|---|---|---|---|---|
| Naive: $\hat x_t = x_{t-1}$ | — | 0 | 49.3 | 17.6% | 0.47 |
| RNN · NumPy (tự cài đặt) | A · 1 lần chạy | 4,289 | 42.5 | 17.5% | 0.60 |
| RNN · Keras `SimpleRNN` | A · 1 lần chạy | 4,289 | 41.3 | 16.1% | 0.63 |
| RNN · PyTorch `nn.RNN` | A · TB 5 seed | 4,353 | 40.8 ± 1.1 | 16.3% | 0.64 |
| <b class="text-blue-600">LSTM · PyTorch `nn.LSTM`</b> | A · TB 5 seed | 17,217 | 51.8 ± 4.4 | 21.5% | 0.41 |
| RNN · PyTorch `nn.RNN` | B · TB 5 seed | 4,353 | 39.6 ± 0.9 | 15.4% | 0.66 |
| <b class="text-blue-600">LSTM · PyTorch `nn.LSTM`</b> | B · TB 5 seed | 17,217 | 40.8 ± 3.1 | 15.3% | 0.63 |

</div>

<div class="text-xs opacity-70 mt-1">A: Adam lr 1e-3, tối đa 150 epoch, patience 15 (cấu hình của 3 notebook RNN) · B: lr 3e-3, tối đa 500 epoch, patience 50 (val loss thấp nhất cho cả hai mô hình) · RMSE tính trên số đơn gốc</div>

<div v-click class="mt-2 p-2 rounded bg-amber-50 small">

**Kết quả: trên chuỗi này LSTM không tốt hơn RNN** (cấu hình B: chênh lệch nằm trong dao động giữa các seed)
- **Phụ thuộc ngắn:** thông tin dự báo nằm trong 1–2 tuần gần nhất (mức đơn hàng, chu kỳ tuần), trong phạm vi RNN cơ bản đã học được
- **Dữ liệu nhỏ:** khoảng 410 mẫu train, LSTM có gấp 4 tham số → hội tụ chậm hơn (TB 221 so với 151 epoch); với cấu hình A, LSTM dừng khi chưa hội tụ

</div>

<style>
.ecom table { font-size: .72rem; line-height: 1.2; }
.ecom th, .ecom td { padding: .2rem .5rem !important; }
.ecom td:nth-child(n+3) { text-align: right; }
.small, .small p, .small li { font-size: .78rem; line-height: 1.35; }
.small p, .small ul { margin: .15rem 0; }
</style>

<!--
**[Người 3 · ~3 phút]**

Bây giờ là thực nghiệm. Thí nghiệm thứ nhất dùng dữ liệu thật: bộ dữ liệu đơn hàng của sàn thương mại điện tử Olist ở Brazil. Chuỗi thời gian là số đơn hàng được đặt mỗi ngày, từ tháng 1/2017 đến tháng 8/2018, tổng cộng 585 ngày. Mỗi mẫu là cửa sổ 14 ngày, mô hình dự báo số đơn của ngày kế tiếp. Dữ liệu được chia 80/20 theo thời gian và chuẩn hóa Min-Max chỉ bằng thống kê của tập train.

Ba dòng RNN đầu lấy từ ba notebook RNN nhóm đã làm trước đó: cùng một kiến trúc, một lớp 64 đơn vị ẩn và một lớp Linear, cài bằng NumPy tự viết, bằng Keras và bằng PyTorch. Cả ba đều tốt hơn baseline naive, tức dự báo bằng giá trị hôm trước: RMSE khoảng 40 đến 42 so với 49.

Nhóm thay `nn.RNN` bằng `nn.LSTM`, giữ nguyên mọi thứ khác. Với cấu hình A, tức đúng siêu tham số của các notebook RNN, LSTM **kém hơn** RNN: RMSE 51.8, còn kém cả baseline. Nguyên nhân là LSTM hội tụ chậm hơn: với learning rate 1e-3, có seed dừng sớm ở epoch 23, có seed chạy hết 150 epoch mà chưa hội tụ.

Để so sánh công bằng, nhóm dò learning rate và patience cho **cả hai** mô hình, chọn theo validation loss chứ không theo tập test. Cấu hình B, learning rate 3e-3 và patience 50, là tốt nhất cho cả hai. Với cấu hình B, RNN đạt RMSE 39.6, LSTM 40.8; độ lệch chuẩn giữa các seed của LSTM là 3.1, nên chênh lệch này không có ý nghĩa thống kê. Nhóm cũng thử cửa sổ 28, 56 và 112 ngày; chênh lệch RMSE giữa hai mô hình đều dưới 1.5. Điểm LSTM thể hiện tốt hơn là độ ổn định: với learning rate 1e-2, RMSE của RNN dao động mạnh giữa các seed, độ lệch chuẩn 6 đến 10, còn của LSTM chỉ khoảng 1.

[click] Vậy tại sao LSTM không tốt hơn ở đây? Thứ nhất, bài toán này **không có phụ thuộc xa**: số đơn ngày mai chủ yếu phụ thuộc vào mức đơn hàng và chu kỳ tuần trong một đến hai tuần gần nhất, nằm trong phạm vi khoảng 10 bước mà RNN cơ bản học được. Cơ chế giữ gradient qua cell state của LSTM không có tác dụng khi không cần truyền thông tin qua nhiều bước. Thứ hai, dữ liệu nhỏ, khoảng 410 mẫu huấn luyện, trong khi LSTM có gấp 4 tham số, nên cần nhiều epoch hơn để hội tụ.

Kết luận: LSTM không phải lúc nào cũng tốt hơn RNN. Thí nghiệm tiếp theo cho thấy LSTM tốt hơn khi nào.
-->

---

# Thí nghiệm 2: phụ thuộc xa (Adding Problem)

<div class="text-sm mb-2"><b>Adding Problem</b>: chuỗi độ dài T, mỗi bước gồm (số ngẫu nhiên ~ U(0, 1), cờ 0/1); đúng 2 vị trí có cờ 1, một ở nửa đầu, một ở nửa sau → dự đoán <b>tổng 2 số tại đó</b>. Cùng cấu hình: hidden size 64, Adam lr 1e-3, batch 64, 5000 bước, clip 1.0</div>

<CompareChart />

<div v-click class="mt-2 p-2 rounded bg-blue-50 text-sm">

**Vì sao LSTM tốt hơn ở đây:** với T = 100, tín hiệu lỗi phải truyền ngược ít nhất 50 bước. RNN: gradient là tích các $\operatorname{diag}(\tanh')\,W_h$ → biến mất (slide 5), loss đứng ở mức cơ sở. LSTM: đường trực tiếp qua cell state chỉ nhân với $f_t$ (slide 19) → gradient vẫn truyền về được.

</div>

<!--
**[Người 3 · ~2 phút]**

Thí nghiệm thứ hai được thiết kế để có phụ thuộc xa. Bài toán là Adding Problem, một bài toán chuẩn có trong bài báo năm 1997. Đầu vào là một chuỗi độ dài T; mỗi bước gồm một số ngẫu nhiên phân phối đều trong khoảng 0 đến 1 và một cờ đánh dấu. Có đúng hai vị trí được đánh dấu, và mô hình phải dự đoán tổng của hai số tại đó. Vị trí thứ nhất luôn nằm ở nửa đầu chuỗi, nên mô hình phải lưu giá trị đó qua ít nhất T/2 bước. Mô hình cơ sở luôn dự đoán hằng số 1, bằng kỳ vọng của tổng, có MSE bằng phương sai của tổng, tức 1/6 xấp xỉ 0.167; đó là đường nét đứt.

**(Bấm T = 10)** Với chuỗi ngắn, **cả hai đều học được**: loss của cả hai giảm xuống dưới đường cơ sở. Test MSE của RNN khoảng 0.0012, của LSTM là 0.0001. Giống thí nghiệm e-commerce, khi phụ thuộc ngắn thì RNN cũng giải được.

**(Bấm T = 100)** Với chuỗi dài, **loss của RNN nằm ở mức đường cơ sở** suốt 5000 bước: test MSE là 0.163, xấp xỉ 0.167 của mô hình cơ sở, nghĩa là RNN không học được phụ thuộc cần thiết. Loss của LSTM cũng nằm quanh mức cơ sở trong khoảng 2500 bước đầu, sau đó giảm nhanh và kết thúc ở test MSE 0.0033, thấp hơn RNN khoảng **50 lần**.

Bảng bên phải cho thấy chi phí: LSTM có 17,473 tham số so với 4,417 của RNN, gần gấp 4, và thời gian huấn luyện lâu hơn khoảng 10–30%.

[click] Lý do đúng như phần toán đã chỉ ra. Với T = 100, tín hiệu lỗi từ đầu ra phải truyền ngược ít nhất 50 bước để tới vị trí được đánh dấu đầu tiên. Ở RNN, gradient là tích của 50 ma trận đường chéo của tanh phẩy, nhân W h, nên biến mất, và loss đứng yên ở mức cơ sở. Ở LSTM, đường trực tiếp qua cell state chỉ nhân với f t; mạng học cách giữ f t gần 1 nên gradient vẫn truyền về được.

Tóm lại hai thí nghiệm: LSTM tốt hơn RNN khi bài toán có phụ thuộc xa; khi phụ thuộc ngắn và dữ liệu ít, RNN cơ bản là đủ. Sang phần cuối, bạn An sẽ nói về cách dùng LSTM trong thực tế.
-->

---

# Hệ quả khi cài đặt

<div class="grid grid-cols-2 gap-6 mt-2">
<div>

### 1 · Khởi tạo forget bias = 1

Khi trọng số khởi tạo nhỏ, $f_t \approx \sigma(b_f)$: với $b_f = 1$ thì $f_t \approx 0.73$ thay vì $0.5$ → mặc định **giữ lại** cell state, gần với bản 1997 ($f \equiv 1$)

```python
for name, p in lstm.named_parameters():
    if 'bias_ih' in name:
        h = p.size(0) // 4
        p.data[h:2*h].fill_(1.0)  # thứ tự i, f, g, o
```

</div>
<div v-click>

### 2 · Vẫn cần gradient clipping

Đường trực tiếp khắc phục gradient **biến mất**, nhưng các số hạng **gián tiếp** (chứa $W$) vẫn có thể **bùng nổ**

```python
loss.backward()
torch.nn.utils.clip_grad_norm_(
    model.parameters(), max_norm=1.0)
optimizer.step()
```

</div>
</div>

<!--
**[Người 4 · ~1.5 phút]**

Cảm ơn Hiếu. Phần cuối nói về cách dùng LSTM trong thực tế, bắt đầu từ hai quy tắc khi cài đặt rút ra từ phân tích gradient ở phần trước.

Thứ nhất: **khởi tạo bias của forget gate bằng 1**, theo khuyến nghị của Jozefowicz và cộng sự năm 2015. Khi trọng số còn nhỏ, f t xấp xỉ xích-ma(b f). Nếu bias bằng 0 thì f xấp xỉ xích-ma(0) bằng 0.5, mỗi bước cell state mất khoảng một nửa giá trị, và gradient theo đường trực tiếp giảm theo 0.5 mũ T. Đặt bias bằng 1 thì f xấp xỉ 0.73, nên ngay từ đầu cell state được giữ lại nhiều hơn. Trong PyTorch, bias được xếp theo thứ tự i, f, g, o, nên phần của forget gate là đoạn thứ hai, chỉ số từ h đến 2h.

[click] Thứ hai: **vẫn phải dùng gradient clipping**. Đường trực tiếp chỉ khắc phục gradient **biến mất**. Các số hạng gián tiếp ở slide 19 vẫn chứa ma trận W, nên gradient vẫn có thể **bùng nổ**. `clip_grad_norm_` chuẩn hóa lại vector gradient khi chuẩn của nó vượt `max_norm`, giúp tránh loss trở thành NaN.
-->

---

# Stacked & Bidirectional LSTM

<div class="grid grid-cols-2 gap-6">
<div>

### Stacked: xếp chồng nhiều lớp
Chuỗi $h_1, \dots, h_T$ của lớp 1 là chuỗi đầu vào của lớp 2 → lớp trên học đặc trưng trừu tượng hơn

### Bidirectional: chạy 2 chiều
$$h_t = [\,\overrightarrow{h}_t\,;\,\overleftarrow{h}_t\,]$$
$\overrightarrow{h}_t$: LSTM chạy từ trái sang phải, $\overleftarrow{h}_t$: chạy từ phải sang trái → $h_t$ phụ thuộc cả $x_{1..t}$ **và** $x_{t..T}$

<div v-click class="text-red-600 text-sm mt-2">⚠️ Không dùng bidirectional khi tại thời điểm dự đoán chưa có dữ liệu tương lai (<b>dự báo chuỗi thời gian</b>, sinh văn bản): mô hình sẽ dùng thông tin không có lúc suy luận (rò rỉ dữ liệu)</div>

</div>
<div>

```python
lstm = nn.LSTM(input_size=d, hidden_size=h,
               num_layers=2,          # stacked
               bidirectional=True,    # 2 chiều
               batch_first=True, dropout=0.2)

output, (h_n, c_n) = lstm(x)   # x: (B, T, d)
# output: (B, T, 2h)   lớp cuối, mọi bước
# h_n:    (2*2, B, h)  trạng thái cuối mỗi lớp×chiều
# (shape của h_n không đổi theo batch_first)
```

</div>
</div>

<!--
**[Người 4 · ~1.5 phút]**

Hai cách mở rộng hay dùng nhất.

**Stacked LSTM**: xếp nhiều lớp LSTM chồng lên nhau. Chuỗi hidden state h 1, chấm chấm chấm, h T của lớp dưới là chuỗi đầu vào của lớp trên. Tương tự CNN nhiều lớp, lớp trên học được đặc trưng trừu tượng hơn.

**Bidirectional LSTM**: dùng hai LSTM độc lập, một chạy từ trái sang phải, một chạy từ phải sang trái, rồi ghép hai hidden state tại mỗi bước. Như vậy biểu diễn tại bước t phụ thuộc vào cả phần trước lẫn phần sau của chuỗi. Cách này phù hợp cho phân loại văn bản hay gán nhãn từ loại, khi toàn bộ chuỗi có sẵn trước khi dự đoán.

[click] Lưu ý: **không** dùng bidirectional khi tại thời điểm dự đoán chưa có dữ liệu tương lai, ví dụ dự báo giá cổ phiếu. Khi huấn luyện, mô hình sẽ dùng thông tin từ tương lai, là thông tin không có khi triển khai; đây là rò rỉ dữ liệu.

Bên phải là code PyTorch. Chỉ cần hai tham số `num_layers` và `bidirectional`; `dropout` được áp dụng giữa các lớp. Chú ý **shape**: `output` có chiều cuối là 2h vì ghép hai chiều; chiều đầu của `h_n` bằng số lớp nhân số chiều, ở đây là 4, và `h_n` luôn có batch ở chiều thứ hai dù đặt `batch_first=True`. Đây là chỗ hay bị lỗi shape nhất.
-->

---

# Ứng dụng & giới hạn

<div class="grid grid-cols-2 gap-6">
<div>

### Ứng dụng
- **many-to-one** (chuỗi → một nhãn): phân loại cảm xúc, phân loại chuỗi
- **many-to-many** (mỗi bước một nhãn): gán nhãn từ loại, nhận dạng giọng nói
- **seq2seq**: dịch máy (encoder–decoder)
- **Chuỗi thời gian**: dự báo nhu cầu, cảm biến, tài chính
- **Sinh dữ liệu**: văn bản, nhạc, chữ viết tay

</div>
<div>

### Giới hạn
- Tính **tuần tự**: bước t phải chờ bước t−1, nên **không song song hóa** theo thời gian được
- Chuỗi rất dài (hàng nghìn token): toàn bộ ngữ cảnh phải nén vào vector $c_t, h_t$ kích thước cố định
- Nhiều tham số hơn RNN gấp 4 lần

<div v-click class="mt-4 p-3 rounded bg-slate-100">

→ **Attention** (2014) → **Transformer** (2017): bỏ cơ chế truy hồi, mỗi vị trí tính trọng số attention trực tiếp tới mọi vị trí khác

<span class="text-sm">Mô hình chuỗi: RNN (1990) → LSTM (1997) → Transformer (2017)</span>

</div>
</div>
</div>

<!--
**[Người 4 · ~1.5 phút]**

Ứng dụng của LSTM có thể phân loại theo dạng đầu vào và đầu ra. **Many-to-one**: cả chuỗi cho ra một nhãn, ví dụ phân loại cảm xúc. **Many-to-many**: mỗi bước một nhãn, ví dụ gán nhãn từ loại. **Seq2seq**: một LSTM encoder đọc câu nguồn, một LSTM decoder sinh câu đích; Google Translate dùng kiến trúc này, kết hợp attention, từ năm 2016. Ngoài ra LSTM được dùng nhiều cho chuỗi thời gian.

LSTM cũng có giới hạn. Lớn nhất là tính **tuần tự**: muốn tính bước t phải có kết quả bước t trừ 1, nên không song song hóa được theo chiều thời gian trên GPU. Với chuỗi rất dài, toàn bộ ngữ cảnh phải được nén vào vector trạng thái có kích thước cố định.

[click] Đó là lý do Attention, và sau đó Transformer năm 2017, ra đời: bỏ cơ chế truy hồi, mỗi vị trí tính trọng số attention trực tiếp tới mọi vị trí khác. Đây là chủ đề cho một buổi khác. Trong nhánh mô hình xử lý chuỗi, thứ tự phát triển là RNN, LSTM, rồi Transformer.
-->

---

# Tổng kết

<div class="grid grid-cols-3 gap-3 text-center text-sm">
<div class="p-1 rounded bg-blue-50">

<b>🧠 Cell state $c_t$</b>: bộ nhớ dài hạn, cập nhật bằng phép nhân từng phần tử và phép cộng

</div>
<div class="p-1 rounded bg-green-50">

<b>🚪 3 cổng f, i, o</b>: xóa · ghi · đọc, đều dùng sigmoid

</div>
<div class="p-1 rounded bg-amber-50">

<b>➕ Phép cộng</b>: $\partial c_t / \partial c_{t-1} \approx \operatorname{diag}(f_t)$ → gradient không biến mất

</div>
</div>

<div class="text-base font-bold mt-3 mb-1">Câu hỏi trắc nghiệm <span class="text-xs font-normal opacity-60">(bấm vào đáp án để kiểm tra)</span></div>

<QuizSet />

<!--
**[Người 4 · ~3.5 phút]**

Tóm lại bài hôm nay bằng ba ý.

Một: LSTM thêm vào RNN một **cell state**, đóng vai trò bộ nhớ dài hạn.
Hai: **ba cổng** forget, input, output, đều dùng sigmoid, quyết định tỉ lệ xóa, ghi và đọc cell state.
Ba: nhờ **phép cộng** trong cập nhật cell state, gradient có một đường truyền trực tiếp chỉ nhân với f t, nên không bị biến mất như ở RNN.

Bây giờ là bốn câu hỏi trắc nghiệm nhanh. Mời các bạn chọn đáp án, mình sẽ bấm vào đáp án được chọn: ô chuyển xanh là đúng, đỏ là sai; nếu sai thì mời bạn khác chọn lại. Khi chọn đúng, lời giải hiện ra bên dưới.

**(Demo)** Câu 1: ba cổng của LSTM là gì? Đáp án A: forget, input, output.

Câu 2: các cổng dùng hàm kích hoạt nào? Đáp án B, sigmoid, vì cần giá trị trong khoảng 0 đến 1.

Câu 3: thành phần nào là bộ nhớ dài hạn? Đáp án C, cell state c t.

Câu 4: LSTM khắc phục vấn đề nào của RNN? Đáp án A, gradient biến mất.
-->

---
layout: center
class: text-center
---

# Cảm ơn thầy và các bạn đã lắng nghe!

## Q&A

<div class="mt-8 text-sm opacity-70">
Tài liệu: Hochreiter & Schmidhuber (1997) · Gers et al. (2000) · Graves & Schmidhuber (2005) · Bengio et al. (1994) · colah.github.io/posts/2015-08-Understanding-LSTMs
</div>

<!--
**[Cả nhóm · ~2 phút]**

Phần trình bày của nhóm mình đến đây là kết thúc. Cảm ơn thầy và các bạn đã lắng nghe. Nhóm mình xin nhận câu hỏi.

*(Gợi ý chuẩn bị trước một số câu hỏi có thể gặp:)*
- *Vì sao không dùng ReLU cho các cổng?* Vì cổng là hệ số nhân, cần giá trị trong (0, 1); ReLU không bị chặn trên.
- *LSTM có loại bỏ hoàn toàn gradient biến mất không?* Không. Nó chỉ tạo một đường truyền mà mạng **có thể học** để giữ gradient; nếu f t nhỏ thì gradient vẫn suy giảm theo tích các f t.
- *Vì sao trên dữ liệu e-commerce LSTM không tốt hơn RNN?* Bài toán chỉ cần thông tin trong 1–2 tuần gần nhất, không có phụ thuộc xa; dữ liệu nhỏ trong khi LSTM có gấp 4 tham số. Nên luôn so sánh với baseline RNN trước khi chọn LSTM.
-->
