import click

from cli.peaks import ingest as ingest_peaks

from peaks_and_tracks_initializer.ingestion.ingestion_controller import IngestionController

ingestion_controller = IngestionController()

@click.group()
def cli():
    """This is the main command for my CLI application."""
    pass


@click.group()
def regions():
    """This is subcommand 1."""
    ...

@click.group()
def routes():
    """
    """
    ...

@click.group()
def peaks():
    ...

peaks.add_command(ingest_peaks)


# Attach subcommands to the main group and subcommands to subcommand1
cli.add_command(regions)
cli.add_command(routes)
cli.add_command(peaks)



if __name__ == "__main__":
    cli()








