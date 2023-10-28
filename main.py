import matplotlib.pyplot as plt
import pandas as pd
from astroplan import FixedTarget, Observer
from astroplan.plots import plot_airmass
from astropy import units as u
from astropy.coordinates import Angle, EarthLocation, SkyCoord
from astropy.time import Time


MAX_AIRMASS = 3.00

location = EarthLocation.from_geodetic(
    lon="3d23m05s",
    lat="37d03m51s",
    height=2896.0 * u.m,
)
telescope = Observer(
    location,
    name="Observatorio Sierra Nevada (OSN)",
    timezone="Europe/Madrid",
)
observation_data = pd.read_csv("comets.dat")
time = Time("2023-12-01 17:00:00", scale="utc")


def main():
    targets = []
    for _, body in observation_data.iterrows():
        name, ra, dec = (
            body["Name"],
            Angle(body["RA(J2000)"], unit=u.hour),
            Angle(body["DE(J2000)"], unit=u.deg),
        )
        target_coords = SkyCoord(ra=ra, dec=dec, frame="icrs")
        targets.append(FixedTarget(coord=target_coords, name=name))

    fig, ax = plt.subplots()
    plot_airmass(
        targets,
        telescope,
        time,
        ax=ax,
        altitude_yaxis=True,
        brightness_shading=True,
        style_kwargs={"linestyle": "-"},
        max_airmass=1.5 * MAX_AIRMASS,
        min_region=3,
    )
    ax.axhline(y=MAX_AIRMASS, color="red")
    ax.legend(shadow=True)
    plt.show()







if __name__ == "__main__":
    main()
