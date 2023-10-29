"""Module containing vairous plotting capabilities."""

import astropy.coordinates
import astropy.time
import matplotlib.axes
import numpy as np


def plot_airmass_moon(
    ax: matplotlib.axes.Axes, 
    time: astropy.time.Time,
    location: astropy.coordinates.EarthLocation,
    **style_kwargs,
):
    """Plot the moon airmass evolution at a given location.

    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Axes used to draw the airmass evolution of the Moon.
    time: astropy.time.Time
        Time of the observation.
    location: astropy.coordinates.EarthLocation
        Location of the observer on Earth.
    style_kwargs: dict
        Dictionary with additional style configuration.

    Returns
    -------
    ax: matplotlib.axes.Axes
        Axes including the airmass evolution of the Moon.

    """
    # Calculate the times for the given day
    datetime = time.datetime
    year, month, date = datetime.year, datetime.month, datetime.day

    start_time = astropy.time.Time(f"{year}-{month}-{date} 00:00:00", format="iso", scale="utc")
    end_time = astropy.time.Time(f"{year}-{month}-{int(date+1)} 23:59:59", format="iso", scale="utc")
    times = start_time + (end_time - start_time) * np.linspace(0, 1, 1000)

    # Calculate the Moon's altitude for each time
    altaz_frame = astropy.coordinates.AltAz(obstime=times, location=location)
    moon_airmass = astropy.coordinates.get_moon(times).transform_to(altaz_frame).secz
    masked_airmass = np.ma.array(moon_airmass, mask=moon_airmass < 1)

    # Plot the Moon's altitude vs. time
    ax.plot(times.datetime, masked_airmass, color="black", label="Moon")

    return ax
