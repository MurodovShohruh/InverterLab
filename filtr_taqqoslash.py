import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

t = np.linspace(0, 0.1, 10000)
freq = 50
amplitude = 220
pwm_freq = 1000

faza1 = amplitude * np.sin(2 * np.pi * freq * t)
carrier = amplitude * np.sin(2 * np.pi * pwm_freq * t)
pwm = np.where(faza1 > carrier, amplitude, -amplitude)

fs = 1 / (t[1] - t[0])
cutoff = 200

# Filtr turlari
b1, a1 = signal.butter(2, cutoff/(fs/2), btype='low')
b2, a2 = signal.cheby1(2, 0.5, cutoff/(fs/2), btype='low')
b3, a3 = signal.bessel(2, cutoff/(fs/2), btype='low')

butter   = signal.filtfilt(b1, a1, pwm)
cheby    = signal.filtfilt(b2, a2, pwm)
bessel_f = signal.filtfilt(b3, a3, pwm)

def calc_thd(sig):
    fft_a = np.abs(np.fft.fft(sig)) / len(t) * 2
    amps = fft_a[:500]
    fund = np.max(amps[:100])
    return np.sqrt(np.sum(amps[100:]**2)) / fund * 100

thd_b = calc_thd(butter)
thd_c = calc_thd(cheby)
thd_be = calc_thd(bessel_f)

print("=" * 40)
print("   FILTR TURLARI TAQQOSLASH")
print("=" * 40)
print(f"  Butterworth  THD: {thd_b:.2f}%")
print(f"  Chebyshev    THD: {thd_c:.2f}%")
print(f"  Bessel       THD: {thd_be:.2f}%")
print("=" * 40)

fig, axes = plt.subplots(2, 2, figsize=(14, 8))

axes[0,0].plot(t[500:1500], pwm[500:1500], 'purple', linewidth=1)
axes[0,0].set_title('Filtrsiz PWM')
axes[0,0].grid(True)

axes[0,1].plot(t[500:1500], butter[500:1500], 'blue', linewidth=2)
axes[0,1].plot(t[500:1500], faza1[500:1500], 'b--', linewidth=1)
axes[0,1].set_title(f'Butterworth (THD={thd_b:.2f}%)')
axes[0,1].grid(True)

axes[1,0].plot(t[500:1500], cheby[500:1500], 'red', linewidth=2)
axes[1,0].plot(t[500:1500], faza1[500:1500], 'r--', linewidth=1)
axes[1,0].set_title(f'Chebyshev (THD={thd_c:.2f}%)')
axes[1,0].grid(True)

axes[1,1].plot(t[500:1500], bessel_f[500:1500], 'green', linewidth=2)
axes[1,1].plot(t[500:1500], faza1[500:1500], 'g--', linewidth=1)
axes[1,1].set_title(f'Bessel (THD={thd_be:.2f}%)')
axes[1,1].grid(True)

plt.suptitle('Filtr turlari taqqoslash', fontsize=14)
plt.tight_layout()
plt.savefig('inverterlab_filtrlar.png')
print("Tayyor: inverterlab_filtrlar.png")