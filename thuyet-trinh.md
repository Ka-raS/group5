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

Xin chào thầy và các bạn. Hôm nay nhóm mình trình bày về LSTM, viết tắt của Long Short-Term Memory. Dịch sát nghĩa thì hơi khó nghe, nhưng ý của cái tên là: một mạng nơ-ron có trí nhớ ngắn hạn, nhưng giữ được lâu.

Mở đầu bằng một trò chơi nhỏ. Các bạn đọc câu này: "Tôi lớn lên ở Pháp, nên tôi nói thành thạo tiếng gì?" Ai cũng trả lời ngay: tiếng Pháp.

[click] Bây giờ mình chèn vào giữa câu một đoạn dài không liên quan: học tiểu học, chuyển nhà, chơi bóng đá… Các bạn vẫn trả lời được, vì các bạn nhớ chữ "Pháp" ở đầu câu.

[click] Nhưng với một mạng nơ-ron hồi quy cơ bản, chữ "Pháp" mờ dần sau mỗi từ, giống như trên màn hình. Đến cuối câu thì mạng gần như đã quên nó. Bài hôm nay trả lời ba câu hỏi: vì sao mạng hồi quy cơ bản hay quên, LSTM nhớ lâu bằng cách nào, và trong thực tế LSTM tốt hơn bao nhiêu.

### Slide 2 · LSTM nằm ở đâu trong các loại mạng nơ-ron?  
*Người 1 · ~1.5 phút*

Trước khi vào LSTM, mình đặt nó vào bức tranh chung các loại mạng nơ-ron mà lớp đã học.

[click] Đầu tiên là MLP, viết tắt của Multi-Layer Perceptron, tức mạng nơ-ron nhiều lớp thông thường. Đầu vào là một vector có kích thước cố định, ví dụ một dòng dữ liệu trong bảng.

[click] Thứ hai là CNN, mạng nơ-ron tích chập, các bạn đã làm ở bài tập trước. CNN dành cho ảnh: cùng một bộ lọc được quét qua mọi vị trí trên ảnh.

[click] Thứ ba là họ RNN, mạng nơ-ron hồi quy, dành cho dữ liệu dạng chuỗi như một câu văn hay chuỗi giá cổ phiếu. RNN đọc lần lượt từng phần tử và mang theo một "bộ nhớ" từ bước này sang bước sau. Ba họ này song song với nhau, mỗi họ hợp với một kiểu dữ liệu, không họ nào sinh ra từ họ nào.

[click] LSTM không phải một họ mới. Nó là một thành viên trong họ RNN: vẫn đọc chuỗi từng bước, vẫn dùng lại cùng một bộ trọng số ở mọi bước, vẫn huấn luyện giống RNN. Điểm khác duy nhất nằm bên trong mỗi bước: LSTM có thêm một bộ nhớ dài hạn và ba "cổng" để quyết định nhớ gì, quên gì.

### Slide 3 · So sánh MLP · CNN · RNN · LSTM  
*Người 1 · ~1 phút*

Bảng này tóm tắt bốn loại mạng. Mình chỉ lưu ý ba dòng.

Dòng bộ nhớ: MLP và CNN không có bộ nhớ, mỗi đầu vào được xử lý riêng. RNN có một bộ nhớ, nhưng bộ nhớ này bị viết lại ở mỗi bước. LSTM có thêm một bộ nhớ dài hạn, và đây là nhân vật chính của cả bài.

Dòng nhớ được bao xa: trong thực tế, RNN cơ bản chỉ học được mối liên hệ trong khoảng 10 bước. Bài báo gốc năm 1997 cho thấy LSTM học được mối liên hệ cách nhau hơn 1000 bước.

Dòng số trọng số: với cùng kích thước, LSTM có gấp 4 lần số trọng số của RNN, vì nó có ba cổng cộng một phần tạo nội dung mới, mỗi phần cần một bộ trọng số riêng.

[click] Tóm lại: LSTM giữ nguyên cách làm việc của RNN, và sửa điểm yếu lớn nhất của RNN là hay quên những gì ở xa.

### Slide 4 · Ôn lại RNN: đọc từng từ, cập nhật một "bản tóm tắt"  
*Người 1 · ~1.5 phút*

Ôn lại nhanh RNN mà các bạn đã làm. Ý tưởng rất đơn giản: RNN đọc câu từng từ một, và luôn giữ một "bản tóm tắt" những gì đã đọc. Bản tóm tắt này có tên chuyên môn là trạng thái ẩn, hidden state.

Ở mỗi bước, bản tóm tắt mới được tính từ hai thứ: bản tóm tắt cũ, và từ đang đọc. Cả hai được nhân với trọng số, cộng lại, rồi đưa qua hàm tanh để ép về khoảng từ trừ 1 đến 1. Công thức trên slide chỉ nói đúng điều đó.

[click] Đọc chữ "Tôi", ra bản tóm tắt thứ nhất. [click] Đọc chữ "lớn", bản tóm tắt được viết lại. [click] Cứ thế tiếp tục, [click] cho tới chữ "tiếng", lúc đó mạng phải dựa vào bản tóm tắt để đoán chữ tiếp theo là "Pháp".

Các bạn để ý mũi tên màu cam: thông tin từ đầu câu muốn tới cuối câu thì phải đi qua tất cả các ô, và ở mỗi ô nó lại bị trộn với từ mới rồi viết lại.

[click] Một điều nữa: mọi ô dùng chung một bộ trọng số. Khi huấn luyện, sai số ở cuối câu được truyền ngược lại từng bước về đầu câu để sửa trọng số. Cách làm này gọi là BPTT, lan truyền ngược theo thời gian. Chính quãng đường đi ngược dài này gây ra vấn đề ở slide sau.

### Slide 5 · Vấn đề: RNN "quên" khi học  
*Người 1 · ~2 phút*

Đây là vấn đề chính của RNN. Khi huấn luyện, nếu mạng đoán sai ở chỗ trống, ta cần một tín hiệu lỗi đi ngược lại để sửa trọng số. Tín hiệu này có tên là gradient, các bạn hiểu đơn giản là nó cho biết cần chỉnh trọng số theo hướng nào và chỉnh bao nhiêu.

Muốn mạng học được rằng chữ "Pháp" quyết định chữ cuối câu, tín hiệu lỗi phải đi ngược về tận chữ "Pháp". Vấn đề là mỗi lần lùi lại một bước, tín hiệu bị nhân với một hệ số, do trọng số và hàm tanh quyết định. Đi ngược 50 bước thì bị nhân 50 lần.

Nếu hệ số nhỏ hơn 1, tín hiệu teo dần về 0. Ta gọi là gradient biến mất. Nếu hệ số lớn hơn 1, tín hiệu phình to, gọi là gradient bùng nổ. Giống như trò chơi truyền tin qua 50 người: chỉ cần mỗi người nói nhỏ đi một chút, đến cuối hàng thì không còn nghe thấy gì.

**(Demo)** Mình thử trên biểu đồ. Thanh trượt trên cùng là số bước cần nhớ lại, tức khoảng cách từ chữ "Pháp" tới chỗ trống, đang là 50. Thanh thứ hai là hệ số mỗi bước, đang là 0.9, tức mỗi bước tín hiệu chỉ giữ lại 90%. Nghe thì có vẻ nhiều, nhưng sau 50 bước, tín hiệu chỉ còn khoảng nửa phần trăm. Kéo số bước lên 100 thì gần như bằng 0. Còn nếu kéo hệ số lên 1.1, đường cong vọt lên trên: đó là bùng nổ.

Ta không thể giữ hệ số đúng bằng 1, vì trọng số thay đổi liên tục trong quá trình học. Đó là lý do RNN không nối được chữ "Pháp" với chữ "tiếng".

### Slide 6 · Ai phát hiện ra vấn đề và sửa nó?  
*Người 1 · ~2 phút*

Vậy ai đã nhìn ra vấn đề này và sửa nó?

[click] Năm 1991, Sepp Hochreiter, khi đó là sinh viên Đại học Kỹ thuật München ở Đức, làm luận văn tốt nghiệp với thầy Jürgen Schmidhuber. Trong luận văn này, ông là người đầu tiên chứng minh bằng toán vì sao RNN hay quên, chính là phép nhân lặp đi lặp lại mà mình vừa demo. Ba năm sau, nhóm của Bengio cũng độc lập tìm ra kết quả tương tự.

[click] Cách sửa của ông rất tự nhiên. Tín hiệu yếu dần vì bị nhân với một số khác 1 nhiều lần. Vậy thì làm một ô nhớ mà ở mỗi bước, nó chỉ giữ nguyên giá trị cũ rồi cộng thêm thông tin mới. Hệ số khi đó luôn đúng bằng 1, nên tín hiệu đi qua bao nhiêu bước cũng không bị yếu đi. Ông đặt tên cho ô nhớ này là CEC, viết tắt của Constant Error Carousel, tạm hiểu là "băng chuyền giữ nguyên lỗi".

[click] Nhưng làm vậy lại sinh ra vấn đề mới: từ nào cũng được cộng vào ô nhớ, kể cả những từ không quan trọng, nên ô nhớ bị lẫn lộn. Giải pháp là thêm các cổng. Các bạn hình dung cổng như một cái van, mở từ 0 đến 1, quyết định lúc nào được ghi vào ô nhớ và lúc nào được đọc ra. Năm 1997, Hochreiter và Schmidhuber công bố bài báo "Long Short-Term Memory", và bài báo này trở thành một trong những bài được trích dẫn nhiều nhất của ngành học sâu.

### Slide 7 · Các mốc phát triển của LSTM  
*Người 1 · ~1 phút*

Điểm qua nhanh hành trình của LSTM.

[click] Bản đầu tiên năm 1997 có cổng ghi và cổng đọc, nhưng chưa có cổng quên. Nghĩa là ô nhớ chỉ được cộng thêm, không có cách nào xóa bớt.

[click] Năm 2000, Felix Gers và cộng sự thêm cổng quên, để mạng tự học khi nào cần xóa bớt nội dung cũ. LSTM mà các bạn dùng trong PyTorch ngày nay chính là phiên bản có cổng quên này.

[click] Năm 2005, LSTM được huấn luyện theo cách đầy đủ hơn, và có thêm LSTM hai chiều, đọc câu cả xuôi lẫn ngược. [click] Năm 2009, LSTM thắng các cuộc thi nhận dạng chữ viết tay. [click] Năm 2014, người ta dùng hai LSTM để dịch máy: một LSTM đọc câu tiếng Anh, một LSTM viết ra câu tiếng Pháp. [click] Khoảng 2015, 2016, nhận dạng giọng nói của Google và Google Dịch đều chuyển sang LSTM. [click] Đến 2017, Transformer, nền tảng của ChatGPT, ra đời và dần thay thế LSTM trong xử lý ngôn ngữ.

[click] Còn cái tên: trí nhớ ngắn hạn là những gì mạng đang giữ trong lúc đọc câu. LSTM là trí nhớ ngắn hạn nhưng giữ được lâu.

### Slide 8 · Bên trong một ô LSTM  
*Người 1 · ~0.5 phút*

Tóm lại phần của mình: RNN hay quên vì tín hiệu lỗi bị nhân đi nhân lại qua rất nhiều bước. Hochreiter sửa bằng một ô nhớ chỉ giữ nguyên rồi cộng thêm, cùng với các cổng để điều khiển nó. Tiếp theo, mời bạn Minh mở ô LSTM ra xem bên trong có gì.

---

## Phần 2 — Bên trong một ô LSTM (Người 2)

### Slide 9 · Hai loại bộ nhớ: trạng thái ẩn và trạng thái ô nhớ  
*Người 2 · ~1 phút*

Cảm ơn Đại. Mình bắt đầu bằng bức tranh tổng thể.

Bên trái là RNN: chỉ có một bộ nhớ, chính là bản tóm tắt. Ở mỗi bước, bản tóm tắt này bị trộn với từ mới, đi qua hàm tanh, và được viết lại hoàn toàn.

Bên phải là LSTM. Các bạn để ý đường màu xanh nằm ngang phía trên. Đó là bộ nhớ dài hạn, tên chuyên môn là trạng thái ô nhớ, tiếng Anh là cell state.

[click] Đường này chạy thẳng qua ô giống như một băng chuyền. Trên đường đi chỉ có hai thao tác: xóa bớt một phần, và cộng thêm thông tin mới. Không có gì viết lại toàn bộ. Đây chính là ô nhớ giữ nguyên của Hochreiter mà bạn Đại vừa kể.

[click] Ngoài ra LSTM vẫn có trạng thái ẩn, là đầu ra ở mỗi bước, giống bản tóm tắt của RNN. Nó được đọc ra từ ô nhớ, và đóng vai trò bộ nhớ ngắn hạn.

Ba cổng tiếp theo điều khiển ba việc trên băng chuyền: xóa, ghi, và đọc. Mình đi lần lượt từng cổng.

### Slide 10 · Cổng 1 · Cổng quên (*forget gate*): giữ lại bao nhiêu bộ nhớ cũ?  
*Người 2 · ~1.5 phút*

Cổng đầu tiên là cổng quên, tiếng Anh là forget gate, tô màu đỏ trên sơ đồ.

Cổng quên nhìn vào hai thứ: từ đang đọc, và đầu ra của bước trước. Từ đó nó quyết định giữ lại bao nhiêu phần bộ nhớ cũ. Kết quả là một con số từ 0 đến 1 cho mỗi ô nhớ. Bằng 0 nghĩa là xóa sạch, bằng 1 nghĩa là giữ nguyên, còn 0.7 nghĩa là giữ lại 70 phần trăm.

[click] Để có con số từ 0 đến 1, cổng dùng hàm sigmoid. Các bạn cứ hình dung nó như độ mở của một cái van: 0 là đóng hẳn, 1 là mở hết.

[click] Ví dụ, khi đoạn văn chuyển sang kể về một người khác, sinh ra ở Nhật chẳng hạn, thì thông tin "Pháp" không còn đúng nữa. Lúc đó mạng học cách đóng cổng quên về gần 0 để xóa nó đi.

[click] Như bạn Đại đã kể, bản năm 1997 chưa có cổng này. Khi đó bộ nhớ chỉ được cộng thêm mà không bao giờ bị xóa, giống một cái tủ chỉ cho thêm đồ vào mà không cho lấy ra.

### Slide 11 · Cổng 2 · Cổng ghi (*input gate*): ghi gì, ghi bao nhiêu?  
*Người 2 · ~1.5 phút*

Cổng thứ hai là cổng ghi, tiếng Anh là input gate, màu xanh lá. Phần này có hai thành phần làm việc cùng nhau.

Thành phần thứ nhất tạo ra nội dung mới, tức thông tin định ghi vào ô nhớ. Nó dùng hàm tanh, nên giá trị nằm trong khoảng từ trừ 1 đến 1, có thể làm ô nhớ tăng lên hoặc giảm xuống.

Thành phần thứ hai là cổng ghi, lại là một cái van từ 0 đến 1, quyết định ghi bao nhiêu phần nội dung đó.

[click] Phần thật sự được ghi vào ô nhớ là cổng ghi nhân với nội dung mới.

[click] Vì sao phải tách làm hai? Vì không phải từ nào cũng đáng nhớ. Tại chữ "Pháp", cổng ghi mở gần hết để ghi thông tin quan trọng này vào. [click] Còn tại những từ như "chơi bóng đá", "mê truyện tranh", cổng ghi gần như đóng, để không ghi đè lên chữ "Pháp" đã lưu. Đây chính là vấn đề lẫn lộn mà Hochreiter giải quyết bằng cổng.

### Slide 12 · Cập nhật bộ nhớ: xóa bớt rồi cộng thêm  
*Người 2 · ~1 phút*

Bây giờ ghép hai cổng lại. Đây là công thức quan trọng nhất của LSTM, và mình viết nó bằng lời: bộ nhớ mới bằng cổng quên nhân bộ nhớ cũ, cộng với cổng ghi nhân nội dung mới. Nói cách khác: xóa bớt một phần cái cũ, rồi cộng thêm một phần cái mới.

[click] So với RNN: ở RNN, mỗi bước bản tóm tắt bị viết lại hoàn toàn, nhân với trọng số rồi đi qua tanh.

[click] Còn ở LSTM, bộ nhớ cũ không bị viết lại. Nó chỉ bị xóa bớt theo cổng quên, rồi được cộng thêm phần mới. Nếu cổng quên mở hết và cổng ghi đóng, bộ nhớ đi qua bước đó y nguyên.

[click] Lát nữa bạn Hiếu sẽ cho thấy chính phép cộng đơn giản này là lý do LSTM học được những mối liên hệ ở xa.

### Slide 13 · Cổng 3 · Cổng đọc (*output gate*): đọc ra bao nhiêu?  
*Người 2 · ~1 phút*

Cổng cuối cùng là cổng đọc, tiếng Anh là output gate, màu tím.

Ô nhớ là thứ cất giữ bên trong. Đầu ra của mỗi bước được đọc ra từ ô nhớ qua hai bước: đưa bộ nhớ qua hàm tanh để ép về khoảng từ trừ 1 đến 1, rồi nhân với cổng đọc. Cổng đọc lại là một cái van, quyết định ở bước này cho đọc ra bao nhiêu.

[click] Nhờ vậy, mạng có thể cất chữ "Pháp" trong ô nhớ suốt 30 bước mà không làm nhiễu đầu ra ở các bước giữa: cổng đọc đóng thì thông tin vẫn nằm yên trong ô nhớ.

[click] Đến chữ "tiếng", khi cần đoán tên ngôn ngữ, cổng đọc mới mở ra để lấy thông tin "Pháp" ra dùng.

### Slide 14 · Tổng hợp: một ô LSTM làm 4 việc  
*Người 2 · ~1 phút*

Đây là toàn bộ LSTM trên một slide. Một ô LSTM làm đúng bốn việc, mình bấm lần lượt để các bạn đối chiếu với sơ đồ.

[click] Việc một: quên. Cổng quên quyết định giữ lại bao nhiêu bộ nhớ cũ.

[click] Việc hai: chuẩn bị ghi. Tạo nội dung mới, và cổng ghi quyết định ghi bao nhiêu.

[click] Việc ba: cập nhật. Bộ nhớ mới bằng phần cũ đã xóa bớt cộng phần mới.

[click] Việc bốn: đọc. Cổng đọc quyết định lấy ra bao nhiêu từ bộ nhớ để làm đầu ra.

Công thức nằm dưới mỗi dòng cho bạn nào muốn đối chiếu với sách. Các bạn để ý ba cổng và phần nội dung mới đều có cùng một dạng, mỗi phần có một bộ trọng số riêng. Bốn bộ trọng số, nên LSTM có gấp 4 lần trọng số so với RNN cùng kích thước, đúng như bảng so sánh lúc đầu.

### Slide 15 · Thử tay: theo dõi bộ nhớ của một ô LSTM  
*Người 2 · ~3 phút*

Bây giờ mình chạy thử một ô LSTM thu nhỏ, trong đó bộ nhớ chỉ là một con số, để các bạn nhìn thấy các cổng hoạt động.

Trọng số của ô này nhóm đặt sẵn, không phải học, sao cho đầu vào có ý nghĩa dễ hiểu, như ô chú thích bên phải: đầu vào bằng 2 nghĩa là "đây là thông tin quan trọng, hãy ghi nhớ", giống chữ "Pháp". Đầu vào bằng 0 là một từ bình thường. Đầu vào bằng trừ 2 nghĩa là "hết ngữ cảnh rồi, hãy xóa đi".

**Demo 1, kéo thanh "Đầu vào lúc này":**
- Đặt bằng 2: cổng ghi mở gần hết, bộ nhớ tăng lên gần 1. Dòng chữ phía dưới sơ đồ báo ô đang GHI.
- Đặt bằng trừ 2: cổng quên đóng về gần 0, bộ nhớ bị XÓA.

**Demo 2, bấm "Làm lại" rồi bấm "Bước tiếp" liên tục.** Chuỗi chạy thử là: một từ quan trọng, ba từ bình thường, một tín hiệu xóa, rồi một từ bình thường.
- Bước 1, từ quan trọng: bộ nhớ lên khoảng 0.99, mạng ghi nhớ.
- Bước 2 đến 4, từ bình thường: cổng ghi gần như đóng nên không ghi gì mới, cổng quên mở khoảng 96% nên bộ nhớ chỉ giảm rất chậm: 0.98, 0.97, 0.95. Các bạn nhìn cột "bộ nhớ" trong bảng bên phải: thông tin được GIỮ.
- Bước 5, tín hiệu xóa: cổng quên đóng, bộ nhớ rơi về gần 0. Mạng XÓA thông tin.

**Demo 3, tích ô "Tự chỉnh các cổng bằng tay":** kéo cổng quên lên 1, cổng ghi về 0. Khi đó bộ nhớ mới bằng đúng bộ nhớ cũ, không mất gì cả. Đây chính là ô nhớ giữ nguyên của Hochreiter năm 1997.

Trong mạng thật, các trọng số này không do mình đặt mà được học từ dữ liệu.

### Slide 16 · Ví dụ: các cổng mở / đóng thế nào trên câu mẫu?  
*Người 2 · ~1 phút*

Quay lại câu ví dụ ở đầu bài. Bảng này cho thấy ba cổng mở hay đóng ở từng từ, theo cách mà ta mong một mô hình đã học tốt sẽ làm. Màu càng đậm thì cổng càng mở. Lưu ý đây là số liệu minh họa để giải thích ý tưởng, không phải số đo từ một mô hình thật.

[click] Tại chữ "Pháp", cổng ghi mở để ghi thông tin vào bộ nhớ.

[click] Ở các từ ở giữa, cổng quên mở để giữ nguyên bộ nhớ, còn cổng ghi đóng để không ghi đè lên.

[click] Tại chữ "tiếng", cổng đọc mở để lấy chữ "Pháp" ra và đoán từ tiếp theo.

Đến đây là toàn bộ cách một ô LSTM hoạt động khi đọc câu. Câu hỏi còn lại là: vì sao cái phép cộng đơn giản kia lại giúp LSTM học được những gì ở xa? Mời bạn Hiếu.

---

## Phần 3 — Vì sao LSTM nhớ lâu + thí nghiệm so sánh với RNN (Người 3)

### Slide 17 · Vì sao LSTM học được những gì ở xa?  
*Người 3 · ~2.5 phút*

Cảm ơn Minh. Phần của mình trả lời câu hỏi: vì sao LSTM học được những gì ở xa, còn RNN thì không?

Khi huấn luyện, mạng đoán sai ở chữ cuối, và tín hiệu lỗi phải đi ngược về tận chữ "Pháp" để mạng biết chữ "Pháp" quan trọng. RNN và LSTM cho tín hiệu này đi theo hai con đường khác nhau.

[click] Ở RNN, tín hiệu chỉ có một đường là đi ngược qua các bản tóm tắt. Mỗi lần lùi một bước, nó bị nhân với trọng số và với đạo hàm của hàm tanh. Hệ số này rất khó giữ đúng bằng 1. Giả sử nó là 0.9, thì sau 50 bước chỉ còn khoảng 0.005, tức nửa phần trăm. Đến chữ "Pháp" thì tín hiệu gần như không còn gì.

[click] Ở LSTM, nhớ lại công thức bộ nhớ của bạn Minh: bộ nhớ mới bằng cổng quên nhân bộ nhớ cũ, cộng phần mới. Vì là phép cộng, khi đi ngược dọc theo băng chuyền bộ nhớ, tín hiệu chỉ bị nhân với cổng quên, không có trọng số, không có tanh. Mà cổng quên là thứ mạng tự học được. Khi cần nhớ, mạng học cách giữ cổng quên gần 1. Với cổng quên bằng 0.99, sau 50 bước tín hiệu vẫn còn khoảng 60 phần trăm.

[click] Nói cho công bằng: LSTM vẫn còn những đường vòng giống RNN, đi qua đầu ra của bước trước, và các đường này vẫn có thể yếu dần. Nhưng tín hiệu là tổng của tất cả các đường. Chỉ cần còn một con đường thẳng qua bộ nhớ là tín hiệu vẫn về tới chữ "Pháp". Đây chính là ý tưởng "giữ nguyên rồi cộng thêm" của Hochreiter năm 1991.

### Slide 18 · Thử tay: RNN và LSTM sau nhiều bước  
*Người 3 · ~1 phút*

Đây là biểu đồ của bạn Đại ở slide 5, thêm đường màu xanh cho LSTM. Trục ngang là số bước đi ngược về quá khứ, trục dọc là phần trăm tín hiệu lỗi còn lại.

**(Demo)** Mình đặt số bước bằng 100. RNN mỗi bước nhân 0.9, còn LSTM có cổng quên bằng 0.99. Sau 100 bước, RNN chỉ còn khoảng ba phần nghìn của một phần trăm, còn LSTM vẫn còn khoảng 37 phần trăm. Chênh nhau hơn mười nghìn lần.

Kéo cổng quên lên đúng 1 thì đường xanh nằm ngang: tín hiệu không mất chút nào. Đó chính là ô nhớ giữ nguyên năm 1997.

Điểm khác biệt cốt lõi: hệ số của RNN phụ thuộc trọng số và hàm tanh, rất khó giữ gần 1. Còn cổng quên của LSTM là thứ mạng có thể chủ động học để giữ gần 1 khi cần nhớ.

### Slide 19 · Ý tưởng quen thuộc: giống "lối tắt" trong ResNet  
*Người 3 · ~1.5 phút*

Ý tưởng này các bạn thật ra đã gặp ở phần mạng tích chập, trong ResNet, viết tắt của Residual Network.

Bên trái là ResNet. Mỗi khối tính đầu ra bằng đầu vào cộng với một phần thay đổi. Nhờ phép cộng đó, tín hiệu lỗi luôn có một lối tắt đi thẳng qua khối mà không bị nhân với trọng số. Đó là lý do ResNet huấn luyện được mạng hơn 100 lớp.

Bên phải là LSTM: bộ nhớ mới bằng cổng quên nhân bộ nhớ cũ, cộng phần mới. Khi cổng quên bằng 1, nó giống hệt lối tắt của ResNet.

[click] Hai mô hình dùng cùng một nguyên lý: phép cộng tạo ra một lối tắt cho tín hiệu lỗi. ResNet làm theo chiều sâu, từ lớp này sang lớp sau. LSTM làm theo chiều thời gian, từ bước này sang bước sau. Và LSTM có ý tưởng này trước ResNet tận 18 năm.

Lý thuyết là vậy. Bây giờ mình kiểm tra trên dữ liệu thật.

### Slide 20 · Thí nghiệm 1: đơn hàng online, chuỗi ngắn (8 bước)  
*Người 3 · ~1.5 phút*

Nhóm so sánh LSTM với RNN trên ba thí nghiệm, xếp theo độ dài chuỗi tăng dần: 8 bước, 60 bước, rồi 100 bước. Ở mọi thí nghiệm, hai mô hình giống hệt nhau về kích thước và cách huấn luyện; điểm khác duy nhất là thay RNN bằng LSTM. Mỗi mô hình được huấn luyện 5 lần với khởi tạo ngẫu nhiên khác nhau, để chắc chắn kết quả không phải do may rủi.

Thí nghiệm thứ nhất dùng dữ liệu của một sàn thương mại điện tử ở Pakistan, khoảng 400 nghìn đơn hàng. Khi khách đặt một đơn, mô hình đoán đơn đó sẽ được giao xong, bị hủy, hay bị trả lại, dựa trên 8 đơn gần nhất của khách đó.

Kết quả: LSTM đoán đúng nhiều hơn, và ROC-AUC cao hơn. ROC-AUC là chỉ số đo khả năng xếp đúng loại đơn lên trước, 0.5 là đoán mò, 1 là hoàn hảo. LSTM hơn ở cả 5 lần chạy. Nhưng mức chênh rất nhỏ: chỉ khoảng 0.3 phần trăm. Và ở hai chỉ số liên quan tới đơn bị trả lại, LSTM còn kém hơn một chút.

[click] Lý do là chuỗi ở đây rất ngắn, chỉ 8 đơn. Thông tin quan trọng nằm ở chính đơn đang đặt và vài đơn gần nhất. Không có gì ở xa cần nhớ, nên bộ nhớ dài hạn của LSTM không có đất dụng võ.

Vậy nếu chuỗi dài hơn thì sao? Đó là thí nghiệm thứ hai.

### Slide 21 · Thí nghiệm 2: cổ phiếu, chuỗi dài (60 bước)  
*Người 3 · ~2 phút*

Thí nghiệm thứ hai dùng giá cổ phiếu theo ngày của Apple, Microsoft và HP. Mô hình nhìn 60 ngày giao dịch gần nhất và dự báo ngày mai giá sẽ dao động mạnh hay nhẹ, tức khoảng cách giữa giá cao nhất và thấp nhất trong ngày. Nhóm chọn bài toán này vì độ dao động có tính "nhớ": giai đoạn sôi động thường kéo dài nhiều tuần. Mô hình học trên dữ liệu từ 1995 đến 2016, và được kiểm tra trên 6 năm từ 2020 đến 2025.

Bảng bên trái là trung bình 5 lần chạy. LSTM tốt hơn ở mọi chỉ số. Sai số trung bình, MAE, giảm từ 0.727 xuống 0.709. Chỉ số R², tức mô hình giải thích được bao nhiêu phần sự lên xuống, tăng từ 0.35 lên 0.38. Và LSTM đoán đúng ngày mai dao động mạnh hơn hay nhẹ hơn nhiều hơn khoảng 1 phần trăm.

**(Demo: bấm qua các chỉ số)** Hình bên phải vẽ riêng từng lần chạy, mỗi chấm là một lần. Năm chấm xanh của LSTM và năm chấm cam của RNN tách hẳn nhau, không chồng lên nhau.

[click] Nghĩa là: lần chạy tệ nhất của LSTM vẫn tốt hơn lần chạy tốt nhất của RNN. Kết quả của LSTM cũng ổn định hơn giữa các lần. Cái giá phải trả là LSTM có gấp 4 lần trọng số và chạy chậm hơn khoảng một lần rưỡi.

Vậy vì sao LSTM tốt hơn ở đây?

### Slide 22 · Vì sao? LSTM dùng được cả những ngày ở xa  
*Người 3 · ~1.5 phút*

Để trả lời, nhóm đo xem mỗi ngày trong 60 ngày ảnh hưởng tới dự báo bao nhiêu: thay đổi dữ liệu của một ngày một chút, rồi xem dự báo thay đổi bao nhiêu.

**(Demo: tab 1)** Trục ngang là 60 ngày, ngày 60 là hôm nay. Trục dọc là mức ảnh hưởng so với hôm nay. Đường cam của RNN tụt rất nhanh: ngày đầu tiên chỉ còn ảnh hưởng khoảng một phần mười nghìn so với hôm nay. Đường xanh của LSTM tụt chậm hơn nhiều, ngày đầu tiên vẫn còn khoảng một phần trăm, gấp khoảng 75 lần RNN. Bảng bên phải: chỉ 3.7 phần trăm ảnh hưởng của RNN đến từ 40 ngày cũ, còn ở LSTM là 25 phần trăm.

**(Demo: tab 2)** Nhóm thử xóa dữ liệu của các ngày cũ rồi cho dự báo lại. Với RNN, giữ 20 ngày hay 60 ngày cũng như nhau, các ngày cũ không đóng góp gì. Với LSTM thì ngược lại: nếu chỉ giữ 5 hay 10 ngày, LSTM còn sai nhiều hơn RNN, vì nó đã quen dựa vào những ngày cũ, bỏ đi thì nó mất thông tin. Từ 20 ngày trở lên thì LSTM tốt hơn RNN.

**(Demo: tab 3)** Nhóm huấn luyện lại với 20, 60 và 120 ngày. RNN với 120 ngày cho kết quả y hệt 60 ngày: 60 ngày thêm vào hoàn toàn vô ích, vì tín hiệu lỗi không đi ngược xa được tới đó. Nhóm cũng phải nói thật: với dữ liệu này, cho xem 20 ngày là tốt nhất ở cả hai mô hình, vì thông tin quan trọng nhất nằm trong khoảng một tháng gần đây. Nhưng ở cả ba trường hợp, LSTM đều tốt hơn RNN.

[click] Tóm lại: RNN gặp đúng hiện tượng tín hiệu lỗi biến mất ở slide 5, còn LSTM nhờ con đường thẳng qua bộ nhớ nên vẫn nghe được tín hiệu từ những ngày xa.

### Slide 23 · Thí nghiệm 3: phải nhớ rất xa (bài toán cộng)  
*Người 3 · ~1.5 phút*

Thí nghiệm thứ ba đẩy độ dài lên mức cực đoan. Đây là bài toán cộng, một bài toán kinh điển có trong chính bài báo năm 1997. Mô hình đọc một chuỗi số ngẫu nhiên, trong đó có đúng hai số được đánh dấu: một số ở nửa đầu, một số ở nửa sau. Nhiệm vụ là trả lời tổng của hai số đó. Với chuỗi 100 số, mô hình phải nhớ số được đánh dấu đầu tiên qua ít nhất 50 bước.

Đường nét đứt là mức "đoán mò": luôn trả lời tổng bằng 1, là giá trị trung bình. Mô hình nào nằm trên đường này là chưa học được gì.

**(Bấm "Chuỗi 10 số")** Với chuỗi ngắn, cả hai mô hình đều học được, sai số giảm xuống dưới mức đoán mò. Giống thí nghiệm 1: khi không cần nhớ xa thì RNN cũng làm được.

**(Bấm "Chuỗi 100 số")** Với chuỗi dài, đường cam của RNN nằm yên ở mức đoán mò suốt quá trình học: RNN không học được gì. LSTM cũng loay hoay ở mức đó một thời gian, rồi đến khoảng giữa quá trình thì "vỡ lẽ", sai số tụt xuống gần 0. Sai số cuối cùng của LSTM thấp hơn RNN khoảng 50 lần.

[click] Tóm lại ba thí nghiệm: chuỗi càng dài thì LSTM càng hơn RNN rõ. 8 bước: hơn rất ít. 60 bước: hơn ở mọi chỉ số, cả 5 lần chạy. 100 bước: RNN không học được, LSTM học được. Đổi lại, LSTM có gấp 4 lần trọng số và chạy chậm hơn. Sang phần cuối, bạn An sẽ nói về cách dùng LSTM trong thực tế.

---

## Phần 4 — LSTM trong thực tế + tổng kết (Người 4)

### Slide 24 · Hai mẹo khi tự cài đặt LSTM  
*Người 4 · ~1.5 phút*

Cảm ơn Hiếu. Phần cuối nói về cách dùng LSTM trong thực tế, bắt đầu từ hai mẹo khi cài đặt, rút ra trực tiếp từ những gì các bạn vừa nghe.

Mẹo thứ nhất: cho cổng quên hơi mở ngay từ đầu. Lúc mới khởi tạo, trọng số còn nhỏ nên cổng quên thường nằm quanh 0.5, tức mỗi bước mạng mất một nửa bộ nhớ, và tín hiệu lỗi cũng yếu đi một nửa mỗi bước. Nếu đặt sẵn độ lệch, tức bias, của cổng quên bằng 1, thì cổng quên khởi đầu ở khoảng 0.73, mạng có xu hướng nhớ ngay từ đầu. Đây là khuyến nghị của một nhóm nghiên cứu ở Google năm 2015. Trong PyTorch, độ lệch của bốn phần được xếp liền nhau theo thứ tự: cổng ghi, cổng quên, nội dung mới, cổng đọc, nên phần của cổng quên là đoạn thứ hai.

[click] Mẹo thứ hai: vẫn phải giới hạn độ lớn của tín hiệu lỗi, gọi là gradient clipping. Con đường thẳng qua bộ nhớ chỉ chữa được việc tín hiệu biến mất. Các đường vòng giống RNN vẫn có thể làm tín hiệu phình to, tức bùng nổ. Hàm clip grad norm làm đúng một việc: nếu tín hiệu lớn hơn ngưỡng, ở đây là 1, thì thu nhỏ nó lại. Nhờ đó quá trình học không bị hỏng giữa chừng. Cả ba thí nghiệm của nhóm đều dùng cách này.

### Slide 25 · Xếp chồng và đọc hai chiều  
*Người 4 · ~1.5 phút*

Hai cách mở rộng LSTM hay dùng nhất.

Thứ nhất là xếp chồng nhiều lớp. Đầu ra ở từng bước của lớp LSTM thứ nhất trở thành đầu vào của lớp thứ hai. Giống CNN nhiều lớp, lớp càng cao thì hiểu ý nghĩa càng trừu tượng.

Thứ hai là đọc hai chiều. Dùng hai LSTM riêng: một cái đọc câu từ trái sang phải, một cái đọc từ phải sang trái, rồi ghép kết quả lại. Như vậy mỗi từ được hiểu nhờ cả phần trước lẫn phần sau của câu. Cách này hợp với các bài toán có sẵn cả câu, ví dụ phân loại một bình luận là khen hay chê.

[click] Nhưng lưu ý: không dùng hai chiều khi phải dự đoán tương lai, ví dụ dự báo giá cổ phiếu như thí nghiệm 2. Lúc học, mô hình sẽ được nhìn trước dữ liệu tương lai, nhưng lúc dùng thật thì không có. Kết quả trong lúc học sẽ đẹp một cách ảo. Lỗi này gọi là rò rỉ dữ liệu.

Bên phải là code PyTorch: chỉ cần hai tham số, số lớp và hai chiều. Dropout là tắt ngẫu nhiên 20 phần trăm kết nối giữa các lớp để chống học vẹt. Đầu ra có chiều cuối gấp đôi vì ghép hai chiều; đây là chỗ hay bị lỗi kích thước nhất khi nối với lớp phía sau.

### Slide 26 · LSTM dùng để làm gì, và giới hạn của nó  
*Người 4 · ~1.5 phút*

LSTM được dùng ở đâu? Có thể chia theo dạng đầu vào và đầu ra. Cả chuỗi cho ra một nhãn, ví dụ đọc một bình luận rồi đoán là khen hay chê, hoặc như thí nghiệm 1 của nhóm: đọc lịch sử đơn hàng rồi đoán đơn có bị hủy không. Mỗi bước một nhãn, ví dụ nhận dạng giọng nói. Chuỗi sang chuỗi, ví dụ dịch máy: một LSTM đọc câu nguồn, một LSTM viết câu đích, Google Dịch từng dùng cách này. Ngoài ra LSTM được dùng rất nhiều cho chuỗi thời gian và để sinh dữ liệu như văn bản hay nhạc.

LSTM cũng có giới hạn. Lớn nhất là phải đọc lần lượt: muốn tính bước sau thì phải có kết quả bước trước, nên không tận dụng được sức chạy song song của card đồ họa. Với chuỗi rất dài, mọi thứ phải nhồi vào một bộ nhớ có kích thước cố định. Và nó có gấp 4 lần trọng số so với RNN.

[click] Đó là lý do Attention, rồi Transformer năm 2017 ra đời: bỏ cách đọc lần lượt, mỗi từ nhìn thẳng vào mọi từ khác trong câu. Đó là chủ đề cho một buổi khác. Dòng phát triển của các mô hình xử lý chuỗi là: RNN, rồi LSTM, rồi Transformer.

### Slide 27 · Tổng kết  
*Người 4 · ~3.5 phút*

Tóm lại bài hôm nay bằng ba ý.

Một: LSTM thêm vào RNN một bộ nhớ dài hạn, gọi là trạng thái ô nhớ. Nó chạy thẳng qua các bước như một băng chuyền, chỉ bị xóa bớt và cộng thêm.

Hai: ba cổng quên, ghi và đọc, mỗi cổng là một cái van mở từ 0 đến 1, quyết định xóa bao nhiêu, ghi bao nhiêu, đọc ra bao nhiêu.

Ba: nhờ phép cộng trong cách cập nhật bộ nhớ, tín hiệu lỗi có một con đường thẳng để đi ngược về quá khứ, nên LSTM học được những gì ở xa. Ba thí nghiệm của nhóm cho thấy chuỗi càng dài thì LSTM càng hơn RNN rõ.

Bây giờ là bốn câu hỏi trắc nghiệm nhanh. Mời các bạn chọn đáp án, mình sẽ bấm vào đáp án được chọn: ô chuyển xanh là đúng, đỏ là sai; nếu sai thì mời bạn khác chọn lại. Khi chọn đúng, lời giải hiện ra bên dưới.

**(Demo)** Câu 1: ba cổng của LSTM là gì? Đáp án A: cổng quên, cổng ghi, cổng đọc.

Câu 2: các cổng dùng hàm kích hoạt nào? Đáp án B, sigmoid, vì cần một con số từ 0 đến 1 giống độ mở của cái van.

Câu 3: thành phần nào là bộ nhớ dài hạn? Đáp án C, trạng thái ô nhớ.

Câu 4: LSTM sinh ra để khắc phục vấn đề nào của RNN? Đáp án A: tín hiệu lỗi yếu dần rồi biến mất.

---

## Q&A (Cả nhóm)

### Slide 28 · Cảm ơn thầy và các bạn đã lắng nghe!  
*Cả nhóm · ~2 phút*

Phần trình bày của nhóm mình đến đây là kết thúc. Cảm ơn thầy và các bạn đã lắng nghe. Nhóm mình xin nhận câu hỏi.

*(Gợi ý chuẩn bị trước một số câu hỏi có thể gặp:)*
- *Vì sao các cổng không dùng ReLU?* Vì cổng là một hệ số nhân, cần nằm trong khoảng 0 đến 1 như độ mở của cái van. ReLU không có giới hạn trên, có thể ra số rất lớn.
- *LSTM có hết hẳn hiện tượng tín hiệu lỗi biến mất không?* Không hẳn. Nó tạo ra một con đường mà mạng có thể học để giữ tín hiệu; nếu cổng quên nhỏ thì tín hiệu vẫn yếu dần.
- *Vì sao ở thí nghiệm đơn hàng, LSTM chỉ hơn RNN rất ít?* Chuỗi chỉ có 8 đơn, thông tin quan trọng nằm ở đơn đang đặt và vài đơn gần nhất, không có gì ở xa cần nhớ. Trong khi đó LSTM có gấp 4 lần trọng số và chạy chậm gấp đôi. Nên luôn thử RNN trước khi chọn LSTM.
- *Với cổ phiếu, sao không cho xem nhiều ngày hơn để LSTM thắng đậm hơn?* Nhóm đã thử 20, 60 và 120 ngày: 20 ngày tốt nhất cho cả hai mô hình, vì thông tin quan trọng nằm trong khoảng một tháng gần đây. LSTM tốt hơn RNN ở cả ba trường hợp, còn RNN với 120 ngày cho kết quả y hệt 60 ngày.

---

**Tổng thời lượng dự kiến:** ~43 phút
