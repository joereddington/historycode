import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.dates as mdates

def time_to_float(t):
    return t.hour + t.minute / 60 + t.second / 3600

def plot_internet_usage(file_path, days_back=14, output_path='site/slots.png'):
    # Load the data from the CSV file
    data = pd.read_csv(file_path)
    
    # Convert the 'Date' column to datetime
    data['Date'] = pd.to_datetime(data['Date'])
    
    # Filter the data to include only the last 'days_back' days
    cutoff_date = datetime.now() - timedelta(days=days_back)
    data = data[data['Date'] >= cutoff_date]
    
    # Convert the 'First Access' and 'Last Access' times to datetime.time objects for plotting
    data['First Access'] = pd.to_datetime(data['First Access'], format='%H:%M:%S').dt.time
    data['Last Access'] = pd.to_datetime(data['Last Access'], format='%H:%M:%S').dt.time
    
    # Convert times to float for plotting
    data['First Access Float'] = data['First Access'].apply(time_to_float)
    data['Last Access Float'] = data['Last Access'].apply(time_to_float)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Add gray background for hours outside 9 AM to 5 PM
    ax.axhspan(6, 9, facecolor='lightgray', alpha=0.3)
    ax.axhspan(17, 23, facecolor='lightgray', alpha=0.3)
    
    # Plot the bars for each date
    for _, row in data.iterrows():
        ax.bar(row['Date'], row['Last Access Float'] - row['First Access Float'], 
               bottom=row['First Access Float'], width=0.8, color='skyblue', edgecolor='blue')

    # Formatting the plot
    ax.set_xlabel('Date')
    ax.set_ylabel('Time of Day')
    ax.set_title('Internet Usage Times Over the Last {} Days'.format(days_back))
    
    # Set the y-axis to show time of day in hours
    ax.set_ylim(6, 23)
    ax.yaxis.set_major_locator(plt.MultipleLocator(1))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):02d}:00'))
    
    # Add light grid lines for 6 AM, 12 PM, and 6 PM
    ax.axhline(6, color='lightgrey', linestyle='--', linewidth=0.5)
    ax.axhline(12, color='lightgrey', linestyle='--', linewidth=0.5)
    ax.axhline(18, color='lightgrey', linestyle='--', linewidth=0.5)
    
    # Set x-axis to show all weekdays
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%a'))
    
    # Rotate x-axis labels for better readability
#    plt.xticks(rotation=45, ha='right')
    
    # Adjust layout and save the plot
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

# Example usage
plot_internet_usage('site/daily_access_times.csv', days_back=14, output_path='site/slots.png')
