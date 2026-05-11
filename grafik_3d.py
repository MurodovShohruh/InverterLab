import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 0.1, 1000)
freq = 50
amplitude = 220

faza1 = amplitude * np.sin(2 * np.pi * freq * t)
faza2 = amplitude * np.sin(2 * np.pi * freq * t - 2*np.pi/3)
faza3 = amplitude * np.sin(2 * np.pi * freq * t - 4*np.pi/3)

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

ax.plot(t, np.ones_like(t)*0, faza1, 'b', linewidth=2, label='Faza A')
ax.plot(t, np.ones_like(t)*1, faza2, 'r', linewidth=2, label='Faza B')
ax.plot(t, np.ones_like(t)*2, faza3, 'g', linewidth=2, label='Faza C')

ax.set_xlabel('Vaqt (s)')
ax.set_ylabel('Faza')
ax.set_zlabel('Kuchlanish (V)')
ax.set_title('Uch fazali inverter — 3D ko\'rinish')
ax.set_yticks([0, 1, 2])
ax.set_yticklabels(['Faza A', 'Faza B', 'Faza C'])
ax.legend()

plt.tight_layout()
plt.savefig('inverterlab_3d.png')
plt.show()
print("Tayyor: inverterlab_3d.png")