# REF to DBC Converter

This repository converts `.REF` files from **[Racelogic's website](https://www.vboxautomotive.co.uk/index.php/en/customer-area/vehicle-can-database)** into `.dbc` (CAN Database) files for use with CAN bus systems.

## About REF Files

`.REF` files from Racelogic contain encoded data that needs to be extracted and converted for CAN analysis tools.

## How It Works

The application provides an intuitive UI that automates the entire conversion process:

1. **Select REF file** through the file browser
2. **Automatic extraction** of compressed hex data from the REF file
3. **Automatic decompression** using zlib inflation
4. **Automatic parsing** of the CAN database structure
5. **Generates a DBC file** with proper formatting for CAN analysis tools.

This allows you to understand how your car talks.

All processing happens automatically once you select your REF file - no manual hex extraction required.

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**
    ```bash
    git clone <repository-url>
    cd ref2dbc4CAN
    ```

2. **Install required dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

### Using the UI

1. **Launch the application** by running `python ref2dbc.py`
2. **Click "Browse"** to select your `.REF` file
3. **Click "Convert"** - the application handles everything automatically
4. **Save the output** `.dbc` file to your preferred location

The UI displays conversion progress and any errors encountered during processing.

### Batch Conversion

Process multiple REF files at once through the UI's batch mode option.

## Output

The generated `.dbc` file will contain:

- CAN message definitions
- Signal mappings
- Scaling factors and units
- Min/max value ranges
- Description fields

The output is compatible with standard CAN analysis tools like CANalyzer, Busmaster, and SavvyCAN.
