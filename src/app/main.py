
import streamlit as st

st.set_page_config(
    page_title="Wifi-AI Secure",
    page_icon="🛡️",
    layout="wide",
)

st.sidebar.title("🛡️ Wifi-AI Secure")

page = st.sidebar.radio(
    "Điều hướng",
    [
        "Tổng quan",
        "AI Detection",
        "Model Evaluation",
        "Attack History",
    ],
)

st.sidebar.divider()
st.sidebar.caption("Version 0.1.0")
st.sidebar.caption("Development mode - APP-00")

st.title(page)

st.info(
    "Hệ thống đang trong giai đoạn phát triển. "
    "Chưa tích hợp mô hình AI thật."
)

if page == "Tổng quan":
    st.subheader("Tổng quan hệ thống")

    col1, col2, col3 = st.columns(3)

    col1.metric("Sự kiện đã phân tích", "—")
    col2.metric("Cảnh báo", "—")
    col3.metric("Mô hình AI", "Chưa tích hợp")

elif page == "AI Detection":
    st.subheader("Phát hiện tấn công Wi-Fi")
    st.caption("Chức năng đang được phát triển.")

elif page == "Model Evaluation":
    st.subheader("Đánh giá mô hình AI")
    st.caption("Chưa có kết quả thực nghiệm.")

elif page == "Attack History":
    st.subheader("Lịch sử phát hiện")
    st.caption("Chưa kết nối cơ sở dữ liệu.")
