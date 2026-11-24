# DATA-02 Báo cáo chất lượng AWID3

**Trạng thái kiểm tra thực tế: BLOCKED.** Chưa có kiểm kê AWID3 để làm đầu vào. Bộ test dùng CSV tổng hợp và không cung cấp số liệu AWID3.

```text
python -m src.data.cli profile --dataset-path <thu-muc-csv> --chunk-size 4096 --source AWID3-CSV --version <dinh-danh-goi> --output <bao-cao-moi.json>
```

| Hạng mục | Phép đo | AWID3 thực tế |
| --- | --- | --- |
| Kiểu quan sát | Numeric, mixed, categorical, string, missing. Báo khác biệt theo tên cột giữa tệp. Text có tối đa 50 giá trị phân biệt được mô tả là categorical. | Chưa đo |
| Missing | Chuỗi rỗng, toàn khoảng trắng, token NaN/NULL/NA/N/A/<NA>, số NaN literal và tỷ lệ trên bản ghi hợp lệ | Chưa đo |
| Duplicate | Số bản ghi dư trong từng tệp. Đếm số bản ghi của mỗi tệp có bản trùng ở tệp khác cùng tập tên cột, kể cả khi thứ tự khác. | Chưa đo |
| Chất lượng feature | Giá trị hữu hạn, lỗi chuyển số trong cột có tín hiệu numeric, cột hằng theo giá trị hiện diện, gần hằng từ 99%, và high cardinality từ 50 giá trị phân biệt chiếm ít nhất 95% giá trị hiện diện | Chưa đo |
| Nhãn | Ứng viên theo tên, hoặc truyền `--label-column` nhiều lần. Báo nhãn nguyên văn, tần suất, số thiếu và tỷ số lớp lớn nhất/nhỏ nhất theo tệp và tổng hợp theo tên cột. | Chưa xác minh tên cột hay phân bố |
| Hiệu năng | Thời gian từng tệp và toàn báo cáo, lỗi đọc, thống kê theo khối | Chưa đo trên dữ liệu thật |

So trùng dựa trên giá trị CSV nguyên văn, kể cả khoảng trắng, sau khi ghép cột theo tên. Không so hàng giữa các schema có tập tên cột khác nhau. Cờ định danh dựa trên tên trường và cần review. Giá trị text trong cột mixed là ứng viên lỗi kiểu, chưa đủ để kết luận sai dữ liệu. Nhãn, thiếu dữ liệu và gần hằng là phép đo mô tả, chưa quyết định cách làm sạch.

Profiler dùng SQLite tạm cho đếm chính xác, có thể cần nhiều dung lượng đĩa vì lưu giá trị để so khớp. Dùng `--scratch-dir` trỏ tới thư mục local đủ dung lượng. Bộ nhớ tăng theo kích thước khối và kích thước đầu ra tần suất nhãn. Phép đo không điền dữ liệu, xoá duplicate, mã hoá nhãn, chọn feature hay tạo split. Báo cáo có lỗi đọc hoặc sai độ rộng chỉ phản ánh phần được đọc hợp lệ.
