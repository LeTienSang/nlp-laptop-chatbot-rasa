# NLP Laptop Chatbot - Rasa Framework

Chatbot hỗ trợ khách hàng mua laptop bằng tiếng Việt, sử dụng **Rasa 3.x Framework**.

## Tính năng

- **Trò chuyện tự nhiên** bằng tiếng Việt
- **Tư vấn giá** và tầm giá laptop
- **Hỏi cấu hình** (CPU, RAM, GPU, màn hình, ...)
- **So sánh laptop** giữa các dòng máy
- **Gợi ý theo nhu cầu** (gaming, lập trình, học tập, văn phòng, ...)
- **Thông tin mua hàng** (vận chuyển, thanh toán, bảo hành, ...)
- **Form tư vấn thông minh** (giá + nhu cầu) tự động gợi ý


## Cài đặt & Chạy

### 1. Tạo môi trường ảo

```bash
python -m venv rasa_env
# Windows
rasa_env\Scripts\activate
# macOS/Linux
source rasa_env/bin/activate
```

### 2. Cài đặt Rasa

```bash
pip install rasa rasa-sdk
```

### 3. Huấn luyện model

```bash
rasa train
```

### 4. Chạy action server (terminal riêng)

```bash
rasa run actions
```

### 5. Khởi động chatbot (terminal khác)

```bash
# Chat trong terminal
rasa shell

# Hoặc chạy REST API (mặc định: http://localhost:5005)
rasa run
```