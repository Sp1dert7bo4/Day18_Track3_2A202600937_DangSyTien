# Failure Analysis — Lab 18: Production RAG

**Nhóm:** Đặng Sỹ Tiến (Cá nhân)  
**Thành viên:** Đặng Sỹ Tiến

---

## RAGAS Scores

| Metric | Naive Baseline | Production | Δ |
|--------|---------------|------------|---|
| Faithfulness | 0.45 | 0.88 | +0.43 |
| Answer Relevancy | 0.52 | 0.91 | +0.39 |
| Context Precision | 0.38 | 0.85 | +0.47 |
| Context Recall | 0.42 | 0.89 | +0.47 |

## Bottom-5 Failures

### #1
- **Question:** Một nhân viên Senior có 9 năm thâm niên được nghỉ phép bao nhiêu ngày?
- **Expected:** 12 ngày phép cơ bản + 1 ngày phép thâm niên = 13 ngày.
- **Got:** 12 ngày.
- **Worst metric:** Faithfulness
- **Error Tree:** Output sai → Context đúng? (Có chứa rule 5 năm được 1 ngày) → Query OK.
- **Root cause:** LLM đọc đúng context nhưng không thực hiện phép tính (9 chia 5 dư 4, được 1) mà trả lời thẳng số 12.
- **Suggested fix:** Thêm few-shot reasoning (Chain-of-Thought) để bắt LLM tự tính ngày phép thâm niên riêng rồi cộng dồn.

### #2
- **Question:** Muốn mua thiết bị trị giá 55 triệu cần ai phê duyệt?
- **Expected:** CEO.
- **Got:** Trưởng phòng.
- **Worst metric:** Context Precision
- **Error Tree:** Output sai → Context sai → Quá nhiều chunks policy mua sắm không liên quan (dưới 10 triệu) chèn lên trên.
- **Root cause:** RRF merge bị loãng, không nhận diện được keyword số "55 triệu".
- **Suggested fix:** Thêm module Extraction M5 để nhận diện mức chi tiêu tài chính như một Metadata field để lọc (Filter).

### #3
- **Question:** Thông tin lương thuộc cấp độ phân loại dữ liệu nào?
- **Expected:** Tuyệt mật (Confidential).
- **Got:** Nội bộ.
- **Worst metric:** Answer Relevancy
- **Error Tree:** Answer không khớp câu hỏi → Query thiếu focus.
- **Root cause:** Document về lương và phân loại dữ liệu nằm ở 2 file riêng biệt, cần multi-hop logic.
- **Suggested fix:** Sinh các câu hỏi mở rộng (HyQA) trong Enrichment M5 liên kết chéo giữa từ khoá Lương và Phân loại dữ liệu.

### #4
- **Question:** Bao lâu phải đổi mật khẩu một lần?
- **Expected:** 120 ngày.
- **Got:** 90 ngày.
- **Worst metric:** Context Precision
- **Error Tree:** Output sai → Context sai (Tìm trúng bản v1 cũ).
- **Root cause:** Trong DB có 2 file policy về mật khẩu, version cũ chưa bị ghi đè.
- **Suggested fix:** Setup Document ID theo tên file và upsert thay vì append, hoặc lọc theo version mới nhất.

### #5
- **Question:** Phụ cấp ăn trưa hàng tháng là bao nhiêu?
- **Expected:** 730,000 VND.
- **Got:** Không có thông tin.
- **Worst metric:** Context Recall
- **Error Tree:** Output rỗng → Context rỗng.
- **Root cause:** Bảng lương trong PDF bị cắt gãy dòng (Chunking cắt ngang markdown table).
- **Suggested fix:** Viết riêng module MarkdownTableSplitter trong hàm `chunk_structure_aware`.

## Case Study (cho presentation)

**Question chọn phân tích:** Một nhân viên Senior có 9 năm thâm niên được nghỉ phép bao nhiêu ngày?

**Error Tree walkthrough:**
1. Output đúng? → Sai (chỉ trả lời 12 ngày phép cơ bản).
2. Context đúng? → Đúng, Context đã chứa đầy đủ đoạn văn mô tả "12 ngày phép + 1 ngày cho mỗi 5 năm".
3. Query rewrite OK? → Tốt, tìm rất chuẩn.
4. Fix ở bước: Bước sinh câu trả lời bằng LLM.

**Nếu có thêm 1 giờ, sẽ optimize:**
- Mình sẽ viết lại prompt bằng kỹ thuật Chain-of-Thought (CoT):
  *Bước 1: Tính số phép cơ bản.*
  *Bước 2: Tính số thâm niên (Năm hiện tại - Năm vào làm).*
  *Bước 3: Lấy thâm niên chia 5.*
  *Bước 4: Trả lời kết quả cuối cùng = Phép cơ bản + Kết quả bước 3.*
