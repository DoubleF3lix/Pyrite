import shutil
import json
import os
import requests
import pyperclip
import nbtlib
import urllib.request
import sys
import zipfile

def serverSetup(createdServerName, selectedVersion):
    versions = requests.get('http://launchermeta.mojang.com/mc/game/version_manifest.json')
    versionsJSON = json.loads(versions.content)
    for version in versionsJSON['versions']:
        if version['id'] == selectedVersion:
            versionData = version['url']
    selectedVersionData = requests.get(versionData)
    selectedVersionJSON = json.loads(selectedVersionData.content)
    versionLink = selectedVersionJSON['downloads']['server']['url']

    try:
        shutil.rmtree(serversPath + '\\' + createdServerName)
    except FileNotFoundError:
        pass
    os.mkdir(f'{serversPath}\\{createdServerName}')
    print('Please wait while the server.jar is downloaded...')
    urllib.request.urlretrieve(versionLink, f'{serversPath}\\{createdServerName}\\server.jar')
    print(f'Done! The server.jar has been successfully downloaded!\nName: {createdServerName}\nVersion: {selectedVersion}\n')

    with open(f'{serversPath}\\{createdServerName}\\eula.txt', 'w') as eula:
        eula.write('eula=true')
        eula.close()

    with open(f'{serversPath}\\{createdServerName}\\{batchFileName}', 'w') as startingBatchFile:
        startingBatchFile.write('java -Xms1G -Xmx1G -jar server.jar nogui')
        startingBatchFile.close()

def copyWorld():
    worldToCopyName = input('Enter the world name you would like to copy: ')
    worldToCopySRC = worldsPath + '\\' + worldToCopyName
    worldToCopyDST = serversPath + '\\' + serverName + '\\' + 'world'
    try:
        shutil.rmtree(worldToCopyDST)
    except FileNotFoundError:
        pass
    try:
        shutil.copytree(worldToCopySRC, worldToCopyDST)
    except FileNotFoundError:
        input(f'ERROR - {worldToCopyName} doesn\'t exist.')
        sys.exit(0)

def clearWorldPlayerData(serverName):
    serverWorld = serversPath + '\\' + serverName + '\\' + 'world'
    shutil.rmtree(serverWorld + '\\advancements')
    shutil.rmtree(serverWorld + '\\playerdata')
    shutil.rmtree(serverWorld + '\\stats')
    with nbtlib.load(serverWorld + '\\level.dat') as leveldat:
        try:
            del leveldat.root['Data']['Player'] 
        except KeyError:
            pass

def startServer(serverName):
    try:
        os.chdir(serversPath + '\\' + serverName)
        os.system(f'start cmd /c "{batchFileName}"')
    except FileNotFoundError:
        input(f'ERROR - You don\'t have a batch file to start your server with! Make sure {batchFileName} is in ' + serversPath + '\\' + serverName)
        sys.exit(0)

def hostServer():
    os.chdir(serversPath)
    if config['refreshNgrokLogin'] == True:
        os.system(f'ngrok.exe authtoken {ngrokAuthToken}')
        with open('C:\\Pyrite\\config.json', 'w') as configFile:
            configData = {
                "serversPath": config['serversPath'],
                "worldsPath": config['worldsPath'],
                "region": config['region'],
                "batchFileName": config['batchFileName'],
                "ngrokAuthToken": config['ngrokAuthToken'],
                "disableNgrok": config['disableNgrok'],
                "refreshNgrokLogin": False
            }
            json.dump(configData, configFile)
    os.system(f'start ngrok.exe tcp -region {region} 25565')

def getServerIP():
    getPortInfo = requests.get('http://localhost:4040/api/tunnels')
    portInfo = json.loads(getPortInfo.content)
    serverIP = portInfo['tunnels'][0]['public_url'][6:]
    pyperclip.copy(serverIP)

def downloadNgrok():
    print('Please wait while ngrok is installed')
    urllib.request.urlretrieve('https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip', f'{serversPath}\\ngrok.zip')
    with zipfile.ZipFile(f'{serversPath}\\ngrok.zip', 'r') as ngrokZip:
        ngrokZip.extractall(serversPath)
    os.remove(f'{serversPath}\\ngrok.zip')

def createConfig():
    with open('C:\\Pyrite\\config.json', 'w') as configFile:
        configData = {
            "serversPath": "",
            "worldsPath": "",
            "region": "",
            "batchFileName": "start.bat",
            "ngrokAuthToken": "",
            "disableNgrok": False,
            "refreshNgrokLogin": True
        }
        json.dump(configData, configFile)
    input('You didn\'t have a config.json, so one has been created for you. Please modify the config.json with valid parameters, and reset the program.')
    sys.exit(0)

def getConfig():
    with open('C:\\Pyrite\\config.json', "r") as configJson:
        configData = json.load(configJson)
        return configData

if __name__ == "__main__:
    if not os.path.isdir('C:\\Pyrite') and not os.path.exists('C:\\Pyrite\\config.json'):
        os.mkdir('C:\\Pyrite')
        createConfig()
    elif os.path.isdir('C:\\Pyrite') and not os.path.exists('C:\\Pyrite\\config.json'):
        createConfig()
    else:
        config = getConfig()
        serversPath = config['serversPath']
        worldsPath = config['worldsPath']
        region = config['region']
        batchFileName = config['batchFileName']
        ngrokAuthToken = config['ngrokAuthToken']
        disableNgrok = config['disableNgrok']
        refreshNgrokLong = config['refreshNgrokLogin']

    setupServerMode = input('Would you like to create a server? (Y/N): ').lower().replace(' ', '')
    if setupServerMode == 'y':
        setupServerName = input('Enter a name for your server: ')
        setupServerVersion = input('Enter a version for your server: ').lower()
        serverSetup(setupServerName, setupServerVersion)

    serverName = input('Enter the server name you would like to setup: ')
    doCopyWorld = input(f'Would you like to copy a world to {serverName}? (Y/N): ').lower().replace(' ', '')
    if doCopyWorld == 'y':
        copyWorld()

        mapTestingMode = input(f'Would you like to enable Map Testing Mode? (Clears all Player Data) (Y/N): ').lower().replace(' ', '')
        if mapTestingMode == 'y':
            clearWorldPlayerData(serverName)

    if config['disableNgrok'] == False:  
        if not os.path.exists(f'{serversPath}\\ngrok.exe'):
            downloadNgrok()  
        hostServer()
        try:
            getServerIP()
            print('Done! The IP to your server has been copied to your clipboard.')
        except ConnectionError:
            print('ERROR - ngrok closed before the server IP could be grabbed!')

    startServer(serverName)
