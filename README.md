
# Spotify Exporter

Spotify Exporter is a simple Python project designed to export your Spotify playlist data into a CSV file. It uses the `spotipy` library and the Spotify API for data retrieval, making use of OAuth2 authentication.

## Features

- Exports Spotify playlists, liked songs and artists to CSV.

## Requirements

- Python 3.x
- `spotipy` library
- A Spotify Developer account with API credentials.

## Installation

1. Clone this repository.
   ```bash
   git clone https://github.com/ohoextra/SpotifyExporter.git
   ```
2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Set up your Spotify developer credentials by creating an app in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and copying the `client_id` and `client_secret` into the `SpotifyDevCreds.txt` file.

2. Run the script:
   ```bash
   python SpotifyExporter.py
   ```

3. Follow the on-screen instructions to authenticate with Spotify and export your playlists.

## Contributing

Feel free to fork this project and create pull requests. Contributions are always welcome.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
