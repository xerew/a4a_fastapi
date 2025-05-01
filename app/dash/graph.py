import dash
import dash_cytoscape as cyto
from dash import html

dash_app = dash.Dash(
    __name__,
    requests_pathname_prefix="/graph/",  # FastAPI will reverse proxy here
)

dash_app.layout = html.Div([
    html.H3("My Dash Cytoscape Graph", style={"textAlign": "center"}),
    cyto.Cytoscape(
        id='cytoscape',
        layout={'name': 'circle'},
        style={'width': '100%', 'height': '600px'},
        elements=[
            {'data': {'id': 'A', 'label': 'Node A'}, 'position': {'x': 50, 'y': 50}},
            {'data': {'id': 'B', 'label': 'Node B'}, 'position': {'x': 200, 'y': 200}},
            {'data': {'source': 'A', 'target': 'B'}}
        ]
    )
])
