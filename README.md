# Site Connectivity Checker

A Python tool that checks the connectivity and response time of multiple websites simultaneously. Available in both command-line and GUI versions.

## Features

- Check multiple websites at once
- Measure response time in milliseconds
- Display HTTP status codes
- Show error messages if sites are unreachable
- Concurrent checking for faster results
- Clean, formatted output
- Modern PyQt5 graphical interface (GUI version)
- Responsive and user-friendly design
- Real-time status updates
- Sortable results table

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Version
Run the script from the command line with one or more URLs as arguments:

```bash
python site_checker.py google.com github.com python.org
```

### GUI Version
Run the GUI version with:

```bash
python site_checker_gui.py
```

The GUI version provides:
- A text input field for entering URLs (comma-separated)
- A "Check Sites" button to start the check
- A status label showing current progress
- A table displaying results with columns for:
  - URL
  - Status Code
  - Response Time
  - Error Messages (if any)
- Modern, high-contrast interface with:
  - Clear typography
  - Responsive design
  - Visual feedback for interactions
  - Grid-based results display

You can specify URLs with or without the `http://` or `https://` prefix. The script will automatically add `https://` if no protocol is specified.

## Output

### Command Line Version
The script will display a table with the following information for each URL:
- URL (truncated if too long)
- HTTP Status Code
- Response Time in milliseconds
- Any error messages (if the site is unreachable)

### GUI Version
Results are displayed in a clean, modern table interface with:
- Sortable columns
- Auto-resizing columns
- Status updates during checking
- Error messages in a dedicated column
- High-contrast text for better readability
- Visual separation between rows
- Clear status indicators

## Example Output

### Command Line Version
```
Site Connectivity Check Results
================================================================================
URL                                      Status     Response Time (ms)    Error
--------------------------------------------------------------------------------
https://google.com                       200        123.45
https://github.com                       200        234.56
https://python.org                       200        345.67
```

### GUI Version
The GUI version provides a modern, interactive interface with the same information displayed in a table format, featuring:
- Real-time status updates
- Clear visual hierarchy
- Easy-to-read results
- Interactive table controls 