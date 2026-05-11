import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

t = np.linspace(0, 0.1, 10000)
freq = 50
amplitude = 220
pwm_freq = 1000

# Signallar
faza1 = amplitude * np.sin(2 * np.pi * freq * t)
pwm_carrier = amplitude * np.sin(2 * np.pi * pwm_freq * t)
pwm1 = np.where(faza1 > pwm_carrier, amplitude, -amplitude)

# LC Filtr
fs = 1 / (t[1] - t[0])
b, a = signal.butter(2, 200 / (fs/2), btype='low')
filtered = signal.filtfilt(b, a, pwm1)

# Energiya hisoblash
def energiya(sig, t):
    return np.trapezoid(sig**2, t)

E_pwm = energiya(pwm1, t)
E_filtered = energiya(filtered, t)
E_ideal = energiya(faza1, t)

tejash = (E_pwm - E_filtered) / E_pwm * 100
samaradorlik = E_filtered / E_ideal * 100

# THD hisoblash
def calc_thd(sig, t):
    fft_a = np.abs(np.fft.fft(sig)) / len(t) * 2
    amps = fft_a[:500]
    fund = np.max(amps[:100])
    return np.sqrt(np.sum(amps[100:]**2)) / fund * 100

thd_pwm = calc_thd(pwm1, t)
thd_filtered = calc_thd(filtered, t)

# Natijalar
print("=" * 40)
print("   INVERTERLAB — ENERGIYA TAHLILI")
print("=" * 40)
print(f"  Filtrsiz PWM:")
print(f"    THD        : {thd_pwm:.1f}%")
print(f"    Energiya   : {E_pwm:.2f} J")
print(f"  LC Filtr bilan:")
print(f"    THD        : {thd_filtered:.1f}%")
print(f"    Energiya   : {E_filtered:.2f} J")
print(f"  Natija:")
print(f"    Tejash     : {tejash:.1f}%")
print(f"    Samaradorlik: {samaradorlik:.1f}%")
print("=" * 40)

# Grafik
fig, axes = plt.subplots(2, 2, figsize=(14, 8))

axes[0,0].plot(t[500:1000], pwm1[500:1000], 'purple', linewidth=1)
axes[0,0].set_title(f'Filtrsiz PWM (THD={thd_pwm:.1f}%)')
axes[0,0].grid(True)

axes[0,1].plot(t[500:1000], filtered[500:1000], 'green', linewidth=2)
axes[0,1].plot(t[500:1000], faza1[500:1000], 'b--', linewidth=1)
axes[0,1].set_title(f'Filtrlangan (THD={thd_filtered:.1f}%)')
axes[0,1].legend(['Filtrlangan', 'Ideal'])
axes[0,1].grid(True)

axes[1,0].bar(['Filtrsiz', 'Filtrlangan'], [thd_pwm, thd_filtered],
              color=['purple', 'green'])
axes[1,0].set_title('THD taqqoslash (%)')
axes[1,0].grid(True, axis='y')

axes[1,1].bar(['Tejash', 'Samaradorlik'], [tejash, samaradorlik],
              color=['orange', 'royalblue'])
axes[1,1].set_title('Energiya ko\'rsatkichlari (%)')
axes[1,1].grid(True, axis='y')

plt.suptitle('InverterLab — Energiya Tahlili', fontsize=14)
plt.tight_layout()
plt.savefig('inverterlab_energiya.png')
print("Grafik saqlandi: inverterlab_energiya.png")