import cv2
import numpy as np
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from skimage.morphology import skeletonize
from skimage import img_as_bool

# ---------- parameters you might want to tweak ----------
TRACK_PATHS=["images/Track1.png","images/Track2.png","images/Track3.png","images/Track4.png","images/Track5.png"]
START_POS=[[100,500],[120,100],[645,445],[708,2261],[521,249]] # starting position of the car for each track
START_ANGLES=[0,math.pi/2,-3*math.pi/4,-3*math.pi/4,math.pi/4]

#TRACK_PATH       = "./images/Track3.png"     # image file
#START_X, START_Y = 645, 445        # given start (image coords: x, y)
#START_DIR        = -3 * math.pi / 4
STEP_SIZE        = 2               # pixel spacing between way‑points
MAX_POINTS       = 10000           # truncate path after this many
PLOT_DOT_EVERY   = 5               # subsample when plotting (purely cosmetic)
NUM_SECTORS      = 10              # number of sectors
# ---------------------------------------------------------

colors = cm.get_cmap('hsv', NUM_SECTORS)


def generate_path(binary_img, start_xy, start_dir,
                  step=STEP_SIZE, max_pts=MAX_POINTS):
    skel = skeletonize(img_as_bool(binary_img)).astype(np.uint8)
    height, width = skel.shape

    def neighbours(pt):
        x, y = pt
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    yield (nx, ny)

    path = [start_xy]
    visited = {start_xy}
    current = start_xy
    current_dir = start_dir
    ANGLES = np.linspace(-math.pi/4, math.pi/4, 9)

    for _ in range(max_pts - 1):
        # Stop if we come back to near the start point (but avoid early exits)
        if len(path) > 50:
            dist = math.hypot(current[0] - start_xy[0], current[1] - start_xy[1])
            if dist < 5:
                print("Path looped close to start. Closing and stopping.")
                path.append(start_xy)  # Explicitly close loop
                break

        candidates = []
        for local_ang in ANGLES:
            ang = current_dir + local_ang
            nx = int(round(current[0] + math.cos(ang) * step))
            ny = int(round(current[1] + math.sin(ang) * step))
            if (0 <= nx < width and 0 <= ny < height
                and skel[ny, nx] and (nx, ny) not in visited):
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

    return path


def main(track_n):
    # 1) read track and make a binary mask: 1 == driveable (white), 0 == walls (black)
    track_path = TRACK_PATHS[track_n]
    start_x, start_y = START_POS[track_n]
    start_angle = START_ANGLES[track_n]
    gray = cv2.imread(track_path, cv2.IMREAD_GRAYSCALE)
    if gray is None:
        raise FileNotFoundError(f"Could not load {track_path}")
    _, binary_inv = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    # we want white road == 1; invert back:
    binary = cv2.bitwise_not(binary_inv)

    # 2) generate centre path
    path = generate_path(binary,
                         start_xy=(start_x, start_y),
                         start_dir=start_angle)
    
    # 3)  path division
    total_points = len(path)
    sector_len = total_points // NUM_SECTORS
    sectors = []

    for i, point in enumerate(path):
        sector_id = min(i // sector_len, NUM_SECTORS - 1)  # last sector gets leftovers
        sectors.append(sector_id)

    # Create one checkpoint per sector (first point of each sector slice)
    checkpoints = []
    for i in range(NUM_SECTORS):
        index = i * sector_len
        if index < len(path):
            checkpoints.append(path[index])


    # 4) plot
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.imshow(cv2.cvtColor(cv2.imread(track_path), cv2.COLOR_BGR2RGB))
    xs, ys = zip(*path)
    ax.plot(xs[::PLOT_DOT_EVERY], ys[::PLOT_DOT_EVERY],
            linewidth=1)               # default blue line & dots
    # Plot each path point with its sector color
    
    for (x, y), sector in zip(path, sectors):
        ax.plot(x, y, marker='o', markersize=2, color=colors(sector), alpha=0.7)

    for (x, y) in checkpoints:
        ax.plot(x, y, marker='o', markersize=5, alpha=0.7)
    
    ax.scatter([xs[0]], [ys[0]], marker='o', s=30, zorder=5)  # start marker
    ax.set_title(f"Centre‑line path – {len(path)} points")
    ax.axis('off')
    plt.tight_layout()
    plt.show()

    # Save path to file
    with open("track_path.txt", "w") as f:
        for x, y in path:
            f.write(f"{x} {y}\n")

    # Save sectors to file
    with open("track_path_sectors.txt", "w") as f:
        f.write("x y sector_id\n")
        for (x, y), sector in zip(path, sectors):
            f.write(f"{x} {y} {sector}\n")

    with open("track_checkpoints.txt", "w") as f:
        f.write("x y sector_id\n")
        for sector_id, (x, y) in enumerate(checkpoints):
            f.write(f"{x} {y} {sector_id}\n")
    return 0

