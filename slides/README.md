# Slide LSTM (Slidev)

```bash
npm install          # lần đầu
npm run dev          # trình chiếu: http://localhost:3030 (presenter mode: /presenter, có lời thoại)
npm run notes        # xuất lời thoại trong slides.md ra ../thuyet-trinh.md
npm run export       # xuất PDF (cần: npx playwright install chromium)
```

- `slides.md`: nội dung 30 slide; lời thoại nằm trong comment `<!-- -->` cuối mỗi slide
- `components/`: LstmCell (sơ đồ ô LSTM), LstmSimulator (slide 15), GradientDecay (slide 5, 20), GateHeatmap (slide 16), SeedStrip (kết quả từng seed, slide 23), StockReach (độ nhạy theo ngày / cắt cửa sổ / độ dài cửa sổ, slide 24), CompareChart (slide 25), Quiz + QuizSet (trắc nghiệm, slide 29)
- `data/lstm_vs_rnn.json` (thí nghiệm e-commerce và cổ phiếu, slide 22–24): kết quả thật sinh bởi `../experiment/lstm_ecommerce.ipynb` và `../experiment/lstm_stock.ipynb` (khoảng 30 + 40 phút CPU), sau đó chạy `python ../experiment/export_slide_data.py` để gom vào file này
- `data/compare.json` (Adding Problem, slide 25): sinh bởi notebook `experiment/LSTM_vs_RNN.ipynb` cũ (đã xóa khỏi thư mục, còn trong lịch sử git, commit `3702c9f`)

**Điều khiển bằng chuột** (`global-bottom.vue`): chuột trái = bước/slide tiếp theo, chuột phải = quay lại. Bấm vào thanh trượt, nút, checkbox trong các demo (slide 5, 15, 20, 23, 24, 25, 29) sẽ không chuyển slide. Bàn phím (→ ←, Space) vẫn dùng bình thường.
