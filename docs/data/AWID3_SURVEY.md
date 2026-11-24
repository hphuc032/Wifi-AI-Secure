# Khảo sát bộ dữ liệu AWID3

**DATA-00 · Wave 0.1 · Wifi-AI Secure · 23/11/2026**

**Phiên bản chọn cho dự án:** AWID3 (CSV) do University of the Aegean phân phối. Trang AWID xác nhận một yêu cầu tải đã được gửi. Ảnh xác nhận chưa cho biết gói được chọn. Workspace chưa có tệp để kiểm tra.

## 1. Giới thiệu AWID3

AWID3 (Aegean Wi-Fi Intrusion Dataset 3) là bộ dữ liệu nghiên cứu phục vụ thiết kế và đánh giá hệ thống phát hiện xâm nhập (IDS) cho mạng Wi-Fi doanh nghiệp. Efstratios Chatzoglou, Georgios Kambourakis và Constantinos Kolias công bố bộ dữ liệu trong IEEE Access năm 2021. [1][2]

## 2. Nguồn phát hành và thông tin phiên bản

| Mục | Kết quả khảo sát | Nguồn |
| --- | --- | --- |
| Đơn vị phân phối | Dự án AWID, Info-Sec-Lab, University of the Aegean | [1][3] |
| AWID3 (PCAP) | Bản capture gốc công bố năm 2021 | [1][2] |
| AWID3 (CSV) | Bản dữ liệu dạng bảng bổ sung, công bố tháng 11/2021. Đây là gói chọn cho DATA-01. | [3][4] |
| Đăng ký tải | Chọn **AWID3 (CSV)** trên biểu mẫu chính thức, cung cấp email hợp lệ của trường hoặc tổ chức và xác nhận qua email trong 48 giờ. Đơn vị phát hành gửi email riêng cho từng gói sau khi duyệt. | [3] |
| Giấy phép | Chưa tìm thấy giấy phép dataset hoặc điều khoản tái phân phối trên các trang đã kiểm tra. Cần đọc điều kiện trong thư duyệt và tài liệu đi kèm gói. | [1][3] |

AWID2 là bộ dữ liệu riêng trong cùng dự án. Cách chia F/R và thống kê của AWID2 nằm ngoài phạm vi khảo sát này. Chưa xác minh mã bản phát hành hoặc phiên bản archive mà nhóm sẽ nhận. [3][6]

## 3. Mục đích và phạm vi dataset

Nhóm tác giả thu thập lưu lượng trong một lab mô phỏng mạng doanh nghiệp với 16 thiết bị vật lý và máy ảo. Môi trường nghiên cứu dùng WPA2-Enterprise, xác thực IEEE 802.1X/EAP và Protected Management Frames (PMF). Dữ liệu bao gồm lưu lượng bình thường và các tình huống tấn công từ tầng MAC đến các tầng cao hơn. Dự án sẽ dùng CSV để đánh giá phân loại lưu lượng offline trước. [1][2][5]

## 4. Cấu trúc và định dạng dữ liệu

| Thành phần | Cách tổ chức theo công bố | Train/Test và cấu trúc thư mục |
| --- | --- | --- |
| AWID3 (PCAP) | Các tệp capture chứa frame mạng. Bảng III của bài báo gốc đối chiếu kịch bản với tệp capture, thời lượng và số frame. | Chưa xác minh cây thư mục, danh sách file hoặc split đi kèm gói cấp quyền. [1][2] |
| AWID3 (CSV) | Các tệp CSV chứa đặc trưng trích xuất từ capture và nhãn. Nghiên cứu của nhóm tác giả mô tả việc đọc nhiều tệp CSV và chọn một tập con theo kịch bản để thực nghiệm. | Chưa xác minh cách chia thư mục, số file, số dòng mỗi file, header từng tệp và việc gói có split Train/Test sẵn hay không. Split trong bài thực nghiệm thuộc phương pháp của nghiên cứu đó. [1][5] |

## 5. Thông tin feature

Nhà phát hành công bố **254 trường**, gồm **253 trường đặc trưng** và **1 trường nhãn**. Đây là mô tả AWID3-CSV ở cấp công bố. Số feature mô hình sẽ phụ thuộc vào schema được xác minh và lựa chọn sau này. [1][4]

| Nhóm trường | Ví dụ được bài nghiên cứu sử dụng | Kiểu cần kiểm tra trên CSV |
| --- | --- | --- |
| Frame và thông tin vô tuyến | `frame.len`, `radiotap.dbm_antsignal`, `wlan_radio.signal_dbm` | Trường độ dài và mức tín hiệu có ý nghĩa số. Kiểm tra giá trị thiếu, đơn vị và kiểu đọc thực tế. [5] |
| IEEE 802.11 | `wlan.duration`, `wlan.fc.ds`, `wlan_radio.phy` | Gồm trường đo thời lượng và trường mang mã phân loại. Kiểm tra cách biểu diễn trong tệp. [5] |
| Giao thức ngoài 802.11 | `ip.ttl`, `udp.length`, `arp.hw.type`, `ip.src`, `ip.dst` | Có trường mang ý nghĩa số, mã giao thức và định danh địa chỉ. Kiểm tra kiểu, giá trị đặc biệt và mức độ sẵn có theo capture. [5] |
| Nhãn | Một trường phục vụ gán nhãn theo công bố | Chưa xác minh tên cột, vị trí, kiểu đọc hoặc các giá trị nguyên văn. [1] |

Danh sách trên là ví dụ có nguồn. Cần lấy header đầy đủ, thứ tự cột và kiểu quan sát được trực tiếp từ gói CSV trước khi chốt hợp đồng schema. [7]

## 6. Thông tin label

| Nhóm | Kết quả khảo sát | Trạng thái |
| --- | --- | --- |
| Lưu lượng bình thường | Nghiên cứu của nhóm tác giả dùng nhãn `Normal` cho lớp bình thường trong thực nghiệm. | Đã xác nhận cách gọi trong bài báo. Cần kiểm tra chuỗi nguyên văn trong CSV. [5] |
| Kịch bản Wi-Fi | Trang phát hành mô tả các kịch bản như deauthentication, disassociation, (re)association, rogue AP, KRACK, Kr00k và evil twin. | Tên kịch bản theo tài liệu. Cần đối chiếu với giá trị nhãn thực tế. [1] |
| Kịch bản tầng cao hơn | Bài nghiên cứu mô tả sáu nhóm capture gồm SSH, botnet, malware, SQL injection, SSDP amplification và website spoofing. | Tên nhóm capture theo tài liệu. Cần kiểm tra cách gán nhãn trên từng tệp CSV. [5] |

Bài nghiên cứu mô tả 21 tình huống tấn công trong AWID3. Số tình huống, số capture và số giá trị nhãn duy nhất là các đại lượng riêng. Chưa chốt số lớp hay bảng ánh xạ nhãn cho dự án. Các lớp `Flooding` và `Other` trong bài *Best of Both Worlds* là cách gộp nhãn phục vụ thực nghiệm đó. [2][5]

## 7. Quy mô dữ liệu

| Đại lượng | Số liệu có thể sử dụng | Phạm vi |
| --- | --- | --- |
| Số mẫu được báo cáo | **13.645.068 mẫu**, khoảng **50%** toàn bộ dữ liệu theo bài nghiên cứu | Chỉ áp dụng cho tập con gồm sáu capture tầng ứng dụng trong bài. Chưa đếm tổng số dòng của gói AWID3-CSV. [5] |
| Số frame và dung lượng PCAP | Bảng III của bài báo gốc báo cáo số frame và dung lượng theo từng tệp capture | Chưa đo dung lượng archive phân phối hoặc dung lượng sau giải nén. [2] |
| Dung lượng AWID3-CSV | Chưa xác minh | DATA-01 ghi kích thước archive và tệp giải nén theo byte. |
| Phân bố nhãn | Bài nghiên cứu ghi nhận mất cân bằng trên tập con của họ | DATA-02 cần đếm theo nhãn và capture trên gói thực tế. [5] |

## 8. Khả năng sử dụng cho Wifi-AI Secure

| Tiêu chí | Đánh giá |
| --- | --- |
| Data format | CSV phù hợp cho khảo sát bằng Python. Có thể đọc theo khối để kiểm kê, đếm dòng và kiểm tra header. |
| Feature | Các trường trải từ thông tin vô tuyến, MAC đến giao thức tầng cao. Cần đo mức thiếu theo capture và xác định trường nào có thể quan sát khi suy luận. [1][5] |
| Labels | Có trường nhãn cho phân loại có giám sát. Cần xác nhận các giá trị trước khi quy định lớp đầu ra. [1] |
| Data volume | Hàng triệu mẫu trong tập con đã công bố cho thấy cần đo RAM và dung lượng đĩa trước khi nạp toàn bộ CSV. [5] |
| Class distribution | Có nguy cơ lớp hiếm. Cần báo cáo phân bố theo nhãn và capture trước khi chọn split, rồi dùng Macro F1 và Recall từng lớp khi đánh giá. [5][7] |
| Random Forest và XGBoost | Phù hợp về dạng dữ liệu bảng sau khi đầu vào được xác thực và chuyển thành ma trận số theo hợp đồng. Hiệu năng cần đo bằng thực nghiệm của nhóm. [7] |
| FeedForward | Khả thi với vector số có thứ tự ổn định và số chiều lấy từ schema. Bài nghiên cứu đã thử MLP trên các nhóm feature do họ lựa chọn. [5][7] |
| Isolation Forest | Có thể khảo sát sau khi xác nhận đủ mẫu bình thường và split phù hợp. Nếu triển khai, fit bằng mẫu bình thường của Train và chọn ngưỡng trên Validation. |
| Limitations | Kết quả offline chịu ảnh hưởng từ thiết bị, kịch bản và cách gán nhãn của lab. Thu thập thực tế còn phụ thuộc trường feature có thể quan sát được. [1][5] |

## 9. Hạn chế và rủi ro

- **Rò rỉ dữ liệu.** Các frame cùng capture có thể tương quan mạnh. Giữ định danh nguồn để khảo sát chia theo capture, phiên hoặc thời gian và kiểm tra độ phủ nhãn trước khi chọn split. Chỉ fit bộ biến đổi trên Train. [2][7]
- **Học dấu vết của lab.** IP, MAC và định danh thiết bị có thể gắn chặt với kịch bản. Rà soát các trường đó và khả năng quan sát của các trường tầng ứng dụng trước khi chốt schema suy luận. [1][5]
- **Khác biệt giữa offline và triển khai.** Các trường có mặt trong capture nghiên cứu có thể thiếu khi lưu lượng thực tế được mã hóa hoặc khi môi trường sử dụng cấu hình mạng khác. [1][5]
- **Dung lượng và chất lượng.** Kiểm tra giá trị trống, biểu diễn bất thường, cột hằng và bản ghi trùng theo tệp. Đo dung lượng trước khi chọn cách nạp dữ liệu. [5][8]

## 10. Đề xuất tổ chức dữ liệu

```text
data/
├── raw/
│   └── awid3/
├── processed/
│   └── awid3/
├── external/
└── README.md
```

| Đường dẫn | Mục đích |
| --- | --- |
| `data/raw/awid3/` | Lưu archive chính thức và bản giải nén cục bộ. Giữ nguyên nội dung gốc. |
| `data/processed/awid3/` | Lưu dữ liệu dẫn xuất ở giai đoạn sau, theo phiên bản dữ liệu và cấu hình xử lý. |
| `data/external/` | Lưu bộ dữ liệu ngoài AWID3 nếu nhóm phê duyệt sử dụng. Ghi rõ nguồn và điều kiện truy cập. |
| `data/README.md` | Tài liệu dự kiến về nguồn, gói được chọn, cách bố trí tệp và quy trình xác minh checksum. |

Giữ các tệp lớn trên ổ đĩa local hoặc kho nhóm có kiểm soát quyền theo điều khoản phát hành. Loại dữ liệu gốc, capture và dữ liệu dẫn xuất lớn khỏi Git. Dùng Git để lưu tài liệu, manifest, checksum SHA-256 và fixture tổng hợp nhỏ. Cây thư mục trên là đề xuất cho các bước sau. [7][8]

## 11. Nguồn tham khảo

### Đối chiếu với repo mẫu wifi-ids

Repo mẫu là nguồn tham khảo triển khai. Nguồn xác nhận cấu trúc gói AWID3 của nhóm vẫn là các tệp chính thức sau khi được cấp quyền.

| Điểm tham khảo | Cách áp dụng trong Wifi-AI Secure |
| --- | --- |
| [Đọc CSV theo khối và xuất thống kê](https://github.com/shahal-dev/wifi-ids/blob/main/README.md) | DATA-01/02 sẽ kiểm kê theo tệp, đọc theo khối để đếm dòng và nhãn, đồng thời lưu đường dẫn tương đối trong manifest để truy vết nguồn. Giữ thông tin thư mục để đối chiếu với nhãn trong tệp. |
| [Kiểm tra thiếu feature trong loader](https://github.com/shahal-dev/wifi-ids/blob/main/src/data/dataset.py) | Sau khi xác minh header, dùng danh sách feature có thứ tự từ schema của nhóm. Báo rõ file và cột thiếu hoặc thừa khi đầu vào sai hợp đồng. |
| [Cấu hình feature, nhãn và seed](https://github.com/shahal-dev/wifi-ids/blob/main/configs/config.yaml) | Dùng danh sách kịch bản của repo mẫu để đối chiếu khi kiểm kê. Lấy số chiều và ánh xạ lớp từ schema đã xác minh. README mẫu ghi cả 29 và 30 feature, còn config đặt 29 feature và 14 lớp. Các giá trị đó chỉ mô tả repo mẫu. |
| [Imputation và cân bằng lớp](https://github.com/shahal-dev/wifi-ids/blob/main/src/data/dataset.py) | Loader mẫu fit median imputer ngay trên dữ liệu được nạp khi gặp giá trị thiếu. Với Wifi-AI Secure, xác định split trước, fit bộ biến đổi một lần trên Train và dùng lại cho Validation/Test. Nếu cân bằng lớp, chỉ thực hiện trên Train. |

Đã xác minh [script tiền xử lý mẫu](https://github.com/shahal-dev/wifi-ids/blob/main/preprocess_script/awid3_preprocessor.py). Công cụ DATA áp dụng cách đọc theo khối, báo khác biệt header và phân nhóm trường bằng tên. Không nhập mã nguồn, danh sách lớp hoặc danh sách cột của repo mẫu.

### Nguồn công bố và tài liệu dự án

Các nguồn dưới đây được kiểm tra trong đợt khảo sát DATA-00. Nguồn [3] là biểu mẫu đăng ký hiện hành. Đường dẫn tải cũ trong mục *Data Availability Statement* của [5] trả về HTTP 404 tại thời điểm kiểm tra.

- [1] [AWID3 — trang mô tả chính thức](https://icsdweb.aegean.gr/awid/awid3)
- [2] [Bài báo gốc AWID3 — hồ sơ Joint Research Centre, DOI 10.1109/ACCESS.2021.3061609](https://publications.jrc.ec.europa.eu/repository/handle/JRC123693)
- [3] [Biểu mẫu yêu cầu tải dữ liệu chính thức](https://icsdweb.aegean.gr/awid/download)
- [4] [Blog AWID — thông báo phát hành AWID3-CSV ngày 01/11/2021](https://icsdweb.aegean.gr/awid/blog)
- [5] [Best of Both Worlds: Detecting Application Layer Attacks through 802.11 and Non-802.11 Features](https://www.mdpi.com/1424-8220/22/15/5633)
- [6] [Trang chủ dự án AWID — phân biệt các bộ dữ liệu](https://icsdweb.aegean.gr/awid/)
- [7] [Hợp đồng tích hợp Wifi-AI Secure](https://github.com/hphuc032/Wifi-AI-Secure/blob/develop/docs/INTERFACE_CONTRACT.md)
- [8] [Kế hoạch triển khai theo Wave](https://github.com/hphuc032/Wifi-AI-Secure/blob/develop/docs/PARALLEL_WORK_MATRIX.md)

## 12. Những thông tin chưa xác minh

| Việc tiếp theo | Bằng chứng cần thu thập | Mốc |
| --- | --- | --- |
| Đăng ký AWID3 (CSV) bằng email trường hoặc tổ chức | Thư duyệt, quyền truy cập và điều khoản đi kèm | Hoàng Phúc, trước DATA-01 |
| Kiểm kê gói được cấp | Tên và phiên bản archive nếu có, SHA-256, dung lượng nén và giải nén, cây thư mục, danh sách tệp và thông tin split sẵn nếu có | DATA-01 |
| Xác nhận schema và nhãn | Header và thứ tự cột theo tệp, kiểu dữ liệu, tên cột nhãn, nhãn bình thường nguyên văn, danh sách và số lớp quan sát được | DATA-01/02 |
| Đo chất lượng và quy mô | Số dòng từng file và toàn gói, phân bố lớp, giá trị thiếu, trùng lặp và metadata dùng để nhóm capture | DATA-02 |

[1]: https://icsdweb.aegean.gr/awid/awid3
[2]: https://publications.jrc.ec.europa.eu/repository/handle/JRC123693
[3]: https://icsdweb.aegean.gr/awid/download
[4]: https://icsdweb.aegean.gr/awid/blog
[5]: https://www.mdpi.com/1424-8220/22/15/5633
[6]: https://icsdweb.aegean.gr/awid/
[7]: https://github.com/hphuc032/Wifi-AI-Secure/blob/develop/docs/INTERFACE_CONTRACT.md
[8]: https://github.com/hphuc032/Wifi-AI-Secure/blob/develop/docs/PARALLEL_WORK_MATRIX.md
