import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

t = np.linspace(0, 2, 10000)
freq = 50
amplitude = 220

# Inverter chiqish signallari
faza1 = amplitude * np.sin(2 * np.pi * freq * t)
faza2 = amplitude * np.sin(2 * np.pi * freq * t - 2*np.pi/3)
faza3 = amplitude * np.sin(2 * np.pi * freq * t - 4*np.pi/3)

# Motor parametrlari
R = 2.5      # Stator qarshiligi (Om)
L = 0.01     # Induktivlik (H)
pole_pairs = 2  # Qutb juftlari

# Motor toki (RL zanjir)
fs = 1 / (t[1] - t[0])
b, a = signal.butter(1, R/(2*np.pi*L) / (fs/2), btype='low')
tok1 = signal.filtfilt(b, a, faza1) / R
tok2 = signal.filtfilt(b, a, faza2) / R
tok3 = signal.filtfilt(b, a, faza3) / R

# Aylanish tezligi
sinxron_tezlik = 60 * freq / pole_pairs
slip = 0.05
rotor_tezlik = sinxron_tezlik * (1 - slip)

# Moment
moment = np.abs(tok1) * amplitude * np.cos(np.arctan(2*np.pi*freq*L/R))
moment_smooth = signal.filtfilt(*signal.butter(2, 10/(fs/2)), moment)

print("=" * 40)
print("   MOTOR SIMULYATSIYASI")
print("=" * 40)
print(f"  Sinxron tezlik : {sinxron_tezlik:.0f} RPM")
print(f"  Rotor tezligi  : {rotor_tezlik:.0f} RPM")
print(f"  Slip           : {slip*100:.0f}%")
print(f"  Max tok        : {np.max(np.abs(tok1)):.2f} A")
print(f"  Max moment     : {np.max(moment_smooth):.2f} Nm")
print("=" * 40)

fig, axes = plt.subplots(3, 1, figsize=(12, 10))

axes[0].plot(t[:500], faza1[:500], 'b', linewidth=1.5, label='Faza A')
axes[0].plot(t[:500], faza2[:500], 'r', linewidth=1.5, label='Faza B')
axes[0].plot(t[:500], faza3[:500], 'g', linewidth=1.5, label='Faza C')
axes[0].set_title('Inverter chiqish kuchlanishi')
axes[0].set_ylabel('Kuchlanish (V)')
axes[0].legend()
axes[0].grid(True)

axes[1].plot(t[:500], tok1[:500], 'b', linewidth=1.5, label='Tok A')
axes[1].plot(t[:500], tok2[:500], 'r', linewidth=1.5, label='Tok B')
axes[1].plot(t[:500], tok3[:500], 'g', linewidth=1.5, label='Tok C')
axes[1].set_title(f'Motor stator toki (Max: {np.max(np.abs(tok1)):.2f} A)')
axes[1].set_ylabel('Tok (A)')
axes[1].legend()
axes[1].grid(True)

axes[2].plot(t[:500], moment_smooth[:500], 'orange', linewidth=2)
axes[2].axhline(np.mean(moment_smooth), color='red', linestyle='--',
                label=f'O\'rtacha: {np.mean(moment_smooth):.2f} Nm')
axes[2].set_title('Motor burish momenti')
axes[2].set_ylabel('Moment (Nm)')
axes[2].set_xlabel('Vaqt (s)')
axes[2].legend()
axes[2].grid(True)

plt.suptitle(f'Asinkron motor simulyatsiyasi\n'
             f'Sinxron: {sinxron_tezlik:.0f} RPM | '
             f'Rotor: {rotor_tezlik:.0f} RPM', fontsize=13)
plt.tight_layout()
plt.savefig('inverterlab_motor.png')
print("Tayyor: inverterlab_motor.png")