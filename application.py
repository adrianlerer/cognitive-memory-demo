#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
application.py - Wrapper for AWS Elastic Beanstalk
Copyright (c) 2025 IntegridAI. All rights reserved.

This file is part of the Cognitive Memory System.
Licensed under MIT License for open source components.
"""
from main import app

# Elastic Beanstalk busca 'application' como punto de entrada
application = app

if __name__ == "__main__":
    # Para desarrollo local
    import uvicorn
    uvicorn.run(application, host="0.0.0.0", port=8000)
