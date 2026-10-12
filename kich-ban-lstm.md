# Kịch bản thuyết trình LSTM (45 phút, 4 người)

**Mạch chung:** Cả lớp đã học CNN và RNN. Bài này đi theo câu hỏi "RNN gặp vấn đề gì → ai đã phát hiện và sửa nó, bằng cách nào → toán chứng minh vì sao LSTM hiệu quả → LSTM trong thực tế". Như vậy LSTM xuất hiện như một lời giải, không phải một định nghĩa đọc lên cho có. Phần so sánh LSTM với RNN gồm **4 slide thí nghiệm** (dữ liệu e-commerce thật, dữ liệu cổ phiếu thật, và Adding Problem), xếp theo độ dài chuỗi tăng dần: 8 → 60 → 100 bước. Thời gian còn lại dành cho cơ chế, lịch sử và toán của LSTM. Không trình bày GRU và Assignment 7.

Code mẫu: **PyTorch**.

**Phân bổ thời gian:**

| Phần | Người | Thời lượng | Mốc | Số slide |
|---|---|---|---|---|
| 1. Vì sao cần LSTM? + lịch sử ra đời | Người 1 · Nguyễn Phú Đại | ~10.5' | 0:00 → 10:30 | 8 |
| 2. Bên trong một ô LSTM | Người 2 · Trần Vũ Tiến Minh | ~11' | 10:30 → 21:30 | 8 |
| 3. Toán của LSTM + thí nghiệm so sánh với RNN | Người 3 · Trần Đình Hiếu | ~15' | 21:30 → 36:30 | 9 |
| 4. Hệ quả khi cài đặt, ứng dụng, tổng kết + trắc nghiệm | Người 4 · Phạm Thanh An | ~8' | 36:30 → 44:30 | 4 |
| Q&A | Cả nhóm | ~2' | 44:30 → 46:30 | — |

---

## Phần 1 — Người 1: "Vì sao cần LSTM?" (~11 phút)

| # | Slide | Nội dung chính | Animation / interaction |
|---|---|---|---|
| 1 | Mở đầu | Câu ví dụ: *"Tôi lớn lên ở Pháp, … (30 từ) …, nên tôi nói thành thạo tiếng ___"*. Mô hình phải nhớ chữ "Pháp" qua 30 bước. | Hiện từng từ, chữ "Pháp" mờ dần |
| 2 | Vị trí của LSTM | **MLP, CNN, RNN là ba họ kiến trúc song song** (không có quan hệ dẫn xuất). MLP: đầu vào là vector kích thước cố định, không chia sẻ trọng số. CNN: chia sẻ trọng số theo **không gian**. RNN: chia sẻ trọng số theo **thời gian**, phép truy hồi $h_t = F(h_{t-1}, x_t)$. **LSTM là một mô hình trong họ RNN** (cùng với RNN cơ bản), khác ở hàm $F$: thêm cell state và 3 cổng. | Ba khối hiện dần theo `v-click`, khối LSTM trong họ RNN hiện cuối cùng |
| 3 | Bảng so sánh | MLP / CNN / RNN / LSTM theo các tiêu chí: kiểu dữ liệu, chia sẻ trọng số, có bộ nhớ không, độ dài phụ thuộc xử lý được, số tham số | Bảng hiện từng cột |
| 4 | Ôn RNN | $h_t = \tanh(W_h h_{t-1} + W_x x_t + b)$, hình unroll theo thời gian | Unroll từng bước |
| 5 | **Toán: gradient biến mất / bùng nổ** | BPTT: $\frac{\partial h_T}{\partial h_k} = \prod_{t=k+1}^{T} \text{diag}(\tanh'(\cdot))\,W_h$. Vì $\tanh' \le 1$ nên nếu $\|W_h\| < 1$ thì tích tiến về 0, nếu $> 1$ thì bùng nổ. | **Thanh trượt:** chỉnh hệ số γ và độ dài T, đồ thị γ^T cập nhật trực tiếp (γ=0.9, T=50 → 0.005) |
| 6 | **Lịch sử: người phát hiện ra vấn đề** | **1991:** Sepp Hochreiter, sinh viên TU München, trong luận văn tốt nghiệp (diploma thesis, thầy hướng dẫn là Jürgen Schmidhuber) là người đầu tiên **phân tích toán học** hiện tượng gradient biến mất ở RNN, tức đúng công thức ở slide 5 (Bengio và cộng sự công bố độc lập năm 1994). **Ý tưởng của ông:** gradient biến mất vì bị nhân lặp lại với hệ số khác 1. Vậy chỉ cần tạo một đơn vị **tự nối với chính nó bằng trọng số đúng bằng 1, hàm kích hoạt tuyến tính** thì lỗi chảy qua bao nhiêu bước cũng không đổi. Ông gọi đó là **Constant Error Carousel (CEC)**, "băng chuyền lỗi không đổi". Vấn đề mới: mọi input đều ghi đè vào bộ nhớ đó. Vì vậy ông thêm các **cổng** (gate) để kiểm soát khi nào được ghi, khi nào được đọc. **1997:** Hochreiter và Schmidhuber công bố bài báo *"Long Short-Term Memory"* trên tạp chí *Neural Computation* (đã có bản technical report năm 1995). | Ảnh 2 tác giả; câu "trọng số = 1" hiện lên rồi biến thành hình băng chuyền |
| 7 | **Lịch sử: hành trình của LSTM** | Timeline: **1997** bản gốc, chỉ có input gate và output gate, **chưa có forget gate** · **1999–2000** Gers, Schmidhuber, Cummins thêm **forget gate** (*"Learning to Forget"*); cùng năm 2000 có thêm peephole · **2005** Graves và Schmidhuber huấn luyện bằng BPTT đầy đủ, ra đời Bidirectional LSTM · **2009** LSTM thắng các cuộc thi nhận dạng chữ viết tay · **2014** seq2seq (Sutskever, dịch máy bằng encoder–decoder LSTM) · **2015–2016** Google Voice và Google Translate dùng LSTM · **2017** Transformer ra đời và dần thay thế LSTM. Ý nghĩa của tên gọi: bộ nhớ *ngắn hạn* (activation) nhưng giữ được *lâu*. | Timeline chạy ngang, mỗi mốc hiện theo click |
| 8 | Chuyển ý | "Hãy mở ô LSTM ra xem bên trong, kể cả cái forget gate được thêm vào sau." → bàn giao cho người 2 | — |

---

## Phần 2 — Người 2: "Bên trong một ô LSTM" (~11 phút) — phần trọng tâm

| # | Slide | Nội dung chính | Animation / interaction |
|---|---|---|---|
| 9 | Ý tưởng | Hai loại trạng thái: **cell state $c_t$** (chính là băng chuyền CEC của Hochreiter, bộ nhớ dài hạn) và **hidden state $h_t$** (đầu ra, bộ nhớ ngắn hạn). So sánh trực quan RNN 1 đường với LSTM 2 đường. | Đặt hai ô cạnh nhau |
| 10 | **Forget gate** | $f_t = \sigma(W_f[h_{t-1}, x_t] + b_f)$: giữ lại bao nhiêu trí nhớ cũ (0 = quên hết, 1 = giữ nguyên). Vì sao dùng sigmoid: đầu ra trong (0,1), đóng vai trò "van". Nhắc lại: cổng này **không có trong bản 1997**. Bản 1997 có $f \equiv 1$, nên bộ nhớ không bao giờ được xóa. | Sơ đồ ô LSTM, chỉ cổng f sáng lên, có dòng chảy dữ liệu |
| 11 | **Input gate + candidate** | $i_t = \sigma(\cdot)$, $\tilde c_t = \tanh(\cdot)$: ghi thông tin mới vào bao nhiêu, ghi nội dung gì | Cổng i và $\tilde c$ sáng lên |
| 12 | **Cập nhật cell** | $c_t = f_t \odot c_{t-1} + i_t \odot \tilde c_t$. Nhấn mạnh **phép CỘNG**, chìa khóa của phần 3. | Băng chuyền chạy |
| 13 | **Output gate** | $o_t = \sigma(\cdot)$, $h_t = o_t \odot \tanh(c_t)$ | Cổng o sáng lên |
| 14 | Tổng hợp 6 phương trình | Cả bộ công thức trên 1 slide, mỗi dòng nối với vùng tương ứng trên sơ đồ | Hover vào công thức thì vùng sơ đồ sáng lên |
| 15 | **★ Slide "số n": mô phỏng tương tác 3 cổng** | Ví dụ số với hidden size = 1. Người xem chỉnh $x_t$, $h_{t-1}$, $c_{t-1}$ (hoặc chỉnh trực tiếp $f$, $i$, $o$) và thấy từng giá trị tính ra trên sơ đồ. Có nút "Step" để chạy chuỗi 5 bước, quan sát $c_t$ được giữ hay bị xóa. | Vue component: sliders, số liệu cập nhật trực tiếp, nút Step / Play |
| 16 | Ví dụ ngữ nghĩa | Câu "Pháp … tiếng ___": tại chữ "Pháp" thì i≈1 (ghi nhớ), ở các từ giữa thì f≈1 (giữ), tại chỗ trống thì o≈1 (lấy ra) | Heatmap giá trị cổng theo từng từ (vẽ minh họa) |

---

## Phần 3 — Người 3: "Toán của LSTM: vì sao nó hiệu quả?" (~15 phút)

| # | Slide | Nội dung chính | Animation / interaction |
|---|---|---|---|
| 17 | Kích thước và số tham số | Gộp 4 ma trận thành $W \in \mathbb{R}^{4h \times (h+d)}$, rồi tách đầu ra thành f, i, o, $\tilde c$ (PyTorch cũng lưu như vậy trong `weight_ih_l0`, `weight_hh_l0`). Số tham số = $4 \cdot [h(h+d) + h]$, gấp **4 lần** RNN. Lưu ý: PyTorch dùng 2 vector bias nên thực tế là $4 \cdot [h(h+d) + 2h]$. Đặt câu hỏi cho lớp tính nhẩm với d=100, h=128. | Đáp án hiện ra sau một click |
| 18 | Ví dụ tính tay forward | Chạy 2–3 bước thời gian với số cụ thể (h=1), điền giá trị f, i, o, c, h vào bảng | Các ô trong bảng hiện dần theo click |
| 19 | **Backward: gradient qua cell state** | **Bước 1, công thức đầy đủ:** $\frac{\partial c_t}{\partial c_{t-1}} = \underbrace{\text{diag}(f_t)}_{\text{trực tiếp}} + \underbrace{\big[\text{diag}(c_{t-1}\odot\sigma'_f)W_{fh} + \text{diag}(\tilde c_t\odot\sigma'_i)W_{ih} + \text{diag}(i_t\odot\tanh'_{\tilde c})W_{ch}\big]\cdot\text{diag}(o_{t-1}\odot\tanh'(c_{t-1}))}_{\text{gián tiếp, đi qua } h_{t-1}}$. Chỉ hiện trong khoảng 30 giây, tô màu 2 nhóm số hạng, **không giảng từng số hạng**. **Bước 2, tập trung vào đường trực tiếp:** chỉ có $f_t$, **không có $W$ nhân lặp lại, không có $\tanh'$**. Qua k bước: $\prod f_t$, và mạng **tự học** để giữ f≈1 khi cần nhớ. Các số hạng gián tiếp giống RNN nên vẫn có thể biến mất hoặc bùng nổ, nhưng chỉ cần còn đường trực tiếp là gradient vẫn đi qua được. **Bước 3, chi tiết lịch sử:** bản gốc 1997 *chủ động cắt bỏ* các số hạng gián tiếp khi tính gradient, chỉ giữ đường trực tiếp. | Bước 1: cả công thức hiện ra, 2 nhóm số hạng tô 2 màu. Bước 2: nhóm gián tiếp mờ đi, $\text{diag}(f_t)$ phóng to. Đặt cạnh công thức RNN của slide 5 |
| 20 | Thanh trượt so sánh gradient | Cùng độ dài T: RNN cho $\gamma^T$, LSTM cho $\prod f_t$ với f≈0.99 | Dùng lại component của slide 5, thêm đường của LSTM |
| 21 | **Nối lại kiến thức CNN** | Phép cộng trên cell state giống **skip connection của ResNet**: $x_{l+1} = x_l + F(x_l)$. Cùng một ý tưởng: tạo "đường cao tốc" cho gradient. (Highway Network năm 2015, tiền thân của ResNet, cũng do nhóm Schmidhuber đề xuất, lấy cảm hứng trực tiếp từ LSTM.) | Hình ResNet block đặt cạnh LSTM cell |
| 22 | **★ Slide "số m" (1): e-commerce, chuỗi ngắn (8 bước)** | Dữ liệu Pakistan e-commerce (`experiment/lstm_ecommerce.ipynb`): dự đoán đơn completed / canceled / refunded từ 8 đơn gần nhất. RNN và LSTM giống hệt nhau, chỉ khác `nn.RNN` ↔ `nn.LSTM`, 5 seed. LSTM tốt hơn ở accuracy, ROC-AUC, MCC (5/5 seed) nhưng rất ít (+0.3 điểm %), kém hơn ở macro F1 và recall lớp refunded. Lý do: chuỗi ngắn. | Kết luận hiện theo click |
| 23 | **★ Slide "số m" (2): cổ phiếu, chuỗi dài (60 bước)** | Dự báo biên độ dao động ngày mai của Apple, Microsoft, HP từ 60 ngày (`experiment/lstm_stock.ipynb`). LSTM tốt hơn ở mọi chỉ số, cả 5/5 seed: MAE 0.709 so với 0.727, R² 0.377 so với 0.348. | **Chọn chỉ số** để xem từng seed (component `SeedStrip`) |
| 24 | **★ Slide "số m" (3): vì sao LSTM tốt hơn ở cổ phiếu** | Độ nhạy của dự báo theo từng ngày: RNN ở ngày 1 chỉ còn ≈ 1e-4 so với ngày 60 (gradient biến mất), LSTM ≈ 1e-2; 40 ngày đầu chiếm 3.7% (RNN) so với 25% (LSTM). Cắt cửa sổ và đổi độ dài cửa sổ 20 / 60 / 120: RNN với 120 ngày y hệt 60 ngày; LSTM tốt hơn ở mọi độ dài. | **3 tab** (component `StockReach`) |
| 25 | **★ Slide "số m" (4): Adding Problem** | Bài toán có phụ thuộc rất xa. T = 10 thì cả hai học được; T = 100 thì RNN đứng ở mức cơ sở, LSTM giảm loss xuống 0.0033. Giải thích bằng gradient: tích $\operatorname{diag}(\tanh')W_h$ so với $\prod f_t$. Tổng hợp: chuỗi càng dài, LSTM càng hơn RNN rõ. | **Toggle độ dài chuỗi** T = 10 / 100 |

> ⚠️ Slide 22–25: **train trước bằng PyTorch và lưu kết quả ra JSON** (`slides/data/lstm_vs_rnn.json`, `slides/data/compare.json`), không train trực tiếp lúc thuyết trình.

---

## Phần 4 — Người 4: "LSTM trong thực tế" (~8 phút) + Q&A

| # | Slide | Nội dung chính | Animation / interaction |
|---|---|---|---|
| 26 | Hệ quả khi cài đặt | Khởi tạo **forget bias = 1** để ban đầu mô hình giữ lại cell state, gần với bản 1997. Các số hạng gián tiếp ở slide 19 vẫn có thể **bùng nổ**, nên vẫn cần gradient clipping. | Mục 2 hiện theo click |
| 27 | Stacked và Bidirectional LSTM | Xếp chồng nhiều lớp (`num_layers`); chạy 2 chiều (`bidirectional=True`) và nối $[\overrightarrow{h}, \overleftarrow{h}]$. Bidirectional không dùng được cho dự báo tương lai. | Cảnh báo hiện theo click |
| 28 | Ứng dụng và giới hạn | Dịch máy (seq2seq), nhận dạng giọng nói, dự báo chuỗi thời gian, sinh văn bản. Giới hạn: tính tuần tự nên không song song hóa được, dẫn tới Attention và Transformer (chỉ giới thiệu) | — |
| 29 | Tổng kết + câu hỏi trắc nghiệm | 3 ý chính (cell state, 3 cổng, phép cộng giúp gradient đi qua) + 4 câu trắc nghiệm dễ, không tính toán (các cổng, hàm sigmoid, cell state, gradient biến mất), bấm đáp án để biết đúng/sai | Component `QuizSet`: đáp án đúng chuyển xanh và hiện lời giải, sai chuyển đỏ |
| 30 | Q&A | ~2 phút | — |

---

## Ghi chú cho cả nhóm

- **Bàn giao giữa các người nói:** mỗi phần kết thúc bằng một câu hỏi mà phần sau trả lời (Người 1: "cấu trúc bên trong ô LSTM", Người 2: "phép cộng này có ý nghĩa gì về mặt toán?", Người 3: "trong thực tế dùng LSTM thế nào?").
- **Sợi chỉ xuyên suốt:** ý tưởng "trọng số = 1" của Hochreiter (slide 6) → cell state (slide 9) → đường trực tiếp $\text{diag}(f_t)$ (slide 19) → ResNet (slide 21). Mỗi người nên nhắc lại ý này một lần.
- **Script cho từng slide:** đặt trong speaker notes của Slidev (`<!-- ... -->`), khoảng 130 từ/phút, khoảng 1–1.5 phút cho mỗi slide (slide 6, 15 và 19 có thể cần 2–3 phút).
- **Các slide khó làm nhất:** slide 5 và 20 (thanh trượt gradient, dùng chung component), slide 15 (mô phỏng 3 cổng), slide 22–25 (thí nghiệm), slide 29 (trắc nghiệm).

## Nguồn tham khảo cho phần lịch sử

- S. Hochreiter (1991). *Untersuchungen zu dynamischen neuronalen Netzen*. Diploma thesis, TU München.
- Y. Bengio, P. Simard, P. Frasconi (1994). *Learning long-term dependencies with gradient descent is difficult*. IEEE TNN.
- S. Hochreiter, J. Schmidhuber (1997). *Long Short-Term Memory*. Neural Computation 9(8).
- F. Gers, J. Schmidhuber, F. Cummins (2000). *Learning to Forget: Continual Prediction with LSTM*. Neural Computation 12(10).
- A. Graves, J. Schmidhuber (2005). *Framewise phoneme classification with bidirectional LSTM*. Neural Networks.
