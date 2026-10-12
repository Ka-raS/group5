# Slide LSTM (Slidev)

```bash
npm install          # lần đầu
npm run dev          # trình chiếu: http://localhost:3030 (presenter mode: /presenter, có lời thoại)
npm run notes        # xuất lời thoại trong slides.md ra ../thuyet-trinh.md
npm run export       # xuất PDF (cần: npx playwright install chromium)
```

- `slides.md`: nội dung 28 slide; lời thoại nằm trong comment `<!-- -->` cuối mỗi slide. Nguyên tắc viết (nói bằng lời, không đọc ký hiệu, viết đầy đủ từ viết tắt lần đầu): xem `../kich-ban-lstm.md`
- `components/`: LstmCell (sơ đồ ô LSTM), LstmSimulator (slide 15), GradientDecay (slide 5, 18), GateHeatmap (slide 16), SeedStrip (kết quả từng lần chạy, slide 21), StockReach (ảnh hưởng theo ngày / xóa bớt ngày cũ / số ngày đưa vào, slide 22), CompareChart (slide 23), Quiz + QuizSet (trắc nghiệm, slide 27)
- `data/lstm_vs_rnn.json` (thí nghiệm e-commerce và cổ phiếu, slide 20–22): kết quả thật sinh bởi `../experiment/lstm_ecommerce.ipynb` và `../experiment/lstm_stock.ipynb` (khoảng 30 + 40 phút CPU), sau đó chạy `python ../experiment/export_slide_data.py` để gom vào file này
- `data/compare.json` (bài toán cộng, slide 23): sinh bởi notebook `experiment/LSTM_vs_RNN.ipynb` cũ (đã xóa khỏi thư mục, còn trong lịch sử git, commit `3702c9f`)

**Điều khiển bằng chuột** (`global-bottom.vue`): chuột trái = bước/slide tiếp theo, chuột phải = quay lại. Bấm vào thanh trượt, nút, checkbox trong các demo (slide 5, 15, 18, 21, 22, 23, 27) sẽ không chuyển slide. Bàn phím (→ ←, Space) vẫn dùng bình thường.
