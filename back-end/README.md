# 🛠️ Moksta Backend

> Moksta는 Flask 기반의 인스타그램 클론 프로젝트입니다. 이 백엔드 서버는 사용자 인증, 게시글, 댓글 기능을 제공합니다. 프론트엔드는 React를 사용하며, MySQL을 기반으로 데이터베이스를 구성했습니다.

---

## 📁 폴더 구조

```
moksta_project/  
├── app.py               # Flask 애플리케이션 진입점
├── config.py            # 환경설정 및 구성 변수
├── .env                 # 환경변수 파일 (DB 연결, 시크릿 키 등)
├── requirements.txt     # 필요 패키지 목록
├── extensions.py        # SQLAlchemy, JWT, Bcrypt 등 확장 모듈
├── models.py            # 모든 DB 모델을 한 파일에 통합 (순환 참조 문제 해결)
├── schemas/             # Marshmallow 스키마 (직렬화) - 그대로 유지
│   ├── user.py          # User 스키마
│   ├── bulletin_board.py # BulletinBoard 스키마
│   └── comment.py       # Comment 스키마
├── routes/              # API 라우트 핸들러
│   ├── auth.py          # 인증 관련 라우트
│   ├── board.py         # 게시판 관련 라우트
│   └── comment.py       # 댓글 관련 라우트
└── uploads/             # 업로드된 이미지 저장 디렉토리
```

---

## 🔧 기술 스택

* Python 3.x
* Flask
* MySQL
* SQLAlchemy
* Marshmallow (직렬화)
* JWT (인증)
* bcrypt (비밀번호 해싱)
* python-dotenv (환경변수)

---

## ⚙️ 로컬 개발 환경 설정

1. **레포 클론**
   ```bash
   git clone https://github.com/your-org/moksta-backend.gitcd moksta-backend
   ```
2. **가상환경 설정**
   ```bash
   python -m venv venvsource venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. **패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```
4. **.env 설정**
   ```env
   FLASK_ENV=developmentMYSQL_URI=mysql+pymysql://root:password@localhost/mokstarJWT_SECRET_KEY=your_real_secret_keyUPLOAD_FOLDER=uploads
   ```
5. **DB 초기화**
   ```bash
   flask db initflask db migrateflask db upgrade
   ```
6. **서버 실행**
   ```bash
   flask run
   ```

---

## 🧩 핵심 기능

* 회원가입 / 로그인(JWT 기반 인증)
* 게시글 작성 / 수정 / 삭제
* 댓글 및 대댓글 작성 / 삭제
* 파일 업로드 (이미지)
* 조회수 관리

---

## 📚 주요 모델

### User 모델

```python
# models/user.py
from extensions import db

class User(db.Model):
    __tablename__ = 'users'
  
    user_id = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    nickname = db.Column(db.String(255), nullable=False, unique=True)
  
    # 관계 설정
    posts = db.relationship('BulletinBoard', backref='author', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')
```

### BulletinBoard 모델

```python
# models/bulletin_board.py
from extensions import db
import datetime

class BulletinBoard(db.Model):
    __tablename__ = 'bulletin_boards'
  
    bill_id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    file_path = db.Column(db.String(255))
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
  
    # 관계 설정
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
```

### Comment 모델

```python
# models/comment.py
from extensions import db
import datetime

class Comment(db.Model):
    __tablename__ = 'comments'
  
    com_id = db.Column(db.String(255), primary_key=True)
    bill_id = db.Column(db.String(255), db.ForeignKey('bulletin_boards.bill_id'), nullable=False)
    user_id = db.Column(db.String(255), db.ForeignKey('users.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    parent_com_id = db.Column(db.String(255), db.ForeignKey('comments.com_id'), nullable=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
  
    # 대댓글 관계
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[com_id]), lazy=True)
```

---

## 🔒 보안 및 정책

* 비밀번호 해시 처리 (bcrypt)
* JWT 토큰 기반 로그인 유지
* CORS 허용 설정
* 환경변수 기반 설정 관리

---

## 📡 API 명세

### 🔐 Auth (인증)

#### ✅ 회원가입

* **URL** : `POST /auth/register`
* **설명** : 사용자 계정 생성
* **요청 바디** (`application/json`)
  ```json
  {  "user_id": "mokpo123",  "pw": "password123",  "email": "mokpo@mokpo.ac.kr",  "nickname": "사용자"}
  ```
* **응답**
  ```json
  {  "access_token": "JWT_TOKEN",  "user": {    "user_id": "mokpo123",    "nickname": "사용자"  }}
  ```

---

#### ✅ 로그인

* **URL** : `POST /auth/login`
* **설명** : JWT 로그인 처리
* **요청 바디**
  ```json
  {  "user_id": "mokpo123",  "pw": "password123"}
  ```
* **응답**
  ```json
  {  "access_token": "JWT_TOKEN",  "user": {    "user_id": "mokpo123",    "nickname": "사용자"  }}
  ```

---

### 📝 게시판

#### ✅ 게시글 작성

* **URL** : `POST /board`
* **인증** : JWT 필요
* **요청 타입** : `multipart/form-data`
* **필드** : `title`, `content`, `file` (선택)

---

#### ✅ 게시글 목록 조회

* **URL** : `GET /board?page=1`
* **응답 예시**
  ```json
  [  {    "bill_id": "B001",    "title": "첫 글!",    "nickname": "사용자",    "view_cnt": 10,    "created_at": "2025-04-13T12:00:00"  }]
  ```

---

#### ✅ 게시글 상세 조회

* **URL** : `GET /board/:bill_id`
* **설명** : 조회수 자동 증가
* **응답**
  ```json
  {  "bill_id": "B001",  "title": "첫 글!",  "content": "내용입니다",  "file_path": "/uploads/abc.jpg",  "view_cnt": 11,  "created_at": "2025-04-13T12:00:00",  "user": {    "user_id": "mokpo123",    "nickname": "사용자"  },  "comments": [ ... ]}
  ```

---

#### ✅ 게시글 수정

* **URL** : `PUT /board/:bill_id`
* **인증** : JWT 필요
* **요청 타입** : JSON 또는 `multipart/form-data`
* **예시**
  ```json
  {  "title": "수정된 제목",  "content": "수정된 내용"}
  ```

---

#### ✅ 게시글 삭제

* **URL** : `DELETE /board/:bill_id`
* **인증** : JWT 필요

---

### 💬 댓글

#### ✅ 댓글 작성

* **URL** : `POST /board/:bill_id/comments`
* **인증** : JWT 필요
* **요청 바디**
  ```json
  {  "content": "댓글입니다",  "pre_comid": null}
  ```

---

#### ✅ 댓글 목록 조회

* **URL** : `GET /board/:bill_id/comments`
* **응답 예시**
  ```json
  [  {    "com_id": "C001",    "content": "댓글입니다",    "nickname": "사용자",    "created_at": "2025-04-13T13:00:00",    "pre_comid": null  }]
  ```

---

#### ✅ 댓글 수정

* **URL** : `PUT /comments/:com_id`
* **인증** : JWT 필요
* **요청 바디**
  ```json
  {  "content": "수정된 댓글"}
  ```

---

#### ✅ 댓글 삭제

* **URL** : `DELETE /comments/:com_id`
* **인증** : JWT 필요
