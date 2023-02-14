# 🏫동국대학교 홍보대사 동감 캠퍼스 투어 신청 사이트

## Built With

- Team leader: [서희찬](https://github.com/seochan99)
- Team member: [안유성](https://github.com/ustar1210), [이영서](#)
## Installation

1. 터미널에 아래 내용 입력

```
git clone https://github.com/ustar1210/Donggam
```

2. 가상환경 켜기

```
pipenv shell
```

3. requirements.txt 내 패키지 설치

```
 pip install -r requirements.txt
```

6. donggam 폴더 내에서 donggam 폴더로 이동

```
cd donggam
```

7. 모델의 변경내용 DB 스키마에 적용하기 위해 마이그레이션 생성

```
python manage.py makemigrations
```

8. DB에 마이그레이션 적용

```
python manage.py migrate
```

9. 실행

```
python manage.py runserver
```

### 관리자 계정 생성 원할시 superuser를 생성하여 로그인
```
python manage.py createsuperuser
```
