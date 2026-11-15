
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read simulation data
data_65 = pd.read_csv("VTC_ltspice.txt", sep=r"\s+")
data_dis = pd.read_csv("VTC_Vdd_5.txt", sep=r"\s+")

# Extract actual voltages
Vin_65 = data_65["Vin"].to_numpy()
Vout_65 = data_65["V(vout)"].to_numpy()

Vin_dis = data_dis["Vin"].to_numpy()
Vout_dis = data_dis["V(vout)"].to_numpy()

# Find switching threshold where VOUT = VIN
def find_vm(vin, vout):
    difference = vout - vin
    indices = np.where(np.diff(np.sign(difference)))[0]

    i = indices[0]

    vm = vin[i] - difference[i] * (
        (vin[i+1] - vin[i]) /
        (difference[i+1] - difference[i])
    )

    return vm

Vm_65 = find_vm(Vin_65, Vout_65)
Vm_dis = find_vm(Vin_dis, Vout_dis)

# Plot
plt.figure(figsize=(11, 7))

plt.plot(Vin_65, Vout_65,
         linewidth=2.5, label="65 nm Inverter")

plt.plot(Vin_dis, Vout_dis,
         linewidth=2.5, label="Discrete Inverter")

# Reference line VOUT = VIN
plt.plot([0, 5], [0, 5], '--',
         color='gray', linewidth=2,
         label="VOUT = VIN")

# Switching threshold points
plt.scatter(Vm_65, Vm_65, color='blue', s=90, zorder=5)
plt.scatter(Vm_dis, Vm_dis, color='red', s=90, zorder=5)

# Guide lines
plt.axvline(Vm_65, ymin=0, ymax=Vm_65/5,
            color='blue', linestyle=':', linewidth=2)

plt.axhline(Vm_65, xmin=0, xmax=Vm_65/5,
            color='blue', linestyle=':', linewidth=2)

plt.axvline(Vm_dis, ymin=0, ymax=Vm_dis/5,
            color='red', linestyle=':', linewidth=2)

plt.axhline(Vm_dis, xmin=0, xmax=Vm_dis/5,
            color='red', linestyle=':', linewidth=2)

# Annotations
plt.annotate(
    f"$V_{{m,65nm}}$ = {Vm_65:.3f} V",
    xy=(Vm_65, Vm_65),
    xytext=(Vm_65 + 0.3, Vm_65 + 0.5),
    color='blue',
    fontsize=12,
    arrowprops=dict(arrowstyle='->', color='blue')
)

plt.annotate(
    f"$V_{{m,discrete}}$ = {Vm_dis:.3f} V",
    xy=(Vm_dis, Vm_dis),
    xytext=(Vm_dis + 0.3, Vm_dis + 0.5),
    color='red',
    fontsize=12,
    arrowprops=dict(arrowstyle='->', color='red')
)

# Axis formatting
plt.xlim(0, 5)
plt.ylim(0, 5)

plt.xlabel("Input Voltage, $V_{IN}$ (V)", fontsize=14)
plt.ylabel("Output Voltage, $V_{OUT}$ (V)", fontsize=14)

plt.title("Voltage Transfer Characteristics: 65 nm vs Discrete Inverter",
          fontsize=15)

plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(fontsize=12, loc='best')

plt.tight_layout()

# Save graph
plt.savefig("VTC_65nm_vs_Discrete.png",
            dpi=300, bbox_inches='tight')

plt.show()

print(f"65 nm switching threshold = {Vm_65:.4f} V")
print(f"Discrete switching threshold = {Vm_dis:.4f} V")
