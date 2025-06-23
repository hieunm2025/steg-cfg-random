## Hướng dẫn Thực Hành Lab Steganography với Ngữ Pháp Phi Ngữ Cảnh và Thuật Toán Ngẫu Nhiên

### 1. Khởi động Lab
```bash
labtainer -r steg-cfg-random
```
Hệ thống tạo 2 container:
- **encoder**: Chứa script nhúng tin (`encoder.py`) và ảnh mẫu (`sample.bmp`)
- **decoder**: Chứa script trích xuất tin (`decoder.py`)

### 2. Quy trình Giấu Tin
**Bước 1: Tạo thông điệp bí mật**
```bash
echo "Nội dung bí mật" > secret.txt
cat secret.txt
```

**Bước 2: Nhúng tin vào ảnh**
```bash
./encoder.py -i images/sample.bmp -o stego_image.bmp -t encoded_text.txt -d "$(cat secret.txt)"
```
Kết quả:
- Ảnh đã giấu tin: `stego_image.bmp`
- Văn bản mã hóa tọa độ: `encoded_text.txt`

**Bước 3: Chuyển files sang container decoder**
Trong encoder:
```bash
nc -w 3 decoder 9000  received_stego.bmp
nc -l -p 9001 > received_text.txt
```

**Bước 4: Trích xuất thông điệp**
```bash
./decoder.py -i received_stego.bmp -t received_text.txt
```
Kết quả hiển thị thông điệp gốc.

### 3. Kiểm tra kết quả
```bash
checkwork
```

### 4. Thử nghiệm với thông điệp khác
1. Tạo thông điệp mới:
```bash
echo "Thông điệp mới" > secret2.txt
```
2. Lặp lại từ Bước 2 với tên file mới.

### Phụ lục: Lệnh Nhanh
**Encoder:**
```bash
echo "Thông điệp" > secret.txt
./encoder.py -i images/sample.bmp -o stego.bmp -t encoded.txt -d "$(cat secret.txt)"
nc -w 3 decoder 9000 < stego.bmp
```

**Decoder:**
```bash
./decoder.py -i received_stego.bmp -t received_text.txt
```
