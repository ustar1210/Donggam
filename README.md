# ๐ซ๋๊ตญ๋ํ๊ต ํ๋ณด๋์ฌ ๋๊ฐ ์บ ํผ์ค ํฌ์ด ์ ์ฒญ ์ฌ์ดํธ

## Built With

- Team leader: [์ํฌ์ฐฌ](https://github.com/seochan99)
- Team member: [์์ ์ฑ](https://github.com/ustar1210), [์ด์์](#)
## Installation

1. ํฐ๋ฏธ๋์ ์๋ ๋ด์ฉ ์๋ ฅ

```
git clone https://github.com/ustar1210/Donggam
```

2. ๊ฐ์ํ๊ฒฝ ์ผ๊ธฐ

```
pipenv shell
```

3. requirements.txt ๋ด ํจํค์ง ์ค์น

```
 pip install -r requirements.txt
```

6. donggam ํด๋ ๋ด์์ donggam ํด๋๋ก ์ด๋

```
cd donggam
```

7. ๋ชจ๋ธ์ ๋ณ๊ฒฝ๋ด์ฉ DB ์คํค๋ง์ ์ ์ฉํ๊ธฐ ์ํด ๋ง์ด๊ทธ๋ ์ด์ ์์ฑ

```
python manage.py makemigrations
```

8. DB์ ๋ง์ด๊ทธ๋ ์ด์ ์ ์ฉ

```
python manage.py migrate
```

9. ์คํ

```
python manage.py runserver
```

### ๊ด๋ฆฌ์ ๊ณ์  ์์ฑ ์ํ ์ superuser๋ฅผ ์์ฑํ์ฌ ๋ก๊ทธ์ธ
```
python manage.py createsuperuser
```
