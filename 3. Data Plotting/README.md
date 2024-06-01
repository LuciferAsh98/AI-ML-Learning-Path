# Cybersecurity Data Visualization 📊

This project uniquely integrates the process of visualization with the cybersecurity data by providing various kinds of plots—scatter, bar, and pie. These visualizations offer insights into attack types, frequencies, incident response times, monthly security incidents, and budget allocations.

## Used Libraries 📚

We leverage the below libraries for data manipulation and visualization:

- **pandas**: Data manipulation and analysis.
- **matplotlib.pyplot**: For plotting.

## Loading Data 📂

We read data from an Excel file to read each sheet into a separate DataFrame:

- **Attack Types and Frequencies**: Types of attacks and frequency of attacks.
- **Incident Response Times**: Data on the time to respond to various incidents.
- **Security Incidents Monthly**: Logs of the security incidents on a month-to-month basis.
- **Security Budget Allocation**: The amount designated or budgeted for spending in each security category.

## Visualizations 🎨

### Scatter Plot 🔵

A scatter plot illustrating the frequencies of the attack kinds vs their kinds, with the x-axis representing the attack kinds and the y-axis representing attack kinds.

### Bar Chart 📊

The bar chart shows the frequency of different types of attacks, making a comparison clear.

### Incident History 📅 Bar Chart

This bar chart visualizes the number of security incidents each month and allows for the analysis of trends.

### Pie Chart 🍰

The pie chart below illustrates the security budget item distribution in the various categories, thus giving a clear impression of the resource allocation.

## Subplots Layout 🖼️

Create a 2x2 grid of subplots with one of the visualizations in each:

1. **Scatter Plot**: Shows the number of attack types.
2. **Bar Chart**: Represents the frequency of the attack types.
3. **Pie Chart**: Visually representing the security budget allocation.
4. **Monthly Incidents Bar Graph**: Depicts the number of security incidents from one month to the next.

The visualizations provide an integrated view of cybersecurity data, enabling the data to be more easily understood across all aspects of cybersecurity incidents and budget allocation.

Feel free to explore and look at these visualizations to understand the data better!
