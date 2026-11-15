
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read LTspice exported data
data_5V = pd.read_csv("VTC_Vdd_5.txt", sep="\t")
data_9V = pd.read_csv("VTC_Vdd_9.txt", sep="\t")


def calculate_vm(data, vdd):

    vin = data["Vin"].to_numpy()
    vout = data["V(vout)"].to_numpy()

    target = vdd / 2

    # Find where Vout crosses VDD/2
    index = np.where(
        (vout[:-1] - target) * (vout[1:] - target) <= 0
    )[0]

    if len(index) == 0:
        raise ValueError(f"No switching threshold found for {vdd} V")

    i = index[0]

    # Linear interpolation
    vm = vin[i] + (
        (target - vout[i]) *
        (vin[i+1] - vin[i]) /
        (vout[i+1] - vout[i])
    )

    return vm


# Calculate switching thresholds
vm_5 = calculate_vm(data_5V, 5)
vm_9 = calculate_vm(data_9V, 9)

print(f"Vm for VDD = 5 V: {vm_5:.4f} V")
print(f"Vm for VDD = 9 V: {vm_9:.4f} V")


# Create figure
plt.figure(figsize=(10, 7))

# Plot both VTC curves
plt.plot(
    data_5V["Vin"],
    data_5V["V(vout)"],
    linewidth=2.5,
    label="VDD = 5 V"
)

plt.plot(
    data_9V["Vin"],
    data_9V["V(vout)"],
    linewidth=2.5,
    label="VDD = 9 V"
)


# Plot diagonal reference line
x = np.linspace(0, 9, 200)

plt.plot(
    x, x,
    linestyle="--",
    color="gray",
    linewidth=1.8,
    label="VOUT = VIN"
)


# Mark Vm for 5 V
plt.axvline(vm_5, ymin=0, ymax=5/9,
            linestyle=":", color="blue", alpha=0.8)

plt.axhline(2.5, xmax=vm_5/9,
            linestyle=":", color="blue", alpha=0.8)

plt.scatter(vm_5, 2.5, color="blue", s=65, zorder=5)

plt.annotate(
    f"$V_{{m,5V}}$ = {vm_5:.3f} V",
    xy=(vm_5, 2.5),
    xytext=(vm_5 + 0.5, 3.3),
    arrowprops=dict(arrowstyle="->", color="blue"),
    color="blue",
    fontsize=10
)


# Mark Vm for 9 V
plt.axvline(vm_9, ymin=0, ymax=4.5/9,
            linestyle=":", color="red", alpha=0.8)

plt.axhline(4.5, xmax=vm_9/9,
            linestyle=":", color="red", alpha=0.8)

plt.scatter(vm_9, 4.5, color="red", s=65, zorder=5)

plt.annotate(
    f"$V_{{m,9V}}$ = {vm_9:.3f} V",
    xy=(vm_9, 4.5),
    xytext=(vm_9 + 0.5, 5.5),
    arrowprops=dict(arrowstyle="->", color="red"),
    color="red",
    fontsize=10
)


# Graph formatting
plt.title("Voltage Transfer Characteristics of Inverter",
          fontsize=14)

plt.xlabel("Input Voltage, $V_{IN}$ (V)", fontsize=12)
plt.ylabel("Output Voltage, $V_{OUT}$ (V)", fontsize=12)

plt.xlim(0, 9)
plt.ylim(0, 9)

plt.xticks(np.arange(0, 10, 1))
plt.yticks(np.arange(0, 10, 1))

plt.grid(True, linestyle="--", alpha=0.5)

plt.legend(fontsize=10)
plt.tight_layout()

# Save graph at 300 DPI
plt.savefig("VTC_Overlay.png", dpi=300, bbox_inches="tight")

plt.show()
