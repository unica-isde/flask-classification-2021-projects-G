import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


def generate(labels, values):
    """! Generate a plot image

    @param labels The classification labels.
    @param values Prediction scores for the labels.

    @return The plotted data as a PNG image.
    """

    colors = ["olivedrab", "yellowgreen", "seagreen", "teal", "palegreen"]

    fig = Figure(figsize=(13,6), dpi=150)

    axis = fig.add_subplot(1, 1, 1)
    axis.barh(labels, values, color=colors)

    axis.set_title("CLASSIFICATION RESULTS")
    axis.set_xlabel("SCORE %")
    axis.set_ylabel("LABEL")
    axis.grid(True)
    axis.invert_yaxis()

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    return output.getvalue()
