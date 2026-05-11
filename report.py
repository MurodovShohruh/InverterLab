import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime

t = np.linspace(0, 0.1, 10000)
freq = 50
amplitude = 220
pwm_freq = 1000

faza1 = amplitude * np.sin(2 * np.pi * freq * t)
carrier = amplitude * np.sin(2 * np.pi * pwm_freq * t)
pwm1 = np.where(faza1 > carrier, amplitude, -amplitude)

fs = 1 / (t[1] - t[0])
b, a = signal.butter(2, 200 / (fs/2), btype='low')
filtered = signal.filtfilt(b, a, pwm1)

def calc_thd(sig):
    fft_a = np.abs(np.fft.fft(sig)) / len(t) * 2
    amps = fft_a[:500]
    fund = np.max(amps[:100])
    return np.sqrt(np.sum(amps[100:]**2)) / fund * 100

def energiya(sig):
    return np.trapezoid(sig**2, t)

thd_pwm = calc_thd(pwm1)
thd_filt = calc_thd(filtered)
E_pwm = energiya(pwm1)
E_filt = energiya(filtered)
tejash = (E_pwm - E_filt) / E_pwm * 100

with PdfPages('InverterLab_Hisobot.pdf') as pdf:

    # 1-sahifa: Sarlavha
    fig = plt.figure(figsize=(11.7, 8.3))
    fig.patch.set_facecolor('white')
    plt.axis('off')
    plt.text(0.5, 0.7, 'InverterLab', fontsize=40, fontweight='bold',
             ha='center', va='center', color='#1a1a2e')
    plt.text(0.5, 0.55, 'Uch fazali inverter tahlil hisoboti',
             fontsize=18, ha='center', color='#378ADD')
    plt.text(0.5, 0.40, f'Muallif: Murodov Shohruh',
             fontsize=14, ha='center', color='gray')
    plt.text(0.5, 0.32, f'Qo\'qon Davlat Universiteti',
             fontsize=12, ha='center', color='gray')
    plt.text(0.5, 0.20, f'Sana: {datetime.now().strftime("%d.%m.%Y")}',
             fontsize=12, ha='center', color='gray')
    pdf.savefig(fig)
    plt.close()

    # 2-sahifa: Signallar
    fig, axes = plt.subplots(3, 1, figsize=(11.7, 8.3))
    axes[0].plot(t[500:1500], faza1[500:1500], 'b', linewidth=2)
    axes[0].set_title('Ideal sinusoidal signal (220V, 50Hz)')
    axes[0].grid(True)

    axes[1].plot(t[500:1500], pwm1[500:1500], 'purple', linewidth=1)
    axes[1].set_title(f'PWM signal (THD={thd_pwm:.1f}%)')
    axes[1].grid(True)

    axes[2].plot(t[500:1500], filtered[500:1500], 'green', linewidth=2)
    axes[2].set_title(f'LC Filtr bilan (THD={thd_filt:.1f}%)')
    axes[2].grid(True)

    plt.suptitle('Signal tahlili', fontsize=14)
    plt.tight_layout()
    pdf.savefig(fig)
    plt.close()

    # 3-sahifa: Natijalar
    fig, axes = plt.subplots(1, 2, figsize=(11.7, 8.3))

    axes[0].bar(['Filtrsiz PWM', 'LC Filtr'],
                [thd_pwm, thd_filt],
                color=['purple', 'green'])
    axes[0].set_title('THD taqqoslash (%)')
    axes[0].grid(True, axis='y')

    axes[1].bar(['Tejash', 'Samaradorlik'],
                [tejash, 100-tejash],
                color=['orange', 'royalblue'])
    axes[1].set_title('Energiya ko\'rsatkichlari (%)')
    axes[1].grid(True, axis='y')

    plt.suptitle('Natijalar', fontsize=14)
    plt.tight_layout()
    pdf.savefig(fig)
    plt.close()

    # 4-sahifa: Xulosa
    fig = plt.figure(figsize=(11.7, 8.3))
    plt.axis('off')
    plt.text(0.5, 0.90, 'Xulosa', fontsize=24,
             fontweight='bold', ha='center', color='#1a1a2e')

    natijalar = [
        f'• Chastota:           {freq} Hz',
        f'• Kuchlanish:         {amplitude} V',
        f'• PWM chastotasi:     {pwm_freq} Hz',
        f'',
        f'• Filtrsiz THD:       {thd_pwm:.1f}%',
        f'• Filtrlangan THD:    {thd_filt:.1f}%',
        f'• THD kamayishi:      {thd_pwm - thd_filt:.1f}%',
        f'',
        f'• Energiya tejash:    {tejash:.1f}%',
        f'• GitHub:             github.com/MurodovShohruh/InverterLab',
    ]

    for i, line in enumerate(natijalar):
        plt.text(0.15, 0.75 - i*0.07, line, fontsize=13,
                 color='#1a1a2e', family='monospace')

    pdf.savefig(fig)
    plt.close()

print("PDF hisobot saqlandi: InverterLab_Hisobot.pdf")