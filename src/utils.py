from pathlib import Path

# Project root directory
project_root = Path(__file__).resolve().parent.parent

# Python package location
package_path = project_root / "python-package" / "employee_events"

# Model file location
model_path = project_root / "assets" / "model.pkl"

event_color = '\033[96m'
complete_color = '\033[92m'
color_end = '\033[0m'