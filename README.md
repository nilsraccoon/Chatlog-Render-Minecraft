# Chatlog Viewer for Minecraft

## Description

Chatlog Viewer for Minecraft is a tool designed to help players easily view their chat logs. This application provides a user-friendly GUI to browse, search, and filter chat messages from minecraft logs.

## Features

- Import and parse Minecraft log files
- Search functionality to find specific messages
- Filter messages by guild or party messages
   
## Usage

### Using the application

1. Download the latest release from the [releases page](https://github.com/nilsraccoon/Chatlog-Viewer-Minecraft/releases) and open it
2. Click on "Open Log File" and select a minecraft log.gz file (usually located at `%appdata%\.minecraft\logs\`)
3. Use the search bar to find specific messages
4. Apply filters as needed

### Running from source

1. Navigate to the project directory
2. Create a virtual environment:

    `python -m venv venv`

3. Activate the virtual environment:
   
    `venv\Scripts\activate`

4. Install the dependencies:
   
   `pip install -r requirements.txt`

5. Run the main script:
   
   `python main.py`

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Minecraft™ is a trademark of Mojang Studios. This project is not affiliated with or endorsed by Mojang Studios.
