# Group Divider Application

A Python application designed to automatically create and manage group divisions for educational settings.

## Overview

Group Divider is a practical solution for educators and class coordinators who need to efficiently divide students into groups. Using principles of discrete mathematics, particularly combinations and probability, this application automates the process of creating fair and balanced groups.

## Features

- **Student Management**: Add, delete, and manage student information
- **CSV Integration**: Import and export student data from CSV files
- **Automated Group Creation**: Generate multiple possible group combinations
- **Group Visualization**: View different group configurations
- **Combination Calculation**: Calculate the number of possible combinations

## Technology Stack

- **PyQt5**: For the graphical user interface
- **CSV Module**: For data management
- **Random Module**: For group randomization
- **Math Module**: For combination calculations

## How to Use

### Student Management

1. Add students by entering names and clicking "Add Student"
2. Remove students by selecting them and clicking "Delete Selected"
3. Save your student list to CSV using "Save to CSV"
4. Import existing student lists with "Load from CSV"

### Creating Groups

1. Enter the desired number of groups
2. Click "Calculate Possibilities" to see potential combinations
3. Enter the number of combinations you want to generate
4. Click "Generate Groups" to create and save the combinations to CSV

### Viewing Groups

1. Load previously generated combinations using "Load Combinations"
2. Select a specific combination from the list
3. Click "View Selected Groups" to see the detailed group breakdown

## Mathematical Principles

This application utilizes discrete mathematics concepts:
- **Combination formula**: C(n,r) = n!/[r!(n-r)!] for calculating possible groupings
- **Probability concepts**: Ensuring equal distribution of students among groups

## Developers

Developed by Group 6 (UNNES - SI 23 R2):
- Syifa Maulidina (2304140046)
- Hammam Jitapsara (2304140050)
- Aisyah Qurrota A'yun (2304140057)
- Saskia Khaerani (2304140061)
- Arif Satria Tama (2304140063)
