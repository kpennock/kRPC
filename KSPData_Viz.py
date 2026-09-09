import pandas as pd
import matplotlib.pyplot as plt

# add some comments to make sure git is working
df = pd.read_csv('flight_telemetry.csv')

fig, ax1 = plt.subplots(figsize=(10, 5))

# Plot Altitude
ax1.set_xlabel('Mission Time (s)')
ax1.set_ylabel('Altitude (m)', color='tab:blue')
ax1.plot(df['time_s'] - df['time_s'].iloc[0], df['altitude_m'], color='tab:blue', label='Altitude')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Plot Velocity on secondary axis
ax2 = ax1.twinx()
ax2.set_ylabel('Speed (m/s)', color='tab:red')
ax2.plot(df['time_s'] - df['time_s'].iloc[0], df['surface_velocity_ms'], color='tab:red', label='Surface Speed')
ax2.tick_params(axis='y', labelcolor='tab:red')

plt.title('KSP Launch Telemetry Profile')
fig.tight_layout()
plt.show()