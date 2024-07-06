# Satellite data handler

## Dependecies

This project requires [SatDump](https://www.satdump.org/download/) to work

## What is this

This simple program accepts demodulated satellite data as input, automatically transmits them to the SatDump program, which decodes them one by one into images, in accordance with the folder names. The output images are sorted by satellite name, date, time and coordinates.

*Project was developed as part of the training practice in SPBSTU*

## How to use

![image](https://github.com/Chrisnisch/SatelliteDataAutomation/assets/86834957/9732bcb2-012c-49be-aeb4-18a8a1c361a5)

- In the first field specify the path to the SatDump folder
- In the second field specify the path to satellite data
- In the third field specify the path to the folder where you want to place satellite images
- Click the button in the middle to start

### Input format
For the handler to work correctly, the input data folder must have the following format

![image](https://github.com/Chrisnisch/SatelliteDataAutomation/assets/86834957/59c3d2d9-6e8d-443c-aa3f-89e73d4aaef8)

## Supported types of data
- Aqua
- Elektro-L3
- Suomi NPP
- Terra

> The rest are at work
