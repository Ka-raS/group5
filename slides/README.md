# Slide LSTM (Slidev)

```bash
npm install          # lần đầu
npm run dev          # trình chiếu: http://localhost:3030 (presenter mode: /presenter, có lời thoại)
npm run notes        # xuất lời thoại trong slides.md ra ../thuyet-trinh.md
npm run export       # xuất PDF (cần: npx playwright install chromium)
```

- `slides.md`: nội dung 28 slide; lời thoại nằm trong comment `<!-- -->` cuối mỗi slide
- `components/`: LstmCell (sơ đồ ô LSTM), LstmSimulator (slide 15), GradientDecay (slide 5, 20), GateHeatmap (slide 16), CompareChart (slide 23), Quiz + QuizSet (trắc nghiệm, slide 27)
- `data/compare.json` (Adding Problem, slide 23) và `data/ecommerce.json` (dữ liệu Olist, slide 22): kết quả thật sinh bởi notebook `../experiment/LSTM_vs_RNN.ipynb` (chạy lại toàn bộ notebook, khoảng 10 phút CPU; notebook tự tải `olist_orders_dataset.csv` nếu chưa có)

**Điều khiển bằng chuột** (`global-bottom.vue`): chuột trái = bước/slide tiếp theo, chuột phải = quay lại. Bấm vào thanh trượt, nút, checkbox trong các demo (slide 5, 15, 20, 23, 27) sẽ không chuyển slide. Bàn phím (→ ←, Space) vẫn dùng bình thường.
