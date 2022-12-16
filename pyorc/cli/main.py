# Main command line routines
import click
from typing import List, Optional, Union
from typeguard import typechecked
import os
import warnings
import numpy as np
from . import cli_utils
from . import log
# import pyorc api below
from .. import __version__
# import cli components below


## MAIN

def print_info(ctx, param, value):
    if not value:
        return {}
    click.echo(f"PyOpenRiverCam, Copyright Localdevices, Rainbow Sensing")
    ctx.exit()


@click.group()
@click.version_option(__version__, message="PyOpenRiverCam version: %(version)s")
@click.option(
    "--info",
    default=False,
    is_flag=True,
    is_eager=True,
    help="Print information and version of PyOpenRiverCam",
    callback=print_info,
)
@click.option(
    '--debug/--no-debug',
    default=False,
    envvar='REPO_DEBUG'
)
@click.pass_context
def cli(ctx, info, debug):  # , quiet, verbose):
    """Command line interface for hydromt models."""
    if ctx.obj is None:
        ctx.obj = {}

    # ctx.obj["log_level"] = max(10, 30 - 10 * (verbose - quiet))
    # logging.basicConfig(stream=sys.stderr, level=ctx.obj["log_level"])


## CAMERA CONFIG
#
@cli.command(short_help="Prepare Camera Configuration file")
@click.argument(
    'OUTPUT',
    type=click.Path(resolve_path=True, dir_okay=False, file_okay=True),
    required=True,
)
@click.option(
    "-v",
    "--videofile",
    type=click.Path(resolve_path=True, dir_okay=False, file_okay=True),
    help="video file with required objective and resolution and control points in view",
    callback=cli_utils.validate_file
)
@click.option(
    "--src",
    type=str,
    callback=cli_utils.parse_src,
    help='Source control points as list of [column, row] pairs.'
)
@click.option(
    "--dst",
    type=str,
    callback=cli_utils.parse_dst,
    help='Destination control points as list of 4 [x, y] pairs, or at least 6 [x, y, z] pairs in local coordinate system.'
)
@click.option(
    "--crs",
    type=str,
    callback=cli_utils.parse_str_num,
    help="Coordinate reference system to be used for camera configuration"
)
@click.option(
    "--shapefile",
    type=click.Path(resolve_path=True, dir_okay=False, file_okay=True),
    help="shapefile or geojson containing point geometries with x, y (4) or x, y, z (6 or more) coordinates with ground control points"
)
@click.option(
    "--corners",
    type=str,
    callback=cli_utils.parse_corners
)
@click.pass_context
@typechecked
def camera_config(
        ctx,
        output: str,
        videofile: str,
        src: Optional[List[List[float]]],
        dst: Optional[List[List[float]]],
        crs: Optional[Union[str, int]],
        shapefile: Optional[str],
        corners: Optional[List[List]]
):
    click.echo(videofile)
    if videofile is not None:
        assert(os.path.isfile(videofile)), f"file {videofile} not available"

    click.echo(type(videofile))
    logger = log.setuplog("cameraconfig", os.path.abspath("pyorc.log"), append=False)
    logger.info(f"Preparing your cameraconfig file in {output}")
    logger.info(f"Found video file  {videofile}")
    if src is not None:
        logger.info("Source points found and validated")
    if dst is not None:
        logger.info("Destination points found and validated")

    click.echo(type(crs))
#     # pass


## VELOCIMETRY
@cli.command(short_help="Estimate velocimetry")
@click.argument(
    'OUTPUT',
    type=click.Path(resolve_path=True, dir_okay=False, file_okay=True),
    required=True,
)
@click.option(
    "-v",
    "--videofile",
    type=click.Path(resolve_path=True, dir_okay=False, file_okay=True),
    help="video file with required objective and resolution and control points in view",
)
@click.option(
    "-o",
    "--optionsfile",
    type=click.Path(resolve_path=True, dir_okay=False, file_okay=True),
    help="Options file (*.yml)",
)
@click.option(
    "-c",
    "--cameraconfig",
    type=click.Path(resolve_path=True, dir_okay=False, file_okay=True),
    help="Camera config file (*.json)",
)
@click.pass_context
def velocimetry(ctx, output, videofile, optionsfile, cameraconfig):
    logger = log.setuplog("velocimetry", os.path.abspath("pyorc.log"), append=False)
    logger.info(f"Preparing your velocimetry result in {output}")
    pass

