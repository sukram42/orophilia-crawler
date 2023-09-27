import click

from peaks_and_tracks_initializer.ingestion.ingestion_controller import get_ingestion_controller

controller = get_ingestion_controller()

@click.command()
@click.option('--region_id')
def ingest(region_id: str):
    """This is subsubcommand 1 under subcommand 1."""
    print(region_id)
    regions = controller.get_ingested_regions()
    region = [*filter(lambda r: str(r.id)==str(region_id), regions.root)]

    if len(region) == 0 : 
        print(f"There is no region with id={region_id}")
        return
    
    if len(region) > 1: 
        print(f"There are {len(region_id)} regions with this id. Choosing the first.")
    
    region = region[0]
    print(f"Ingesting peaks for region {region.name}({region.id}) ")
    controller.ingest_peaks_per_region(region=region)


@click.command()
def delete():
    """This is subsubcommand 2 under subcommand 1."""
    click.echo("Executing subsubcommand2 under subcommand1!")
