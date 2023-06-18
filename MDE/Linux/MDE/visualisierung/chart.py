from chart import *

import matplotlib.pyplot as plt

# Define the data for the pie chart
labels = ['HB', 'An und nicht bekannt', 'An und läuft nicht', 'An und läuft']
sizes = [20, 10, 30, 40]

# Create the pie chart
plt.pie(sizes, labels=labels, autopct='%1.1f%%')

# Add a title to the chart
plt.title('Maschinenzustand')

# Display the chart
plt.show()
