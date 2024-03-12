import csv
import psycopg2
from psycopg2 import Error

# Thông tin kết nối PostgreSQL
db_config = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "postgres",
}

# Đường dẫn đến tệp CSV
csv_file_path = "test.csv"


def create_table(cursor, header):
    try:
        # Tạo câu lệnh CREATE TABLE dựa trên header của CSV
        columns = [f"{col} TEXT" for col in header]
        create_table_query = f"CREATE TABLE IF NOT EXISTS test ({', '.join(columns)});"
        cursor.execute(create_table_query)
        print("Bảng 'test' đã được tạo hoặc đã tồn tại")

    except (Exception, Error) as error:
        print("Lỗi khi tạo bảng 'test':", error)


def load_data_from_csv(csv_file, conn):
    try:
        cursor = conn.cursor()

        # Đọc header của tệp CSV để xác định cấu trúc bảng
        with open(csv_file, "r") as file:
            reader = csv.reader(file)
            header = next(reader)

        # Tạo bảng 'test' nếu chưa tồn tại
        create_table(cursor, header)
        print("Bảng 'test' đã được tạo hoặc đã tồn tại")

        # Đọc dữ liệu từ tệp CSV và chèn vào cơ sở dữ liệu
        with open(csv_file, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Bỏ qua dòng tiêu đề nếu có

            # Get all rows from the CSV file
            rows = [tuple(row) for row in reader]

            # Điều chỉnh câu lệnh INSERT tùy theo cấu trúc của bảng trong cơ sở dữ liệu
            insert_query = (
                f"INSERT INTO test VALUES ({', '.join(['%s'] * len(header))})"
            )

            # Execute the INSERT statement with executemany
            cursor.executemany(insert_query, rows)

        conn.commit()
        print(
            f"Dữ liệu đã được tải thành công từ CSV vào bảng 'test' trong PostgreSQL ({len(rows)} rows)"
        )

    except (Exception, Error) as error:
        print("Lỗi khi tải dữ liệu từ CSV vào bảng 'test' trong PostgreSQL:", error)

    finally:
        if conn:
            cursor.close()


try:
    # Kết nối đến cơ sở dữ liệu PostgreSQL
    connection = psycopg2.connect(**db_config)

    # Gọi hàm để tải dữ liệu từ CSV vào bảng 'test' trong PostgreSQL
    load_data_from_csv(csv_file_path, connection)

except (Exception, Error) as error:
    print("Lỗi kết nối tới PostgreSQL:", error)

finally:
    if connection:
        connection.close()
