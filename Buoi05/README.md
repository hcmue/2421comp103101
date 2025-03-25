# FastAPI

`https://fastapi.tiangolo.com/`

## Tạo môi trường ảo (virtual environment)

`$ python -m venv venv`

## Di chuyển vào thư mục chứa môi trường [option]

`$ cd proj`

## Active môi trường ảo

`$ venv\Scripts\activate`

(Inactive) `$ deactivate`

## Cài thư viện FastAPI

`pip install "fastapi[standard]"`

## Export packages đã dùng trong project

`pip freeze > requirements.txt`

## Dựng lại môi trường

    - Tạo môi trường ảo (chú ý version python mà proj yêu cầu)
    - Activate môi trường ảo
    - Dựng lại packages:
        `pip install -r requirements.txt`

# Chạy ứng dụng fastAPI.

Giả sử file chính là main.py
`fastapi dev main.py`
