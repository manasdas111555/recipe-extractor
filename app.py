import sys
from pathlib import Path

# Bootstrap sys.path for Streamlit application execution
root_dir = Path(__file__).parent.resolve()
services_dir = root_dir / "backend" / "app" / "services"
core_dir = root_dir / "backend" / "app" / "core"
backend_dir = root_dir / "backend"

for p in [str(services_dir), str(core_dir), str(backend_dir), str(root_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)

streamlit_app_path = services_dir / "streamlit_app.py"
with open(streamlit_app_path, "r", encoding="utf-8") as f:
    code = compile(f.read(), str(streamlit_app_path), "exec")
    exec(code)
