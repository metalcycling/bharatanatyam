# %% Modules

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# %% Global variables

NUM_MARKERS = 6
CHEST = 0
STOMACH = 1
LEFT_KNEE = 2
RIGHT_KNEE = 3
LEFT_FOOT = 4
RIGHT_FOOT = 5

line_width = 2
marker_size = 8

label_size = 16
ticks_size = 15
legend_size = 16

# %% Data

jump_types = ["1d", "2d"]

good = { jump_type: { "time": None, "pos": { "x": None, "y": None }, "vel": { "x": None, "y": None } } for jump_type in jump_types }
bad  = { jump_type: { "time": None, "pos": { "x": None, "y": None }, "vel": { "x": None, "y": None } } for jump_type in jump_types }

for jump_type in jump_types:
    # Good motion
    good_raw = np.stack([np.loadtxt("data/good/%s/marker_%d.txt" % (jump_type, marker_id + 1)) for marker_id in range(NUM_MARKERS)])

    good[jump_type]["time"] = good_raw[0, :, 0]

    good[jump_type]["pos"]["x"] = good_raw[:, :, 1]
    good[jump_type]["pos"]["y"] = good_raw[:, :, 2]

    good[jump_type]["vel"]["x"] = np.stack([np.gradient(good[jump_type]["pos"]["x"][mid], good[jump_type]["time"]) for mid in range(NUM_MARKERS)])
    good[jump_type]["vel"]["y"] = np.stack([np.gradient(good[jump_type]["pos"]["y"][mid], good[jump_type]["time"]) for mid in range(NUM_MARKERS)])

    # Bad motion
    bad_raw = np.stack([np.loadtxt("data/bad/%s/marker_%d.txt" % (jump_type, marker_id + 1)) for marker_id in range(NUM_MARKERS)])

    bad[jump_type]["time"] = bad_raw[0, :, 0]

    bad[jump_type]["pos"]["x"] = bad_raw[:, :, 1]
    bad[jump_type]["pos"]["y"] = bad_raw[:, :, 2]

    bad[jump_type]["vel"]["x"] = np.stack([np.gradient(bad[jump_type]["pos"]["x"][mid], bad[jump_type]["time"]) for mid in range(NUM_MARKERS)])
    bad[jump_type]["vel"]["y"] = np.stack([np.gradient(bad[jump_type]["pos"]["y"][mid], bad[jump_type]["time"]) for mid in range(NUM_MARKERS)])


# Stick figure rendering

def stick_figure(data, frame):
    """
    Create a stick figure at frame
    """
    x   = data["pos"]["x"][[LEFT_FOOT, LEFT_KNEE, STOMACH, CHEST, STOMACH, RIGHT_KNEE, RIGHT_FOOT], frame]
    y   = data["pos"]["y"][[LEFT_FOOT, LEFT_KNEE, STOMACH, CHEST, STOMACH, RIGHT_KNEE, RIGHT_FOOT], frame]
    v_x = data["vel"]["x"][[LEFT_FOOT, LEFT_KNEE, STOMACH, CHEST, STOMACH, RIGHT_KNEE, RIGHT_FOOT], frame]
    v_y = data["vel"]["y"][[LEFT_FOOT, LEFT_KNEE, STOMACH, CHEST, STOMACH, RIGHT_KNEE, RIGHT_FOOT], frame]

    return x, y, v_x, v_y

# Animation

def create_animation(data, with_velocities = False):
    xlim = (-1.5, 0.5)
    ylim = (-0.1, 1.75)

    scaling = 0.1
    num_frames = data["time"].shape[0]
    interval = data["time"][1]

    fig = plt.figure(figsize = (12, 8))
    ax = fig.add_subplot(autoscale_on = False, xlim = xlim, ylim = ylim)
    ax.set_aspect("equal")
    ax.grid()

    plt.xlabel("Horizontal axis", fontsize = label_size)
    plt.ylabel("Vertical axis", fontsize = label_size)
    plt.xticks(fontsize = ticks_size)
    plt.yticks(fontsize = ticks_size)

    outline, = ax.plot([], [], "-", color = "black", linewidth = line_width)
    markers, = ax.plot([], [], "o", color = "red", markersize = marker_size)

    if with_velocities:
        velocity = [ax.arrow(0.0, 0.0, 0.0, 0.0, color = "green") for mdx in range(NUM_MARKERS + 1)]

    floor, = ax.plot(xlim, [0.0, 0.0], "-", color= "blue", linewidth = 4)
    time_template = "Time = %.2f s"
    time_text = ax.text(0.05, 0.9, "", transform = ax.transAxes, fontsize = legend_size)

    def animate(frame):
        x, y, v_x, v_y = stick_figure(data, frame)
        outline.set_data(x, y)
        markers.set_data(x, y)
        time_text.set_text(time_template % (data["time"][frame]))

        if with_velocities:
            for mdx in range(NUM_MARKERS + 1):
                velocity[mdx].set_data(x = x[mdx], y = y[mdx], dx = scaling * (x[mdx] + v_x[mdx]), dy = scaling * (y[mdx] + v_y[mdx]))

            return [floor, outline, markers, time_text] + velocity
        else:
            return [floor, outline, markers, time_text]

    jump = animation.FuncAnimation(fig, animate, num_frames, interval = 1400 * interval, blit = True)
    plt.show()

jump_type = "2d"
with_velocities = True
create_animation(bad[jump_type], with_velocities)
create_animation(good[jump_type], with_velocities)

plt.show()

# %%

jump_type = "2d"
data = bad[jump_type]
num_frames = data["time"].shape[0]

for frame in [0, 16, num_frames - 1]:
    xlim = (-1.5, 0.5)
    ylim = (-0.1, 1.75)

    fig = plt.figure(figsize = (6, 6))
    ax = fig.add_subplot(autoscale_on = False, xlim = xlim, ylim = ylim)
    ax.set_aspect("equal")
    ax.grid()

    plt.xlabel("Horizontal axis", fontsize = label_size)
    plt.ylabel("Vertical axis", fontsize = label_size)

    x, y, v_x, v_y = stick_figure(data, frame)

    floor, = ax.plot(xlim, [0.0, 0.0], "-", color= "blue", linewidth = 4)
    plt.plot(x, y, "-", color = "black", linewidth = line_width)
    plt.plot(x, y, "o", color = "red", linewidth = line_width)

    plt.xticks(np.linspace(xlim[0], xlim[1], 5), fontsize = ticks_size)
    plt.yticks(fontsize = ticks_size)

    #plt.savefig("good_2d_%d.png" % (frame), bbox_inches = "tight")
    plt.savefig("bad_2d_%d.png" % (frame), bbox_inches = "tight")

    plt.show()

# %% End of script

# %% End of script
