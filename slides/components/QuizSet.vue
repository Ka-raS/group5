<script setup lang="ts">
import Quiz from './Quiz.vue'

// Câu hỏi trắc nghiệm của slide Tổng kết: câu hỏi nhận biết, không cần tính toán (answer = chỉ số đáp án đúng, tính từ 0)
const questions = [
  {
    q: 'Đâu là ba cổng của LSTM?',
    options: ['Cổng quên, cổng ghi, cổng đọc', 'Cổng vào, cổng ẩn, cổng nhớ', 'Tích chập, gộp, đầu ra', 'Truy vấn, khóa, giá trị'],
    answer: 0,
    explain: 'Cổng quên (forget gate) xóa bớt bộ nhớ, cổng ghi (input gate) ghi thêm, cổng đọc (output gate) đọc ra. Tích chập và gộp thuộc CNN; truy vấn, khóa, giá trị thuộc Transformer.',
  },
  {
    q: 'Các cổng của LSTM dùng hàm kích hoạt nào?',
    options: ['ReLU', 'Sigmoid', 'Softmax', 'Hàm tuyến tính (giữ nguyên giá trị)'],
    answer: 1,
    explain: 'Sigmoid cho giá trị từ 0 đến 1, giống độ mở của một cái van: 0 là đóng hẳn, 1 là mở hết.',
  },
  {
    q: 'Thành phần nào đóng vai trò bộ nhớ dài hạn của LSTM?',
    options: ['Đầu vào', 'Trạng thái ẩn (hidden state)', 'Trạng thái ô nhớ (cell state)', 'Ma trận trọng số'],
    answer: 2,
    explain: 'Trạng thái ô nhớ chỉ bị xóa bớt (nhân với cổng quên) và cộng thêm (nội dung mới), không bị viết lại toàn bộ mỗi bước, nên giữ được thông tin lâu.',
  },
  {
    q: 'LSTM được đề xuất để khắc phục vấn đề nào của RNN?',
    options: ['Tín hiệu lỗi (gradient) yếu dần rồi biến mất', 'Thiếu dữ liệu huấn luyện', 'Quá ít trọng số', 'Không xử lý được ảnh'],
    answer: 0,
    explain: 'Khi học, tín hiệu lỗi của RNN yếu dần sau mỗi bước đi ngược, nên RNN không học được mối liên hệ giữa hai từ cách xa nhau.',
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
