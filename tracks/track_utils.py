import cv2
import numpy as np
import os
import math
import json

from skimage.morphology import skeletonize
from skimage import img_as_bool

JSON_PATH = 'tracks/assets/Track_info.json'

class Track:
    def __init__(self, track_name):
        self.base_name = track_name
        self.json_path = JSON_PATH
        self.png_path = f'tracks/assets/{track_name}.png'
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
        # Try both keys: PIXEL_DISTANCE or DISTANCE
        self.pixel_distance = track_info.get('PIXEL_DISTANCE', track_info.get('DISTANCE', None))

        # If pixel distance missing, compute it using the centerline generator and persist to JSON
        if self.pixel_distance is None:
            try:
                self.pixel_distance = self.get_distance()
                # Persist into the JSON file under PIXEL_DISTANCE for this track
                with open(self.json_path, 'r', encoding='utf-8') as jf:
                    all_tracks = json.load(jf)
                # Ensure the key exists
                if self.base_name in all_tracks:
                    all_tracks[self.base_name]['PIXEL_DISTANCE'] = self.pixel_distance
                    # Write back safely
                    with open(self.json_path, 'w', encoding='utf-8') as jf:
                        json.dump(all_tracks, jf, ensure_ascii=False, indent=4)
                else:
                    # Unexpected: track not present when saving
                    raise ValueError(f"Track {self.base_name} not present in JSON when trying to save PIXEL_DISTANCE")
            except Exception as e:
                # Do not crash; record error and leave pixel_distance as None
                self.error = f"Failed to compute or save PIXEL_DISTANCE: {e}"
                self.pixel_distance = None

    def get_distance(self, step=2, max_pts=10000):
        """Compute the centreline pixel distance for this track using its image."""
        # desvantagem: já não desenha o path criado, tenho de analizar, pode valer a pena manter
        gray = cv2.imread(self.png_path, cv2.IMREAD_GRAYSCALE)
        if gray is None:
            raise FileNotFoundError(f"Could not load image file: {self.png_path}")

        # Create binary image: white road == 1, black == walls
        _, binary_inv = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        binary = cv2.bitwise_not(binary_inv)

        # Skeletonize to get the centerline
        skel = skeletonize(img_as_bool(binary)).astype(np.uint8)
        height, width = skel.shape
        start_x, start_y = map(int, self.start_pos)
        start_dir = self.start_angle

        path = [(start_x, start_y)]
        visited = {(start_x, start_y)}
        current = (start_x, start_y)
        current_dir = start_dir
        ANGLES = np.linspace(-math.pi / 4, math.pi / 4, 9)

        def neighbours(pt):
            x, y = pt
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        yield (nx, ny)

        for _ in range(max_pts - 1):
            if len(path) > 50:
                dist = math.hypot(current[0] - start_x, current[1] - start_y)
                if dist < 5:
                    break

            candidates = []
            for local_ang in ANGLES:
                ang = current_dir + local_ang
                nx = int(round(current[0] + math.cos(ang) * step))
                ny = int(round(current[1] + math.sin(ang) * step))
                if (0 <= nx < width and 0 <= ny < height and skel[ny, nx] and (nx, ny) not in visited):
                    candidates.append(((nx, ny), ang))

            if not candidates:
                for n in neighbours(current):
                    if skel[n[1], n[0]] and n not in visited:
                        ang = math.atan2(n[1] - current[1], n[0] - current[0])
                        candidates.append((n, ang))
                if not candidates:
                    break

            next_pt, next_dir = min(candidates, key=lambda c: abs(c[1] - current_dir))
            path.append(next_pt)
            visited.add(next_pt)
            current, current_dir = next_pt, next_dir

        # Compute total Euclidean distance
        total = 0.0
        for (x1, y1), (x2, y2) in zip(path[:-1], path[1:]):
            total += math.hypot(x2 - x1, y2 - y1)
        return total

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