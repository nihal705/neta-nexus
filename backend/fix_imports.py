import os
import re

def fix_imports():
    """Fix import statements in all backend files"""
    
    backend_dir = "backend"
    
    for root, dirs, files in os.walk(backend_dir):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Fix imports
                content = re.sub(r'from backend.database import', 'from backend.database import', content)
                content = re.sub(r'from backend.models import', 'from backend.models import', content)
                content = re.sub(r'from backend.schemas import', 'from backend.schemas import', content)
                content = re.sub(r'from routes\.', 'from backend.routes.', content)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
    
    print("✅ Imports fixed!")

if __name__ == "__main__":
    fix_imports()