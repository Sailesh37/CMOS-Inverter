import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv("VTC_Vdd_5.txt", sep=r"\s+")
Vin = data["Vin"].to_numpy()
Vout = data["V(vout)"].to_numpy()
difference = Vout - Vin
indices = np.where(np.diff(np.sign(difference)))[0]
i = indices[0]
Vm = Vin[i] - difference[i] * (
    (Vin[i+1] - Vin[i]) /
    (difference[i+1] - difference[i])
)
plt.figure(figsize=(11, 7))
plt.plot(Vin, Vout, linewidth=2.5,
         color='blue', label="Discrete Inverter (VDD = 5 V)")
plt.plot([0, 5], [0, 5], '--',
         color='gray', linewidth=2,
         label="VOUT = VIN")
plt.scatter(Vm, Vm, color='red', s=90, zorder=5)
plt.axvline(Vm, ymin=0, ymax=Vm/5,
            color='red', linestyle=':', linewidth=2)
plt.axhline(Vm, xmin=0, xmax=Vm/5,
            color='red', linestyle=':', linewidth=2)
plt.annotate(
    f"$V_m$ = {Vm:.3f} V",
    xy=(Vm, Vm),
    xytext=(Vm + 0.4, Vm + 0.7),
    color='red',
    fontsize=13,
    arrowprops=dict(arrowstyle='->', color='red')
)
plt.xlim(0, 5)
plt.ylim(0, 5)
plt.xlabel("Input Voltage, $V_{IN}$ (V)", fontsize=14)
plt.ylabel("Output Voltage, $V_{OUT}$ (V)", fontsize=14)
plt.title("Voltage Transfer Characteristics of Discrete Inverter",fontsize=15)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig("VTC_Discrete_5V.png",dpi=300, bbox_inches='tight')
plt.show()
print(f"Switching threshold Vm = {Vm:.4f} V")
