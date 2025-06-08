# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a MicroPython project for a remote-controlled LED lamp ("lampada-ines"). It creates a web server that allows users to control a NeoPixel LED strip via a web interface, associating colors with emotions.

## Architecture

The project consists of a single main.py file that:
- Connects to WiFi network
- Sets up a NeoPixel strip with 44 LEDs on pin 0
- Runs a web server on port 80
- Serves an HTML interface for color control
- Handles HTTP requests to change LED colors based on emotions or custom RGB values

## Key Components

- WiFi credentials are stored in wifi_config.py (excluded from git)
- LED configuration: 44 NeoPixels on GPIO pin 0
- Web interface allows selection of emotion-based colors (gioia, rabbia, paura, disgusto, tristezza, ansia, noia)
- Special effects: rainbow animation
- Custom color picker for RGB values

## Development Notes

This is a MicroPython project intended to run on an embedded device (likely ESP32/ESP8266). No traditional Python development tools (pip, pytest, etc.) apply here. Code deployment requires flashing to the microcontroller.