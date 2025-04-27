# 🛠️ Moksta Backend

> Moksta는 Flask 기반의 인스타그램 클론 프로젝트입니다. 이 백엔드 서버는 사용자 인증, 게시글, 댓글 기능을 제공합니다. 프론트엔드는 React를 사용하며, MySQL을 기반으로 데이터베이스를 구성했습니다.

---

## 📁 폴더 구조

```
moksta_project/  
├── app.py               # 두둔 프로젝트 시~작
├── config.py            # 기본 설정
├── .env                 # 모두가 아는 그 것 22
├── requirements.txt     # 모두가 아는 그 것
├── models/              # DB 모델
├── routes/              # 라우트 함수
├── schemas/             # 직렬화/역직렬화를 위한
├── extensions.py        # DB JWT등의 익스텐션 보관
└── uploads/             # 업로드된 사진 파일 보관

```

---

## 🔧 기술 스택

* Python 3.x
* Flask
* MySQL
* SQLAlchemy
* Marshmallow (직렬화)
* JWT (인증)
* python-dotenv (환경변수)

---

## ⚙️ 로컬 개발 환경 설정

1. **레포 클론**
   ```bash
   git clone https://github.com/your-org/moksta-backend.git
   cd moksta-backend
   ```
2. **가상환경 설정**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. **패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```
4. **.env 설정**
   ```env
   FLASK_ENV=development
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=비밀번호
   DB_NAME=moksta
   SECRET_KEY=시크릿키
   ```
5. **DB 초기화**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
6. **서버 실행**
   ```bash
   flask run
   ```

---

## 🧩 핵심 기능

* 회원가입 / 로그인( )JWT 기반 인증 )
* 게시글 작성 / 수정 / 삭제
* 댓글 작성 / 삭제 / 부모 댓글 구조
* 사용자 인증 및 권한 체크

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
  {
    "user_id": "mokpo123",
    "pw": "password123",
    "email": "mokpo@mokpo.ac.kr",
    "nickname": "사용자"
  }
  ```
* **응답**
  ```json
  {
    "access_token": "JWT_TOKEN",
    "user": {
      "user_id": "mokpo123",
      "nickname": "사용자"
    }
  }
  ```

---

#### ✅ 로그인

* **URL** : `POST /auth/login`
* **설명** : JWT 로그인 처리
* **요청 바디**
  ```json
  {
    "user_id": "mokpo123",
    "pw": "password123"
  }
  ```
* **응답**
  ```json
  {
    "access_token": "JWT_TOKEN",
    "user": {
      "user_id": "mokpo123",
      "nickname": "사용자"
    }
  }
  ```

---

#### 🚧 비밀번호 재설정 *(예정)*

* **URL** : `POST /auth/reset-password`

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
  [
    {
      "bill_id": "B001",
      "title": "첫 글!",
      "nickname": "사용자",
      "view_cnt": 10,
      "created_at": "2025-04-13T12:00:00"
    }
  ]
  ```

---

#### ✅ 게시글 상세 조회

* **URL** : `GET /board/:bill_id`
* **설명** : 조회수 자동 증가
* **응답**
  ```json
  {
    "bill_id": "B001",
    "title": "첫 글!",
    "content": "내용입니다",
    "file_path": "/media/abc.jpg",
    "file_type": "image/jpeg",
    "view_cnt": 11,
    "created_at": "2025-04-13T12:00:00",
    "user": {
      "user_id": "mokpo123",
      "nickname": "사용자"
    },
    "comments": [ ... ]
  }
  ```

---

#### ✅ 게시글 수정

* **URL** : `PUT /board/:bill_id`
* **인증** : JWT 필요
* **요청 타입** : JSON 또는 `multipart/form-data`
* **예시**
  ```json
  {
    "title": "수정된 제목",
    "content": "수정된 내용"
  }
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
  {
    "content": "댓글입니다",
    "pre_comid": null
  }
  ```

---

#### ✅ 댓글 목록 조회

* **URL** : `GET /board/:bill_id/comments`
* **응답 예시**
  ```json
  [
    {
      "com_id": "C001",
      "content": "댓글입니다",
      "nickname": "사용자",
      "created_at": "2025-04-13T13:00:00",
      "pre_comid": null
    }
  ]
  ```

---

#### ✅ 댓글 수정

* **URL** : `PUT /comments/:com_id`
* **인증** : JWT 필요
* **요청 바디**
  ```json
  {
    "content": "수정된 댓글"
  }
  ```

---

#### ✅ 댓글 삭제

* **URL** : `DELETE /comments/:com_id`
* **인증** : JWT 필요

---
