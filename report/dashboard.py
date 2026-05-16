from fasthtml.common import *
import matplotlib.pyplot as plt

# Import QueryBase, Employee, Team from employee_events
from employee_events import QueryBase, Employee, Team

# import the load_model function from the utils.py file
from utils import load_model

from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
)

from combined_components import FormGroup, CombinedComponent


# Dropdown
class ReportDropdown(Dropdown):

    def build_component(self, entity_id, model):

        self.label = model.name.capitalize()

        return super().build_component(entity_id, model)

    def component_data(self, entity_id, model):

        return model.names()

# Header
class Header(BaseComponent):

    def build_component(self, entity_id, model):

        return H1(f"{model.name.capitalize()} Dashboard")


# Line chart
class LineChart(MatplotlibViz):

    def visualization(self, entity_id, model):

        data = model.event_counts(entity_id)

        data = data.fillna(0)

        data = data.set_index("event_date")

        data = data.sort_index()

        data = data.cumsum()

        data.columns = ['Positive', 'Negative']

        fig, ax = plt.subplots()

        data.plot(ax=ax)

        self.set_axis_styling(
            ax,
            bordercolor='black',
            fontcolor='black'
        )

        ax.set_title('Cumulative Events')
        ax.set_xlabel('Date')
        ax.set_ylabel('Events')


# Bar chart
class BarChart(MatplotlibViz):

    predictor = load_model()

    def visualization(self, entity_id, model):

        data = model.model_data(entity_id)

        pred = self.predictor.predict_proba(data)[:,1]

        if model.name == "team":
            pred = pred.mean()

        else:
            pred = pred[0]

        fig, ax = plt.subplots()

        ax.barh([''], [pred])

        ax.set_xlim(0,1)

        ax.set_title(
            'Predicted Recruitment Risk',
            fontsize=20
        )

        self.set_axis_styling(
            ax,
            bordercolor='black',
            fontcolor='black'
        )


# Visualization group
class Visualizations(CombinedComponent):

    children = [
        LineChart(),
        BarChart()
    ]

    outer_div_type = Div(cls='grid')


# Notes table
class NotesTable(DataTable):

    def component_data(self, entity_id, model):

        return model.notes(entity_id)


class DashboardFilters(FormGroup):

    id = "top-filters"
    action = "/update_data"
    method="POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
        ),

        ReportDropdown(
            id="selector",
            name="user-selection"
        )
    ]


# Main report page
class Report(CombinedComponent):

    children = [
        Header(),
        DashboardFilters(),
        Visualizations(),
        NotesTable()
    ]


# FastHTML app
app = FastHTML()

report = Report()


@app.get("/")
def index():

    return report(1, Employee())


@app.get("/employee/{id:str}")
def employee(id: str):

    return report(id, Employee())


@app.get("/team/{id:str}")
def team(id: str):

    return report(id, Team())


# Keep unchanged below
@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print('PARAM', r.query_params['profile_type'])
    if r.query_params['profile_type'] == 'Team':
        return dropdown(None, Team())
    elif r.query_params['profile_type'] == 'Employee':
        return dropdown(None, Employee())


@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)


serve()