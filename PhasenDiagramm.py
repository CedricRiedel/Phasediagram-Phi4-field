import matplotlib.pyplot as plt
import numpy as np
import os

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
# Neue Punkte der Systematischen Messung
# for Z2 in (-1,):
#     for msqr in (-0.5, 0, 0.1, 0.25, 0.5, 0.75, -0.75, -1, -1.25, -1.5, -1.75, -2):
#         color = "grey"
#         xycolor[0].append(Z2)
#         xycolor[1].append(msqr)
#         xycolor[2].append(color)
#         image = [f"./Plots/MsqrZ2Variation/msqr{msqr}Z2{Z2}{N}.png" for N in N_variants1]
#         image2 = [f"./Plots/Heatmaps/msqr{msqr}Z2{Z2}{N}.png" for N in N_variants]
#         images.append(image)
#         images2.append(image2)

# for msqr in (-2,):
#     for Z2 in (-0.1, -0.5, -0.25, -1, 0.1, 0.25, 0.5, 0, 1):
#         color = "grey"
#         xycolor[0].append(Z2)
#         xycolor[1].append(msqr)
#         xycolor[2].append(color)
#         image = [f"./Plots/MsqrZ2Variation/msqr{msqr}Z2{Z2}{N}.png" for N in N_variants1]
#         image2 = [f"./Plots/Heatmaps/msqr{msqr}Z2{Z2}{N}.png" for N in N_variants]
#         images.append(image)
#         images2.append(image2)
#Bilder vorladen für Zeiteffizienz
loaded_images1 = [[plt.imread(path) if os.path.exists(path) else None for path in img_set] for img_set in images]
loaded_images2 = [[plt.imread(path) if os.path.exists(path) else None for path in img_set] for img_set in images2]

fig_Diagramm, ax_Diagramm = plt.subplots()
sc = ax_Diagramm.scatter(xycolor[0], xycolor[1], c=xycolor[2])

fig, axes = plt.subplots(2, 1)
axes = axes.flatten()
im1 = axes[0].imshow(np.zeros((10, 15, 3)))  # Initialisiere leere Bilder
im2 = axes[1].imshow(np.zeros((10, 20, 3)))  

for ax in axes:
    ax.axis("off")

current_index = 0
current_images1 = []
current_images2 = []

def on_click(event):
    global current_index, current_images1, current_images2
    if event.inaxes == ax_Diagramm:
        cont, ind = sc.contains(event)
        if cont:
            current_images1 = loaded_images1[ind["ind"][0]]
            current_images2 = loaded_images2[ind["ind"][0]]
            current_index = 0
            show_images(current_images1[current_index], current_images2[current_index])

def on_key(event):
    global current_index, current_images1, current_images2
    if event.key == "right":
        current_index = (current_index + 1) % 4
    elif event.key == "left":
        current_index = (current_index - 1) % 4
    show_images(current_images1[current_index], current_images2[current_index])

def show_images(img1, img2):
    if img1 is not None and img2 is not None:
        im1.set_data(img1)
        im2.set_data(img2)
        fig.canvas.draw()

fig_Diagramm.canvas.mpl_connect("button_press_event", on_click)
fig_Diagramm.canvas.mpl_connect("key_press_event", on_key)

#Phasendiagramm erstellen
ax_Diagramm.axhline(0, color='black', lw=0.5)
ax_Diagramm.axvline(0, color='black', lw=0.5)

ax_Diagramm.set_title("Phasediagramm, Z4=1, T=1, Lambda=1")
ax_Diagramm.set_ylabel("Msqr")
ax_Diagramm.set_xlabel("Z2")

#Mean Field Lösung dazu Plotten
def MeanFieldPhasenGrenze(Z2MF):
    return Z2MF ** 2 / 4
msqrMF = np.linspace(-4, 0)
ax_Diagramm.plot(msqrMF, MeanFieldPhasenGrenze(msqrMF), label = "Meanfield MOAT-Inhomo-Boarder")
ax_Diagramm.legend(loc = "upper right")
plt.tight_layout()

plt.show()
