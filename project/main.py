"""
Single entry-point that resolves the
import dependencies. Blueprints could be imported here.

This file is also used to run the app:
    python main.py
"""
import os
from .app import app
from .views import *

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)