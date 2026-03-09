# Web Ilova - Railway Setup

## Loyiha tuzilishi

Bu web ilova 2 ta komponentdan iborat:
1. **Backend API** (`server.py`) - PostgreSQL dan ma'lumot oladi va JSON qaytaradi
2. **Frontend** (`index.html`) - Telegram Mini App interfeysi

## Railway da Deploy qilish

### 1. PostgreSQL Database
Agar hali yaratmagan bo'lsangiz:
- Railway dashboard → **New** → **Database** → **PostgreSQL**

### 2. Web Service Environment Variables

```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
PORT=8080
```

**Muhim:** 
- `DATABASE_URL` bot service bilan bir xil PostgreSQL ga reference qilishi kerak
- `PORT` Railway avtomatik beradi, lekin 8080 default

### 3. Start Command

Railway da web service uchun start command:

```bash
python server.py
```

Yoki `Procfile` yarating:
```
web: python server.py
```

### 4. API Endpoints

Backend server quyidagi endpoint larni taqdim etadi:

- `GET /api/user?user_id={telegram_id}` - Foydalanuvchi ma'lumotlari
- `GET /health` - Server health check
- `GET /` - Server status

#### Response Format (GET /api/user):

```json
{
  "user": {
    "telegram_id": 123456789,
    "username": "john_doe",
    "full_name": "John Doe",
    "points": 150,
    "rank": 5,
    "referrals": 10,
    "joined_at": "2026-03-09T10:00:00"
  },
  "top_users": [
    {
      "telegram_id": 987654321,
      "username": "top_user",
      "full_name": "Top User",
      "points": 500
    }
  ],
  "contest_active": true,
  "deadline": "2026-03-15T23:59:59",
  "total_users": 1234
}
```

## Frontend (index.html)

### API URL ni o'zgartirish

`index.html` faylning 181-qatorida API URL ni yangilang:

```javascript
// Eski
const API_URL = 'https://konkurs-production-a818.up.railway.app/api';

// Yangi (sizning Railway service URL ingiz)
const API_URL = 'https://your-web-service.up.railway.app/api';
```

### Bot Username ni o'zgartirish

203-qatorda bot username ni yangilang:

```javascript
const BOT_USERNAME = 'your_bot_username';
```

## Telegram Mini App sozlamalari

1. **BotFather** ga `/newapp` yuboring
2. Bot tanlang
3. App nomi va tavsifini kiriting
4. Web App URL ni kiriting: `https://your-web-service.up.railway.app/`
5. GIF/Photo yuklang

## Arxitektura

```
┌─────────────────┐
│  Telegram Bot   │
│   (konkurs)     │
└────────┬────────┘
         │
         ├─── Telegram API
         │
         └─── PostgreSQL ◄─────┐
                                │
┌─────────────────┐             │
│   Web Service   │             │
│  (konkursweb)   │─────────────┘
└────────┬────────┘
         │
         ├─── server.py (Backend API)
         │
         └─── index.html (Frontend)
```

## Local Testing

### 1. PostgreSQL server ishga tushiring:

```bash
docker run -p 5432:5432 -e POSTGRES_PASSWORD=password postgres
```

### 2. Environment variables sozlang:

```bash
export DATABASE_URL="postgresql://postgres:password@localhost:5432/postgres"
export PORT=8080
```

### 3. Dependencies o'rnating:

```bash
pip install -r requirements.txt
```

### 4. Server ishga tushiring:

```bash
python server.py
```

### 5. Test qiling:

```bash
curl http://localhost:8080/health
curl "http://localhost:8080/api/user?user_id=123456789"
```

## CORS Settings

Server CORS ni qo'llab-quvvatlaydi, shuning uchun Telegram Mini App ishlaydi.

Headers:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type`

## Performance

- **Connection Pooling**: 5-20 connections
- **Async I/O**: aiohttp + asyncpg
- **CORS**: Pre-configured for Telegram Mini Apps

## Troubleshooting

### 500 Internal Server Error
- DATABASE_URL to'g'ri sozlanganligini tekshiring
- PostgreSQL ishga tushganligini tekshiring
- Logs ni ko'rib chiqing

### CORS Error
- Server to'g'ri CORS headers yuborayotganligini tekshiring
- Browser DevTools → Network → Response Headers

### Connection Refused
- Railway web service ishga tushganligini tekshiring
- PORT environment variable to'g'ri sozlanganligini tekshiring

## Production Checklist

- ✅ PostgreSQL database yaratilgan
- ✅ DATABASE_URL environment variable sozlangan
- ✅ Bot bilan bir xil database ga ulangan
- ✅ API URL index.html da to'g'ri
- ✅ Bot username to'g'ri
- ✅ Telegram Mini App BotFather da sozlangan
- ✅ Health check ishlayapti: `/health`
