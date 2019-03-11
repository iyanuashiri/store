import io
import json
from pathlib import Path

import click
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file as f, tools, client
from terminaltables import SingleTable


SCOPES = 'https://www.googleapis.com/auth/drive.file'

folder = Path().home() / 'source_data'

folder.mkdir(exist_ok=True)

directory = folder / 'commands.json'

directory.touch()

id_directory = folder / 'file.txt'

id_directory.touch()


def authorize_google_drive():
    store = f.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    service = build('drive', 'v3', http=creds.authorize(Http()))
    return service


@click.group()
def main():
    pass


@main.command('init', short_help='Initialize the file')
def init():
    if directory.exists():
        click.echo('File has already been initialized')
    else:
        with open(directory, 'w') as file:
            commands = dict()
            commands['description'] = 'command'
            json.dump(commands, file)
        click.echo('File has been initialized')


@main.command('save', short_help='Save a command')
@click.option('-d', '--description', help='Description of the command')
@click.option('-c', '--command', help='The command that needs to be saved')
def save(description, command):
    with open(directory, 'r') as file:
        commands = json.load(file)
        commands[description] = command

    with open(directory, 'w') as file:
        json.dump(commands, file)
    click.echo('Command has been saved')


@main.command('search', short_help='Search for a command')
@click.option('-q', '--query', help='What do you want to search for?')
def search(query):
    with open(directory) as file:
        commands = json.load(file)
        results = list()
        results.append(['description', 'command'])
        for k, v in commands.items():
            if query in k or query in v:
                results.append([k, v])

        table = SingleTable(results)
        click.echo(table.table)


@main.command('push', short_help='Push the file to your Google drive')
@click.option('f', '--first', is_flag=True, help='Use this option if this is the first time you are using push command')
def push(first=False):
    service = authorize_google_drive()
    file_metadata = {'name': 'commands.json'}
    commands_file = MediaFileUpload('{0}'.format(directory), resumable=True)

    if first:
        file_ = service.files().create(body=file_metadata, media_body=commands_file, fields='id').execute()
        push_id = file_.get('id')
        with open(id_directory, 'w') as file:
            file.write(push_id)

    else:
        with open(id_directory) as file:
            push_id = file.read()
        file_ = service.files().update(fileId=push_id, media_body=commands_file, fields='id',
                                       body=file_metadata).execute()
        push_id = file_.get('id')

    click.echo('Push is complete. Your push_id is {}'.format(push_id))
    click.echo('Write down your push id in a safe place')


@main.command('pull', short_help='Pull the file from Google drive')
@click.option('-p', '--push_id', help='Use your upload_id as a commandline argument')
def pull(push_id):
    service = authorize_google_drive()
    request = service.files().get_media(fileId=push_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        click.echo("Download {}.".format(int(status.progress() * 100)))
    click.echo("Download complete")


@main.command('list', short_help='List all saved commands')
def list_all():
    with open(directory) as file:
        commands = json.load(file)
        results = list()
        results.append(['description', 'command'])
        for k, v in commands.items():
            results.append([k, v])

        table = SingleTable(results)
        click.echo(table.table)


@main.command('show', short_help='Print the push_id')
def show():
    with open(id_directory) as file:
        click.echo('Your push id is:')
        click.echo(file.read())


if __name__ == '__main__':
    main()
