import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy import signal

fig, axes = plt.subplots(2, 1, figsize=(12, 8))
plt.subplots_adjust(bottom=0.35)

t = np.linspace(0, 0.1, 10000)

def generate(freq, amplitude, pwm_freq, cutoff):
    faza1 = amplitude * np.sin(2 * np.pi * freq * t)
    carrier = amplitude * np.sin(2 * np.pi * pwm_freq * t)
    pwm = np.where(faza1 > carrier, amplitude, -amplitude)
    fs = 1 / (t[1] - t[0])
    b, a = signal.butter(2, cutoff / (fs/2), btype='low')
    filtered = signal.filtfilt(b, a, pwm)
    return faza1, pwm, filtered

def calc_thd(sig):
    fft_a = np.abs(np.fft.fft(sig)) / len(t) * 2
    amps = fft_a[:500]
    fund = np.max(amps[:100])
    return np.sqrt(np.sum(amps[100:]**2)) / fund * 100

# Boshlang'ich qiymatlar
freq0, amp0, pwm0, cut0 = 50, 220, 1000, 200

faza1, pwm, filtered = generate(freq0, amp0, pwm0, cut0)

line1, = axes[0].plot(t[500:1500], pwm[500:1500], 'purple', linewidth=1, label='PWM')
line2, = axes[0].plot(t[500:1500], faza1[500:1500], 'b--', linewidth=1.5, label='Ideal')
line3, = axes[0].plot(t[500:1500], filtered[500:1500], 'green', linewidth=2, label='Filtrlangan')
axes[0].legend()
axes[0].grid(True)
thd_text = axes[0].set_title(f'THD: {calc_thd(filtered):.1f}%')

fft_f = np.fft.fftfreq(len(t), t[1]-t[0])
pos = fft_f > 0
freqs = fft_f[pos][:300]
amps_filt = np.abs(np.fft.fft(filtered))[pos][:300] / len(t) * 2
bar_container = axes[1].bar(freqs, amps_filt, width=3, color='royalblue')
axes[1].set_xlim(0, 600)
axes[1].set_title('Harmonik tahlil')
axes[1].grid(True)

# Sliderlar
ax_freq = plt.axes([0.15, 0.25, 0.7, 0.03])
ax_amp  = plt.axes([0.15, 0.20, 0.7, 0.03])
ax_pwm  = plt.axes([0.15, 0.15, 0.7, 0.03])
ax_cut  = plt.axes([0.15, 0.10, 0.7, 0.03])

s_freq = Slider(ax_freq, 'Chastota (Hz)', 10, 100, valinit=freq0, valstep=1)
s_amp  = Slider(ax_amp,  'Kuchlanish (V)', 50, 400, valinit=amp0, valstep=10)
s_pwm  = Slider(ax_pwm,  'PWM freq (Hz)', 200, 5000, valinit=pwm0, valstep=100)
s_cut  = Slider(ax_cut,  'Filtr (Hz)', 50, 1000, valinit=cut0, valstep=10)

def update(val):
    f, a, p, c = s_freq.val, s_amp.val, s_pwm.val, s_cut.val
    faza1, pwm, filtered = generate(f, a, p, c)
    line1.set_ydata(pwm[500:1500])
    line2.set_ydata(faza1[500:1500])
    line3.set_ydata(filtered[500:1500])
    axes[0].set_title(f'THD: {calc_thd(filtered):.1f}%')
    amps_new = np.abs(np.fft.fft(filtered))[pos][:300] / len(t) * 2
    for bar, h in zip(bar_container, amps_new):
        bar.set_height(h)
    fig.canvas.draw_idle()

s_freq.on_changed(update)
s_amp.on_changed(update)
s_pwm.on_changed(update)
s_cut.on_changed(update)

plt.suptitle('InverterLab — Interaktiv Tahlil', fontsize=13)
plt.show()