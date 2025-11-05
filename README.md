# Vehicle Path and Speed Optimization Simulator

This project simulates and optimizes the path and velocity profile of a vehicle moving along a track.  
It includes algorithms for path generation, trajectory optimization, and performance visualization.
This version is still in development, but you can find a functional one here: 
https://github.com/Francisco114492/Trabalhos_Praticos/tree/main/FIA/_Pt2

---

## Requirements

- **Python 3.11** or later  
- Required Python libraries can be installed using the following commands:

```bash
# Create and activate a virtual environment
python -m venv ProjectEnv
source ProjectEnv/bin/activate   # On Windows: ProjectEnv\Scripts\activate (no 'source' command)

# Install dependencies
pip install -r requirements.txt
```

## Code Structure

```
.
├── cars/
│   ├── car_base.py # car base class
│   └── ...
├── neural_networks/ # nn base class
│   ├── neural_network.py # base class
│   └── ...
├── tracks/
│   ├── track_utils.py
│   └── assets/ # images and information of tracks
│       ├── Track_info.json
│       ├── Track1.png
│       ├── Track2.png
│       └── ...
├── ui_utils/
│   ├── assets/
│   │   └── #images used by utils
│   ├── components/ # reusable UI components
│   │   ├── button.py
│   │   ├── slider.py
│   │   ├── textbox.py
│   │   └── ...
│   ├── core/ # core UI 
│   │   ├── item.py
│   │   ├── menu.py
│   │   └── manager.py
│   ├── screens/
│   │   ├── main_menu.py
│   │   └── simulation.py
│   └── utils/
│       ├── colors.py
│       ├── fonts.py
│       └── themes.py
└── menu.py # main file used to run
```