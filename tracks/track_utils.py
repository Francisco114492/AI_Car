import os
import math
import json
import re

JSON_PATH = 'Tracks/assets/Track_info.json'

class Track:
    def __init__(self, track_name):
        self.base_name = track_name
        self.json_path = JSON_PATH
        self.png_path = f'images/{track_name}.png'
        self.error = None

        try:
            if self.check_track():
                self.set_data()

        except (FileNotFoundError, ValueError) as e:
            self.error = str(e)

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

    def check_track(self):
        if not os.path.isfile(self.json_path):
            raise FileNotFoundError(f"O ficheiro {self.json_path} não foi encontrado.")
        if not os.path.isfile(self.png_path):
            raise FileNotFoundError(f"O ficheiro {self.png_path} não foi encontrado.")
        with open(self.json_path, 'r', encoding='utf-8') as f:
            all_tracks = json.load(f)
        if self.base_name not in all_tracks:
            raise ValueError(f"A pista '{self.base_name}' não foi encontrada no ficheiro JSON.")
        return True

    def set_data(self):
        data = {}
        with open(self.json_path, 'r', encoding="utf-8") as file:
            track_info = json.load(file)[self.base_name]

        required_fields = ['MAP_STATS', 'START_POS', 'START_ANGLE']
        for field in required_fields:
            if field not in track_info:
                raise ValueError(f'Mandatory field "{field}" is missing on file: {self.txt_path}')

        self.map_stats = tuple(track_info['MAP_STATS'])
        self.start_pos = tuple(track_info['START_POS'])

        angle = track_info['START_ANGLE']
        if isinstance(angle, str) and angle.endswith(("º", "°")):
            self.start_angle = math.radians(float(angle[:-1]))
        else:
            self.start_angle = float(angle)
        self.bound_color = tuple(track_info.get('BOUND_COLOR', (0, 0, 0)))
        self.finish_color = tuple(track_info.get('FINISH_COLOR', (0, 255, 0)))
        self.real_distance = track_info.get('REAL_DISTANCE', None)

        self.track_name = track_info.get('NAME', self.base_name)
        self.description = track_info.get('DESCRIPTION', '')
        self.pixel_distance = track_info.get('PIXEL_DISTANCE' or 'DISTANCE', None)

        if self.pixel_distance is None:
            self.pixel_distance = self.get_distance()

    @classmethod
    def get_tracks(cls):
        """
        Loads all tracks defined in the JSON and returns a list of track objects and
        a dictionary with track names as keys and descriptions as values.
        """
        if not os.path.isfile(JSON_PATH):
            raise FileNotFoundError(f"O ficheiro JSON {JSON_PATH} não foi encontrado.")

        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            all_tracks = json.load(f)

        cls.tracks_list = []
        cls.tracks_dict = {}

        for track_name in all_tracks.keys():
            track = Track(track_name)
            cls.tracks_list.append(track)
            cls.tracks_dict[track.track_name] = track.description

        return cls.tracks_list, cls.tracks_dict

    @classmethod
    def get_track(cls, name):
        """
        Searches for a track by its name in the loaded tracks list.

        Parameters:
            name (str): Name of the track to search for.

        Returns:
            
        Return the track object if found.
        """
        for track in cls.tracks_list:
            if track.track_name == name:
                return track
        return None