import subprocess
import time
import random

# Function to open PowerShell and run a counting script
def open_terminal(command):
    subprocess.Popen(['start', 'powershell', '-NoExit', '-Command', command], shell=True)

# Command to count numbers from a specific starting point in PowerShell and print to the console
def counting_command(terminal_number, start_from):
    return f'''
    $start = {start_from}
    for ($i=0; $i -lt 10; $i++) {{
        $value = $start + $i
        Write-Host "Terminal {terminal_number} counting: $value"  # Print on screen
        Start-Sleep -Seconds 1;  # Pause for 1 second
    }}
    '''

# Command for terminal 5 to sum the values and print the result
def summing_command():
    return f'''
    $values = @(0, 0, 0, 0)  # Initialize an array for the values
    while ($true) {{
        # Simulate getting values from counting terminals
        # Randomly generate values for demonstration (replace this logic with actual value retrieval)
        for ($i=0; $i -lt 4; $i++) {{
            $values[$i] = $i * 10 + (Get-Random -Minimum 0 -Maximum 10)  # Simulating the latest values
        }}
        
        # Calculate the sum
        $sum = ($values | Measure-Object -Sum).Sum
        Write-Host "Sum of all terminals: $sum"  # Print sum
        Start-Sleep -Seconds 1  # Pause for 1 second
    }}
    '''

# Starting values for each terminal
start_values = [1, 11, 21, 31]  # Change these values as needed

# Commands for each PowerShell terminal (1-4)
commands = [
    counting_command(1, start_values[0]),  # Terminal 1 starts from 1
    counting_command(2, start_values[1]),  # Terminal 2 starts from 11
    counting_command(3, start_values[2]),  # Terminal 3 starts from 21
    counting_command(4, start_values[3])   # Terminal 4 starts from 31
]

# Open the four counting terminals
for cmd in commands:
    open_terminal(cmd)

# Open the fifth terminal for summing the values from all four terminals
open_terminal(summing_command())