# Panduan cara menjalankan Django Project pada Local Development Environment

Pastikan bahwa `Python`, `pip`, dan `postgresql` sudah ter-*install* pada komputer kalian.

1. Clone repository

    ```shell
    git clone https://github.com/co-bersih/co-bersih-backend.git
    ```

2. Buat virtual environment

    ```shell
    python -m venv env
    ```

3. Aktifkan virtual environment

    ```shell
    env\Scripts\activate
    ```

    > Note: Perintah di atas dijalankan pada sistem operasi Windows

4. Install semua *dependencies*

    ```shell
    pip install -r requirements.txt
    ```

5. Masukkan `.env` file pada folder project `cobersih` (see Discord).

    `DB_USER` dan `DB_PASSWORD` dapat Anda sesuaikan dengan `username` dan `password` akun postgres Anda. Selain itu, variabel yang berkaitan dengan cloudinary dapat disesauikan pada saat produksi.

    > :memo: Note: Perhatikan bahwa pada **production enviroment** `SECRET_KEY` harus di-*generate* [^1] dan `DEBUG` di-*set* dengan `False`.

6. Buat database `cobersih` pada `postgresql`.

    ```postgresql
    CREATE DATABASE cobersih;
    ```

7. Jalankan migrasi

    ```shell
    python manage.py makemigrations
    python manage.py migrate
    ```

8. Jalankan development server

    ```shell
    python manage.py runserver
    ```

[^1]: [How to Generate a Secret Key in Django](https://codinggear.blog/django-generate-secret-key/#:~:text=Secret%20Key%20Safe-,What%20is%20a%20Django%20secret%20key%3F,of%20our%20hashes%20and%20tokens.)
