FROM python:3.9-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép toàn bộ nội dung của dự án vào thư mục làm việc
COPY . .


# Cài đặt các thư viện Python từ file requirements.txt
# RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# CMD sẽ được chạy khi container khởi động
CMD ["python", "./main.py"]
