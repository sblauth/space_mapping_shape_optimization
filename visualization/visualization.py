# Copyright (C) 2022 Sebastian Blauth

import matplotlib.pyplot as plt
import json


plt.style.use("tableau-colorblind10")
plt.rcParams.update({"font.size": 20})
lw = 2
ms = 6

# --- semi linear transmission problem ---
with open("../semi_linear_transmission_problem/sm_history.json", "r") as file:
    history = json.load(file)

fig, ax = plt.subplots()
ax.plot(
    range(len(history["cost_function_value"])),
    history["cost_function_value"],
    marker="s",
    markersize=ms,
    lw=lw,
)
ax.semilogy()
ax.set_xlabel("Iterations")
ax.set_ylabel("Cost functional value")
ax.set_xticks([0, 1, 2, 3, 4, 5])
fig.tight_layout()
fig.savefig("./img/transmission/cost_functional.pdf", dpi=1000)

fig, ax = plt.subplots()
ax.plot(
    range(len(history["eps"])),
    history["eps"],
    marker="s",
    markersize=ms,
    lw=lw,
)
ax.semilogy()
ax.set_xlabel("Iterations")
ax.set_ylabel("Stationarity measure")
ax.set_xticks([0, 1, 2, 3, 4, 5])
fig.tight_layout()
fig.savefig("./img/transmission/eps.pdf", dpi=1000)


# --- uniform flow distribution ---
with open("../uniform_flow_distribution/sm_history.json", "r") as file:
    history = json.load(file)

fig, ax = plt.subplots()
ax.plot(
    range(len(history["cost_function_value"])),
    history["cost_function_value"],
    marker="s",
    markersize=ms,
    lw=lw,
)
ax.semilogy()
ax.set_xlabel("Iterations")
ax.set_ylabel("Cost functional value")
ax.set_xticks([0, 1, 2, 3, 4, 5])
fig.tight_layout()
fig.savefig("./img/flow/cost_functional.pdf", dpi=1000)

fig, ax = plt.subplots()
ax.plot(
    range(len(history["eps"])),
    history["eps"],
    marker="s",
    markersize=ms,
    lw=lw,
)
ax.semilogy()
ax.set_xlabel("Iterations")
ax.set_ylabel("Stationarity measure")
ax.set_xticks([0, 1, 2, 3, 4, 5])
fig.tight_layout()
fig.savefig("./img/flow/eps.pdf", dpi=1000)

with open("../uniform_flow_distribution/flow_values.json", "r") as file:
    flow_values = json.load(file)

plt.rcParams.update({"font.size": 24})

width = 0.75

for i in range(6):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.bar(["left", "middle", "right"], flow_values[i], width=width)
    ax.axhline(1 / 3, color="k", ls=":", lw=5, label=r"$q_\mathrm{des}$")
    ax.legend(loc="upper left")
    ax.set_ybound(0.0, 0.6)
    ax.set_ylabel(r"$q_\mathrm{out}$")
    ax.set_xlabel("Channel location")
    fig.tight_layout()
    fig.savefig(f"./img/flow/distribution_{i}.png", dpi=250, bbox_inches="tight")
    plt.close(fig)
