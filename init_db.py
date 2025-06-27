#!/usr/bin/env python3
"""
Initialize database tables for Cognitive Memory System
Run this script to create all necessary tables and extensions
"""
import asyncio
import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def init_database():
    print("Connecting to database...")
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        print("Creating pgvector extension...")
        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        print("✓ Extension created")
        
        print("Creating messages table...")
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                conversation_id UUID NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                embedding vector(1536),
                metadata JSONB,
                created_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        print("✓ Messages table created")
        
        print("Creating indexes...")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_msg_conversation_id ON messages(conversation_id)")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_msg_created_at ON messages(created_at)")
        print("✓ Indexes created")
        
        print("Creating conversations table...")
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id TEXT,
                metadata JSONB,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        print("✓ Conversations table created")
        
        print("Creating metrics table...")
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                conversation_id UUID,
                cognitive_score FLOAT,
                relevance_score FLOAT,
                temporal_score FLOAT,
                pattern_score FLOAT,
                created_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        print("✓ Metrics table created")
        
        print("\n✅ Database initialized successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
    finally:
        await conn.close()

if __name__ == "__main__":
    print("Cognitive Memory System - Database Initialization")
    print("=" * 50)
    asyncio.run(init_database())
