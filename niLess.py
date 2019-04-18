#
# niLess.py
#
import matplotlib.pyplot as plt
import math
import numpy as np

import sys
# Process command line arguments

if (len(sys.argv) < 3):
    print('argv too short, usage: python3 <interval> <dosage>')
    print('Using default values for interval (8) and dosage (100)')

    Vinterval = 8   # 8 hours between doses
    Vdosage = 100   # dosage 100mg
else:
    Vinterval = int(sys.argv[1])  # hours between doses
    Vdosage = int(sys.argv[2])    # dosage


half_life = 42            # Polyjuice Potion half-life
interval = Vinterval      # Interval between doses
MEC = 80.                 # Effective concentration
MTC = 160.                 # Toxic concentration
volume = 3000             # blood plasma volume
dosage = Vdosage*1000         # dosage 100mg 
absorption_fraction = 0.42
drug_in_system = 0        # initial amount of drug in system
ln05 = math.log(0.5)
elimination_constant = -ln05/half_life
pulse = 0
entering = absorption_fraction * pulse * dosage
elimination = elimination_constant * drug_in_system
concentration = drug_in_system/volume

simulation_time = 500     # simulation time 500
time_step_size = 1        # time step = 1 hour
num_steps = int(simulation_time/time_step_size)
cumulative_time = 0.0     # initial time = 0

print('\nPARAMETERS\n')

print('niLess half-life:\t',half_life)
print('Interval between doses: \t', interval)
print('Effective concentration:\t', MEC)
print('Toxic concentration: \t', MTC)
print('Blood plasma volume: \t', volume)
print('Dosage: \t', dosage)
print('Absorption fraction: \t', absorption_fraction)
print('Initial amt drug in system: \t', drug_in_system)
print('Elimination constant: \t', elimination_constant)
print('Simulation time (hrs): \t', simulation_time)
print('Time step size: \t', time_step_size)
print('Number of timesteps: \t', num_steps)

values = np.empty(num_steps) 

for time_step in range (num_steps):
    values[time_step] = concentration
    if (time_step % interval == 0):
       pulse = 1
    else:
       pulse = 0
    entering = absorption_fraction * pulse * dosage
    elimination = elimination_constant * drug_in_system
    drug_in_system = drug_in_system - elimination + entering
    concentration = drug_in_system / volume

times = np.linspace(0, simulation_time - time_step_size, num_steps)
# print(values)

MECline = np.full(num_steps, MEC)
MTCline = np.full(num_steps, MTC)

if values.mean() > MEC and values.mean() < MTC and values.max() < MTC:
    plt.figure()
    plt.title('niLess Concentration')
    plt.xlabel('Time (hours)')
    plt.ylabel('Concentration')
    plt.plot(times, values, '-', times, MECline, 'g-', times, MTCline, 'r-')
    plt.ylim(0, 200)
    #plt.plot(values)
    plt.savefig('niLess_dosage_' + 'I' + str(Vinterval)+'_D' + str(Vdosage) + '.png')
    print('\nRESULTS\n')
    print('Minimum value: \t', values.min())
    print('Maximum value: \t', values.max())
    print('Average value: \t', values.mean())
    effective = 0
    while effective < len(values) and values[effective] < MEC :
        effective += 1
        print(len(values))
        print(effective)
    if (effective < len(values)):
        print('Effective at : \t', effective)
        print('Minimum post-effective value: \t', values[effective:].min())
        print('Maximum post-effective value: \t', values[effective:].max())
        print('Average post-effective value: \t', values[effective:].mean())
    else:
        print('Effective at : \t', 0)
        print('Minimum post-effective value: \t', 0)
        print('Maximum post-effective value: \t', 0)
        print('Average post-effective value: \t', 0)

