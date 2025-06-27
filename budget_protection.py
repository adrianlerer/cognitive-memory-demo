#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Budget Protection Module
Copyright (c) 2025 IntegridAI. All rights reserved.

This file is part of the Cognitive Memory System.
Licensed under MIT License for open source components.
"""

import json
import os
from datetime import datetime, date
from fastapi import HTTPException

# Budget tracking
DAILY_BUDGET = float(os.getenv("DAILY_BUDGET_USD", "0.35"))
TOTAL_BUDGET = float(os.getenv("TOTAL_BUDGET_USD", "10"))
COST_PER_REQUEST = 0.0015

# Simple file-based tracking (para demo)
USAGE_FILE = "usage_tracking.json"

def load_usage():
    """Load usage tracking data from file"""
    try:
        with open(USAGE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"total_spent": 0, "daily": {}}

def save_usage(usage):
    """Save usage tracking data to file"""
    with open(USAGE_FILE, 'w') as f:
        json.dump(usage, f)

def check_budget():
    """Check if request is within budget limits"""
    usage = load_usage()
    today = str(date.today())
    
    # Check total budget
    if usage["total_spent"] >= TOTAL_BUDGET:
        raise HTTPException(status_code=429, detail="Demo budget agotado. Gracias por probar!")
    
    # Check daily budget
    daily_spent = usage["daily"].get(today, 0)
    if daily_spent >= DAILY_BUDGET:
        raise HTTPException(status_code=429, detail="Límite diario alcanzado. Vuelve mañana!")
    
    # Update usage
    usage["total_spent"] += COST_PER_REQUEST
    usage["daily"][today] = daily_spent + COST_PER_REQUEST
    save_usage(usage)
    
    return usage["total_spent"]
