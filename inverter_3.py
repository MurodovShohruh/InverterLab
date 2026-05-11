import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# O'zbekiston standartiga mos xisoblangan

t = np.linspace(0, 0.1, 10000) # vaqt o'qi — 0 dan 0.1 sekundgacha, 10000 ta nuqta.Xuddi ruletka kabi — 0.1 sm ni 10000 ga bo'lib chiqasiz.
freq = 50   # chiqish to'lqini tezligi.Inverter chiqish chastotasi — 50 Hz.O'zbekiston elektr tarmog'i standarti — 1 sekundda 50 marta to'lqin takrorlanadi.
amplitude = 220 # kuchlanish— 220 Volt.O'zbekiston rozetkasidagi kuchlanish aynan shu.
pwm_freq = 1000 # kalit ishlash tezligi.PWM tashuvchi chastotasi — 1000 Hz.Bu inverterning "kalit yoqib-o'chirish" tezligi. Asosiy signaldan 20 marta tez — shuning uchun PWM signal mayda to'rtburchaklarga bo'linadi.

faza1 = amplitude * np.sin(2 * np.pi * freq * t) # Bu — asosiy signal. 50 Hz, 220V sinusoida.2 * np.pi * freq * t — burchak tezligi, radianda.np.sin(...) — sinusoida shakli.amplitude * — balandligini 220V ga ko'taradi.
pwm_carrier = amplitude * np.sin(2 * np.pi * pwm_freq * t) # Bu — tashuvchi signal. 1000 Hz, 220V sinusoida.Xuddi faza1 ga o'xshash — lekin 20 marta tezroq.Vazifasi: faza1 bilan taqqoslanadi.
pwm1 = np.where(faza1 > pwm_carrier, amplitude, -amplitude) # Bu — PWM ning asosi. Mantiq juda oddiy:agar faza1 > pwm_carrier → +220V chiqar agar faza1 < pwm_carrier → -220V chiqar

# LC Filtr
fs = 1 / (t[1] - t[0])
cutoff = 200
b, a = signal.butter(2, cutoff / (fs/2), btype='low')
filtered = signal.filtfilt(b, a, pwm1)

# THD hisoblash funksiyasi
def calc_thd(sig, t):
    fft_s = np.fft.fft(sig)
    fft_f = np.fft.fftfreq(len(t), t[1]-t[0])
    fft_a = np.abs(fft_s) / len(t) * 2
    pos = fft_f > 0
    amps = fft_a[pos][:500]
    fund = np.max(amps[:100])
    return np.sqrt(np.sum(amps[100:]**2)) / fund * 100

thd_pwm = calc_thd(pwm1, t)
thd_filtered = calc_thd(filtered, t)

fig, axes = plt.subplots(3, 1, figsize=(12, 10))

axes[0].plot(t[500:1000], pwm1[500:1000], 'purple', linewidth=1, label=f'PWM (THD={thd_pwm:.1f}%)')
axes[0].set_title('Filtrsiz PWM signal')
axes[0].legend()
axes[0].grid(True)

axes[1].plot(t[500:1000], filtered[500:1000], 'green', linewidth=2, label=f'Filtrlangan (THD={thd_filtered:.1f}%)')
axes[1].plot(t[500:1000], faza1[500:1000], 'b--', linewidth=1, label='Ideal sinusoidal')
axes[1].set_title('LC Filtr qo\'shilgan signal')
axes[1].legend()
axes[1].grid(True)

axes[2].bar(['Filtrsiz PWM', 'LC Filtr bilan'], 
            [thd_pwm, thd_filtered],
            color=['purple', 'green'], width=0.4)
axes[2].set_title('THD taqqoslash')
axes[2].set_ylabel('THD (%)')
axes[2].grid(True, axis='y')

plt.tight_layout()
plt.savefig('inverterlab_filtr.png')
print(f"Filtrsiz THD: {thd_pwm:.1f}%")
print(f"Filtrlangan THD: {thd_filtered:.1f}%")