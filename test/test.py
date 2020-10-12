from ocr_service import predict

file_path = "/app/test/billboard.jpg"

result = predict(file_path)

print(result)