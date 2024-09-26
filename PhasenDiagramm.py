import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os

# Title for the Streamlit App
st.title("Interaktives Phasendiagramm")

# Beispieldaten
images = []
images2 = []
xycolor = [[], [], []]
MOAT = ((-0.5, 1), (-0.5, 3), (-0.5, 0), (-1.5, 3), (-1.5, 1), (-3, 3), (-1.5, -1), (-2, 1), (-2, 3))
symmetrisch = ((1, 3), (1, 1), (3, 3), (3, 1))
broken = ((1, -1), (3, -1), (1, -3), (3, -3))
inhomo = ((1, -3), (-1.5, 0), (3, -1), (-2, 0), (-2, -1), (-2, -3), (-3, 0), (-4, 0,), (-4, -3), (-4, 3), (-3, 1), (-4, 1), (-1.5, -1), (-1.5, -3), (-3, -3), (-3, -1), (-4, -1), (-4, -3))
N_variants = ["N64", "N96", "N128", "N256"]
N_variants1 = ["N256", "N256", "N256", "N256"]

for Z2 in (-0.5, -1.5, -2, -3, -4, -5,  1, 3):
    for msqr in (3, 1, -1, -3, 0):
        if(msqr == 0 and Z2 > 0):
            continue
        color = "black"
        if ((Z2, msqr) in MOAT):
            color = "blue"
        if ((Z2, msqr) in symmetrisch):
            color = "red"
        if ((Z2, msqr) in inhomo or Z2 < -4):
            color = "green"
        if ((Z2, msqr) in broken):
            color = "yellow"
        xycolor[0].append(Z2)
        xycolor[1].append(msqr)
        xycolor[2].append(color)
        image = [f"./Plots/MsqrZ2Variation/msqr{msqr}Z2{Z2}{N}.png" for N in N_variants1]
        image2 = [f"./Plots/Heatmaps/msqr{msqr}Z2{Z2}{N}.png" for N in N_variants]
        images.append(image)
        images2.append(image2)

# Bilder vorladen
loaded_images1 = [[plt.imread(path) if os.path.exists(path) else None for path in img_set] for img_set in images]
loaded_images2 = [[plt.imread(path) if os.path.exists(path) else None for path in img_set] for img_set in images2]

# Phasendiagramm
fig_Diagramm, ax_Diagramm = plt.subplots()
sc = ax_Diagramm.scatter(xycolor[0], xycolor[1], c=xycolor[2])

# Achsen und Titel setzen
ax_Diagramm.axhline(0, color='black', lw=0.5)
ax_Diagramm.axvline(0, color='black', lw=0.5)
ax_Diagramm.set_title("Phasediagramm, Z4=1, T=1, Lambda=1")
ax_Diagramm.set_ylabel("Msqr")
ax_Diagramm.set_xlabel("Z2")

# Mean Field Lösung dazu Plotten
def MeanFieldPhasenGrenze(Z2MF):
    return Z2MF ** 2 / 4

msqrMF = np.linspace(-4, 0)
ax_Diagramm.plot(msqrMF, MeanFieldPhasenGrenze(msqrMF), label="Meanfield MOAT-Inhomo-Boarder")
ax_Diagramm.legend(loc="upper right")

# Diagramm in Streamlit anzeigen
st.pyplot(fig_Diagramm)

# Interaktive Bildanzeige
st.sidebar.title("Interaktive Bilder")
selected_point = st.sidebar.selectbox("Wähle einen Punkt auf dem Diagramm", range(len(xycolor[0])))

# Zeige die passenden Bilder zu dem ausgewählten Punkt
if selected_point is not None:
    current_images1 = loaded_images1[selected_point]
    current_images2 = loaded_images2[selected_point]

    # Zeige die Bilder in Streamlit
    if current_images1[0] is not None and current_images2[0] is not None:
        st.image([current_images1[0], current_images2[0]], caption=["Bild 1", "Bild 2"], width=300)
