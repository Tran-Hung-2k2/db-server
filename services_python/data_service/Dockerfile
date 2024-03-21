FROM python:3.9-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép toàn bộ nội dung của dự án vào thư mục làm việc
COPY . .

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

# Cài đặt các thư viện Python từ file requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r services_python/data_service/requirements.txt

# Mở cổng 8080 trên container
EXPOSE 8080

# CMD sẽ được chạy khi container khởi động
CMD ["python", "./services_python/data_service/app/main.py"]
