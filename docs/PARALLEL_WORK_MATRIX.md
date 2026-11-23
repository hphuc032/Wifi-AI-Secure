# Wifi-AI Secure — ma trận giai đoạn làm song song và tránh xung đột

> Mục tiêu: ba thành viên có thể phát triển đồng thời nhưng không sửa trùng file, không tự ý đổi schema/API của nhau và không tích hợp dữ liệu chưa được xác minh.

## 1. Nguyên tắc chia việc

1. Mỗi module có **một người sở hữu chính**. Người khác góp ý qua Issue/PR, không sửa trực tiếp cùng file.
2. Có thể làm song song khi đầu vào đã được mô tả bằng **contract** hoặc mock fixture.
3. Việc phụ thuộc dữ liệu thật chỉ bắt đầu sau khi Hoàng Phúc xác nhận schema, nhãn, thứ tự feature và split.
4. Thay đổi contract dùng chung phải được cả ba đồng ý trước khi merge vào `develop`.
5. Mỗi người làm trên branch riêng; Pull Request vào `develop`; không commit trực tiếp vào `main`/ `develop`.
6. Không commit AWID3 gốc, PCAP riêng tư, model lớn hoặc secret vào Git.

## 2. Bảng giai đoạn tổng thể — ai làm cùng lúc được?

| Giai đoạn | Hoàng Phúc — DATA | Quốc Đạt — AI | Tiến Đạt — APP | Có thể làm song song? | Điều kiện / điểm bàn giao |
|---|---|---|---|---|---|
| GĐ 0. Thống nhất nền tảng (1–2 ngày) | Cùng thống nhất nguồn AWID3, tên trường nhãn dự kiến, cách lưu dữ liệu | Cùng thống nhất bài toán, đầu ra mô hình và chỉ số đánh giá | Tạo repo skeleton, quy ước branch/PR và môi trường mẫu | **Cả 3 làm chung** | Chốt Python, folder ownership, data contract, prediction/event contract |
| GĐ 1. Khảo sát + dựng khung (Tuần 1) | Tải/kiểm kê AWID3; kiểm tra CSV, nhãn, dtype, missing, phân bố lớp | Dựng khung train/evaluate bằng **synthetic fixture** theo contract; chưa kết luận hiệu năng | Dựng API/UI/SQLite skeleton bằng **mock prediction** | **Cả 3 làm song song** | AI và APP chỉ dùng fixture/mock; không tự giả định feature AWID3 |
| GĐ 2. Xác minh schema + module độc lập (Tuần 2) | Chốt feature schema, label mapping, báo cáo chất lượng; viết loader/cleaner ban đầu | Viết Random Forest baseline và khung metric trên fixture; chuẩn bị XGBoost/NN skeleton | Hoàn thiện dashboard, endpoint nhận event mẫu, lịch sử cảnh báo | **Cả 3 làm song song** | Schema/label mapping cần được DATA review; mock data phải đánh dấu rõ |
| GĐ 3. Data pipeline + AI baseline (Tuần 3–4) | Hoàn thiện preprocessing, split train/valid/test, metadata và leakage audit | Khi có split đã duyệt, huấn luyện RF/XGBoost; sau đó FeedForward; Isolation Forest là nhánh thử nghiệm riêng | Tiếp tục API, alert rule, database và dashboard bằng mock event | **Song song có điều kiện** | AI không train kết luận chính thức trước khi nhận split/schema đã duyệt; APP vẫn không phụ thuộc AI |
| GĐ 4. Tích hợp model (Tuần 5–6) | Đóng gói transformer, feature order, label mapping; hỗ trợ kiểm tra input | Đóng gói predictor, model version, output contract, metrics | Thay mock predictor bằng model thật; nối API → inference → DB → UI | **Có phần song song, có phần phải nối tiếp** | Chỉ tích hợp khi preprocessor + predictor cùng tuân thủ contract; đổi schema phải báo cả nhóm |
| GĐ 5. Kiểm thử hệ thống (Tuần 7) | Kiểm tra input lỗi, dữ liệu lệch schema, tái lập split | Phân tích false positive/negative, class-wise metrics, latency | Integration tests, lỗi API/DB/UI, kiểm tra event history | **Cả 3 kiểm thử song song**, sau đó chạy E2E chung | Dùng cùng model artifact, config và test fixture đã version hóa |
| GĐ 6. Chốt và demo (Tuần 8) | Chốt tài liệu dataset, preprocessing và giới hạn | Chốt kết quả thực nghiệm, bảng so sánh và giải thích AI | Chốt README, cách cài, demo flow và đóng gói ứng dụng | **Làm song song**, cuối tuần tổng duyệt chung | Chỉ đưa số liệu đã chạy thật; không ghi mock result thành kết quả thực nghiệm |

## 3. Bảng việc nào làm chung, việc nào không nên làm chung?

| Công việc | Cách làm | Lý do |
|---|---|---|
| Chốt schema feature, label mapping và prediction contract | **Cả 3 cùng họp/chốt**; Hoàng Phúc ghi schema, Quốc Đạt xác nhận input AI, Tiến Đạt xác nhận output app | Đây là ranh giới kết nối giữa ba module |
| Khảo sát AWID3 và viết loader/cleaner | Hoàng Phúc sở hữu; Quốc Đạt review yêu cầu feature/label | Tránh hai người cùng sửa pipeline dữ liệu |
| Viết mô hình và training loop | Quốc Đạt sở hữu; Hoàng Phúc cung cấp dataset contract | Tránh sửa trùng code AI |
| Dashboard, API, DB, alert | Tiến Đạt sở hữu; Quốc Đạt review predictor interface | Tránh sửa trùng app |
| Viết test | Mỗi người viết test cho module của mình; cả 3 cùng viết/duyệt E2E test | Unit test độc lập, E2E cần tích hợp |
| Thay đổi file contract chung | Tạo PR riêng, thông báo cả nhóm, cả 3 review | Ngăn schema/API thay đổi âm thầm |
| Merge vào develop | Người sở hữu tạo PR; ít nhất 1 người khác review; thay đổi contract cần cả 3 đồng ý | Giảm xung đột và lỗi tích hợp |
| Demo cuối tuần | Cả 3 cùng tham gia, mỗi người demo phần mình | Phát hiện lỗi giao tiếp sớm |

## 4. Quyền sở hữu file — không sửa chồng chéo

| Đường dẫn | Người chịu trách nhiệm | Quy tắc |
|---|---|---|
| `src/data/**`, `data/**`, `configs/data/**`, `tests/data/**` | Hoàng Phúc | Thành viên khác chỉ góp ý qua PR |
| `src/models/**`, `src/training/**`, `src/evaluation/**`, `tests/models/**`, `docs/ai/**` | Quốc Đạt | Không tự thay đổi schema dữ liệu |
| `src/api/**`, `src/app/**`, `src/database/**`, `src/alerts/**`, `tests/api/**` | Tiến Đạt | Dùng mock cho tới khi predictor thật sẵn sàng |
| `docs/INTERFACE_CONTRACT.md`, `configs/shared/**`, `requirements.txt` | Đồng sở hữu | Báo cả nhóm; thay đổi phải được review trước khi merge |
| `README.md`, `docs/WORK_PLAN.md` | Tiến Đạt điều phối; cả nhóm góp nội dung | Tránh sửa đồng thời; thống nhất một PR tại một thời điểm |

## 5. Các cổng bàn giao bắt buộc (dependency gates)

| Gate | Người bàn giao | Bên nhận | Điều kiện đạt |
|---|---|---|---|
| G1 — Data schema ready | Hoàng Phúc | Quốc Đạt + Tiến Đạt | Tên cột/feature, dtype, label column và label mapping được xác minh trên AWID3 thực tế |
| G2 — Dataset split ready | Hoàng Phúc | Quốc Đạt | Train/Validation/Test manifest, seed, split strategy và preprocessing chỉ fit trên Train |
| G3 — Model interface ready | Quốc Đạt | Tiến Đạt | Hàm predict thống nhất, output schema, model metadata; không bịa confidence nếu model không hỗ trợ |
| G4 — App integration ready | Tiến Đạt | Cả nhóm | App nhận event/prediction, lưu DB, hiển thị lịch sử; phân biệt offline replay và live capture |
| G5 — Release ready | Cả 3 | Cả 3 | Unit + integration test đạt; kết quả đánh giá có thể tái lập; README/demo đã kiểm tra |

**Không vượt gate bằng lời nói.** Người bàn giao phải đính kèm PR, file schema/metadata, test log hoặc demo phù hợp.

## 6. Nhịp làm việc đề xuất

| Thời điểm | Việc cần làm | Người tham gia |
|---|---|---|
| Đầu tuần (Thứ 2) | Chọn task từ GitHub Issues, xác nhận người phụ trách và đầu ra | Cả 3 |
| Giữa tuần (Thứ 4) | Kiểm tra blocker, contract và thay đổi có thể ảnh hưởng module khác | Cả 3 |
| Cuối tuần (Thứ 6) | Review PR, merge phần độc lập vào develop, chạy integration test | Cả 3 |
| Sau merge | Demo ngắn, cập nhật Issue và kế hoạch tuần tiếp theo | Cả 3 |

Mỗi thành viên cập nhật Issue theo mẫu: **Done / Next / Blocked / PR link**.

## 7. Quy tắc tránh xung đột Git

- Trước khi bắt đầu task: `git fetch origin`, cập nhật branch cá nhân từ `develop`.
- Chỉ sửa các đường dẫn thuộc module được giao.
- Commit nhỏ, mô tả rõ; không gom thay đổi của người khác vào commit của mình.
- Nếu cần sửa file do người khác sở hữu: mở Issue/comment và chờ owner xác nhận.
- Không sửa cùng một file đồng thời. Nếu buộc phải sửa file chung, một người tạo PR trước; người còn lại chờ PR merge rồi cập nhật branch.
- Trước PR: chạy test liên quan, kiểm tra `git diff`, không commit dữ liệu/model lớn.
- Khi có conflict: người sở hữu file giải quyết cùng người tạo thay đổi; không tự chọn “accept theirs/ours” nếu chưa hiểu nội dung.

## 8. Quyết định kỹ thuật cần nhớ

- AWID3 là dữ liệu nghiên cứu offline. Huấn luyện/đánh giá AWID3 không tự chứng minh hệ thống đã giám sát Wi-Fi live được.
- Không mặc định số lượng feature hoặc số lớp theo repository tham khảo; xác minh từ đúng bản AWID3 nhóm tải về.
- Không fit preprocessing trên toàn bộ dataset; fit trên Train, transform Validation/Test.
- Isolation Forest là nhánh anomaly detection riêng; anomaly score không phải tên một loại tấn công.
- Dashboard có thể phát triển sớm bằng mock, nhưng phải ghi rõ mock và thay bằng model thật ở Giai đoạn 4.
