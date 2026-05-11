import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 0.1, 10000)
freq = 50
amplitude = 220
pwm_freq = 1000

# Uch fazali signal
faza1 = amplitude * np.sin(2 * np.pi * freq * t)
faza2 = amplitude * np.sin(2 * np.pi * freq * t - 2*np.pi/3)
faza3 = amplitude * np.sin(2 * np.pi * freq * t - 4*np.pi/3)

# PWM signal
pwm_carrier = amplitude * np.sin(2 * np.pi * pwm_freq * t)
pwm1 = np.where(faza1 > pwm_carrier, amplitude, -amplitude)

# Grafik
fig, axes = plt.subplots(3, 1, figsize=(12, 8))

axes[0].plot(t, faza1, 'b', label='Faza A', linewidth=1.5)
axes[0].plot(t, faza2, 'r', label='Faza B', linewidth=1.5)
axes[0].plot(t, faza3, 'g', label='Faza C', linewidth=1.5)
axes[0].set_title('Uch fazali signal')
axes[0].legend()
axes[0].grid(True)

axes[1].plot(t[:500], pwm_carrier[:500], 'gray', label='Tashuvchi', linewidth=0.8)
axes[1].plot(t[:500], faza1[:500], 'b', label='Modulyator', linewidth=1.5)
axes[1].set_title('PWM — tashuvchi vs modulyator')
axes[1].legend()
axes[1].grid(True)

axes[2].plot(t[:500], pwm1[:500], 'purple', label='PWM chiqish', linewidth=1)
axes[2].set_title('PWM chiqish signali')
axes[2].legend()
axes[2].grid(True)

plt.tight_layout()
plt.savefig('inverterlab_pwm.png')
print("Tayyor: inverterlab_pwm.png")