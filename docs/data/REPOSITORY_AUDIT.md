# Kiểm tra repository Wifi-AI Secure

Kiểm tra ngày 24/11/2026 trên workspace DATA sau khi fetch `origin`.

| Nhánh | SHA tại thời điểm kiểm tra | Nội dung |
| --- | --- | --- |
| `main` | `fb735f8` | README gốc |
| `develop` | `f9e3a47` | README, kế hoạch nhóm, hợp đồng và ma trận theo Wave |
| `feature/data-pipeline` | `f069ec2` trước đồng bộ | Tài liệu DATA-00 và README module. Survey có chỉnh sửa local từ lần đối chiếu repo mẫu. |
| `feature/ai-models` | `7ac8a9a` | README khung AI |
| `feature/dashboard` | `65930ff` | FastAPI, Streamlit, test smoke, tài liệu APP-00, requirements riêng và đề xuất Git ignore |

Merge `4e4abb5` đưa `develop` vào nhánh DATA mà không có conflict. Khảo sát DATA-00 và phần đối chiếu local được giữ lại. [PR #4](https://github.com/hphuc032/Wifi-AI-Secure/pull/4) là PR DATA đang mở. [PR #5](https://github.com/hphuc032/Wifi-AI-Secure/pull/5) là PR APP-00 đang mở, có kiểm thử API/dashboard và chưa tích hợp AWID3.

| Khu vực | Owner và kết quả rà soát |
| --- | --- |
| `src/data`, `data`, `configs/data`, `tests/data`, `docs/data` | Hoàng Phúc. Thêm CLI, kiểm kê, profiling, test và báo cáo. Cấu hình qua CLI nên chưa cần tạo thư mục config rỗng. |
| `src/models`, `src/training`, `src/evaluation` | Quốc Đạt. Pipeline huấn luyện và tích hợp model thuộc các Wave sau. |
| `src/app`, `src/api`, `src/database`, `src/alerts` | Tiến Đạt. APP-00 còn trên PR #5. |
| Hợp đồng, dependency và cấu hình chung | Cả nhóm. README hiện đề cập `requirements.txt` nhưng file chưa có trên DATA/`develop`. PR #5 có `requirements-app.txt` riêng. DATA dùng thư viện chuẩn Python 3.11+, pytest chỉ dùng cho test. Máy kiểm thử hiện có Python 3.14. |

Không phát hiện tệp cần xoá trong phạm vi DATA. Kế hoạch 8 tuần và ma trận theo Wave mô tả các khía cạnh phối hợp khác nhau. README cấp repo và README DATA có phạm vi riêng. Ma trận có chỗ gọi `docs/WAVE_DEPENDENCY_PLAN.md` trong khi tệp đang được theo dõi là `docs/PARALLEL_WORK_MATRIX.md`. Đề nghị owner tài liệu thống nhất tên đường dẫn.

**Phối hợp với APP.** Dùng một `.gitignore` chung qua PR #5. Bản APP hiện có quy tắc cache, venv, database và secrets. Đề xuất thêm phạm vi `/data/raw/`, `/data/processed/`, `/data/external/` và các vị trí model artifacts sau khi thống nhất với AI. Trước khi quy tắc được tích hợp, giữ dữ liệu thật ngoài worktree và truyền `--dataset-path`. Thống nhất cách README chung hướng dẫn cài dependency theo từng module.

**Phối hợp với AI.** Sau khi nhận AWID3, xác minh header, nhãn, nguồn capture và phiên bản dữ liệu rồi review schema trước G1. Giữ nguyên hợp đồng hiện hành. Công cụ chỉ quan sát dữ liệu, chưa thực hiện preprocessing, feature selection hoặc split.
