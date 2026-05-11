import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 0.1, 10000)
freq = 50
amplitude = 220

faza1 = amplitude * np.sin(2 * np.pi * freq * t)

# PWM qo'shamiz — haqiqiy inverter signali
pwm_freq = 1000
pwm_carrier = amplitude * np.sin(2 * np.pi * pwm_freq * t)
pwm1 = np.where(faza1 > pwm_carrier, amplitude, -amplitude)

# Fourier — PWM signal uchun
fft_signal = np.fft.fft(pwm1)
fft_freq = np.fft.fftfreq(len(t), t[1] - t[0])
fft_amplitude = np.abs(fft_signal) / len(t) * 2

positive = fft_freq > 0
freqs_pos = fft_freq[positive]
amps_pos = fft_amplitude[positive]

mask = freqs_pos < 3000
freqs_show = freqs_pos[mask]
amps_show = amps_pos[mask]

fundamental = np.max(amps_show[:100])
thd = np.sqrt(np.sum(amps_show[100:]**2)) / fundamental * 100

fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# PWM signal — to'g'ri interval
axes[0].plot(t[500:1000], pwm1[500:1000], 'purple', linewidth=1)
axes[0].plot(t[500:1000], faza1[500:1000], 'b', linewidth=2, label='Sinusoidal')
axes[0].set_title('PWM chiqish signali va sinusoidal')
axes[0].set_xlabel('Vaqt (s)')
axes[0].set_ylabel('Kuchlanish (V)')
axes[0].legend()
axes[0].grid(True)

axes[1].bar(freqs_show, amps_show, width=5, color='royalblue')
axes[1].set_title(f'PWM Harmonik tahlil (THD = {thd:.1f}%)')
axes[1].set_xlabel('Chastota (Hz)')
axes[1].set_ylabel('Amplituda (V)')
axes[1].grid(True)

plt.tight_layout()
plt.savefig('inverterlab_harmonik2.png')
print(f"Tayyor! THD = {thd:.1f}%")
