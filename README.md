
![Store Logo](store.png)

A tool to store terminal commands and create a backup on Google drive.

## Features

* Save a command
* Search for a command
* Push store file ( Create backup on Google drive)
* Pull store file (Restore file from Google drive)
* List all commands

## Problem

After initially searching Google and Stackoverflow for a command, I have to search again the next time I need to use the command.
I think ctrl + r has a limit of commands it can save. 

## Installation

Python 3.6+

```commandline
$ pip install store-cli
```


## How to Use

```commandline
$ store --help
```
Displays the list of commands 

```commandline
$ store save --help
```
Displays the options available for a command

```commandline
$ store init
```
Initializes the file where the commands are saved.

```commandline
$ store save -d 'commit' -c 'git commit -m 'commit message'
```
Saves the command and the description of the command

```commandline
$ store search -q 'init'
```
Search for the query init

```commandline
store list
```
Lists all the commands that has been saved

```commandline
$ store push -f
```
This pushes the updated file to your Google drive account. Use the `--first` option the first time you are
using the `push` command. Subsequently, just use `store push` to push to Google drive.

```commandline
$ store pull -p 'push_id'
```
Whenever you use the push command, a push_id will be given to you. Save the id. You need this id to 
restore/sync your commands between computers. 

```commandline
$ store show
```
This displays the push id. You receive a push id after using the `push` command.


## Development Purposes

* For Development
    * clone the repo
    ```commandline
        $ git clone https://github.com/iyanuashiri/store.git
    ```
    * get your `client_secret.json` from [Oauth](https://console.cloud.google.com/apis/credentials/oauthclient). Make sure to enable [Drive Api](https://console.cloud.google.com/apis/library/drive.googleapis.com?q=Drive) for the project.
    * rename the client secret to `credentials.json` and place it in the same directory as setup.py.
    * install the package:
    ```sh
        # move into setup.py directory
        $ cd 
        # install package in edit mode
        $ pip install -e . #note the dot
    ```




## How to Contribute

Click here to read the [contributing](https://github.com/iyanuashiri/store/blob/master/CONTRIBUTING.md) guide.

Feature requests, suggestions and improvements are welcomed.


## Contributors

[Iyanu Ajao](http://github.com/iyanuashiri)

