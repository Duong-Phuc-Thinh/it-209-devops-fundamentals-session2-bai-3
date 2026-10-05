# Bài 3: Bảo mật tài nguyên bằng HTTP Basic Authentication

Thư mục này chứa cấu hình và tập lệnh tự động để cài đặt HTTP Basic Authentication cho thư mục quản trị `/admin` trên Nginx Web Server.

## Cấu trúc thư mục
- `nginx.conf`: File cấu hình Server Block mẫu cho Nginx chứa thiết lập xác thực cho `/admin`.
- `.htpasswd`: File chứa thông tin tài khoản mẫu đã được mã hóa (User: `admin_user`).
- `setup.py`: Script Python tự động cài đặt công cụ cần thiết, cấu hình và khởi chạy lại Nginx.

## Chức năng đã thực hiện
1. **Cài đặt công cụ băm mật khẩu:** Sử dụng `apache2-utils` để lấy tiện ích `htpasswd` tạo tài khoản và băm mật khẩu an toàn.
2. **Tạo tài khoản admin_user:** Lưu thông tin tài khoản đã băm tại vị trí an toàn ngoài Document Root (`/etc/nginx/.htpasswd`).
3. **Cấu hình Nginx:** Tạo một block `location /admin` tích hợp thuộc tính `auth_basic` và `auth_basic_user_file`.

## Hướng dẫn triển khai

### Cách 1: Triển khai thủ công
1. Cài đặt công cụ băm mật khẩu:
   ```bash
   sudo apt update && sudo apt install apache2-utils -y
   ```
2. Tạo file mật khẩu ẩn `.htpasswd` cho tài khoản `admin_user`:
   ```bash
   sudo htpasswd -c /etc/nginx/.htpasswd admin_user
   ```
3. Sao chép nội dung cấu hình trong file `nginx.conf` của bài tập này vào file cấu hình Server Block của bạn (thường ở `/etc/nginx/sites-available/default`).
4. Kiểm tra cấu hình và khởi động lại Nginx:
   ```bash
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Cách 2: Chạy tự động bằng Python
Chạy file `setup.py` dưới quyền Root để hệ thống tự động hoá toàn bộ các bước cài đặt và cấu hình:
```bash
sudo python3 setup.py
```

## Kiểm tra kết quả

1. Truy cập không thông qua tài khoản mật khẩu (Phải trả về lỗi `401 Unauthorized`):
   ```bash
   curl -I http://localhost/admin
   ```
2. Truy cập với thông tin xác thực chính xác (Phải trả về trạng thái `200 OK`):
   ```bash
   curl -u admin_user:<PASSWORD> http://localhost/admin/
   ```