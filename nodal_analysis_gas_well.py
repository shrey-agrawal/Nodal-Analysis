import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

excel_file = 'data.xlsx'

ipr = pd.read_excel(excel_file, sheet_name='IPR')
tpr = pd.read_excel(excel_file, sheet_name='TPR')

# Function to find the intersection points between IPR and TPR curves
def find_intersection(ipr_q, ipr_p, tpr_q, tpr_p):
    # function to calculate the difference between interpolated IPR and TPR pressures
    def difference(q):
        ipr_interp = np.interp(q, ipr_q, ipr_p)
        tpr_interp = np.interp(q, tpr_q, tpr_p)
        return ipr_interp - tpr_interp

    # fsolve--->find the root of the difference function 
    intersection_q = fsolve(difference, x0=3000)[0]
    return intersection_q

# Calculate intersection points
q_190 = find_intersection(ipr['Q'], ipr['Pwf'], tpr['q'], tpr['Pwf_190'])
p_190_intersection = np.interp(q_190, ipr['Q'], ipr['Pwf'])

q_2375 = find_intersection(ipr['Q'], ipr['Pwf'], tpr['q'], tpr['Pwf_2375'])
p_2375_intersection = np.interp(q_2375, ipr['Q'], ipr['Pwf'])

q_2875 = find_intersection(ipr['Q'], ipr['Pwf'], tpr['q'], tpr['Pwf_2875'])
p_2875_intersection = np.interp(q_2875, ipr['Q'], ipr['Pwf'])

plt.figure(figsize=(10, 6))
plt.style.use('fast')

# Plot IPR
plt.plot(ipr['Q'], ipr['Pwf'], label='IPR', linewidth=1.5)

# Plot TPR
plt.plot(tpr['q'], tpr['Pwf_190'], label='TPR for 1.9" tubing', linewidth=1.5)
plt.plot(tpr['q'], tpr['Pwf_2375'], label='TPR for 2.375" tubing', linewidth=1.5)
plt.plot(tpr['q'], tpr['Pwf_2875'], label='TPR for 2.875" tubing', linewidth=1.5)

# Mark intersections
plt.scatter([q_190, q_2375, q_2875], [p_190_intersection, p_2375_intersection, p_2875_intersection], color='red', zorder=5)
plt.text(q_190, p_190_intersection, f'({q_190:.2f}, {p_190_intersection:.2f})', fontsize=8, ha='right')
plt.text(q_2375, p_2375_intersection, f'({q_2375:.2f}, {p_2375_intersection:.2f})', fontsize=8, ha='right')
plt.text(q_2875, p_2875_intersection, f'({q_2875:.2f}, {p_2875_intersection:.2f})', fontsize=8, ha='right')

#Formating
plt.xlabel('FlowRate (Mscf/D)')
plt.ylabel('Flowing BHP (Psia)')
plt.title('Nodal Analysis of Gas Well')
plt.grid()
plt.legend(loc='upper right', prop={'size': 10})
plt.show()
