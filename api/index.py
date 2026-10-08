import sys
import os

# Add project root to sys.path so Vercel can resolve the 'backend' package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mangum import Mangum
from backend.app.main import app

handler = Mangum(app, lifespan="off")