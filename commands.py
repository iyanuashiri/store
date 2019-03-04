from pathlib import Path
import json
import io

from terminaltables import SingleTable
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import click

from .utils import authorize_google_drive


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


@main.command('push', short_help='Push the file to your Google drive')
@click.option('--first_time', default=False, help='Set to True if this is the first time you are using push command')
def push(first_time=False):
    service = authorize_google_drive()
    file_metadata = {'name': 'commands.json'}
    commands_file = MediaFileUpload('{0}'.format(directory), resumable=True)

    if not first_time:
        file = service.files().create(body=file_metadata, media_body=commands_file, fields='id').execute()
        push_id = file.get('id')
        with open(id_directory, 'w') as f:
            f.write(push_id)

    else:
        with open(id_directory) as f:
            push_id = f.read()
        file = service.files().update(fileId=push_id, media_body=commands_file, fields='id',
                                      body=file_metadata).execute()
        push_id = file.get('id')

    click.echo('Push is complete. Your push_id is {}'.format(push_id))


@main.command('pull', short_help='Pull the file from Google drive')
@click.argument('push_id', help='Use your upload_id as a commandline argument')
def pull(push_id):
    service = authorize_google_drive()
    request = service.files().get_media(fileId=push_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        click.echo("Download {}.".format(int(status.progress() * 100)))
