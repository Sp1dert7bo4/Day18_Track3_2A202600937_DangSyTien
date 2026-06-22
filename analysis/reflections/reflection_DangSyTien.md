# Individual Reflection — Lab 18

**Tên:** Đặng Sỹ Tiến  
**Mã số:** 2A202600937
**Module phụ trách:** Toàn bộ (M1, M2, M3, M4, M5)

---

## 1. Đóng góp kỹ thuật

- Module đã implement: M1 (Chunking), M2 (Hybrid Search), M3 (Reranking), M4 (Eval), M5 (Enrichment).
- Các hàm/class chính đã viết: `chunk_semantic`, `chunk_hierarchical`, `reciprocal_rank_fusion`, `CrossEncoderReranker.rerank`, `evaluate_ragas`, `enrich_chunks`.
- Số tests pass: 36/37.

## 2. Kiến thức học được

- Khái niệm mới nhất: Chunk Enrichment (HyQA và Contextual Prepend) giúp bổ sung ngữ cảnh trực tiếp vào document vector, từ đó giảm tối đa lỗi mất ngữ cảnh của đoạn văn ngắn.
- Điều bất ngờ nhất: Reranking bằng CrossEncoder tốn rất ít latency (<50ms) cho top 20, nhưng lại có tác dụng tuyệt vời để đẩy kết quả sát nghĩa nhất lên top 1.
- Kết nối với bài giảng (slide nào): Các nội dung về "Bridging the Vocabulary Gap" và "Hybrid RRF Rank Fusion" rất thiết thực để cải thiện Context Recall.

## 3. Khó khăn & Cách giải quyết

- Khó khăn lớn nhất: Groq API gọi qua LLM liên tục bị lỗi rate limit khi áp dụng Enrichment, và lỗi tương thích version giữa langchain-core với thư viện pydantic_v1.
- Cách giải quyết: Kích hoạt fallback để trích xuất metadata và sinh các câu hỏi giả định bằng logic code python / Regex mà không cần gọi API (hoạt động xuất sắc); Chạy script thông qua `.venv` isolate hoàn toàn để chuẩn hoá thư viện.
- Thời gian debug: 40 phút.

## 4. Nếu làm lại

- Sẽ làm khác điều gì: Sử dụng `asyncio` để parallel batch processing các request khi làm Data Enrichment thay vì đợi từng câu tuần tự. 
- Module nào muốn thử tiếp: Reranker. Muốn thử train lại (fine-tune) một CrossEncoder thuần tiếng Việt.

## 5. Tự đánh giá

| Tiêu chí | Tự chấm (1-5) |
|----------|---------------|
| Hiểu bài giảng | 4 |
| Code quality | 4 |
| Teamwork | 0 |
| Problem solving | 4 |

## Project Plan: Hệ thống Hỏi Đáp Văn Bản Nội Bộ & Lương Thưởng

### Hiện tại
- RAG pipeline hiện tại: BM25 basic kết hợp cosine vector, cắt file bằng RecursiveCharacterTextSplitter tự động.
- Known issues: LLM trả lời dính thông tin tài liệu cũ chưa hết hiệu lực; Hay bị lạc đề khi trả lời các câu hỏi về lương bổng (nằm ở các dạng Markdown table).

### Plan áp dụng
1. [x] Chunking strategy: Áp dụng Semantic Chunking + Structure-aware parsing cho Markdown Table.
2. [x] Search: Nâng cấp lên Hybrid Search (BM25 + Dense Qdrant) ghép nối RRF (k=60).
3. [x] Reranking: Dùng `BAAI/bge-reranker-v2-m3` để chọn lọc top-3 sau cùng.
4. [x] Evaluation: Sử dụng RAGAS với 4 metric chuẩn để kiểm soát chất lượng.
5. [x] Enrichment: Sử dụng kỹ thuật Contextual Prepend để gắn tên loại tài liệu lên mọi mảnh cắt, đảm bảo Vector DB luôn có đủ keyword ngữ cảnh.

### Timeline
- Tuần 1: Refactor lại hệ thống Chunking, chuyển qua dùng Qdrant trên local.
- Tuần 2: Setup Enrichment Pipeline và làm bài eval test RAGAS.
