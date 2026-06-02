---
name: implement-task
description: >
  Sử dụng khi user muốn THỰC THI (implement) một task file có sẵn trong tasks/backlog/.
  Skill này đọc file task → implement theo checklist → tick checklist → move sang tasks/done/.
  KHÔNG dùng khi user muốn TẠO task mới (dùng /create-task).
license: "MIT"
metadata:
  author: "thiennq"
  version: "1.0.0"
---

# Skill: /implement-task — Thực thi Task từ Backlog

Bạn là một **Senior Engineer AI**. Skill này thực thi một task file đã có sẵn trong `tasks/backlog/`, đảm bảo mọi checklist item được hoàn thành và file được chuyển sang `tasks/done/`.

> **User Intent mẫu:** "Implement @[tasks/backlog/xxx.md]", "Thực thi task xxx", "Làm task này"

## Quy trình BẮT BUỘC

```
Bước 1: Đọc & Hiểu task file
   └→ Đọc toàn bộ file task (bối cảnh, mục tiêu, yêu cầu, checklist)
   └→ Xác định files cần tạo/sửa từ bảng "Thiết kế kỹ thuật"
   └→ Đọc các file target để hiểu code hiện tại

Bước 2: Implement từng checklist item
   └→ Làm theo thứ tự checklist (trừ khi có dependency khác)
   └→ Mỗi item xong → tick ngay trong file task: "- [ ]" → "- [x]"
   └→ Nếu gặp blocker → ghi vào Notes & Open Questions

Bước 3: Review & Verify
   └→ Kiểm tra lại tất cả checklist items đã tick
   └→ Verify code changes không break existing functionality
   └→ Chạy build/lint nếu task liên quan đến code

Bước 4: Finalize
   └→ Cập nhật frontmatter: status "backlog" → "done"
   └→ Move file: tasks/backlog/xxx.md → tasks/done/xxx.md
   └→ Tạo thư mục tasks/done/ nếu chưa có
```

---

## Bước 1: Đọc & Hiểu

### Checklist đọc hiểu
- Đọc section **Bối cảnh** — hiểu WHY
- Đọc section **Mục tiêu** — hiểu WHAT
- Đọc section **Yêu cầu** — hiểu HOW (rules, constraints)
- Đọc section **Thiết kế kỹ thuật** — xác định files cần sửa
- Đọc section **Checklist** — đây là danh sách việc cần làm
- Đọc section **Notes & Open Questions** — những lưu ý quan trọng

### Đọc files target
Dùng `view_file` để đọc từng file trong bảng "Files cần tạo/sửa" **trước khi bắt đầu implement**. Hiểu context xung quanh vị trí cần sửa.

---

## Bước 2: Implement

### Nguyên tắc
1. **Theo đúng checklist** — không thêm, không bớt, không sáng tạo ngoài scope
2. **Tick ngay khi xong** — mỗi checklist item hoàn thành → cập nhật file task
3. **Giữ code chạy được** — sau mỗi thay đổi, code phải ở trạng thái hoạt động
4. **Respect existing code** — không xoá/sửa code ngoài scope task

### Cách tick checklist
```markdown
# Trước
- [ ] Thêm rule X vào SKILL.md

# Sau
- [x] Thêm rule X vào SKILL.md
```

---

## Bước 3: Review

### Verify checklist
- Đếm số `- [ ]` còn lại — phải = 0
- Đếm số `- [x]` — phải = tổng số items ban đầu
- Nếu có item không thể hoàn thành → ghi rõ lý do trong Notes

### Verify code (nếu task liên quan đến code)
- Build pass: `npm run build` hoặc `npx tsc --noEmit`
- Không có import errors
- Không break existing tests

---

## Bước 4: Finalize

### Cập nhật frontmatter
```yaml
# Trước
status: "backlog"

# Sau
status: "done"
```

### Move file
```bash
# Tạo thư mục nếu chưa có
mkdir -p tasks/done

# Move file
mv tasks/backlog/xxx.md tasks/done/xxx.md
```

> **Lưu ý:** Giữ nguyên tên file, chỉ thay đổi thư mục.

---

## Edge Cases

### Thiếu tên file task
Nếu người dùng yêu cầu thực thi task nhưng không cung cấp tên file task cụ thể:
1. Tìm kiếm và liệt kê 5 file task được tạo gần đây nhất trong thư mục `tasks/backlog/`.
2. Hiển thị danh sách này để người dùng lựa chọn.
3. Ưu tiên sử dụng `ask_question` / `ask_user_question` hoặc các công cụ tương đương nếu môi trường hỗ trợ để tạo trải nghiệm trắc nghiệm tương tác cho người dùng.

### Task có `depends_on`
Nếu task phụ thuộc task khác chưa done → thông báo user và DỪNG. Không implement task có dependency chưa giải quyết.

### Checklist item quá mơ hồ
Nếu checklist item không đủ rõ ràng để implement → hỏi user clarification trước khi tiếp tục.

### Task cần tạo file mới
Nếu task yêu cầu tạo file mới → tạo file + thêm nội dung theo spec trong task.

### Partial completion
Nếu chỉ hoàn thành được 1 phần → cập nhật status thành `"wip"`, tick các items đã xong, move sang `tasks/wip/` thay vì `tasks/done/`.

---

## Quy tắc quan trọng

1. **LUÔN đọc task file trước** — không bao giờ implement mà không hiểu context
2. **LUÔN tick checklist** — không bao giờ quên cập nhật trạng thái
3. **LUÔN move file** — task xong phải rời khỏi backlog
4. **Không over-engineer** — chỉ làm đúng những gì checklist yêu cầu
5. **Ghi lại quyết định** — nếu phải make judgement call, ghi vào Notes
