#!/usr/bin/env python3
"""
Punto de entrada alternativo para Heroku
"""
import os
from dotenv import load_dotenv
load_dotenv()

# Importar después de cargar variables
from main import main

if __name__ == "__main__":
    main()