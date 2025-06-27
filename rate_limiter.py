#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rate Limiting y Control de Costos para Developer Trial
Copyright (c) 2025 IntegridAI. All rights reserved.

This file is part of the Cognitive Memory System.
Licensed under MIT License for open source components.
"""
from datetime import datetime, timedelta
from typing import Dict, Optional
import json
import asyncio
from collections import defaultdict

class UsageTracker:
    """
    Tracker simple en memoria para prueba de developers
    En producción usar Redis
    """
    def __init__(self, free_tier_limit: int = 100):
        self.usage: Dict[str, int] = defaultdict(int)
        self.api_keys: Dict[str, Dict] = {}
        self.free_tier_limit = free_tier_limit
        self.reset_date = datetime.utcnow() + timedelta(days=30)
    
    async def register_developer(self, email: str) -> str:
        """Registrar developer y generar API key"""
        import secrets
        
        # Generar API key única
        api_key = f"mahout_dev_{secrets.token_urlsafe(16)}"
        
        self.api_keys[api_key] = {
            "email": email,
            "created_at": datetime.utcnow().isoformat(),
            "tier": "free_trial",
            "limit": self.free_tier_limit,
            "active": True
        }
        
        return api_key
    
    async def check_usage(self, api_key: str) -> Dict:
        """Verificar uso actual"""
        if api_key not in self.api_keys:
            return {"valid": False, "error": "Invalid API key"}
        
        if not self.api_keys[api_key]["active"]:
            return {"valid": False, "error": "API key deactivated"}
        
        current_usage = self.usage.get(api_key, 0)
        limit = self.api_keys[api_key]["limit"]
        
        return {
            "valid": True,
            "usage": current_usage,
            "limit": limit,
            "remaining": limit - current_usage,
            "reset_date": self.reset_date.isoformat()
        }
    
    async def increment_usage(self, api_key: str) -> bool:
        """Incrementar uso y verificar límite"""
        check = await self.check_usage(api_key)
        
        if not check["valid"]:
            return False
        
        if check["remaining"] <= 0:
            return False
        
        self.usage[api_key] += 1
        return True
    
    async def get_stats(self) -> Dict:
        """Estadísticas generales"""
        total_developers = len(self.api_keys)
        total_usage = sum(self.usage.values())
        
        # Estimar costos
        llm_cost_per_call = 0.01  # ~$0.01 por llamada promedio
        embedding_cost_per_call = 0.00013
        total_cost_estimate = total_usage * (llm_cost_per_call + embedding_cost_per_call)
        
        return {
            "total_developers": total_developers,
            "total_api_calls": total_usage,
            "estimated_cost_usd": round(total_cost_estimate, 2),
            "average_usage_per_dev": round(total_usage / max(total_developers, 1), 2),
            "reset_date": self.reset_date.isoformat()
        }

# Instancia global
usage_tracker = UsageTracker(free_tier_limit=100)

# Middleware para FastAPI
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

async def rate_limit_middleware(request: Request, call_next):
    """Middleware para controlar límites"""
    
    # Solo aplicar a rutas de API
    if request.url.path.startswith("/api/"):
        api_key = request.headers.get("X-API-Key")
        
        if not api_key:
            return JSONResponse(
                status_code=401,
                content={"error": "API key required"}
            )
        
        # Verificar uso
        usage_check = await usage_tracker.check_usage(api_key)
        
        if not usage_check["valid"]:
            return JSONResponse(
                status_code=403,
                content={"error": usage_check.get("error", "Invalid API key")}
            )
        
        if usage_check["remaining"] <= 0:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Free tier limit reached",
                    "limit": usage_check["limit"],
                    "reset_date": usage_check["reset_date"],
                    "upgrade_url": "https://mahout.ai/pricing"
                }
            )
        
        # Incrementar uso
        await usage_tracker.increment_usage(api_key)
        
        # Agregar headers de rate limit
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(usage_check["limit"])
        response.headers["X-RateLimit-Remaining"] = str(usage_check["remaining"] - 1)
        response.headers["X-RateLimit-Reset"] = usage_check["reset_date"]
        
        return response
    
    return await call_next(request)

# Endpoints para gestión de developers
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

developer_router = APIRouter(prefix="/dev", tags=["developers"])

class DeveloperSignup(BaseModel):
    email: EmailStr
    company: Optional[str] = None
    use_case: Optional[str] = None

@developer_router.post("/signup")
async def developer_signup(signup: DeveloperSignup):
    """Registro instantáneo para developers"""
    
    # Generar API key
    api_key = await usage_tracker.register_developer(signup.email)
    
    # TODO: Enviar email con API key y documentación
    
    return {
        "message": "Welcome to Cognitive Memory System!",
        "api_key": api_key,
        "docs_url": "https://docs.mahout.ai",
        "limits": {
            "free_tier": 100,
            "period": "30 days",
            "included": [
                "100 API calls",
                "MAHOUT™ optimization",
                "Community support"
            ]
        },
        "quick_start": {
            "python": """
# Install
pip install cognitive-memory-client

# Use
from cognitive_memory import Client
client = Client(api_key="{}")
response = client.chat("Hello!", session_id="test")
print(response)
            """.format(api_key),
            "curl": """
curl -X POST https://api.mahout.ai/v1/chat \\
  -H "X-API-Key: {}" \\
  -H "Content-Type: application/json" \\
  -d '{{"message": "Hello!", "session_id": "test"}}'
            """.format(api_key)
        }
    }

@developer_router.get("/usage")
async def check_developer_usage(api_key: str):
    """Verificar uso actual"""
    usage = await usage_tracker.check_usage(api_key)
    
    if not usage["valid"]:
        raise HTTPException(status_code=403, detail=usage.get("error"))
    
    return usage

@developer_router.get("/stats")
async def get_trial_stats(admin_key: str):
    """Stats generales (solo admin)"""
    # TODO: Verificar admin key
    if admin_key != "your_admin_key_here":
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    return await usage_tracker.get_stats()

# Landing page HTML para developers
DEVELOPER_LANDING_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Cognitive Memory System - Free Developer Trial</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #0f0f1e;
            color: white;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 4rem 2rem;
        }
        h1 {
            font-size: 3rem;
            background: linear-gradient(90deg, #00f5ff, #0099ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }
        .mahout-badge {
            display: inline-block;
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid rgba(0, 255, 136, 0.3);
            border-radius: 24px;
            padding: 0.5rem 1.5rem;
            color: #00ff88;
            font-weight: bold;
            margin-bottom: 2rem;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin: 3rem 0;
        }
        .feature {
            background: rgba(255, 255, 255, 0.05);
            padding: 2rem;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .signup-form {
            background: rgba(255, 255, 255, 0.05);
            padding: 2rem;
            border-radius: 16px;
            margin-top: 3rem;
        }
        input {
            width: 100%;
            padding: 1rem;
            margin: 0.5rem 0;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            color: white;
            font-size: 1rem;
        }
        button {
            width: 100%;
            padding: 1rem;
            background: linear-gradient(90deg, #00f5ff, #0099ff);
            border: none;
            border-radius: 8px;
            color: white;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            margin-top: 1rem;
        }
        .code {
            background: rgba(0, 0, 0, 0.5);
            padding: 1rem;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            margin: 1rem 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Free Developer Trial</h1>
        <div class="mahout-badge">Powered by MAHOUT™</div>
        
        <p style="font-size: 1.2rem; color: #a0a0a0;">
            Get 100 free API calls to test our Cognitive Memory System. 
            No credit card required.
        </p>

        <div class="features">
            <div class="feature">
                <h3>🚀 100 Free Calls</h3>
                <p>Full access to all features including MAHOUT™ optimization</p>
            </div>
            <div class="feature">
                <h3>📚 Complete SDK</h3>
                <p>Python, JavaScript, and REST API with examples</p>
            </div>
            <div class="feature">
                <h3>⚡ Instant Access</h3>
                <p>Get your API key immediately, start building in minutes</p>
            </div>
        </div>

        <div class="signup-form">
            <h2>Get Your Free API Key</h2>
            <form id="signupForm">
                <input type="email" id="email" placeholder="your@email.com" required>
                <input type="text" id="company" placeholder="Company (optional)">
                <textarea id="useCase" placeholder="What will you build? (optional)" 
                          style="height: 100px; resize: vertical;"></textarea>
                <button type="submit">Get API Key →</button>
            </form>
        </div>

        <div id="result" style="display: none; margin-top: 2rem;">
            <h2>🎉 Success!</h2>
            <p>Your API Key: <code id="apiKey" style="color: #00ff88;"></code></p>
            
            <h3>Quick Start</h3>
            <div class="code">
pip install cognitive-memory-client<br>
<br>
from cognitive_memory import Client<br>
client = Client(api_key="<span id="apiKey2"></span>")<br>
response = client.chat("Hello!", session_id="test")<br>
print(response)
            </div>
            
            <p>📖 Full documentation: <a href="https://docs.mahout.ai" style="color: #00f5ff;">docs.mahout.ai</a></p>
        </div>
    </div>

    <script>
        document.getElementById('signupForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const data = {
                email: document.getElementById('email').value,
                company: document.getElementById('company').value,
                use_case: document.getElementById('useCase').value
            };
            
            try {
                const response = await fetch('/dev/signup', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.api_key) {
                    document.getElementById('apiKey').textContent = result.api_key;
                    document.getElementById('apiKey2').textContent = result.api_key;
                    document.getElementById('signupForm').style.display = 'none';
                    document.getElementById('result').style.display = 'block';
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        });
    </script>
</body>
</html>
"""
