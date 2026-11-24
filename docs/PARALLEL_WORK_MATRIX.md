# Wifi-AI Secure — Wave & Dependency Master Plan

> Mục tiêu: 3 thành viên phát triển song song theo từng Wave, giảm tối đa việc sửa trùng file/module và chỉ chuyển giai đoạn khi các dependency gate đã đạt.

## Quy ước thành viên

- **Hoàng Phúc (HP) — DATA:** AWID3, data audit, loader, cleaning, preprocessing, feature schema, dataset split.
- **Quốc Đạt (QD) — AI:** Random Forest, XGBoost, FeedForward, Isolation Forest, training, evaluation, model packaging.
- **Tiến Đạt (TD) — APP:** API/backend, dashboard, database, alert, integration, test hệ thống.
- **DONE:** chỉ đánh dấu khi có PR đã merge, test/log hoặc artifact chứng minh hoàn thành. Việc tạo branch/Issue không đồng nghĩa task code đã DONE.

## 1. Master execution table — Wave + Dependency

| Wave | Hoàng Phúc — DATA | Tiến Đạt — APP | Quốc Đạt — AI | Điều kiện / Dependency |
|---|---|---|---|---|
| **Wave 0.1** | DATA-00: xác định nguồn AWID3, phiên bản/file cần dùng, cách lưu dữ liệu | APP-00: chuẩn bị repo skeleton, app entry point và môi trường chạy | AI-00: chốt bài toán phân loại, anomaly detection và chỉ số đánh giá | Cả 3 thống nhất Python, cấu trúc thư mục, cách chạy project |
| **Wave 0.2** | DATA-01: kiểm kê file, schema sơ bộ, label candidate, dung lượng | APP-01: dựng API/UI skeleton, SQLite schema draft | AI-01: dựng train/evaluate skeleton bằng synthetic fixture | Có thể làm song song; AI và APP chỉ dùng dữ liệu mẫu, chưa giả định schema AWID3 |
| **Wave 0.3** | DATA-02: báo cáo cột, dtype, missing, duplicate, label distribution | APP-02: dashboard hiển thị mock detection event | AI-02: tạo synthetic fixture đúng format contract, baseline pipeline chưa dùng để báo cáo kết quả | Review data schema và prediction/event contract |
| **Gate S0** | Review feature/label schema | Review API/event schema | Review model input/output | Contract chung được cả 3 xác nhận; không tự ý đổi tên field sau gate |
| **Wave 1.1** | DATA-03: hoàn thiện loader đọc AWID3 theo file thực tế | APP-03: hoàn thiện layout Dashboard, trang Detection/History | AI-03: implement Random Forest baseline trên fixture | Ba module độc lập, không sửa file của nhau |
| **Wave 1.2** | DATA-04: cleaning, xử lý missing/invalid, loại cột không phù hợp có lý do | APP-04: endpoint nhận event/prediction mock và lưu SQLite | AI-04: metric pipeline, confusion matrix, per-class report trên fixture | DATA cung cấp schema đã xác minh; APP vẫn dùng mock rõ ràng |
| **Wave 1.3** | DATA-05: label mapping và feature schema cố định | APP-05: bộ lọc lịch sử, trang chi tiết event | AI-05: tích hợp RF với schema đã xác minh, kiểm tra input shape | **G1 — Schema Ready:** tên feature, dtype, label field và label mapping được xác minh |
| **Wave 1.4** | DATA-06: tạo train/validation/test split và split manifest | APP-06: hoàn thiện event contract, trạng thái alert và log | AI-06: chạy RF baseline trên split chính thức, lưu config/seed | AI chỉ dùng split đã được DATA bàn giao; không dùng Test để tuning |
| **Gate S1** | Bàn giao dataset split + preprocessing metadata | Xác nhận app event schema | Xác nhận RF baseline và evaluation report | **G2 — Dataset Ready:** split tái lập, leakage audit sơ bộ, preprocessor fit trên Train |
| **Wave 2.1** | DATA-07: hoàn thiện preprocessing pipeline và transform API | APP-07: hoàn thiện backend service và database repository | AI-07: XGBoost training/tuning trên Train/Validation | Có thể song song; giữ nguyên feature order và split đã chốt |
| **Wave 2.2** | DATA-08: kiểm tra class imbalance, duplicate/overlap và leakage | APP-08: hoàn thiện alert rules/configuration, dashboard metrics placeholder | AI-08: FeedForward training, checkpoint, early stopping | QD dùng đúng preprocessing đã bàn giao; tuning chỉ trên Validation |
| **Wave 2.3** | DATA-09: đóng gói preprocessor, feature schema, label mapping, version metadata | APP-09: chuẩn bị model adapter interface và integration tests bằng mock | AI-09: Isolation Forest trên Normal-only Train, threshold chọn bằng Validation | Isolation Forest là nhánh anomaly riêng; không thay thế classifier |
| **Wave 2.4** | Review data quality + reproducibility | Review app contract và event flow | AI-10: so sánh RF/XGBoost/FeedForward; per-class metrics, Macro F1, FPR | **G3 — Model/Data Ready:** artifacts và metadata khớp schema, kết quả có thể tái lập |
| **Wave 3.1** | DATA-10: hỗ trợ kiểm tra feature input và transform trên dữ liệu mới | APP-10: tích hợp Predictor thật vào API, thay mock adapter | AI-11: đóng gói predictor thống nhất, model version, output schema | Cần G2 + G3; không tích hợp nếu feature order hoặc label mapping không khớp |
| **Wave 3.2** | DATA-11: test file lỗi, cột thiếu/thừa, dữ liệu ngoài phân phối | APP-11: nối API → inference → alert → SQLite → Dashboard | AI-12: kiểm tra prediction consistency, confidence/anomaly score và latency | Có thể test module song song; sau đó chạy E2E cùng một model artifact |
| **Wave 3.3** | DATA-12: xác nhận pipeline chạy lại từ raw data tới processed data | APP-12: chạy offline CSV replay và hiển thị detection history | AI-13: đánh giá cuối trên Test untouched, phân tích false positive/negative | **G4 — End-to-End Ready:** demo offline từ dữ liệu đầu vào đến cảnh báo |
| **Gate S3** | Review pipeline và dữ liệu | Review toàn bộ luồng app | Review kết quả AI | Cả 3 cùng xác nhận hệ thống offline chạy ổn định |
| **Wave 4.1 (Optional)** | PCAP-01: khảo sát cách ánh xạ packet/frame thành feature tương thích | PCAP-02: thêm giao diện nạp/replay PCAP nếu được duyệt | PCAP-03: đánh giá khả năng inference và domain shift | Chỉ bắt đầu sau G4; không giả định PCAP tạo trực tiếp đúng feature AWID3 |
| **Wave 4.2 (Optional)** | Kiểm tra feature extractor và dữ liệu lab được phép | Tích hợp luồng PCAP replay vào app | Đánh giá trên bộ PCAP riêng, ghi rõ giới hạn | Không gọi là live detection nếu mới chỉ replay file |
| **Wave 5.1** | QA-01: unit test data/preprocessing, reproducibility | QA-02: API, DB, dashboard, error handling | QA-03: model loading, inference, metrics regression | Cả 3 chạy test độc lập |
| **Wave 5.2** | Fix lỗi dữ liệu | Fix lỗi app/integration | Fix lỗi model/evaluation | Không thay đổi contract lớn nếu chưa review |
| **Wave 5.3** | DOC-01: tài liệu AWID3, schema, preprocessing | DOC-02: README cài đặt, API, Dashboard, demo guide | DOC-03: mô hình, metrics, thực nghiệm, limitations | Tài liệu phải khớp đúng phần code và kết quả thực tế |
| **Wave 5.4** | Review release | Review release và chạy trên máy sạch | Review model artifacts và reproducibility | **G5 — Release Ready:** test đạt, hướng dẫn cài đặt, demo tái lập |
| **Wave 5.5** | Hỗ trợ nghiệm thu | Merge develop → main sau khi được duyệt | Hỗ trợ demo và kiểm tra kết quả | Tag release; không merge khi còn lỗi P0/P1 |

## 2. Các Gate bắt buộc — không vượt bước khi chưa đạt

| Gate | Người bàn giao | Người nhận | Điều kiện để qua Gate |
|---|---|---|---|
| **G0 — Project/Contract Ready** | Cả 3 | Cả 3 | Repo, branch, folder ownership, Python/dependency policy, data contract và event contract thống nhất |
| **G1 — Schema Ready** | Hoàng Phúc | Quốc Đạt + Tiến Đạt | Đã xác minh cột nhãn, feature được chọn, dtype, thứ tự feature, label mapping từ AWID3 thật |
| **G2 — Dataset Ready** | Hoàng Phúc | Quốc Đạt | Train/Validation/Test manifest, seed, split strategy, leakage checks; preprocessing chỉ fit trên Train |
| **G3 — Model Ready** | Quốc Đạt | Tiến Đạt | Predictor API, model artifact, model version, label mapping, output schema và evaluation report |
| **G4 — E2E Ready** | Tiến Đạt điều phối | Cả 3 | Nạp dữ liệu → preprocessing → AI inference → alert → SQLite → Dashboard chạy được |
| **G5 — Release Ready** | Cả 3 | Cả 3 | Unit/integration test, README, demo, báo cáo, model/data version và giới hạn đã được kiểm tra |

**Quy tắc:** Nếu gate chưa đạt, người nhận có thể tiếp tục làm mock, test fixture hoặc phần độc lập; không được dùng kết quả chưa xác minh làm kết quả chính thức.

## 3. Việc nào có thể làm đồng thời?

| Nhóm công việc | Có thể chạy song song? | Điều kiện |
|---|---|---|
| AWID3 audit ↔ AI skeleton ↔ Dashboard mock | **Có** | AI dùng synthetic fixture; APP dùng mock event |
| Loader/cleaner ↔ RF code skeleton ↔ API/SQLite skeleton | **Có** | Mỗi người chỉ sửa folder sở hữu |
| Preprocessing/split ↔ App UI ↔ AI tuning | **Có điều kiện** | AI tuning chính thức chỉ sau G2; APP tiếp tục bằng mock |
| XGBoost ↔ FeedForward | **Có** | Quốc Đạt quản lý riêng config/artifact; tránh cùng sửa một file model |
| Dashboard ↔ Alert/DB | **Có thể** | Tiến Đạt tự chia module/file hoặc làm lần lượt nếu cùng file |
| Model packaging ↔ Dashboard hoàn thiện | **Có** | Cùng tuân thủ contract; APP chưa tích hợp model thật trước G3 |
| Data validation ↔ AI evaluation ↔ App integration test | **Có** | Dùng cùng phiên bản schema/model/data |
| PCAP parser ↔ Live capture | **Chưa nên làm sớm** | Chỉ sau G4 và phải xác minh cách tạo feature tương thích |
| E2E test và release | **Không hoàn toàn** | Có thể chuẩn bị riêng, nhưng nghiệm thu cuối phải chạy chung |

## 4. Code ownership — tránh sửa cùng file

| Khu vực | Owner | Người khác xử lý thế nào? |
|---|---|---|
| `src/data/**`, `data/**`, `configs/data/**`, `tests/data/**` | Hoàng Phúc | Tạo Issue/comment hoặc review PR; không tự commit vào các file này |
| `src/models/**`, `src/training/**`, `src/evaluation/**`, `tests/models/**`, `docs/ai/**` | Quốc Đạt | Hoàng Phúc góp ý schema; Tiến Đạt góp ý predictor contract qua PR |
| `src/api/**`, `src/app/**`, `src/database/**`, `src/alerts/**`, `tests/api/**` | Tiến Đạt | Không tự sửa app; thay đổi interface đề nghị qua Issue/PR |
| `docs/INTERFACE_CONTRACT.md`, `configs/shared/**`, `requirements.txt` | Cả 3 đồng sở hữu | Một PR tại một thời điểm; cả 3 review nếu đổi contract/dependency |
| `README.md`, `docs/WORK_PLAN.md`, `docs/WAVE_DEPENDENCY_PLAN.md` | Tiến Đạt điều phối | Thành viên gửi nội dung cho owner; tránh cùng sửa file |

## 5. Git workflow theo từng Wave

- Branch cá nhân: `feature/data-pipeline`, `feature/ai-models`, `feature/dashboard`.
- Tất cả PR cá nhân merge vào `develop`; không push trực tiếp `main`/ `develop`.
- Trước khi bắt đầu Wave mới: fetch và cập nhật branch từ `develop`.
- PR phải ghi task ID, file thay đổi, test đã chạy, dependency liên quan và ảnh/metrics nếu có.
- Một file chỉ có một owner. Nếu cần thay đổi file của người khác, mở Issue và chờ owner xác nhận.
- Contract thay đổi cần thông báo cả nhóm và cập nhật contract test.
- Merge xong mới đánh dấu task DONE; cập nhật Issue theo `Done / Next / Blocked / PR link`.

## 6. Nhịp điều phối

| Thời điểm | Hoạt động |
|---|---|
| Đầu tuần | Chọn Wave/task có thể chạy, xác nhận dependency và người owner |
| Giữa tuần | Kiểm tra blocker, contract, file conflict và artifact bàn giao |
| Cuối tuần | Review PR, merge vào develop, chạy integration tests |
| Sau mỗi Gate | Cả 3 xác nhận đạt/chưa đạt trước khi chuyển Wave |

## 7. Các lưu ý kỹ thuật không được bỏ qua

- Không mặc định AWID3 có đúng 29 feature hoặc 14 class theo nguồn tham khảo; xác minh trên đúng phiên bản nhóm tải.
- Không commit raw AWID3, PCAP riêng tư, model artifact lớn hoặc secrets lên Git.
- Không fit scaler/encoder/imputer trên toàn bộ dataset; chỉ fit trên Train.
- Không dùng Test để tuning hoặc chọn threshold.
- Isolation Forest anomaly score không phải tên loại tấn công.
- AWID3 offline result không chứng minh live Wi-Fi detection. PCAP/live capture là giai đoạn mở rộng, cần feature extraction tương thích và dữ liệu lab được phép.
- Cảnh báo là tín hiệu hỗ trợ phân tích, không tự động khẳng định một thiết bị/người dùng đang tấn công.

## 8. Trạng thái hiện tại

Các branch, tài liệu khởi tạo và ba GitHub Issues đã được tạo trước đó. **Các task triển khai DATA/AI/APP trong bảng này chưa được tự động đánh dấu DONE**; nhóm cần cập nhật trạng thái theo PR/commit/test thực tế.

- [Issue #1 — Hoàng Phúc / DATA](https://github.com/hphuc032/Wifi-AI-Secure/issues/1)
- [Issue #2 — Quốc Đạt / AI](https://github.com/hphuc032/Wifi-AI-Secure/issues/2)
- [Issue #3 — Tiến Đạt / APP](https://github.com/hphuc032/Wifi-AI-Secure/issues/3)
