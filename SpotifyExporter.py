import spotipy
from spotipy.oauth2 import SpotifyOAuth
import keyring
import os
import csv
import traceback

# Spotify Service names for keyring
SERVICE_NAME_CLIENT_ID = 'spotify_client_id'
SERVICE_NAME_CLIENT_SECRET = 'spotify_client_secret'
SERVICE_NAME_REDIRECT_URI = 'spotify_redirect_uri'

# Function to prompt the user for credentials and save them using keyring
def prompt_for_credentials():
    client_id = input("ClientID: ")
    client_secret = input("ClientSecret: ")
    redirect_uri = "http://localhost:8888/callback"

    keyring.set_password(SERVICE_NAME_CLIENT_ID, 'user', client_id)
    keyring.set_password(SERVICE_NAME_CLIENT_SECRET, 'user', client_secret)
    keyring.set_password(SERVICE_NAME_REDIRECT_URI, 'user', redirect_uri)

    return client_id, client_secret, redirect_uri

# Function to load credentials from keyring
def load_credentials():
    client_id = keyring.get_password(SERVICE_NAME_CLIENT_ID, 'user')
    client_secret = keyring.get_password(SERVICE_NAME_CLIENT_SECRET, 'user')
    redirect_uri = keyring.get_password(SERVICE_NAME_REDIRECT_URI, 'user')
    return client_id, client_secret, redirect_uri

# Function to create 'Exports' and 'MyPlaylists' directories if they don't exist
def ensure_exports_folders():
    export_dir = 'Exports'
    playlists_dir = os.path.join(export_dir, 'MyPlaylists')
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    if not os.path.exists(playlists_dir):
        os.makedirs(playlists_dir)
    return export_dir, playlists_dir

# Function to load existing tracks from a CSV file
def load_existing_tracks(file_path):
    existing_tracks = set()
    if os.path.exists(file_path):
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header
            for row in reader:
                existing_tracks.add(row[0])  # Assuming 'Artist - Song Name' format is in the first column
    return existing_tracks

# Function to write liked songs to a CSV file
def write_liked_songs_to_csv(saved_tracks):
    _, playlists_dir = ensure_exports_folders()
    file_name = 'MyLikes.csv'
    file_path = os.path.join(playlists_dir, file_name)
    
    print(f"{len(saved_tracks)} liked songs found online.")
    existing_tracks = load_existing_tracks(file_path)
    new_tracks = [track for track in saved_tracks if track not in existing_tracks]

    if new_tracks:
        new_tracks = sorted(new_tracks)  # Sort alphabetically
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if os.stat(file_path).st_size == 0:
                writer.writerow(['Artist - Song Name'])
            writer.writerows([[track] for track in new_tracks])
        print(f"{len(new_tracks)} new liked songs exported.")

# Function to write unique songs to MySongs.csv
def write_tracks_to_csv(all_tracks):
    export_dir, _ = ensure_exports_folders()
    file_name = 'MySongs.csv'
    file_path = os.path.join(export_dir, file_name)
    
    existing_tracks = load_existing_tracks(file_path)
    new_tracks = [track for track in all_tracks if track not in existing_tracks]

    if new_tracks:
        new_tracks = sorted(new_tracks)  # Sort alphabetically
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if os.stat(file_path).st_size == 0:
                writer.writerow(['Artist - Song Name'])
            writer.writerows([[track] for track in new_tracks])
        print(f"{len(new_tracks)} new songs exported to MySongs.csv.")

# Function to write unique artists to MyArtists.csv
def write_artists_to_csv(all_tracks):
    export_dir, _ = ensure_exports_folders()
    file_name = 'MyArtists.csv'
    file_path = os.path.join(export_dir, file_name)
    
    existing_artists = load_existing_tracks(file_path)
    new_artists = {track.split(" - ")[0] for track in all_tracks if track.split(" - ")[0] not in existing_artists}

    if new_artists:
        new_artists = sorted(new_artists)  # Sort alphabetically
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if os.stat(file_path).st_size == 0:
                writer.writerow(['Artist'])
            writer.writerows([[artist] for artist in new_artists])
        print(f"{len(new_artists)} new artists exported to MyArtists.csv.")

# Function to retrieve playlist tracks
def write_playlists_to_csv():
    _, playlists_dir = ensure_exports_folders()
    all_playlist_tracks = []

    playlists = sp.current_user_playlists()
    while playlists:
        for playlist in playlists['items']:
            playlist_name = playlist['name']
            playlist_id = playlist['id']
            playlist_tracks = []

            results = sp.playlist_tracks(playlist_id)
            while results:
                for item in results['items']:
                    track = item['track']
                    artist_name = track['artists'][0]['name']
                    song_name = track['name']
                    playlist_tracks.append(f"{artist_name} - {song_name}")
                results = sp.next(results) if results['next'] else None

            all_playlist_tracks.extend(playlist_tracks)

            playlist_file = os.path.join(playlists_dir, f"{playlist_name}.csv")
            existing_tracks = load_existing_tracks(playlist_file)
            new_tracks = [track for track in playlist_tracks if track not in existing_tracks]

            if new_tracks:
                new_tracks = sorted(new_tracks)  # Sort alphabetically
                with open(playlist_file, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    if os.stat(playlist_file).st_size == 0:
                        writer.writerow(['Artist - Song Name'])
                    writer.writerows([[track] for track in new_tracks])
                print(f"{len(new_tracks)} new tracks exported to '{playlist_name}.csv'.")
            else:
                print(f"No new tracks to export for '{playlist_name}'.")
        playlists = sp.next(playlists) if playlists['next'] else None

    return all_playlist_tracks

# Main function
def main():
    try:
        print("Starting Spotify export process...")  # Debugging statement

        # Authenticate and log into Spotify
        print("Loading credentials...")  # Debugging statement
        client_id, client_secret, redirect_uri = load_credentials()
        if not client_id or not client_secret or not redirect_uri:
            print("Prompting for credentials...")  # Debugging statement
            client_id, client_secret, redirect_uri = prompt_for_credentials()

        SCOPE = 'user-library-read playlist-read-private'
        global sp
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=SCOPE
        ))

        print("Retrieving liked songs...")  # Debugging statement
        # Retrieve liked songs
        saved_tracks = []
        results = sp.current_user_saved_tracks(limit=9999)
        while results:
            for item in results['items']:
                track = item['track']
                artist_name = track['artists'][0]['name']
                song_name = track['name']
                saved_tracks.append(f"{artist_name} - {song_name}")
            results = sp.next(results) if results['next'] else None

        # Export 'Liked Songs'
        write_liked_songs_to_csv(saved_tracks)

        # Export playlists
        print("Retrieving playlists...")  # Debugging statement
        playlist_tracks = write_playlists_to_csv()

        # Combine saved and playlist tracks
        all_tracks = set(saved_tracks + playlist_tracks)

        # Export unique songs and artists
        print("Exporting unique songs and artists...")  # Debugging statement
        write_tracks_to_csv(list(all_tracks))
        write_artists_to_csv(list(all_tracks))

        print("Spotify export process completed successfully!")

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()  # Print full traceback for detailed debugging

    input("Press any key to exit...")  # Pause to keep console open

if __name__ == "__main__":
    main()
