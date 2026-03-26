# brand-social-crawler - 실제 진입점 및 컴포넌트

**분석 일시**: 2026-03-26

## 실제 진입점

### Crawler (Python)
- **`crawler/src/main.py`** — `python -m src.main` (Dockerfile CMD)
  - `run_all()` 즉시 1회 실행 → `schedule.every(INTERVAL).seconds.do(run_all)` 루프
  - `CRAWL_INTERVAL_SEC` 환경변수로 주기 조절 (기본 3600초)

### Backend (Spring Boot)
- **`CrawlerApplication.java`** — `@SpringBootApplication` 메인 클래스
- **`PostController`** — `GET /api/posts`, `GET /api/posts/{id}`
  - `?platform=instagram` 쿼리 필터 지원
  - `Pageable` 서버사이드 페이징 (기본 size=20, sort=crawledAt DESC)

### Frontend (React + TypeScript)
- **`frontend/src/main.tsx`** — `ReactDOM.createRoot` + `BrowserRouter` + `ThemeProvider`
- **`App.tsx`** — `AppBar` + `Routes`
- **`pages/PostListPage.tsx`** — MUI DataGrid, 플랫폼 Select 필터 (완전 타입화)

## 실제 컴포넌트 상세

### Crawler 컴포넌트
```
crawler/src/
├── db.py         → SQLAlchemy engine (mysql+pymysql://{env변수})
│                   SessionLocal = sessionmaker(bind=engine)
├── models.py     → Brand (brand_id, brand_name, platform, account_handle)
│                   Post  (post_id, brand_id, platform, external_post_id, ...)
├── crawler.py    → _fetch_html(url)       : Playwright headless 렌더링
│                   _parse_posts(html, ...) : BeautifulSoup 파싱
│                   _upsert_posts(rows)     : 신규만 INSERT
│                   insert_dummy_posts()    : 개발용 더미 Insert (현재 활성)
│                   run_all()              : 크롤링 실행 진입점
└── main.py       → schedule 루프 + 즉시 1회 실행
```

### Backend 컴포넌트
```
domain/entity/Post.java         → @Entity, @JdbcTypeCode(JSON) for media_urls/hashtags
domain/repository/PostRepository → JpaRepository + findByPlatform, findByBrandId
api/dto/PostResponse.java        → static from(Post) 팩토리 메서드
api/controller/PostController    → @CrossOrigin, @RequestParam platform, Pageable
```

### Frontend 컴포넌트
```
types/post.ts         → Post, PageResponse<T>, FetchPostsParams 인터페이스
api/posts.ts          → axios('/api').get<PageResponse<Post>>('/posts', { params })
pages/PostListPage    → useEffect [platform, page, pageSize]
                         → GridColDef<Row>, GridRenderCellParams 타입 적용
                         → SelectChangeEvent<Platform> 핸들러
```

## nginx 라우팅
```nginx
location /          → try_files (SPA React Router)
location /api/      → resolver 127.0.0.11; set $upstream http://backend:8080; proxy_pass $upstream
```
※ 동적 resolve: nginx 시작 시 backend 미기동 상태여도 크래시하지 않음

## Vite 개발 서버 프록시
```ts
proxy: { '/api': { target: VITE_API_BASE_URL || 'http://localhost:8080' } }
```
