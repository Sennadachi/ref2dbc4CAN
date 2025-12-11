# REF to DBC Converter

This repository converts `.REF` files from **[Racelogic's website](https://www.vboxautomotive.co.uk/index.php/en/customer-area/vehicle-can-database)** into `.dbc` (CAN Database) files for use with CAN bus systems.

## About REF Files

`.REF` files from Racelogic contain encoded data that needs to be extracted and converted for CAN analysis tools.

## Data Extraction Process

The conversion requires extracting specific hex data from the `.REF` file:

1. **Locate the hex data** that starts with `78 da`
2. **Position**: This data appears immediately after the serial number in the file
3. **Format**: The data is stored as binary/hex, not ASCII text

## Required Tools

- **[Free Hex Editor Neo](https://www.hhdsoftware.com/free-hex-editor)** - Used to read and extract the hex data from `.REF` files

## Usage

1. Open the `.REF` file in Free Hex Editor Neo
2. Find the serial number section
3. Locate the hex sequence starting with `78 da` immediately following the serial number
4. Extract this hex data
5. Input the extracted data into the converter

## Why Hex Editor?

The `.REF` file format stores this critical data in binary format, not as readable ASCII text. A standard text editor won't display this data correctly, which is why a hex editor is necessary to properly read and extract the required bytes.

