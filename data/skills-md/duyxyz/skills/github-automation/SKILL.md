---
name: github-automation
description: Kỹ năng tự động hóa quy trình trên GitHub bao gồm gắn thẻ phiên bản (tag), tối ưu hóa bộ nhớ đệm (cache) và quản lý Pull Request.
---

# Kỹ năng: GitHub Automation

Kỹ năng này giúp tối ưu hóa việc sử dụng GitHub làm nền tảng CI/CD và cộng tác.

## 1. Tự động gắn thẻ Phiên bản (Auto-tagging)
- **Quy tắc đếm tùy chỉnh**:
    - Patch (số cuối) tăng từ 0 đến 9.
    - Khi Patch chạm ngưỡng 9, lần tăng tiếp theo sẽ reset Patch về 0 và tăng Minor (số giữa).
    - Ví dụ: `1.0.8` -> `1.0.9` -> `1.1.0`.
- **Thực thi**: Nên được thực hiện tự động qua GitHub Actions sau khi code được merge vào nhánh chính.

## 2. Tối ưu hóa Cache Build
- **Mục tiêu**: Giảm thời gian chờ đợi CI bằng cách lưu trữ các tài nguyên nặng.
- **Flutter Caching**:
    - Cache thư mục `pub-cache`.
    - Cache Gradle wrapper và dependencies cho Android.
- **Tooling**: Sử dụng `actions/cache@v4` với các key dựa trên mã băm (hash) của `pubspec.lock`.

## 3. Quản lý Pull Request & Issue
- **PR Templates**: Sử dụng tệp `.github/pull_request_template.md` để yêu cầu thông tin đầy đủ về thay đổi, danh sách kiểm tra (checklist) và ảnh chụp màn hình nếu có thay đổi UI.
- **Labels**: Tự động gắn nhãn (label) dựa trên loại thay đổi (feat, fix, docs).

## 4. GitHub Releases
- **Changelog Tự động**: Tích hợp các công cụ tự động tạo ghi chú phát hành (release notes) dựa trên các tiêu đề commit.
- **Draft Releases**: Luôn tạo bản nháp (Draft) trước khi công bố chính thức để kiểm tra lại các tệp binary đính kèm.

## Tham chiếu liên quan
- [CI/CD & DevOps (Android)](file:///c:/Users/PC/Documents/Github/skills/skills/android/cicd-devops/SKILL.md)
- [Giao thức Tương tác (Strict Protocol)](file:///c:/Users/PC/Documents/Github/skills/skills/strict-protocol/SKILL.md)
