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


@main.command('save', short_help='Save a command')
@click.argument('description', help='Description of the command')
@click.argument('command', help='The command that needs to be saved')
def save(description, command):
    with open(directory, 'w') as f:
        commands = json.load(f)
        commands[description] = command
        json.dump(commands, f)
    click.echo('Command has been saved')


@main.command('search', short_help='Search for a command')
@click.argument('query', help='What do you want to search for?')
def search(query):
    with open(directory) as f:
        commands = json.load(f)
        results = list()
        results.append(['description', 'command'])
        for k, v in commands.items():
            if query in k or query in v:
                results.append([k, v])

        table = SingleTable(results)
        click.echo(table.table)
