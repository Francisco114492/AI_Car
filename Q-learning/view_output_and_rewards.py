import matplotlib.pyplot as plt

def main():
    try:
        with open("best_outputs.txt", "r") as f1:
            output = [tuple(map(float, line1.strip().split(","))) for line1 in f1]
    except FileNotFoundError:
        print("Error: best_outputs.txt not found! Run the training first.")

    try:
        with open("all_rewards.txt", "r") as f2:
            rewards = [tuple(map(float, line2.strip().split(","))) for line2 in f2]
    except FileNotFoundError:
        print("Error: all_rewards.txt not found! Run the training first.")

    steps = []
    steer = []

    for i in range(len(output)-1):
        steps.append(output[i][0])
        steer.append(output[i][1])

    episodes = []
    reward = []

    for j in range(len(rewards)-1):
        episodes.append(rewards[j][0])
        reward.append(rewards[j][1])

    plt.figure(figsize=(10, 5))

    plt.subplot(2, 1, 1)
    plt.plot(steps, steer, label='Steer')
    plt.title("Steering angle over distance")
    plt.xlabel("Steps")
    plt.ylabel("Steer (in radians)")
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(episodes, reward, label='Reward', color='orange')
    plt.title("Reward values over episodes")
    plt.xlabel("Episodes")
    plt.ylabel("Reward")
    plt.legend()

    plt.tight_layout()
    plt.show()
