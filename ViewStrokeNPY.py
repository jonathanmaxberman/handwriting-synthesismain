#import matplotlib
from matplotlib import pyplot

#import svgwrite
import numpy as np
#from IPython.display import SVG, display

def plot_stroke(stroke, save_name=None):
    # Plot a single example.
    print("plot the strokes")
    f, ax = pyplot.subplots()

    x = np.cumsum(stroke[:, 0])
    y = np.cumsum(stroke[:, 1])

    size_x = x.max() - x.min() + 1.0
    size_y = y.max() - y.min() + 1.0

    f.set_size_inches(5.0 * size_x / size_y, 5.0)

    cuts = np.where(stroke[:, 2] == 1)[0]
    start = 0

    for cut_value in cuts:
        ax.plot(x[start:cut_value], y[start:cut_value], "k-", linewidth=3)
        start = cut_value + 1

    ax.axis("off")  # equal
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

    if save_name is None:
        pyplot.show()
    else:
        try:
            pyplot.savefig(save_name, bbox_inches="tight", pad_inches=0.5)
        except Exception:
            print("Error building image!: " + save_name)

    pyplot.close()

file_path = 'style-16-strokes.npy'
stroke_data = np.load(file_path)
plot_stroke(stroke_data)