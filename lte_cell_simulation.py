import numpy as np
import matplotlib.pyplot as plt


cell_radius = 500  
num_users = 20
num_rbs = 50  
bandwidth_per_rb = 180e3  
tx_power_dbm = 43  
noise_dbm = -100
num_slots = 50  
shadow_std_db = 8  
mobility_std = 10  
scheduler = 'PF'  


def path_loss(distance):
    return 128.1 + 37.6 * np.log10(distance / 1000)

# --- CQI to achievable data rate per RB (simplified, Mbps) ---
cqi_to_rate = np.linspace(0.1, 2.0, 15)  # 0.1 to 2 Mbps per RB

# --- Initialize user positions ---
angles = np.random.uniform(0, 2 * np.pi, num_users)
radii = cell_radius * np.sqrt(np.random.uniform(0, 1, num_users))
x = radii * np.cos(angles)
y = radii * np.sin(angles)

# --- Store throughput history ---
throughput_history = np.zeros((num_users, num_slots))

# --- Round Robin pointer ---
rr_pointer = 0

for slot in range(num_slots):
    # User mobility: random walk
    x += np.random.normal(0, mobility_std, num_users)
    y += np.random.normal(0, mobility_std, num_users)
    # Keep users within cell
    r = np.sqrt(x**2 + y**2)
    outside = r > cell_radius
    x[outside] *= cell_radius / r[outside]
    y[outside] *= cell_radius / r[outside]
    distances = np.sqrt(x**2 + y**2)
    distances[distances < 1] = 1  # Avoid log(0)

    # Shadow fading
    shadow = np.random.normal(0, shadow_std_db, num_users)
    pl = path_loss(distances) + shadow
    rssi_dbm = tx_power_dbm - pl

    # CQI based on RSSI
    cqi = np.clip(((rssi_dbm + 100) / 5).astype(int), 1, 15)

    # Scheduling
    rb_allocation = np.zeros(num_users, dtype=int)
    inst_rate = cqi_to_rate[cqi - 1]
    if slot == 0:
        past_throughput = np.ones(num_users)
    # Proportional Fair
    if scheduler == 'PF':
        for rb in range(num_rbs):
            pf_metric = inst_rate / past_throughput
            user = np.argmax(pf_metric)
            rb_allocation[user] += 1
            past_throughput[user] += inst_rate[user]
    # Round Robin
    elif scheduler == 'RR':
        for rb in range(num_rbs):
            user = (rr_pointer + rb) % num_users
            rb_allocation[user] += 1
        rr_pointer = (rr_pointer + num_rbs) % num_users
        past_throughput += inst_rate * rb_allocation
    # Max C/I
    elif scheduler == 'MaxCI':
        for rb in range(num_rbs):
            user = np.argmax(inst_rate)
            rb_allocation[user] += 1
        past_throughput += inst_rate * rb_allocation

    # Throughput per user this slot
    user_throughput = rb_allocation * inst_rate
    throughput_history[:, slot] = user_throughput

# --- Plot cell and users (last slot) ---
plt.figure(figsize=(7,7))
circle = plt.Circle((0, 0), cell_radius, color='b', fill=False, linestyle='--')
plt.gca().add_patch(circle)
sc = plt.scatter(x, y, c=throughput_history[:, -1], cmap='viridis', s=80, label='Users')
plt.colorbar(sc, label='Throughput (Mbps)')
plt.title(f'LTE Cell User Distribution and Throughput ({scheduler} Scheduling)')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.axis('equal')
plt.grid(True)
plt.show()

# --- Plot throughput over time for each user ---
plt.figure(figsize=(10,5))
for i in range(num_users):
    plt.plot(throughput_history[i], label=f'User {i+1}')
plt.xlabel('Time Slot')
plt.ylabel('Throughput (Mbps)')
plt.title(f'User Throughput Over Time ({scheduler} Scheduling)')
plt.grid(True)
plt.tight_layout()
plt.show()


print("User\tCQI\tRBs\tThroughput (Mbps)")
for i in range(num_users):
    print(f"{i+1}\t{cqi[i]}\t{rb_allocation[i]}\t{throughput_history[i, -1]:.2f}")

print(f"\nAverage user throughput (last slot): {np.mean(throughput_history[:, -1]):.2f} Mbps")