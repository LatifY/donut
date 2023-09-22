import numpy as np
import time as t
import gui
import threading
import config
import os

os.system('color')

def change_color(color):
    print(f"{color}")

screen_size = 40
theta_spacing = 0.07
phi_spacing = 0.02

# illumination = np.fromiter(config.ITER_STR, dtype="<U1")

# def change_illumination():
#     global illumination
#     ITER = config.ITER_STR if config.REVERSED == False else config.REVERSED_ITER_STR
#     illumination = np.fromiter(ITER, dtype="<U1")
#     print(illumination)

A = 1
B = 1
R1 = 1
R2 = 2
K2 = 5
K1 = screen_size * K2 * 3 / (8 * (R1 + R2))


def render_frame(A: float, B: float) -> np.ndarray:
    cos_A = np.cos(A)
    sin_A = np.sin(A)
    cos_B = np.cos(B)
    sin_B = np.sin(B)

    output = np.full((screen_size, screen_size), " ")
    zbuffer = np.zeros((screen_size, screen_size))

    cos_phi = np.cos(phi := np.arange(0, 2 * np.pi, phi_spacing))
    sin_phi = np.sin(phi)
    cos_theta = np.cos(theta := np.arange(0, 2 * np.pi, theta_spacing))
    sin_theta = np.sin(theta)
    circle_x = R2 + R1 * cos_theta
    circle_y = R1 * sin_theta

    x = (np.outer(cos_B * cos_phi + sin_A * sin_B * sin_phi, circle_x) - circle_y * cos_A * sin_B).T
    y = (np.outer(sin_B * cos_phi - sin_A * cos_B * sin_phi, circle_x) + circle_y * cos_A * cos_B).T
    z = ((K2 + cos_A * np.outer(sin_phi, circle_x)) + circle_y * sin_A).T
    ooz = np.reciprocal(z)  # Calculates 1/z
    xp = (screen_size / 2 + K1 * ooz * x).astype(int)
    yp = (screen_size / 2 - K1 * ooz * y).astype(int)
    L1 = (((np.outer(cos_phi, cos_theta) * sin_B) - cos_A * np.outer(sin_phi, cos_theta)) - sin_A * sin_theta)
    L2 = cos_B * (cos_A * sin_theta - np.outer(sin_phi, cos_theta * sin_A))
    L = np.around(((L1 + L2) * 8)).astype(int).T
    mask_L = L >= 0
    chars = np.fromiter(config.ITER_STR if config.REVERSED == False else config.REVERSED_ITER_STR, dtype="<U1")[L]

    for i in range(90):
        mask = mask_L[i] & (ooz[i] > zbuffer[xp[i], yp[i]])  # (315,)

        zbuffer[xp[i], yp[i]] = np.where(mask, ooz[i], zbuffer[xp[i], yp[i]])
        output[xp[i], yp[i]] = np.where(mask, chars[i], output[xp[i], yp[i]])

    return output


def pprint(array: np.ndarray) -> None:
    print (*[" ".join(row) for row in array], sep="\n")

def start_donut(A, B):
    for _ in range(screen_size * screen_size):
        A += theta_spacing
        B += phi_spacing
        print("\x1b[H")
        pprint(render_frame(A, B))
        s = 100 - config.SPEED
        t.sleep(s / 1000)

def start_gui():
    window_gui = gui.GUI()

if __name__ == "__main__":
    threading.Thread(target=start_donut, args=(A,B)).start()
    start_gui()