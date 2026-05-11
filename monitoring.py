import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import signal

fig, axes = plt.subplots(2, 2, figsize=(14, 8))
plt.subplots_adjust(hspace=0.4, wspace=0.3)

freq = 50
amplitude = 220
pwm_freq = 1000
fs = 10000
dt = 1/fs

# Bufer
buf_size = 500
t_buf = np.linspace(0, buf_size*dt, buf_size)
phase = [0]

b, a = signal.butter(2, 200/(fs/2), btype='low')
zi1 = signal.lfilter_zi(b, a) * 0
zi2 = signal.lfilter_zi(b, a) * 0

data = {
    'pwm': np.zeros(buf_size),
    'filtered': np.zeros(buf_size),
    'tok': np.zeros(buf_size),
    'thd': []
}

line_pwm,      = axes[0,0].plot(t_buf, data['pwm'], 'purple', lw=1)
line_filtered, = axes[0,1].plot(t_buf, data['filtered'], 'green', lw=2)
line_tok,      = axes[1,0].plot(t_buf, data['tok'], 'orange', lw=2)
bar_thd = axes[1,1].bar(['THD'], [0], color='royalblue')

axes[0,0].set_title('PWM signal')
axes[0,0].set_ylim(-250, 250)
axes[0,0].grid(True)

axes[0,1].set_title('Filtrlangan signal')
axes[0,1].set_ylim(-250, 250)
axes[0,1].grid(True)

axes[1,0].set_title('Motor toki (A)')
axes[1,0].set_ylim(-60, 60)
axes[1,0].grid(True)

axes[1,1].set_title('THD (%)')
axes[1,1].set_ylim(0, 150)
axes[1,1].grid(True)

thd_text = axes[1,1].text(0, 5, '0%', ha='center', fontsize=14, fontweight='bold')

def update(frame):
    chunk = 50
    t_chunk = np.arange(chunk) * dt + phase[0]
    phase[0] += chunk * dt

    faza = amplitude * np.sin(2*np.pi*freq*t_chunk)
    carrier = amplitude * np.sin(2*np.pi*pwm_freq*t_chunk)
    pwm_chunk = np.where(faza > carrier, amplitude, -amplitude)

    filt_chunk, zi1[:] = signal.lfilter(b, a, pwm_chunk, zi=zi1)
    tok_chunk = filt_chunk / 2.5

    data['pwm'] = np.roll(data['pwm'], -chunk)
    data['pwm'][-chunk:] = pwm_chunk

    data['filtered'] = np.roll(data['filtered'], -chunk)
    data['filtered'][-chunk:] = filt_chunk

    data['tok'] = np.roll(data['tok'], -chunk)
    data['tok'][-chunk:] = tok_chunk

    fft_a = np.abs(np.fft.fft(data['filtered'])) / buf_size * 2
    fund = np.max(fft_a[:50])
    if fund > 0:
        thd = np.sqrt(np.sum(fft_a[50:]**2)) / fund * 100
    else:
        thd = 0

    line_pwm.set_ydata(data['pwm'])
    line_filtered.set_ydata(data['filtered'])
    line_tok.set_ydata(data['tok'])
    bar_thd[0].set_height(min(thd, 150))
    thd_text.set_text(f'{thd:.1f}%')
    thd_text.set_y(min(thd, 140) + 2)

    axes[0,0].set_title(f'PWM signal — {freq}Hz, {amplitude}V')
    axes[0,1].set_title(f'Filtrlangan — {filt_chunk[-1]:.1f}V')
    axes[1,0].set_title(f'Motor toki — {tok_chunk[-1]:.2f}A')

    return line_pwm, line_filtered, line_tok, bar_thd[0], thd_text

ani = animation.FuncAnimation(fig, update, interval=50, blit=True, cache_frame_data=False)

plt.suptitle('InverterLab — Real Vaqt Monitoring', fontsize=13)
plt.show()