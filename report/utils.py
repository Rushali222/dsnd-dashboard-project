from pathlib import Path
import pickle

# Using pathlib create a project_root
# variable set to the absolute path
# for the root of this project
project_root = Path(__file__).resolve().parent.parent

# Using the project_root variable
# create a model_path variable
# that points to model.pkl
# inside the assets folder
model_path = project_root / "assets" / "model.pkl"

package_path = project_root / "python-package" / "employee_events"

event_color = '\033[96m'
complete_color = '\033[92m'
color_end = '\033[0m'


def load_model():

    with model_path.open('rb') as file:
        model = pickle.load(file)

    return model