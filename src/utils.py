"""Module containing various utilities."""


import pathlib

import astropy.coordinates
import astropy.table
import astropy.time
import astroplan
import yaml


def load_configuration_file(configuration_file: pathlib.Path) -> dict:
    """Load a configuration as a dictionary.

    Parameters
    ----------
    configuration_file: ~pathlib.Path
        Configuration file in YML format.

    Returns
    -------
    dict
        A dictionary with the declared configuration.

    Examples
    --------
    import pathlib
    config_file = pathlib.Path("config.yml")
    config_dict = load_configuration_file(config_file)

    """
    with open(configuration_file, "r") as file:
        return yaml.safe_load(file)


def create_earth_location_from_config(config: dict) -> astropy.coordinates.EarthLocation:
    """Create an ``EarthLocation`` instance according to the given configuration.

    Parameters
    ----------
    config: dict
        A dictionary with the declared configuration.

    Returns
    -------
    astropy.coordinates.EarthLocation
        Location of the observer in the Earth.

    Examples
    --------
    config = {"location": {"lon": "", "lat": "", "alt": ""}, ...}

    """
    lon, lat, alt = config["location"].values()
    return astropy.coordinates.EarthLocation.from_geodetic(lon, lat, alt)


def create_observer_from_config(config: dict) -> astroplan.Observer:
    """Create an ``Observer`` instance from the given configuration.

    Parameters
    ----------
    config: dict
        A dictionary with the declared configuration.

    Returns
    -------
    astroplan.Observer
        Observer at the given location in the configuration file.

    """
    location = create_earth_location_from_config(config)
    location_name = config["observation"]["name"]
    timezone = config["observation"]["timezone"]
    return astroplan.Observer(location, timezone=timezone, name=location_name)

def create_time_from_config(config: dict) -> astropy.time.Time:
    """Create a ``Time`` instance from the given configuration.

    Parameters
    ----------
    config: dict
        Dictionary with the declared configuration.

    Returns
    -------
    astropy.time.Time
        Time instance representing the observation time.

    """
    return astropy.time.Time(config["observation"]["datetime"])


def create_targets_from_config(config: dict) -> list[astroplan.FixedTarget]:
    """Create a list of ``FixedTarget`` instances from the given configuration.

    Parameters
    ----------
    config: dict
        Dictionary with the declared configuration.

    Returns
    -------
    list[astroplan.FixedTarget]
        List of targets to be observed.

    """
    targets_file = config["observation"]["targets-file"]
    return [
        astroplan.FixedTarget(
            astropy.coordinates.SkyCoord(
                ra=ra, dec=dec, frame="icrs",equinox="J2000"
            ),
            name=name
        )
        for name, ra, dec in astropy.table.Table.read(targets_file, format="csv")
    ]

def parse_config(config):
    """Parse the given configuration to get fundamental data for the simulation.

    Returns the location, observer, list of targets, and observation time.

    Parameters
    ----------
    config: dict
        Dictionary with the declared configuration.

    """
    location = create_earth_location_from_config(config)
    observer = create_observer_from_config(config)
    targets = create_targets_from_config(config)
    time = create_time_from_config(config)
    return [location, observer, targets, time]
