import asyncio
from aiohttp import web
import asyncpg
import os
from datetime import datetime

# PostgreSQL connection
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable must be set")

# Connection pool
pool = None

async def get_pool():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(DATABASE_URL, min_size=5, max_size=20)
    return pool

async def get_user_data(user_id: int):
    """Get user data with rank"""
    conn_pool = await get_pool()
    async with conn_pool.acquire() as conn:
        # Get user info
        user = await conn.fetchrow(
            "SELECT * FROM users WHERE telegram_id = $1", 
            user_id
        )
        
        if not user:
            return None
        
        # Get user rank
        rank_row = await conn.fetchrow("""
            SELECT COUNT(*) + 1 as rank 
            FROM users 
            WHERE points > $1
        """, user['points'])
        
        # Get referrals count
        ref_count = await conn.fetchval(
            "SELECT COUNT(*) FROM users WHERE referrer_id = $1",
            user_id
        )
        
        return {
            "telegram_id": user['telegram_id'],
            "username": user['username'],
            "full_name": user['full_name'],
            "points": user['points'],
            "rank": rank_row['rank'] if rank_row else None,
            "referrals": ref_count or 0,
            "joined_at": user['joined_at'].isoformat() if user['joined_at'] else None
        }

async def get_top_users_data(limit: int = 100):
    """Get top users list"""
    conn_pool = await get_pool()
    async with conn_pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT telegram_id, username, full_name, points FROM users ORDER BY points DESC LIMIT $1",
            limit
        )
        return [dict(row) for row in rows]

async def get_contest_data():
    """Get contest status and deadline"""
    conn_pool = await get_pool()
    async with conn_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT is_active, deadline FROM contest_settings WHERE id = 1"
        )
        
        if not row:
            return {"is_active": False, "deadline": None}
        
        return {
            "is_active": bool(row['is_active']),
            "deadline": row['deadline']
        }

async def get_total_users():
    """Get total users count"""
    conn_pool = await get_pool()
    async with conn_pool.acquire() as conn:
        count = await conn.fetchval("SELECT COUNT(*) FROM users")
        return count or 0

# CORS middleware
@web.middleware
async def cors_middleware(request, handler):
    if request.method == "OPTIONS":
        response = web.Response()
    else:
        response = await handler(request)
    
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# API Handlers
async def handle_user(request):
    """GET /api/user?user_id=123456789"""
    try:
        user_id = request.query.get('user_id')
        if not user_id:
            return web.json_response({'error': 'user_id required'}, status=400)
        
        user_id = int(user_id)
        
        # Get all data
        user = await get_user_data(user_id)
        top_users = await get_top_users_data(100)
        contest = await get_contest_data()
        total_users = await get_total_users()
        
        response_data = {
            "user": user,
            "top_users": top_users,
            "contest_active": contest['is_active'],
            "deadline": contest['deadline'],
            "total_users": total_users
        }
        
        return web.json_response(response_data)
    
    except ValueError:
        return web.json_response({'error': 'Invalid user_id'}, status=400)
    except Exception as e:
        print(f"Error in handle_user: {e}")
        return web.json_response({'error': 'Internal server error'}, status=500)

async def handle_index(request):
    """GET / - Serve index.html"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return web.Response(text=html_content, content_type='text/html')
    except FileNotFoundError:
        return web.Response(text='index.html not found', status=404)
    """GET /health - Health check endpoint"""
    try:
        conn_pool = await get_pool()
        async with conn_pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        
        return web.json_response({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return web.json_response({
            'status': 'unhealthy',
            'error': str(e)
        }, status=503)

async def on_startup(app):
    """Initialize database connection pool on startup"""
    print("Starting web server...")
    await get_pool()
    print("Database connection pool initialized")

async def on_cleanup(app):
    """Close database connection pool on shutdown"""
    global pool
    if pool:
        await pool.close()
        print("Database connection pool closed")

def create_app():
    """Create and configure the aiohttp application"""
    app = web.Application(middlewares=[cors_middleware])
    
    # Add routes
    app.router.add_get('/', handle_index)
    app.router.add_get('/api/user', handle_user)
    app.router.add_get('/health', handle_health)
    
    # Add startup/cleanup handlers
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 8080))
    print(f"Starting server on port {port}")
    web.run_app(app, host='0.0.0.0', port=port)
