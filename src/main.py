import pathlib

import matplotlib.pyplot as plt
import astroplan.plots

from plotting import plot_airmass_moon
from utils import load_configuration_file, parse_config


CONFIG_FILE = pathlib.Path(__file__).parent.parent / "config.yml"
"""YML file declaring the configuration of the session."""


def main():
    """Entry point of the script."""
    config = load_configuration_file(CONFIG_FILE)

    location, observer, targets, time = parse_config(config)

    _, ax = plt.subplots()
    astroplan.plots.plot_airmass(
        targets,
        observer,
        time,
        ax=ax,
        altitude_yaxis=True,
        brightness_shading=True,
        style_kwargs={"linestyle": "--", "marker": "o"},
    )
    plot_airmass_moon(ax=ax, time=time, location=location, style_kwargs={"color": "black"})
    ax.legend(shadow=True)
    plt.show()




if __name__ == "__main__":
    main()
