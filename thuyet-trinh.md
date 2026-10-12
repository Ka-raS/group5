# Lời thoại thuyết trình LSTM (45 phút, 4 người)

> File được sinh tự động từ speaker notes trong `slides/slides.md` (lệnh `npm run notes` trong thư mục `slides`). Muốn sửa lời thoại thì sửa trong `slides.md` rồi chạy lại lệnh, để slide và file này luôn khớp nhau.
>
> Ký hiệu: **[click]** = bấm sang bước animation tiếp theo · **(Demo)** = thao tác trên slide tương tác.
>
> Phân công: Người 1 = Nguyễn Phú Đại · Người 2 = Trần Vũ Tiến Minh · Người 3 = Trần Đình Hiếu · Người 4 = Phạm Thanh An.

---

## Phần 1 — Vì sao cần LSTM? + lịch sử ra đời (Người 1)

### Slide 1 · LSTM — Long Short-Term Memory  
*Người 1 · ~1 phút*

Xin chào thầy và các bạn. Hôm nay nhóm mình trình bày về LSTM, viết tắt của Long Short-Term Memory.

Trước khi vào bài, mời các bạn đọc câu này: "Tôi lớn lên ở Pháp, nên tôi nói thành thạo tiếng ___". Ai cũng điền được ngay: tiếng Pháp.

[click] Nếu chèn vào giữa câu khoảng 30 từ không liên quan, thì để điền được chỗ trống, mô hình phải **giữ thông tin "Pháp" qua khoảng 30 bước thời gian**.

[click] Với RNN cơ bản, ảnh hưởng của từ "Pháp" lên trạng thái ở cuối câu gần như bằng 0. Bài hôm nay trả lời ba câu hỏi: vì sao RNN không học được phụ thuộc xa, LSTM khắc phục bằng cơ chế nào, và vì sao về mặt toán học cơ chế đó hiệu quả.

### Slide 2 · Vị trí của LSTM trong các kiến trúc mạng nơ-ron  
*Người 1 · ~1.5 phút*

Trước khi vào LSTM, mình xác định vị trí của nó so với các kiến trúc mà lớp đã học.

[click] **MLP** là mạng kết nối đầy đủ: đầu vào là một vector có kích thước cố định, mỗi trọng số gắn với một vị trí đầu vào cố định. MLP không khai thác cấu trúc không gian hay thời gian của dữ liệu.

[click] **CNN**, các bạn đã làm ở assignment trước, dành cho dữ liệu dạng lưới như ảnh. Cùng một kernel được áp dụng tại mọi vị trí, tức là **chia sẻ trọng số theo không gian**.

[click] **RNN** dành cho dữ liệu chuỗi. Cùng một bộ trọng số được áp dụng ở mọi bước thời gian, tức là **chia sẻ trọng số theo thời gian**. Trạng thái ẩn được cập nhật theo phép truy hồi h t bằng F(h t trừ 1, x t). Lưu ý: MLP, CNN và RNN là **ba họ kiến trúc song song**, mỗi họ ứng với một giả định về cấu trúc dữ liệu; không họ nào được suy ra từ họ nào.

[click] LSTM **không phải một họ mô hình mới, mà là một mô hình trong họ RNN**, giống RNN cơ bản. Nó dùng cùng phép truy hồi, cùng chia sẻ trọng số qua các bước, và cùng được huấn luyện bằng lan truyền ngược theo thời gian, viết tắt là BPTT. Điểm khác duy nhất là hàm F: RNN cơ bản dùng một lớp tanh, còn LSTM dùng thêm một cell state c t và ba cổng để điều khiển việc ghi, xóa và đọc cell state.

### Slide 3 · So sánh MLP · CNN · RNN · LSTM  
*Người 1 · ~1 phút*

Bảng này tóm tắt khác biệt giữa bốn mô hình. Mình lưu ý ba dòng.

Dòng **trạng thái**: MLP và CNN không có trạng thái, mỗi mẫu đầu vào được xử lý độc lập. RNN có một hidden state h t. LSTM có **hai** trạng thái: h t và cell state c t. Cell state c t là thành phần trung tâm của cả bài.

Dòng **phạm vi ngữ cảnh**: trên thực tế RNN cơ bản thường chỉ học được phụ thuộc trong khoảng 10 bước. Bài báo gốc năm 1997 cho thấy LSTM học được phụ thuộc cách nhau hơn 1000 bước.

Dòng **số tham số**: với cùng kích thước, LSTM có gấp 4 lần số tham số của RNN. Lát nữa bạn Hiếu sẽ giải thích vì sao đúng bằng 4.

[click] Tóm lại: LSTM giữ nguyên cơ chế truy hồi của RNN, và khắc phục hạn chế chính của RNN là khó học phụ thuộc xa.

### Slide 4 · Ôn lại RNN  
*Người 1 · ~1.5 phút*

Ôn lại nhanh RNN mà các bạn đã làm. Ở mỗi bước t, trạng thái ẩn mới h t được tính từ trạng thái ẩn trước h t trừ 1 và đầu vào x t: nhân h t trừ 1 với ma trận W h, nhân x t với ma trận W x, cộng bias b, rồi áp dụng tanh cho từng phần tử. Với d là kích thước đầu vào và h là kích thước trạng thái ẩn, W h có kích thước h nhân h, W x có kích thước h nhân d. Hàm tanh đưa giá trị về khoảng (trừ 1, 1).

[click] [click] [click] [click] Khi trải mạng theo thời gian (unrolling), ta được một chuỗi các ô nối tiếp nhau. Các mũi tên ngang màu cam là phép nhân với **cùng một ma trận W h** ở mọi bước; các mũi tên dọc là phép nhân với cùng một W x.

[click] Để huấn luyện, ta dùng lan truyền ngược theo thời gian (BPTT), tức là áp dụng backpropagation trên đồ thị đã trải theo thời gian. Vì W h xuất hiện ở mọi bước, gradient từ bước cuối truyền về bước đầu phải nhân qua W h nhiều lần. Đây là nguồn gốc của vấn đề ở slide tiếp theo.

### Slide 5 · Vấn đề: gradient biến mất / bùng nổ  
*Người 1 · ~2 phút*

Đây là phần toán chính của phần mở đầu. Để biết lỗi ở bước cuối T ảnh hưởng thế nào tới trạng thái ở bước k, ta tính đạo hàm partial h T trên partial h k. Theo quy tắc chuỗi, đạo hàm này là **tích** của T trừ k ma trận Jacobian partial h t trên partial h t trừ 1. Mỗi Jacobian bằng ma trận đường chéo chứa đạo hàm tanh tại a t, nhân với W h; a t là giá trị bên trong tanh.

Đạo hàm của tanh bằng 1 trừ tanh mũ 2, luôn nằm trong khoảng (0, 1]. Gọi ga-ma là cận trên chuẩn của mỗi thừa số, bằng chuẩn của W h nhân với giá trị lớn nhất của tanh phẩy:
- nếu ga-ma nhỏ hơn 1, chuẩn của tích bị chặn bởi ga-ma mũ T trừ k, nên tiến về 0 theo hàm mũ: gradient biến mất;
- nếu chuẩn của W h lớn hơn 1, tích **có thể** tăng theo hàm mũ: gradient bùng nổ. Đây là điều kiện cần, không phải điều kiện đủ.

**(Demo)** Đồ thị dùng mô hình đơn giản hóa: mỗi thừa số có độ lớn đúng bằng ga-ma. Với ga-ma bằng 0.9 và T bằng 50 bước, ta được 0.9 mũ 50 xấp xỉ 0.005, tức là độ lớn gradient truyền từ bước 50 về bước đầu chỉ còn **0.5%**. Tăng T lên 100 thì còn khoảng 3 nhân 10 mũ trừ 5. Tăng ga-ma lên 1.1 thì đồ thị tăng theo hàm mũ: gradient bùng nổ.

Không thể giữ ga-ma đúng bằng 1 trong suốt quá trình huấn luyện, vì W h thay đổi sau mỗi lần cập nhật và tanh phẩy thay đổi theo dữ liệu. Đó là lý do RNN không học được phụ thuộc giữa từ "Pháp" và vị trí cần dự đoán ở slide đầu.

### Slide 6 · Lịch sử: phát hiện vấn đề và đề xuất LSTM  
*Người 1 · ~2 phút*

Vậy ai là người đã nhìn ra vấn đề này và sửa nó?

[click] Năm 1991, Sepp Hochreiter, khi đó là **sinh viên** Đại học Kỹ thuật München, làm luận văn tốt nghiệp dưới sự hướng dẫn của Jürgen Schmidhuber. Trong luận văn này, ông đưa ra **phân tích toán học đầu tiên** giải thích vì sao RNN không học được phụ thuộc xa, chính là tích các ma trận Jacobian ở slide trước. Năm 1994, Bengio, Simard và Frasconi công bố độc lập kết quả tương tự.

[click] Hướng khắc phục suy ra trực tiếp từ công thức: gradient suy giảm vì bị nhân lặp lại với hệ số khác 1. Vì vậy ông dùng một đơn vị có **liên kết tự hồi quy với trọng số cố định bằng 1** và hàm kích hoạt tuyến tính. Khi đó đạo hàm của c t theo c t trừ 1 đúng bằng 1, nên tín hiệu lỗi truyền qua bao nhiêu bước cũng không đổi độ lớn. Ông gọi đơn vị này là **Constant Error Carousel**, viết tắt CEC.

[click] Cách làm này sinh ra vấn đề mới: mọi đầu vào đều được cộng trực tiếp vào c t, kể cả đầu vào không liên quan, nên nội dung đã lưu bị ghi đè. Giải pháp là thêm các **cổng**, là các hệ số nhân trong khoảng 0 đến 1, đặt ở đầu vào và đầu ra của CEC để điều khiển khi nào được ghi và khi nào được đọc. Kết quả được công bố trong bài báo "Long Short-Term Memory" năm 1997 trên tạp chí Neural Computation, một trong những bài báo được trích dẫn nhiều nhất của lĩnh vực học sâu.

### Slide 7 · Các mốc phát triển của LSTM  
*Người 1 · ~1 phút*

Điểm qua nhanh hành trình của LSTM.

[click] Bản gốc năm 1997 chỉ có hai cổng: input gate và output gate. **Chưa có forget gate**, nghĩa là cell state chỉ được cộng thêm, không có cơ chế xóa.

[click] Năm 1999–2000, Felix Gers, Schmidhuber và Cummins thêm **forget gate**, cho phép mạng học cách xóa nội dung trong cell state. LSTM dùng ngày nay, kể cả `nn.LSTM` trong PyTorch, là phiên bản có forget gate. Cũng năm 2000, Gers và Schmidhuber đề xuất kết nối peephole, cho các cổng đọc trực tiếp cell state; PyTorch không dùng peephole.

[click] Năm 2005, Alex Graves và Schmidhuber huấn luyện LSTM bằng gradient BPTT đầy đủ, thay vì gradient bị cắt bớt như bản 1997, và giới thiệu Bidirectional LSTM. [click] Năm 2009, LSTM thắng các cuộc thi nhận dạng chữ viết tay. [click] Năm 2014, Sutskever và cộng sự dùng hai LSTM làm encoder và decoder cho dịch máy, gọi là seq2seq. [click] Khoảng 2015–2016, nhận dạng giọng nói của Google và Google Translate chuyển sang LSTM. [click] Đến 2017, Transformer xuất hiện và dần thay thế LSTM trong xử lý ngôn ngữ.

[click] Về tên gọi: trong bài báo gốc, "short-term memory" là giá trị kích hoạt của mạng, phân biệt với "long-term memory" là các trọng số được học chậm qua huấn luyện. "Long short-term memory" nghĩa là giá trị kích hoạt đó được duy trì qua nhiều bước thời gian.

### Slide 8 · Cấu trúc bên trong một ô LSTM  
*Người 1 · ~0.5 phút*

Tóm lại, RNN không học được phụ thuộc xa vì gradient bị nhân lặp lại qua W h và tanh phẩy, và Hochreiter khắc phục bằng một đơn vị tự hồi quy có trọng số bằng 1 (CEC) kết hợp với các cổng. Tiếp theo, mời bạn Minh trình bày cấu trúc bên trong ô LSTM và cách từng cổng hoạt động.

---

## Phần 2 — Bên trong một ô LSTM (Người 2)

### Slide 9 · Hai trạng thái: hidden state và cell state  
*Người 2 · ~1 phút*

Cảm ơn Đại. Chúng ta bắt đầu bằng hình ảnh tổng thể.

Bên trái là RNN: chỉ có **một trạng thái** h. Toàn bộ thông tin cần lưu phải nằm trong h, và ở mỗi bước h đều bị nhân với W h rồi đi qua tanh.

Bên phải là LSTM. Đường màu xanh nằm ngang phía trên là **cell state c t**, một vector cùng kích thước h với hidden state.

[click] Trên đường đi từ c t trừ 1 đến c t chỉ có một phép nhân từng phần tử và một phép cộng, không có ma trận trọng số và không có hàm kích hoạt. Đây là Constant Error Carousel của Hochreiter, đóng vai trò bộ nhớ dài hạn.

[click] h t vẫn là đầu ra tại mỗi bước như ở RNN. Nó được tính từ c t thông qua output gate, đóng vai trò bộ nhớ ngắn hạn.

Ba cổng tiếp theo điều khiển ba thao tác trên cell state: xóa, ghi và đọc.

### Slide 10 · Cổng 1 · Forget gate: giữ lại bao nhiêu từ $c_{t-1}$?  
*Người 2 · ~1.5 phút*

Cổng đầu tiên là **forget gate**, màu đỏ.

Đầu vào của cổng là hidden state trước h t trừ 1 và đầu vào hiện tại x t, ghép nối thành một vector kích thước h cộng d. Vector này được nhân với ma trận W f kích thước h nhân (h cộng d), cộng bias b f, rồi đi qua hàm sigmoid xích-ma(z) bằng 1 trên (1 cộng e mũ trừ z).

[click] Kết quả f t là một vector cùng kích thước với cell state, mỗi phần tử nằm trong khoảng 0 đến 1.

[click] Nếu một phần tử của f t bằng 0, phần tử tương ứng của c t trừ 1 bị nhân với 0, tức là bị **xóa hoàn toàn**. [click] Nếu bằng 1 thì phần tử đó được **giữ nguyên**.

[click] Lý do dùng sigmoid thay vì ReLU hay tanh: sigmoid cho đầu ra trong khoảng (0, 1), phù hợp để làm hệ số nhân: 0 chặn hoàn toàn, 1 cho qua hoàn toàn. ReLU không bị chặn trên, còn tanh cho giá trị âm.

[click] Như bạn Đại đã nói, cổng này **không có** trong bản gốc năm 1997. Bản gốc tương đương với f luôn bằng 1, nên cell state chỉ được cộng thêm mà không có cơ chế xóa. Ví dụ, khi văn bản chuyển sang một chủ đề khác, mạng cần xóa thông tin "Pháp" khỏi cell state. Forget gate cho phép mạng học khi nào cần xóa.

### Slide 11 · Cổng 2 · Input gate: ghi gì, ghi bao nhiêu?  
*Người 2 · ~1.5 phút*

Cổng thứ hai, màu xanh lá, gồm hai thành phần có cùng dạng với forget gate, mỗi thành phần có ma trận trọng số và bias riêng.

Thành phần thứ nhất là **candidate** c̃ t, dùng hàm tanh. [click] Đây là **nội dung** mới cần ghi vào cell state. Vì dùng tanh nên giá trị nằm trong khoảng −1 đến 1, cho phép tăng hoặc giảm giá trị của cell state.

[click] Thành phần thứ hai là **input gate** i t, dùng sigmoid. Nó quyết định **tỉ lệ** được ghi cho từng phần tử: 0 là không ghi, 1 là ghi toàn bộ.

[click] Phần thực sự được ghi vào là tích từng phần tử i t nhân từng phần tử c̃ t. Ký hiệu hình tròn chấm là phép nhân từng phần tử của hai vector cùng kích thước.

Lý do tách thành hai thành phần: đây chính là vấn đề Hochreiter giải quyết bằng cổng, không phải đầu vào nào cũng cần được lưu. Với câu ví dụ, tại từ "Pháp", i gần 1 để ghi; tại các từ như "học tiểu học", "chơi bóng đá", i gần 0 để nội dung đã lưu không bị ghi đè.

### Slide 12 · Cập nhật cell state bằng phép cộng  
*Người 2 · ~1 phút*

Bây giờ ghép hai cổng lại để cập nhật cell state. Công thức trong khung là công thức quan trọng nhất của LSTM.

[click] Diễn giải: cell state mới bằng phần được giữ lại từ cell state cũ, **cộng** với phần được ghi mới.

[click] So sánh với RNN: trạng thái cũ h t trừ 1 bị nhân với ma trận W h rồi đi qua tanh ở **mỗi bước**.

[click] Ở LSTM, c t trừ 1 chỉ được nhân từng phần tử với f t, có giá trị trong khoảng 0 đến 1, rồi **cộng** thêm phần ghi mới. Không có phép nhân ma trận, không có hàm kích hoạt.

[click] Lát nữa bạn Hiếu sẽ chứng minh chính phép cộng này giúp gradient không bị biến mất.

### Slide 13 · Cổng 3 · Output gate: đọc ra bao nhiêu?  
*Người 2 · ~1 phút*

Cổng cuối cùng là **output gate**, màu tím.

Cell state là trạng thái nội bộ của ô. Đầu ra h t được tính từ cell state qua hai bước. [click] Đầu tiên cho c t qua tanh để đưa giá trị về khoảng −1 đến 1. [click] Sau đó nhân từng phần tử với output gate o t, cũng là một sigmoid với trọng số W o và bias b o riêng, để quyết định tỉ lệ đọc ra của từng phần tử.

[click] Hệ quả: mạng có thể **lưu** thông tin "Pháp" trong cell state suốt 30 bước mà không ảnh hưởng tới các đầu ra ở giữa. Đến từ "tiếng", khi cần dự đoán tên ngôn ngữ, output gate mới mở để đọc thông tin đó ra h t.

### Slide 14 · Tổng hợp: 6 phương trình của LSTM  
*Người 2 · ~1 phút*

Đây là toàn bộ LSTM trên một slide: sáu phương trình. Mình bấm lần lượt để đối chiếu từng phương trình với vị trí tương ứng trên sơ đồ.

[click] Forget gate. [click] Input gate và candidate. [click] Cập nhật cell state. [click] Output gate và đầu ra h t.

Để ý rằng bốn phương trình f, i, c̃, o có **cùng một dạng**: nhân ma trận với [h t trừ 1, x t], cộng bias, rồi cho qua sigmoid hoặc tanh. Điểm này rất quan trọng khi tính số tham số và khi xem cách PyTorch lưu trọng số. Bạn Hiếu sẽ quay lại điểm này.

### Slide 15 · Mô phỏng tính toán trong một ô LSTM  
*Người 2 · ~3 phút*

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

### Slide 16 · Ví dụ minh họa: giá trị các cổng trên câu mẫu  
*Người 2 · ~1 phút*

Quay lại câu ví dụ ở đầu bài. Bảng này minh họa giá trị của ba cổng tại từng từ mà ta mong muốn một mô hình đã huấn luyện tốt có được. Lưu ý đây là số liệu minh họa, không phải số đo từ một mô hình đã huấn luyện.

[click] Tại từ "Pháp", input gate gần 1 để ghi thông tin vào cell state.

[click] Ở các từ ở giữa, forget gate gần 1 để giữ cell state, input gate gần 0 để không ghi đè.

[click] Tại từ "tiếng", output gate gần 1 để đọc thông tin "Pháp" ra h t và dự đoán từ tiếp theo.

Đến đây là toàn bộ cơ chế lan truyền xuôi của LSTM. Câu hỏi còn lại: phép cộng trong cập nhật cell state có ý nghĩa gì về mặt toán? Mời bạn Hiếu.

---

## Phần 3 — Toán của LSTM + thí nghiệm so sánh với RNN (Người 3)

### Slide 17 · Kích thước ma trận và số tham số  
*Người 3 · ~1.5 phút*

Cảm ơn Minh. Phần của mình đi vào toán, bắt đầu bằng một câu hỏi rất thực tế: một lớp LSTM có bao nhiêu tham số?

Gọi kích thước đầu vào là d, kích thước hidden là h. Vector ghép [h t trừ 1, x t] có kích thước h cộng d. Mỗi cổng cần một ma trận h nhân (h cộng d) và một bias h.

Như bạn Minh đã nói, bốn phương trình f, i, c̃, o có cùng dạng, nên ta có thể **gộp 4 ma trận thành một** ma trận 4h nhân (h cộng d), thực hiện một phép nhân rồi tách vector kết quả thành 4 đoạn, mỗi đoạn dài h, sau đó áp dụng sigmoid hoặc tanh cho từng đoạn. PyTorch cũng làm đúng như vậy: các bạn mở `weight_ih_l0` sẽ thấy nó có 4h hàng, theo thứ tự i, f, g, o, trong đó g là candidate.

Vậy số tham số là 4 nhân [h(h cộng d) cộng h]. Mời các bạn tính nhẩm với d = 100, h = 128.

[click] Kết quả là 117,248, đúng gấp 4 lần RNN. Lưu ý: PyTorch dùng hai vector bias riêng cho phần đầu vào và phần trạng thái ẩn, nên nếu đếm trong code sẽ ra 117,760. Tương tự, `nn.RNN` với cùng kích thước có 29,440 tham số. Đây là điểm hay gây nhầm lẫn khi làm bài.

### Slide 18 · Tính tay lan truyền xuôi qua 2 bước thời gian  
*Người 3 · ~2 phút*

Để kiểm tra lại quá trình lan truyền xuôi, mình tính tay hai bước với LSTM vô hướng ở slide mô phỏng. Ban đầu h 0 bằng c 0 bằng 0.

**Bước 1, x = 2.** [click] Forget gate bằng sigmoid của 0.5 nhân 0 cộng 3 nhân 2 cộng 3 bằng 9, ra khoảng 0.9999. Input gate bằng sigmoid của 5, ra 0.9933. Candidate bằng tanh của 4, ra 0.9993.
[click] Cell state: c 0 bằng 0 nên chỉ còn phần ghi mới, 0.9933 nhân 0.9993 bằng 0.9926.
[click] Output gate bằng sigmoid của 3, ra 0.9526. Vậy h 1 bằng 0.9526 nhân tanh(0.9926) bằng 0.7225.

**Bước 2, x = 0.** Bây giờ h 1 bằng 0.7225, nên 0.5 h bằng 0.361.
[click] f bằng sigmoid của 3.361, ra 0.9665. i bằng sigmoid của −2.639, ra 0.0667, rất nhỏ. Candidate là 0.3463.
[click] Cell state: 0.9665 nhân 0.9926 cộng 0.0667 nhân 0.3463 bằng 0.9825.
[click] o là 0.796, và h 2 bằng 0.6003.

[click] Điểm cần thấy: ở bước 2 gần như không có gì mới được ghi, nhưng cell state vẫn giữ ở mức 0.98. Giá trị đã ghi ở bước 1 được giữ lại nhờ forget gate gần bằng 1.

### Slide 19 · Lan truyền ngược: gradient qua cell state  
*Người 3 · ~2.5 phút*

Đây là câu hỏi cốt lõi: khi lan truyền ngược, gradient đi từ c t về c t trừ 1 như thế nào?

[click] Nhìn lại công thức c t bằng f t nhân từng phần tử c t trừ 1 cộng i t nhân từng phần tử c̃ t. Biến c t trừ 1 ảnh hưởng tới c t qua **hai đường**.

- **Đường trực tiếp**, màu xanh: c t trừ 1 được nhân từng phần tử với f t. Đạo hàm theo đường này là ma trận đường chéo của f t.
- **Đường gián tiếp**, màu xám: c t trừ 1 tạo ra h t trừ 1 bằng o t trừ 1 nhân từng phần tử tanh(c t trừ 1), và h t trừ 1 là đầu vào của các cổng ở bước t. Đạo hàm theo đường này cho ra ba số hạng trong ngoặc vuông, ứng với f t, i t và c̃ t. W fh, W ih, W ch là phần của các ma trận trọng số nhân với h t trừ 1. Không cần nhớ chi tiết các số hạng này; điểm cần thấy là mỗi số hạng đều chứa **ma trận W** và **đạo hàm của sigmoid hoặc tanh**, tức là có cấu trúc giống RNN.

[click] Bây giờ đặt RNN và đường trực tiếp của LSTM cạnh nhau. Bên trái, RNN: tích của các ma trận đường chéo của tanh phẩy, nhân W h, nên biến mất hoặc bùng nổ. Bên phải, LSTM: chỉ là tích các hàm đường chéo của f t. **Không có ma trận trọng số, không có đạo hàm của hàm kích hoạt.** Hơn nữa, f t là đại lượng mạng **học** được: khi cần lưu thông tin, mạng học cách giữ f gần 1, và gradient truyền qua gần như không suy giảm.

Các số hạng gián tiếp vẫn có thể biến mất. Nhưng gradient toàn phần là tổng theo các đường, nên **chỉ cần đường trực tiếp còn thì gradient vẫn truyền về được**.

[click] Một chi tiết lịch sử: trong bài báo năm 1997, Hochreiter và Schmidhuber **chủ động cắt bỏ** các số hạng gián tiếp khi huấn luyện (truncated gradient), chỉ giữ đường trực tiếp. Phải đến năm 2005, Graves mới huấn luyện bằng gradient đầy đủ.

### Slide 20 · So sánh $\gamma^T$ (RNN) và $\prod f_t$ (LSTM)  
*Người 3 · ~1 phút*

Đây là đồ thị của bạn Đại ở slide 5, thêm đường màu xanh cho đường trực tiếp của LSTM, giả sử f t bằng nhau ở mọi bước.

**(Demo)** Đặt ga-ma = 0.9 cho RNN, f = 0.99 cho LSTM, T = 100. RNN còn khoảng 3 nhân 10 mũ trừ 5, LSTM còn khoảng 0.37, chênh nhau hơn **10 mũ 4 lần**.

Đặt f = 1: đường xanh nằm ngang, gradient không suy giảm. Đây là trường hợp CEC của bản 1997.

Khác biệt nằm ở chỗ ga-ma của RNN phụ thuộc vào W h và tanh phẩy, rất khó giữ gần 1, còn f t là đầu ra của một cổng mà mạng có thể học để đặt gần 1 khi cần lưu thông tin.

### Slide 21 · Liên hệ với ResNet  
*Người 3 · ~1.5 phút*

Slide này liên hệ với ResNet trong phần CNN các bạn đã học.

Bên trái là ResNet. Khối residual tính x l cộng 1 bằng x l cộng F(x l), với x l là đầu ra của lớp l và F là các lớp bên trong khối. Đạo hàm bằng ma trận đơn vị I cộng với Jacobian của F. Nhờ số hạng I, gradient luôn có một đường truyền thẳng qua các lớp. Đó là lý do ResNet huấn luyện được mạng hơn 100 lớp.

Bên phải là LSTM: c t bằng f t nhân từng phần tử c t trừ 1 cộng chấm chấm chấm. Đạo hàm theo đường trực tiếp là hàm đường chéo của f t. Khi f bằng 1 thì chính là ma trận đơn vị.

[click] Hai mô hình dùng **cùng một nguyên lý**: phép cộng tạo một đường truyền gradient không đi qua ma trận trọng số. ResNet áp dụng theo chiều sâu, LSTM áp dụng theo chiều thời gian, và LSTM ra đời trước ResNet 18 năm. Ngoài ra, Highway Network, tiền thân trực tiếp của ResNet, do nhóm của Schmidhuber đề xuất và dùng cơ chế cổng của LSTM theo chiều sâu.

### Slide 22 · Thí nghiệm 1: e-commerce, chuỗi ngắn (8 bước)  
*Người 3 · ~1.5 phút*

Bây giờ là thực nghiệm. Nhóm so sánh LSTM với RNN trên hai bộ dữ liệu thật mà nhóm đã làm với RNN trong bài tập trước, và một bài toán tổng hợp.

Ở cả hai bộ dữ liệu, hai mô hình **giống hệt nhau**: hai lớp hồi quy 64 và 32 đơn vị, cùng optimizer, cùng learning rate, cùng gradient clipping, cùng thứ tự batch. Thứ duy nhất khác là thay `nn.RNN` bằng `nn.LSTM`. Mỗi mô hình chạy 5 seed để thấy độ dao động. Nhóm cũng kiểm tra lại: RNN với seed 42 cho đúng con số của bài tập trước.

Thí nghiệm thứ nhất: dữ liệu thương mại điện tử của Pakistan, khoảng 400 nghìn đơn hàng. Khi khách đặt một đơn, mô hình dự đoán đơn đó sẽ hoàn thành, bị hủy hay bị trả lại, dựa trên **8 đơn gần nhất** của khách. Dữ liệu chia theo thời gian.

LSTM tốt hơn RNN ở accuracy, ROC-AUC và MCC, và tốt hơn ở **cả 5 seed**. Nhưng mức chênh rất nhỏ: accuracy chỉ tăng 0.3 điểm phần trăm. Ở macro F1 và recall của lớp bị trả lại, LSTM còn kém hơn một chút.

[click] Lý do là chuỗi ở đây rất ngắn, chỉ 8 bước. Thông tin quan trọng nằm ở đơn đang đặt và vài đơn gần nhất, nên không có phụ thuộc xa để cell state phát huy. Còn lớp bị trả lại thì khó với cả hai mô hình, vì lúc đặt hàng nó trông giống hệt một đơn sẽ hoàn thành.

Vậy nếu chuỗi dài hơn thì sao? Đó là thí nghiệm thứ hai.

### Slide 23 · Thí nghiệm 2: cổ phiếu, chuỗi dài (60 bước)  
*Người 3 · ~2 phút*

Thí nghiệm thứ hai dùng giá cổ phiếu theo ngày của Apple, Microsoft và HP. Mô hình dự báo **biên độ dao động của ngày mai**, tức giá cao nhất chia giá thấp nhất trong ngày, từ **60 ngày giao dịch** trước đó. Nhóm chọn biên độ thay vì giá, vì biến động có tính "nhớ": ngày sôi động thường đi sau ngày sôi động, và tương quan này kéo dài nhiều tuần. Mô hình học trên dữ liệu từ 1995 đến 2016, và được đánh giá trên 6 năm từ 2020 đến 2025. Cấu hình giống hệt thí nghiệm 1.

Bảng bên trái là trung bình 5 seed. LSTM tốt hơn ở **mọi chỉ số**: sai số tuyệt đối trung bình MAE giảm từ 0.727 xuống 0.709, R² tăng từ 0.35 lên 0.38, và đoán đúng hướng biến động nhiều hơn khoảng 1 điểm phần trăm.

**(Demo: bấm qua các chỉ số MAE, RMSE, R²)** Hình bên phải vẽ từng seed: mỗi chấm là một lần huấn luyện. Năm chấm xanh của LSTM và năm chấm cam của RNN **tách hẳn nhau**, không chồng lên nhau.

[click] Nghĩa là LSTM tốt hơn ở cả 5 trên 5 seed. Seed tệ nhất của LSTM vẫn tốt hơn seed tốt nhất của RNN. LSTM cũng ổn định hơn: kết quả giữa các seed dao động ít hơn khoảng 6 lần. Đổi lại, LSTM có gấp 4 lần tham số và mỗi epoch chậm hơn khoảng 1.5 lần.

Câu hỏi tiếp theo: vì sao LSTM tốt hơn ở đây?

### Slide 24 · Vì sao? LSTM dùng được những ngày xa hơn  
*Người 3 · ~1.5 phút*

Để trả lời, nhóm đo xem dự báo thay đổi bao nhiêu khi thay đổi dữ liệu của từng ngày trong cửa sổ, tức đạo hàm của đầu ra theo đầu vào ở từng ngày. Đạo hàm này đi ngược qua các bước thời gian, nên chính là thứ bị biến mất ở RNN.

**(Demo: hình 1, độ nhạy theo ngày)** Trục tung là thang log, so với ngày gần nhất. Đường cam của RNN rơi rất nhanh: ở ngày đầu tiên của cửa sổ chỉ còn khoảng một phần mười nghìn. Đường xanh của LSTM giảm chậm hơn nhiều, ở ngày đầu vẫn còn khoảng một phần trăm, lớn hơn RNN khoảng 75 lần. Bảng bên phải: chỉ 3.7% độ nhạy của RNN đến từ 40 ngày đầu, còn ở LSTM là 25%.

**(Demo: hình 2, chỉ giữ k ngày gần nhất)** Xóa dữ liệu của các ngày cũ rồi chạy lại. Với RNN, từ 20 ngày trở đi, thêm ngày cũ không làm sai số thay đổi chút nào. LSTM thì ngược lại: nếu chỉ giữ 5 hay 10 ngày, LSTM còn sai nhiều hơn RNN, vì nó đã học cách dựa vào những ngày cũ; bỏ những ngày đó đi thì nó mất thông tin. Từ 20 ngày trở lên thì LSTM tốt hơn RNN.

**(Demo: hình 3, độ dài cửa sổ)** Khi huấn luyện lại với cửa sổ 120 ngày, RNN cho kết quả y hệt cửa sổ 60 ngày: 60 ngày thêm vào không truyền được gradient về. Nhóm cũng phải nói rõ: với dữ liệu này, cửa sổ 20 ngày cho kết quả tốt nhất ở cả hai mô hình, vì thông tin quan trọng nhất nằm trong khoảng một tháng gần đây. Nhưng ở cả ba độ dài, LSTM đều tốt hơn RNN.

[click] Tóm lại: RNN gặp đúng hiện tượng gradient biến mất ở slide 5, còn LSTM nhờ đường truyền qua cell state ở slide 19 nên giữ được tín hiệu từ những ngày xa.

### Slide 25 · Thí nghiệm 3: phụ thuộc rất xa (Adding Problem)  
*Người 3 · ~1.5 phút*

Thí nghiệm thứ ba đẩy độ dài lên mức cực đoan, và được thiết kế để có phụ thuộc xa. Bài toán là Adding Problem, một bài toán chuẩn có trong bài báo năm 1997. Đầu vào là một chuỗi độ dài T; mỗi bước gồm một số ngẫu nhiên phân phối đều trong khoảng 0 đến 1 và một cờ đánh dấu. Có đúng hai vị trí được đánh dấu, và mô hình phải dự đoán tổng của hai số tại đó. Vị trí thứ nhất luôn nằm ở nửa đầu chuỗi, nên mô hình phải lưu giá trị đó qua ít nhất T/2 bước. Mô hình cơ sở luôn dự đoán hằng số 1, bằng kỳ vọng của tổng, có MSE bằng phương sai của tổng, tức 1/6 xấp xỉ 0.167; đó là đường nét đứt.

**(Bấm T = 10)** Với chuỗi ngắn, **cả hai đều học được**: loss của cả hai giảm xuống dưới đường cơ sở. Test MSE của RNN khoảng 0.0012, của LSTM là 0.0001. Giống thí nghiệm 1, khi phụ thuộc ngắn thì RNN cũng giải được.

**(Bấm T = 100)** Với chuỗi dài, **loss của RNN nằm ở mức đường cơ sở** suốt 5000 bước: test MSE là 0.163, xấp xỉ 0.167 của mô hình cơ sở, nghĩa là RNN không học được phụ thuộc cần thiết. Loss của LSTM cũng nằm quanh mức cơ sở trong khoảng 2500 bước đầu, sau đó giảm nhanh và kết thúc ở test MSE 0.0033, thấp hơn RNN khoảng **50 lần**.

[click] Lý do đúng như phần toán đã chỉ ra. Với T = 100, tín hiệu lỗi từ đầu ra phải truyền ngược ít nhất 50 bước để tới vị trí được đánh dấu đầu tiên. Ở RNN, gradient là tích của 50 ma trận đường chéo của tanh phẩy, nhân W h, nên biến mất, và loss đứng yên ở mức cơ sở. Ở LSTM, đường trực tiếp qua cell state chỉ nhân với f t; mạng học cách giữ f t gần 1 nên gradient vẫn truyền về được.

Tóm lại ba thí nghiệm: **chuỗi càng dài thì LSTM càng hơn RNN rõ**. Với 8 bước, LSTM chỉ hơn rất ít. Với 60 bước, LSTM hơn ở mọi chỉ số và ở cả 5 seed. Với 100 bước, RNN không học được còn LSTM học được. Cái giá là LSTM có gấp 4 lần tham số và chạy chậm hơn. Sang phần cuối, bạn An sẽ nói về cách dùng LSTM trong thực tế.

---

## Phần 4 — LSTM trong thực tế + tổng kết (Người 4)

### Slide 26 · Hệ quả khi cài đặt  
*Người 4 · ~1.5 phút*

Cảm ơn Hiếu. Phần cuối nói về cách dùng LSTM trong thực tế, bắt đầu từ hai quy tắc khi cài đặt rút ra từ phân tích gradient ở phần trước.

Thứ nhất: **khởi tạo bias của forget gate bằng 1**, theo khuyến nghị của Jozefowicz và cộng sự năm 2015. Khi trọng số còn nhỏ, f t xấp xỉ xích-ma(b f). Nếu bias bằng 0 thì f xấp xỉ xích-ma(0) bằng 0.5, mỗi bước cell state mất khoảng một nửa giá trị, và gradient theo đường trực tiếp giảm theo 0.5 mũ T. Đặt bias bằng 1 thì f xấp xỉ 0.73, nên ngay từ đầu cell state được giữ lại nhiều hơn. Trong PyTorch, bias được xếp theo thứ tự i, f, g, o, nên phần của forget gate là đoạn thứ hai, chỉ số từ h đến 2h.

[click] Thứ hai: **vẫn phải dùng gradient clipping**. Đường trực tiếp chỉ khắc phục gradient **biến mất**. Các số hạng gián tiếp ở slide 19 vẫn chứa ma trận W, nên gradient vẫn có thể **bùng nổ**. `clip_grad_norm_` chuẩn hóa lại vector gradient khi chuẩn của nó vượt `max_norm`, giúp tránh loss trở thành NaN.

### Slide 27 · Stacked & Bidirectional LSTM  
*Người 4 · ~1.5 phút*

Hai cách mở rộng hay dùng nhất.

**Stacked LSTM**: xếp nhiều lớp LSTM chồng lên nhau. Chuỗi hidden state h 1, chấm chấm chấm, h T của lớp dưới là chuỗi đầu vào của lớp trên. Tương tự CNN nhiều lớp, lớp trên học được đặc trưng trừu tượng hơn.

**Bidirectional LSTM**: dùng hai LSTM độc lập, một chạy từ trái sang phải, một chạy từ phải sang trái, rồi ghép hai hidden state tại mỗi bước. Như vậy biểu diễn tại bước t phụ thuộc vào cả phần trước lẫn phần sau của chuỗi. Cách này phù hợp cho phân loại văn bản hay gán nhãn từ loại, khi toàn bộ chuỗi có sẵn trước khi dự đoán.

[click] Lưu ý: **không** dùng bidirectional khi tại thời điểm dự đoán chưa có dữ liệu tương lai, ví dụ dự báo giá cổ phiếu. Khi huấn luyện, mô hình sẽ dùng thông tin từ tương lai, là thông tin không có khi triển khai; đây là rò rỉ dữ liệu.

Bên phải là code PyTorch. Chỉ cần hai tham số `num_layers` và `bidirectional`; `dropout` được áp dụng giữa các lớp. Chú ý **shape**: `output` có chiều cuối là 2h vì ghép hai chiều; chiều đầu của `h_n` bằng số lớp nhân số chiều, ở đây là 4, và `h_n` luôn có batch ở chiều thứ hai dù đặt `batch_first=True`. Đây là chỗ hay bị lỗi shape nhất.

### Slide 28 · Ứng dụng & giới hạn  
*Người 4 · ~1.5 phút*

Ứng dụng của LSTM có thể phân loại theo dạng đầu vào và đầu ra. **Many-to-one**: cả chuỗi cho ra một nhãn, ví dụ phân loại cảm xúc. **Many-to-many**: mỗi bước một nhãn, ví dụ gán nhãn từ loại. **Seq2seq**: một LSTM encoder đọc câu nguồn, một LSTM decoder sinh câu đích; Google Translate dùng kiến trúc này, kết hợp attention, từ năm 2016. Ngoài ra LSTM được dùng nhiều cho chuỗi thời gian.

LSTM cũng có giới hạn. Lớn nhất là tính **tuần tự**: muốn tính bước t phải có kết quả bước t trừ 1, nên không song song hóa được theo chiều thời gian trên GPU. Với chuỗi rất dài, toàn bộ ngữ cảnh phải được nén vào vector trạng thái có kích thước cố định.

[click] Đó là lý do Attention, và sau đó Transformer năm 2017, ra đời: bỏ cơ chế truy hồi, mỗi vị trí tính trọng số attention trực tiếp tới mọi vị trí khác. Đây là chủ đề cho một buổi khác. Trong nhánh mô hình xử lý chuỗi, thứ tự phát triển là RNN, LSTM, rồi Transformer.

### Slide 29 · Tổng kết  
*Người 4 · ~3.5 phút*

Tóm lại bài hôm nay bằng ba ý.

Một: LSTM thêm vào RNN một **cell state**, đóng vai trò bộ nhớ dài hạn.
Hai: **ba cổng** forget, input, output, đều dùng sigmoid, quyết định tỉ lệ xóa, ghi và đọc cell state.
Ba: nhờ **phép cộng** trong cập nhật cell state, gradient có một đường truyền trực tiếp chỉ nhân với f t, nên không bị biến mất như ở RNN.

Bây giờ là bốn câu hỏi trắc nghiệm nhanh. Mời các bạn chọn đáp án, mình sẽ bấm vào đáp án được chọn: ô chuyển xanh là đúng, đỏ là sai; nếu sai thì mời bạn khác chọn lại. Khi chọn đúng, lời giải hiện ra bên dưới.

**(Demo)** Câu 1: ba cổng của LSTM là gì? Đáp án A: forget, input, output.

Câu 2: các cổng dùng hàm kích hoạt nào? Đáp án B, sigmoid, vì cần giá trị trong khoảng 0 đến 1.

Câu 3: thành phần nào là bộ nhớ dài hạn? Đáp án C, cell state c t.

Câu 4: LSTM khắc phục vấn đề nào của RNN? Đáp án A, gradient biến mất.

---

## Q&A (Cả nhóm)

### Slide 30 · Cảm ơn thầy và các bạn đã lắng nghe!  
*Cả nhóm · ~2 phút*

Phần trình bày của nhóm mình đến đây là kết thúc. Cảm ơn thầy và các bạn đã lắng nghe. Nhóm mình xin nhận câu hỏi.

*(Gợi ý chuẩn bị trước một số câu hỏi có thể gặp:)*
- *Vì sao không dùng ReLU cho các cổng?* Vì cổng là hệ số nhân, cần giá trị trong (0, 1); ReLU không bị chặn trên.
- *LSTM có loại bỏ hoàn toàn gradient biến mất không?* Không. Nó chỉ tạo một đường truyền mà mạng **có thể học** để giữ gradient; nếu f t nhỏ thì gradient vẫn suy giảm theo tích các f t.
- *Vì sao trên dữ liệu e-commerce LSTM chỉ hơn RNN rất ít?* Chuỗi chỉ 8 đơn, thông tin chủ yếu nằm ở đơn đang đặt và vài đơn gần nhất, không có phụ thuộc xa; trong khi LSTM có gấp 4 tham số và chậm hơn 2 lần. Nên luôn so sánh với RNN trước khi chọn LSTM.
- *Với cổ phiếu, sao không dùng cửa sổ dài hơn để LSTM thắng đậm hơn?* Nhóm đã thử 20, 60 và 120 ngày: cửa sổ 20 ngày tốt nhất cho cả hai mô hình, vì thông tin quan trọng nằm trong khoảng một tháng gần đây. LSTM tốt hơn RNN ở cả ba độ dài; còn RNN với 120 ngày cho kết quả y hệt 60 ngày.

---

**Tổng thời lượng dự kiến:** ~46.5 phút
