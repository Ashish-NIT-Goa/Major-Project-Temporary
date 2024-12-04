import subprocess
import time
import os

# Shared file to store the values from the four terminals
shared_file = os.path.abspath('shared_values.txt')

# Ensure the shared file is created and emptied before starting
with open(shared_file, 'w') as f:
    f.write('0,0,0,0\n')  # Initial values for terminals 1, 2, 3, 4

# Function to open PowerShell and run a counting script
def open_terminal(command):
    subprocess.Popen(['start', 'powershell', '-NoExit', '-Command', command], shell=True)

# Command to count numbers from a specific starting point in PowerShell and write to file
def counting_command(terminal_number, start_from, count_to):
    return f'''
    for ($i={start_from}; $i -lt {start_from} + {count_to}; $i++) {{
        $current_values = Get-Content "{shared_file}" | Out-String
        $values = $current_values.Split(",")
        $values[{terminal_number}-1] = $i
        $new_values = $values -join ","
        Set-Content "{shared_file}" $new_values
        Write-Host "Terminal {terminal_number} count: $i"
        Start-Sleep -Seconds 1
    }}
    '''

# Command for terminal 5 to read the values from the file, sum them, and print the result
def summing_command():
    return f'''
    while ($true) {{
        $current_values = Get-Content "{shared_file}" | Out-String
        $values = $current_values.Split(",")
        $sum = 0
        foreach ($value in $values) {{ $sum += [int]$value }}
        Write-Host "Sum of all terminals: $sum"
        Start-Sleep -Seconds 1
    }}
    '''

# Number of counts per terminal
count_to = 10

# Commands for each PowerShell terminal (1-4 for counting, terminal 5 for summing)
commands = [
    counting_command(1, 1, count_to),  # Terminal 1 counts from 1
    counting_command(2, 11, count_to), # Terminal 2 counts from 11
    counting_command(3, 21, count_to), # Terminal 3 counts from 21
    counting_command(4, 31, count_to)  # Terminal 4 counts from 31
]

# Open the four counting terminals
for cmd in commands:
    open_terminal(cmd)

# Open the fifth terminal for summing the values from all four terminals
open_terminal(summing_command())
