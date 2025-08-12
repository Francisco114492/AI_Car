import os
import math

class Track:
    def __init__(self, track_name):
        self.track_name = track_name
        self.txt_path = f'images/{track_name}.txt'
        self.png_path = f'images/{track_name}.png'
        self.error = None

        try:
            if self.get_track():
                self.set_data()
        except (FileNotFoundError, ValueError) as e:
            self.error = str(e)

    def get_track(self):
        if not os.path.isfile(self.txt_path):
            raise FileNotFoundError(f"O ficheiro {self.txt_path} não foi encontrado.")
        if not os.path.isfile(self.png_path):
            raise FileNotFoundError(f"O ficheiro {self.png_path} não foi encontrado.")
        return True

    def set_data(self):
        data = {}
        with open(self.txt_path, 'r') as file:
            for line in file:
                if '=' not in line:
                    continue
                key, value = line.strip().split('=')
                data[key.strip()] = value.strip()

        required_fields = ['MAP_STATS', 'START_POS', 'START_ANGLE']
        for field in required_fields:
            if field not in data:
                raise ValueError(f'O campo obrigatório "{field}" está em falta no ficheiro: {self.txt_path}')

        angle_str = data['START_ANGLE']
        # para depois verificar se o ângulo usa "º" ou "°", ou seja, se está em graus

        self.map_stats = tuple(map(int, data['MAP_STATS'].split(',')))
        self.start_pos = tuple(map(int, data['START_POS'].split(',')))
        self.start_angle = math.radians(float(angle_str[:-1])) if angle_str.endswith(("º", "°")) else float(angle_str)
        self.bound_color = tuple(map(int, data.get('BOUND_COLOR', '0,0,0').split(',')))
        self.finish_color = tuple(map(int, data.get('FINISH_COLOR', '0,255,0').split(',')))

        return True