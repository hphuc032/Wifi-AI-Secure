# DATA-01 Kiểm kê AWID3

**Trạng thái kiểm kê thực tế: BLOCKED.** Chưa tìm thấy AWID3 trong workspace. Ảnh trang AWID xác nhận yêu cầu đã gửi và chờ duyệt, chưa xác định được gói từ ảnh.

Từ thư mục gốc, chạy lệnh dưới đây với đường dẫn local đã cấp quyền. Nếu bỏ `--dataset-path`, công cụ dùng `data/raw/awid3`.

```text
python -m src.data.cli inventory --dataset-path <thu-muc-csv> --source AWID3-CSV --version <dinh-danh-goi> --output <manifest-moi.json>
```

| Nội dung | Công cụ xuất | AWID3 thực tế |
| --- | --- | --- |
| Tệp và dung lượng | Tên, thư mục tương đối, định dạng theo đuôi, bytes, số tệp và số CSV | Chưa đếm |
| Toàn vẹn | SHA-256 theo byte gốc và nhóm checksum trùng | Chưa tính |
| CSV | Encoding chọn theo BOM hoặc mặc định UTF-8, header theo thứ tự, số bản ghi hợp lệ, số dòng sai độ rộng và lỗi đọc | Chưa kiểm tra |
| Khác biệt schema | Nhóm header so khớp cả tên lẫn thứ tự. Phân nhóm sơ bộ theo tên trường. | Chưa xác minh |
| Nguồn và bản phát hành | Tham số metadata `--source` và `--version` do người vận hành cung cấp | Chờ gói chính thức |

CSV nhiều dòng trong dấu nháy được tính là một bản ghi. Với dấu nháy hỏng hoặc lỗi giải mã, công cụ báo lỗi và số đếm có thể chỉ là phần đã đọc. Có thể chỉ định `--encoding` sau khi xác minh encoding. Archive được ghi như tệp thường nếu có trong thư mục, không tự giải nén. Kho dữ liệu và báo cáo JSON chứa metadata nội bộ nên được giữ ngoài Git.
