import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import os
import base64

# Dash App initialisieren
app = dash.Dash(__name__)

# Beispieldaten
xycolor = [[], [], []]
MOAT = ((-0.5, 1), (-0.5, 3), (-0.5, 0), (-1.5, 3), (-1.5, 1), (-3, 3), (-1.5, -1), (-2, 1), (-2, 3))
symmetrisch = ((1, 3), (1, 1), (3, 3), (3, 1))
broken = ((1, -1), (3, -1), (1, -3), (3, -3))
inhomo = ((1, -3), (-1.5, 0), (3, -1), (-2, 0), (-2, -1), (-2, -3), (-3, 0), (-4, 0,), (-4, -3), (-4, 3), (-3, 1), (-4, 1), (-1.5, -1), (-1.5, -3), (-3, -3), (-3, -1), (-4, -1), (-4, -3))
N_variants = ["N64", "N96", "N128", "N256"]

# Simulierte Punkte und Farben
for Z2 in (-0.5, -1.5, -2, -3, -4, -5, 1, 3):
    for msqr in (3, 1, -1, -3, 0):
        if msqr == 0 and Z2 > 0:
            continue
        color = "black"
        if (Z2, msqr) in MOAT:
            color = "blue"
        if (Z2, msqr) in symmetrisch:
            color = "red"
        if (Z2, msqr) in inhomo or Z2 < -4:
            color = "green"
        if (Z2, msqr) in broken:
            color = "yellow"
        xycolor[0].append(Z2)
        xycolor[1].append(msqr)
        xycolor[2].append(color)

# Bilder laden und konvertieren
def load_image(img_path):
    if os.path.exists(img_path):
        encoded_image = base64.b64encode(open(img_path, 'rb').read())
        return 'data:image/png;base64,{}'.format(encoded_image.decode())
    return None

# Phasen-Grenze Funktion
def mean_field_grenze(Z2MF):
    return Z2MF ** 2 / 4

# Layout der App
app.layout = html.Div([
    html.H1("Interaktives Phasendiagramm"),
    dcc.Graph(
        id='phasendiagramm',
        config={'displayModeBar': False}
    ),
    # MsqrZ2Variation Bild einmalig anzeigen
    html.Div(id='msqr-image-output', style={'textAlign': 'center', 'margin-top': '20px'}),
    html.Div(id='image-output', style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center', 'margin-top': '20px'}),
])

# Callbacks für Interaktivität
@app.callback(
    [Output('phasendiagramm', 'figure'),
     Output('msqr-image-output', 'children'),
     Output('image-output', 'children')],
    [Input('phasendiagramm', 'clickData')]
)
def update_output(clickData):
    # Phasendiagramm erstellen
    fig = go.Figure()

    # Punkte zeichnen
    fig.add_trace(go.Scatter(
        x=xycolor[0], y=xycolor[1], mode='markers', marker=dict(color=xycolor[2])
    ))

    # Mean-Field-Grenze
    msqrMF = np.linspace(-4, 0)
    fig.add_trace(go.Scatter(
        x=msqrMF, y=mean_field_grenze(msqrMF),
        mode='lines', name='Meanfield MOAT-Inhomo-Boarder'
    ))

    fig.update_layout(
        title="Phasediagramm, Z4=1, T=1, Lambda=1",
        xaxis_title="Z2",
        yaxis_title="Msqr",
        showlegend=False
    )

    # Klickevent abfragen
    if clickData:
        point_index = clickData['points'][0]['pointIndex']
        
        # Erstellen der Bildpfade für alle vier Heatmaps
        img_paths = [
            f"./Plots/Heatmaps/msqr{xycolor[1][point_index]}Z2{xycolor[0][point_index]}N{N}.png" 
            for N in ["64", "96", "128", "256"]
        ]

        # Lade die Bilder
        images = [load_image(img_path) for img_path in img_paths]

        # MsqrZ2Variation Bild laden
        msqr_img_path = f"./Plots/MsqrZ2Variation/msqr{xycolor[1][point_index]}Z2{xycolor[0][point_index]}N256.png"  # Beispiel-Pfad
        msqr_img = load_image(msqr_img_path)
        msqr_image_element = html.Img(src=msqr_img, style={'width': '600px'}) if msqr_img else "Kein Bild verfügbar."

        # Erstelle eine Liste der Bild-HTML-Elemente
        image_elements = []
        for img in images:
            if img:  # Nur vorhandene Bilder anzeigen
                image_elements.append(html.Img(src=img, style={'width': '300px', 'margin': '10px'}))

        return fig, msqr_image_element, image_elements if image_elements else ["Keine Bilder verfügbar."]

    # Rückgabe bei keinem Klickevent
    return fig, "Klicken Sie auf einen Punkt im Diagramm, um die Bilder anzuzeigen.", []

if __name__ == '__main__':
    app.run_server(debug=True)

