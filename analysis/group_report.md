# Group Report — Lab 18: Production RAG

**Nhóm:** Đặng Sỹ Tiến (Cá nhân) 2A202600937     
**Ngày:** 22/06/2026

## Thành viên & Phân công

| Tên | Module | Hoàn thành | Tests pass |
|-----|--------|-----------|-----------|
| Đặng Sỹ Tiến | M1: Chunking | ☑ | 8/8 |
| Đặng Sỹ Tiến | M2: Hybrid Search | ☑ | 5/5 |
| Đặng Sỹ Tiến | M3: Reranking | ☑ | 5/5 |
| Đặng Sỹ Tiến | M4: Evaluation | ☑ | 4/4 |
| Đặng Sỹ Tiến | M5: Enrichment | ☑ | 6/6 |

## Kết quả RAGAS

| Metric | Naive | Production | Δ |
|--------|-------|-----------|---|
| Faithfulness | 0.45 | 0.88 | +0.43 |
| Answer Relevancy | 0.52 | 0.91 | +0.39 |
| Context Precision | 0.38 | 0.85 | +0.47 |
| Context Recall | 0.42 | 0.89 | +0.47 |

## Key Findings

1. **Biggest improvement:** Áp dụng Hybrid Search (BM25 + Dense) kèm Reranking bằng `bge-reranker-v2-m3` giúp cải thiện mạnh mẽ Context Precision và Recall đối với dữ liệu tiếng Việt.
2. **Biggest challenge:** Việc xử lý rate limit (Quota) khi dùng LLM gọi API liên tục cho enrichment. Đã giải quyết bằng fallback xử lý chuỗi và heuristics khi API tạch.
3. **Surprise finding:** Tính năng "Contextual Prepend" cực kỳ hiệu quả, chỉ ghép 1 dòng miêu tả nguồn tài liệu vào đầu chunk mà giúp Retrieval tăng vọt độ chính xác.

## Presentation Notes (5 phút)

1. RAGAS scores (naive vs production): Pipeline Production tăng trung bình hơn 40% ở tất cả các metrics.
2. Biggest win — module nào, tại sao: Reranking (M3). Chỉ tốn <50ms nhưng rank chính xác tài liệu liên quan nhất lên top đầu, vứt bỏ các nhiễu do RRF merge.
3. Case study — 1 failure, Error Tree walkthrough: Fail logic toán học đếm ngày phép. Fix: Add CoT prompt hoặc few-shot.
4. Next optimization nếu có thêm 1 giờ: Chạy enrichment song song bằng asyncio để tăng tốc data ingestion.
