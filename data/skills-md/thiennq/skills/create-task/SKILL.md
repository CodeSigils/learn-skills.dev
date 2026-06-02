---
name: create-task
description: >
  Sử dụng khi user muốn TẠO TASK MỚI cho dự án. Skill này dẫn dắt quy trình
  interview → refine → viết file markdown vào tasks/backlog/. KHÔNG dùng khi
  user chỉ hỏi thông tin hoặc muốn thực hiện task ngay lập tức.
license: "MIT"
metadata:
  author: "thiennq"
  version: "1.0.0"
---

# Skill: /create-task — Tạo Task qua Interview

Bạn là một **Tech Lead / Product Manager AI**. Skill này biến yêu cầu mơ hồ của user thành một task file markdown rõ ràng, actionable, sẵn sàng để implement.

> **User Intent mẫu:** "Tôi muốn thêm tính năng X", "Cần build Y", "Refactor Z", "Fix bug A"

## Quy trình BẮT BUỘC

```
Bước 1: Nhận yêu cầu thô từ user

Bước 2: Interview — đặt 3–5 câu hỏi có chọn lọc
   └→ Mỗi câu hỏi phải nhắm vào 1 điểm mơ hồ cụ thể
   └→ Không hỏi những điều đã rõ ràng
   └→ Nhóm câu hỏi liên quan vào 1 câu nếu được

Bước 3: Nhận response từ user → Refine requirements

Bước 4: Viết task file markdown vào tasks/backlog/
   └→ Xác nhận với user trước khi tạo (optional nếu rõ ràng)
```

---

## Bước 2: Hướng dẫn Interview

### Các chiều cần làm rõ (chọn 3–5 cái phù hợp)

| Chiều | Câu hỏi gợi ý |
|-------|--------------| 
| **Output/Format** | Kết quả trả về dạng gì? (JSON, HTML, markdown, số?) |
| **Scope/Boundary** | Cái gì nằm trong scope, cái gì ngoài? |
| **Auth/Permission** | Ai được phép dùng? Cần xác thực không? |
| **Error handling** | Khi thất bại trả về gì? Retry hay fail fast? |
| **Performance** | Giới hạn size/row/response time? |
| **Integration** | Tích hợp với hệ thống nào hiện có? |
| **Edge cases** | Trường hợp đặc biệt nào cần xử lý? |
| **Priority** | Urgent hay backlog? Blocking cái gì không? |

### Nguyên tắc đặt câu hỏi

- **Cụ thể, không chung chung** — "Giới hạn bao nhiêu rows?" tốt hơn "Performance thế nào?"
- **Đưa options khi có thể** — "Trả về A, B hay C?" giúp user trả lời nhanh hơn
- **Sử dụng công cụ tương tác** — Ưu tiên sử dụng `ask_question` / `ask_user_question` hoặc các công cụ tương đương nếu môi trường hỗ trợ để tạo trải nghiệm trắc nghiệm tương tác cho người dùng.
- **Số thứ tự rõ ràng** — Đánh số 1, 2, 3... để user trả lời từng cái
- **Không hỏi quá 5 câu** — Nếu cần hỏi thêm, có thể có vòng 2 ngắn hơn

---

## Bước 4: Viết Task File

### Quy tắc file

- **Thư mục:** `tasks/backlog/`
  - Nếu chưa có thư mục `tasks/` trong repo, tự tạo cả cây `tasks/backlog/`, `tasks/wip/`, `tasks/done/`
- **Tên file:** `YYYY-MM-DD-ten-task-ngan-gon.md`
  - Dùng ngày hiện tại
  - Tên kebab-case, tối đa 5-6 từ, mô tả đúng nội dung
  - VD: `2026-04-08-explore-query-tool.md`

### Template bắt buộc

```markdown
---
title: "[Tên task đầy đủ]"
status: "backlog"
priority: "high | medium | low"
created: "YYYY-MM-DD"
depends_on: ["file-task-khac.md"]   # [] nếu không có dependency
tags: ["tag1", "tag2"]              # keywords để filter/group
---

# [Tên task đầy đủ]

## Bối cảnh

[1-2 đoạn giải thích WHY: vấn đề hiện tại là gì, tại sao cần làm task này]

## Mục tiêu

[1 câu súc tích mô tả WHAT: sẽ build/fix/refactor cái gì]

## Yêu cầu

### Input / Trigger
[Ai/cái gì kích hoạt tính năng này]

### Output / Behavior
[Kết quả mong đợi, format cụ thể, ví dụ]

### Constraints & Rules
[Giới hạn, edge cases, error handling]

### Auth / Permission
[Ai được dùng, cần token không]

## Thiết kế kỹ thuật (nếu biết)

### Files cần tạo/sửa
| File | Action |
|------|--------|
| ... | MỚI / SỬA / XÓA |

### Pseudocode / API Design (nếu phức tạp)
\`\`\`
...
\`\`\`

## Phân biệt với tính năng hiện có (nếu có)

[So sánh với tool/feature đã có để tránh nhầm lẫn]

## Checklist

- [ ] [Bước implement cụ thể 1]
- [ ] [Bước implement cụ thể 2]
- [ ] TypeScript build pass
- [ ] Test thủ công
- [ ] [Test case quan trọng]

## Notes & Open Questions

- [Lưu ý kỹ thuật, trade-offs, quyết định cần confirm sau]
```

### Frontmatter Schema

| Field | Type | Bắt buộc | Mô tả |
|-------|------|----------|-------|
| `title` | string | ✅ | Tên task đầy đủ (dùng trong script/listing) |
| `status` | `backlog` \| `wip` \| `done` | ✅ | Trạng thái hiện tại |
| `priority` | `high` \| `medium` \| `low` | ✅ | Mức độ ưu tiên |
| `created` | `YYYY-MM-DD` | ✅ | Ngày tạo (không đổi) |
| `depends_on` | `string[]` | ✅ | Danh sách file task phụ thuộc, `[]` nếu không có |
| `tags` | `string[]` | ✅ | Keywords để filter/group, `[]` nếu không có |



### Nguyên tắc viết task tốt

1. **Bối cảnh trước, Solution sau** — Giải thích WHY trước khi nói WHAT
2. **Ví dụ cụ thể** — Output format phải có ví dụ JSON/code thực tế
3. **Checklist actionable** — Mỗi item checkbox phải là 1 việc cụ thể, có thể tick được
4. **Ghi Notes trung thực** — Trade-offs, edge cases chưa quyết định, kỹ thuật cần nghiên cứu
5. **Phân biệt với tính năng hiện có** — Tránh duplicate, làm rõ boundary

---

## Ví dụ Tham khảo

> Xem: `tasks/backlog/2026-04-08-explore-query-tool.md`

Đây là một task được viết tốt: có bối cảnh, mục tiêu, bảng so sánh, pseudocode, checklist chi tiết và Notes về trade-offs.

---

## Quy tắc quan trọng

1. **LUÔN interview trước** — Không bao giờ viết task ngay từ yêu cầu thô
2. **Không hỏi những điều đã rõ** — Đọc kỹ yêu cầu trước khi đặt câu hỏi
3. **3–5 câu hỏi là đủ** — Không làm user mệt mỏi với quá nhiều câu hỏi
4. **File luôn vào `tasks/backlog/`** — Không skip thư mục dù task "urgent"
5. **Ngày trong tên file là ngày tạo** — Không dùng ngày dự kiến hoàn thành
