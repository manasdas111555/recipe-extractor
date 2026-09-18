import sys
from pathlib import Path

# Automatically add backend/app/services, backend/app/core, and backend to sys.path
# to allow legacy top-level imports (e.g. `import gemini_processor`) to resolve cleanly.
root_dir = Path(__file__).parent.resolve()
services_dir = root_dir / "backend" / "app" / "services"
core_dir = root_dir / "backend" / "app" / "core"
backend_dir = root_dir / "backend"

for path_str in [str(services_dir), str(core_dir), str(backend_dir), str(root_dir)]:
    if path_str not in sys.path:
        sys.path.insert(0, path_str)
