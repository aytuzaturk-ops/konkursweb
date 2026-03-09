# Konkurs Web App

Telegram Mini App - Konkurs tizimi uchun web interfeys.

## 📋 Tarkibi

- **Backend API** (`server.py`) - aiohttp + asyncpg
- **Frontend** (`index.html`) - Telegram Mini App
- **Database** - PostgreSQL (bot bilan umumiy)

## 🚀 Xususiyatlari

### Backend (server.py)
- ✅ PostgreSQL connection pooling
- ✅ Async I/O (aiohttp + asyncpg)
- ✅ CORS support
- ✅ Health check endpoint
- ✅ User statistics API
- ✅ Top users leaderboard
- ✅ Contest status va deadline

### Frontend (index.html)
- ✅ Telegram Mini App integratsiyasi
- ✅ Real-time countdown timer
- ✅ Leaderboard (top 100)
- ✅ Referral system
- ✅ User statistics
- ✅ Responsive design
- ✅ Modern gradient UI

## 📦 O'rnatish

### Requirements

```bash
pip install -r requirements.txt
```

Dependencies:
- aiohttp==3.9.1
- asyncpg==0.29.0
- python-dotenv==1.0.0

### Environment Variables

`.env` fayl yarating:

```env
DATABASE_URL=postgresql://user:password@host:port/dbname
PORT=8080
```

## 🏃 Ishga tushirish

### Local

```bash
python server.py
```

Server `http://localhost:8080` da ishga tushadi.

### Railway

1. PostgreSQL database yarating
2. Web service yarating
3. Environment variables sozlang:
   ```
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   ```
4. Deploy qiling

Batafsil: [RAILWAY_SETUP.md](RAILWAY_SETUP.md)

## 🔌 API Endpoints

### GET /api/user?user_id={telegram_id}

Foydalanuvchi ma'lumotlarini qaytaradi.

**Response:**
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
  "top_users": [...],
  "contest_active": true,
  "deadline": "2026-03-15T23:59:59",
  "total_users": 1234
}
```

### GET /health

Server health check.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-03-09T10:00:00"
}
```

## 🎨 Frontend sozlamalari

`index.html` faylda quyidagilarni o'zgartiring:

### 1. API URL (181-qator)

```javascript
const API_URL = 'https://your-service.up.railway.app/api';
```

### 2. Bot Username (182-qator)

```javascript
const BOT_USERNAME = '@your_bot_username';
```

## 🔧 Telegram Mini App sozlash

1. BotFather ga `/newapp` yuboring
2. Botni tanlang
3. App ma'lumotlarini kiriting
4. Web App URL: `https://your-service.up.railway.app/`
5. Icon yuklang

## 🏗 Arxitektura

```
User (Telegram) 
    ↓
index.html (Frontend)
    ↓
server.py (API)
    ↓
PostgreSQL Database
    ↑
bot.py (Telegram Bot)
```

## 🔒 Security

- ✅ CORS configured
- ✅ Input validation
- ✅ Error handling
- ⚠️ Production da API authentication qo'shish tavsiya etiladi

## 📊 Performance

- **Connection Pool**: 5-20 connections
- **Async**: Non-blocking I/O
- **Response time**: < 100ms

## 🐛 Debugging

### Health Check

```bash
curl https://your-service.up.railway.app/health
```

### User Data

```bash
curl "https://your-service.up.railway.app/api/user?user_id=123456789"
```

### Logs

Railway dashboard → Service → Deployments → View Logs

## 📝 TODO

- [ ] API authentication (Telegram initData validation)
- [ ] Rate limiting
- [ ] Caching (Redis)
- [ ] Admin panel
- [ ] Analytics

## 📄 License

MIT

## 👨‍💻 Developer

Created for Konkurs Bot system - Telegram Mini App interface.
