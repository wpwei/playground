import numpy as np
from scipy.special import expit
from PIL import Image
import argparse
from tqdm import tqdm


def walk(canvas_width, canvas_height, n_steps,
         init_x=None, init_y=None):

    if init_x is None:
        init_x = int(canvas_width / 2)
    if init_y is None:
        init_y = int(canvas_height / 2)

    canvas = np.zeros([canvas_height, canvas_width])

    x, y = init_x, init_y

    for _ in tqdm(range(int(n_steps)), desc='Walking...'):
        canvas[x, y] += 1

        dx = np.random.randint(-1, high=2)
        dy = np.random.randint(-1, high=2)

        x += dx
        y += dy

        x = x % canvas_width
        y = y % canvas_height

    return canvas


def save_image(canvas, path, ink_shade):
    img = 1 - expit(canvas * ink_shade) * 2 + 1
    img = Image.fromarray(np.uint8(img * 255))
    img.save(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--output_file', default='random_walk.jpg',
                        help='output file path', type=str)

    parser.add_argument('-cw', '--canvas_width', default=2048,
                        help='width of the canvas in pixel', type=int)

    parser.add_argument('-ch', '--canvas_height', default=2048,
                        help='height of the canvas in pixel', type=int)

    parser.add_argument('-s', '--n_steps', default=int(2e6),
                        help='number of steps to walk', type=int)

    parser.add_argument('-i', '--ink_shade', default=0.13,
                        help='the higher, the darker ink gets', type=float)

    args = parser.parse_args()

    image = walk(args.canvas_width,
                 args.canvas_height,
                 args.n_steps)

    save_image(image, args.output_file, args.ink_shade)

    print(f'Saved to {args.output_file}.')
