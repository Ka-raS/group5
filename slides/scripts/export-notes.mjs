// Xuất speaker notes trong slides.md ra file lời thoại ../thuyet-trinh.md
// Chạy: npm run notes
import { readFileSync, writeFileSync } from 'node:fs'
import { parse } from '@slidev/parser'

const src = 'slides.md'
const out = '../thuyet-trinh.md'
const data = await parse(readFileSync(src, 'utf8'), src)

const parts = [
  { who: 'Người 1', name: 'Phần 1 — Vì sao cần LSTM? + lịch sử ra đời' },
  { who: 'Người 2', name: 'Phần 2 — Bên trong một ô LSTM' },
  { who: 'Người 3', name: 'Phần 3 — Vì sao LSTM nhớ lâu + thí nghiệm so sánh với RNN' },
  { who: 'Người 4', name: 'Phần 4 — LSTM trong thực tế + tổng kết' },
  { who: 'Cả nhóm', name: 'Q&A' },
]

let md = `# Lời thoại thuyết trình LSTM (45 phút, 4 người)\n\n`
md += `> File được sinh tự động từ speaker notes trong \`slides/slides.md\` (lệnh \`npm run notes\` trong thư mục \`slides\`). `
md += `Muốn sửa lời thoại thì sửa trong \`slides.md\` rồi chạy lại lệnh, để slide và file này luôn khớp nhau.\n>\n`
md += `> Ký hiệu: **[click]** = bấm sang bước animation tiếp theo · **(Demo)** = thao tác trên slide tương tác.\n>\n`
md += `> Phân công: Người 1 = Nguyễn Phú Đại · Người 2 = Trần Vũ Tiến Minh · Người 3 = Trần Đình Hiếu · Người 4 = Phạm Thanh An.\n\n`

let current = ''
let total = 0
data.slides.forEach((slide, idx) => {
  const note = (slide.note || '').trim()
  const head = note.match(/^\*\*\[(.+?) · ~([\d.]+) phút\](.*?)\*\*/m)
  const who = head ? head[1] : '?'
  const minutes = head ? Number(head[2]) : 0
  total += minutes
  const part = parts.find(p => p.who === who)
  if (part && part.name !== current) {
    current = part.name
    md += `---\n\n## ${part.name} (${who})\n\n`
  }
  const title = (slide.title || '').replace(/<[^>]+>/g, '') || '(không tiêu đề)'
  const body = (head ? note.replace(/^.*\n*/, '') : note).trim()
  md += `### Slide ${idx + 1} · ${title}  \n*${who} · ~${minutes} phút*\n\n${body}\n\n`
})
md += `---\n\n**Tổng thời lượng dự kiến:** ~${total} phút\n`

writeFileSync(out, md, 'utf8')
console.log(`Đã ghi ${out}: ${data.slides.length} slide, ~${total} phút`)
