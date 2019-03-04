from pathlib import Path
import json

from terminaltables import SingleTable
import click


folder = Path().home() / 'source_data'

folder.mkdir(exist_ok=True)

directory = folder / 'commands.json'

directory.touch()

id_directory = folder / 'file.txt'


@click.group()
def main():
    pass


@main.command('init', short_help='Initialize the file')
def init():
    with open(directory, 'w') as f:
        commands = dict()
        json.dump(commands, f)
    click.echo('File has been initialized')
