<script setup lang="ts">
import Quiz from './Quiz.vue'

// Câu hỏi trắc nghiệm của slide Tổng kết: câu hỏi nhận biết, không cần tính toán (answer = chỉ số đáp án đúng, tính từ 0)
const questions = [
  {
    q: 'Đâu là ba cổng của LSTM?',
    options: ['Forget, input, output', 'Input, hidden, cell', 'Convolution, pooling, output', 'Query, key, value'],
    answer: 0,
    explain: 'LSTM có forget gate (xóa), input gate (ghi) và output gate (đọc). Convolution/pooling thuộc CNN; query/key/value thuộc attention.',
  },
  {
    q: 'Các cổng của LSTM dùng hàm kích hoạt nào?',
    options: ['ReLU', 'Sigmoid', 'Softmax', 'Hàm tuyến tính'],
    answer: 1,
    explain: 'Sigmoid cho giá trị trong (0, 1), dùng làm hệ số nhân: 0 là chặn, 1 là cho qua.',
  },
  {
    q: 'Thành phần nào đóng vai trò bộ nhớ dài hạn của LSTM?',
    options: ['Đầu vào x<sub>t</sub>', 'Hidden state h<sub>t</sub>', 'Cell state c<sub>t</sub>', 'Ma trận trọng số W'],
    answer: 2,
    explain: 'Cell state c<sub>t</sub> chỉ được cập nhật bằng phép nhân từng phần tử và phép cộng nên giữ được thông tin qua nhiều bước.',
  },
  {
    q: 'LSTM được đề xuất để khắc phục vấn đề nào của RNN?',
    options: ['Gradient biến mất', 'Thiếu dữ liệu huấn luyện', 'Quá ít tham số', 'Không xử lý được ảnh'],
    answer: 0,
    explain: 'Gradient của RNN suy giảm theo hàm mũ qua các bước thời gian nên RNN không học được phụ thuộc xa.',
  },
]
</script>

<template>
  <div class="qs">
    <Quiz v-for="(x, k) in questions" :key="k" :n="k + 1" v-bind="x" />
  </div>
</template>

<style scoped>
.qs { display: grid; grid-template-columns: 1fr 1fr; gap: .5rem; }
</style>
