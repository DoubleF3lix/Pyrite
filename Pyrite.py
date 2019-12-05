import shutil
import json
import os
import requests
import pyperclip
import nbtlib
import urllib.request
import sys
import zipfile
import shlex

def serverSetup(serversPath, batchFileName, createdServerName, selectedVersion):
    versions = requests.get('http://launchermeta.mojang.com/mc/game/version_manifest.json')
    versionsJSON = json.loads(versions.content)
    if selectedVersion == 'latest':
        for version in versionsJSON['versions']:
            versionData = version['url']
            serverVersion = version['id']
            break

    elif selectedVersion == 'latest.release':
        for version in versionsJSON['versions']:
            if version['type'] == 'release':
                versionData = version['url']
                serverVersion = version['id']
                break

    elif selectedVersion == 'latest.snapshot':
        for version in versionsJSON['versions']:
            if version['type'] == 'snapshot':
                versionData = version['url']
                serverVersion = version['id']
                break

    else:
        for version in versionsJSON['versions']:
            if version['id'] == selectedVersion:
                versionData = version['url']
                serverVersion = version['id']
                
    selectedVersionData = requests.get(versionData)
    selectedVersionJSON = json.loads(selectedVersionData.content)
    versionLink = selectedVersionJSON['downloads']['server']['url']

    try:
        shutil.rmtree(os.path.join(serversPath, createdServerName))
    except FileNotFoundError:
        pass
    os.mkdir(os.path.join(serversPath, createdServerName))
    print('Please wait while the server.jar is downloaded...')
    urllib.request.urlretrieve(versionLink, os.path.join(serversPath, createdServerName, '/server.jar'))
    print(f'\n{createdServerName} has been successfully created with version {serverVersion}')

    with open(f'{serversPath}\\{createdServerName}\\eula.txt', 'w') as eula:
        eula.write('eula=true')
        eula.close()

    with open(f'{serversPath}\\{createdServerName}\\{batchFileName}', 'w') as startingBatchFile:
        startingBatchFile.write('java -Xms1G -Xmx1G -jar server.jar nogui')
        startingBatchFile.close()

def copyWorld(worldToCopyName, worldsPath, serversPath, serverName):
    worldToCopySRC = worldsPath + '\\' + worldToCopyName
    worldToCopyDST = serversPath + '\\' + serverName + '\\' + 'world'
    try:
        shutil.rmtree(worldToCopyDST)
    except FileNotFoundError:
        pass
    try:
        shutil.copytree(worldToCopySRC, worldToCopyDST)
    except FileNotFoundError:
        input(f'ERROR - {worldToCopyName} doesn\'t exist.\n')

def clearWorldPlayerData(serverName, serversPath):
    serverWorld = serversPath + '\\' + serverName + '\\' + 'world'
    shutil.rmtree(serverWorld + '\\advancements')
    shutil.rmtree(serverWorld + '\\playerdata')
    shutil.rmtree(serverWorld + '\\stats')
    with nbtlib.load(serverWorld + '\\level.dat') as leveldat:
        try:
            del leveldat.root['Data']['Player'] 
        except KeyError:
            pass

def startServer(serversPath, serverName, batchFileName):
    try:
        os.chdir(serversPath + '\\' + serverName)
        os.system(f'start cmd /c "{batchFileName}"')
    except FileNotFoundError:
        input(f'ERROR - You don\'t have a batch file to start your server with! Make sure {batchFileName} is in ' + serversPath + '\\' + serverName)

def hostServer(serversPath, ngrokAuthToken, region, config):
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
                "ngrokDisabled": config['ngrokDisabled'],
                "refreshNgrokLogin": False,
            }
            json.dump(configData, configFile)
    os.system(f'start ngrok.exe tcp -region {region} 25565')

def copyServerIP():
    getPortInfo = requests.get('http://localhost:4040/api/tunnels')
    portInfo = json.loads(getPortInfo.content)
    serverIP = portInfo['tunnels'][0]['public_url'][6:]
    pyperclip.copy(serverIP)
    print('Server IP has been copied!\n')

def downloadNgrok(serversPath):
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
            "ngrokDisabled": False,
            "refreshNgrokLogin": True
        }
        json.dump(configData, configFile)

def createAliases():
    with open('C:\\Pyrite\\aliases.json', 'w') as aliasesFile:
        aliasData = {
            "config": ["config"],
            "configAliases": {
                "serversPath": ["serversPath"],
                "worldsPath": ["worldsPath"],
                "region": ["region"],
                "batchFileName": ["batchFileName"],
                "ngrokAuthToken": ["ngrokAuthToken"],
                "ngrokDisabled": ["ngrokDisabled"],
                "toggleNgrok": ["toggleNgrok"],
                "refreshNgrokLogin": ["refreshNgrokLogin"]
            },
            "startServer": ["startServer"],
            "createServer": ["createServer"],
            "copyIP": ["copyIP"],
            "alias": ["alias"]
        }
        json.dump(aliasData, aliasesFile)

def main():
    if not os.path.isdir('C:\\Pyrite') and not os.path.exists('C:\\Pyrite\\config.json'):
        os.mkdir('C:\\Pyrite')
        createConfig()
    elif os.path.isdir('C:\\Pyrite') and not os.path.exists('C:\\Pyrite\\config.json'):
        createConfig()

    if not os.path.isdir('C:\\Pyrite') and not os.path.exists('C:\\Pyrite\\aliases.json'):
        os.mkdir('C:\\Pyrite')
        createAliases()
    elif os.path.isdir('C:\\Pyrite') and not os.path.exists('C:\\Pyrite\\aliases.json'):
        createAliases()

    while True:
        cmd = input('> ')
        cmd = shlex.split(cmd)

        with open('C:\\Pyrite\\config.json', 'r') as configJson:
            config = json.load(configJson)

        serversPath = config['serversPath']
        worldsPath = config['worldsPath']
        region = config['region']
        batchFileName = config['batchFileName']
        ngrokAuthToken = config['ngrokAuthToken']
        ngrokDisabled = config['ngrokDisabled']
        refreshNgrokLogin = config['refreshNgrokLogin']

        with open('C:\\Pyrite\\aliases.json', 'r') as aliasesJson:
            aliases = json.load(aliasesJson)

        configAliases = aliases['config']
        serversPathAliases = aliases['configAliases']['serversPath']   
        worldsPathAliases = aliases['configAliases']['worldsPath']
        regionAliases = aliases['configAliases']['region']
        batchFileNameAliases = aliases['configAliases']['batchFileName']
        ngrokAuthTokenAliases = aliases['configAliases']['ngrokAuthToken']
        ngrokDisabledAliases = aliases['configAliases']['ngrokDisabled']  
        toggleNgrokAliases = aliases['configAliases']['toggleNgrok']
        refreshNgrokLoginAliases = aliases['configAliases']['refreshNgrokLogin']
        startServerAliases = aliases['startServer']
        createServerAliases = aliases['createServer']
        copyIPAliases = aliases['copyIP']
        aliasAliases = aliases['alias']

        if cmd[0] in configAliases:
            if cmd[1] in serversPathAliases:
                config.update({'serversPath': cmd[2]})

            elif cmd[1] in worldsPathAliases:
                config.update({'worldsPath': cmd[2]})
            
            elif cmd[1] in regionAliases:
                config.update({'region': cmd[2]})

            elif cmd[1] in batchFileNameAliases:
                config.update({'batchFileName': cmd[2]})

            elif cmd[1] in ngrokAuthTokenAliases:
                config.update({'ngrokAuthToken': cmd[2]})
            
            elif cmd[1] in ngrokDisabledAliases:
                config.update({'ngrokDisabled': cmd[2]})

            elif cmd[1] in toggleNgrokAliases:
                if config['ngrokDisabled'] == False:
                    config.update({'ngrokDisabled': json.loads('true')})

                if config['ngrokDisabled'] == True:
                    config.update({'ngrokDisabled': json.loads('false')})

            elif cmd[1] in refreshNgrokLoginAliases:
                config.update({'refreshNgrokLogin': json.loads('true')})

            with open('C:\\Pyrite\\config.json', 'w') as configFile:
                json.dump(config, configFile)

        elif cmd[0] in startServerAliases:
            if (cmd[1].startswith('"') and cmd[1].endswith('"')) or (cmd[1].startswith("'") and cmd[1].endswith("'")):
                cmd[1] == cmd[1][1:][:1]
            
            try:
                if cmd[2].startswith('copyworld='):
                    copyworldname = cmd[2][10:]
                    if cmd[2].endswith('.cpd'):
                        copyworldname = copyworldname[:-4]
                    copyWorld(copyworldname, worldsPath, serversPath, cmd[1])
                    if cmd[2].endswith('.cpd'):
                        clearWorldPlayerData(cmd[1], serversPath)

            except IndexError:
                pass

            startServer(serversPath, cmd[1], batchFileName)
            print(f'Server {cmd[1]} has been successfully started.\n')
            if config['ngrokDisabled'] == 'false':
                hostServer(serversPath, ngrokAuthToken, region, config)

        elif cmd[0] in createServerAliases:
            serverSetup(serversPath, batchFileName, cmd[1], cmd[2])

        elif cmd[0] in copyIPAliases:
            copyServerIP()
        
        elif cmd[0] in aliasAliases:
            if cmd[1] in configAliases:
                if cmd[2] == 'add':
                    configAliases.append(cmd[3])
                elif cmd[2] == 'remove' or cmd[2] == 'del':
                    try:
                        configAliases.remove(cmd[3])
                    except ValueError:
                        print(f'{cmd[3]} is not an alias for \'config\'')

            elif cmd[1] in serversPathAliases:
                if cmd[2] == 'add':
                    serversPathAliases.append(cmd[3])
                elif cmd[2] == 'remove' or cmd[2] == 'del':
                    try:
                        serversPathAliases.remove(cmd[3])
                    except ValueError:
                        print(f'{cmd[3]} is not an alias for \'serversPath\'')

            elif cmd[1] in worldsPathAliases:
                if cmd[2] == 'add':
                    worldsPathAliases.append(cmd[3])
                elif cmd[2] == 'remove' or cmd[2] == 'del':
                    try:
                        worldsPathAliases.remove(cmd[3])
                    except ValueError:
                        print(f'{cmd[3]} is not an alias for \'worldsPath\'')

            elif cmd[1] in regionAliases:
                if cmd[2] == 'add':
                    regionAliases.append(cmd[3])
                elif cmd[2] == 'remove' or cmd[2] == 'del':
                    try:
                        regionAliases.remove(cmd[3])
                    except ValueError:
                        print(f'{cmd[3]} is not an alias for \'region\'')

            elif cmd[1] in batchFileNameAliases:
                if cmd[2] == 'add':
                    batchFileNameAliases.append(cmd[3])
                elif cmd[2] == 'remove' or cmd[2] == 'del':
                    try:
                        batchFileNameAliases.remove(cmd[3])
                    except ValueError:
                        print(f'{cmd[3]} is not an alias for \'batchFileName\'')

            elif cmd[1] in ngrokAuthTokenAliases:
                if cmd[2] == 'add':
                    ngrokAuthTokenAliases.append(cmd[3])
                elif cmd[2] == 'remove' or cmd[2] == 'del':
                    try:
                        ngrokAuthTokenAliases.remove(cmd[3])
                    except ValueError:
                        print(f'{cmd[3]} is not an alias for \'ngrokAuthToken\'')

            elif cmd[1] in ngrokDisabledAliases:
                if cmd[2] == 'add':
                    ngrokDisabledAliases.append(cmd[3])
                elif cmd[2] == 'remove' or cmd[2] == 'del':
                    try:
                        ngrokDisabledAliases.remove(cmd[3])
                    except ValueError:
                        print(f'{cmd[3]} is not an alias for \'ngrokDisabled\'')

            elif cmd[1] in toggleNgrokAliases:
                if cmd[2] == 'add':
                    toggleNgrokAliases.append(cmd[3])
                elif cmd[2] == 'remove' or cmd[2] == 'del':
                    try:
                        toggleNgrokAliases.remove(cmd[3])
                    except ValueError:
                        print(f'{cmd[3]} is not an alias for \'toggleNgrok\'')

            elif cmd[1] in refreshNgrokLoginAliases:
                if cmd[2] == 'add':
                    refreshNgrokLoginAliases.append(cmd[3])
                elif cmd[2] == 'remove' or cmd[2] == 'del':
                    try:
                        refreshNgrokLoginAliases.remove(cmd[3])
                    except ValueError:
                        print(f'{cmd[3]} is not an alias for \'refreshNgrokLogin\'')

            elif cmd[1] in startServerAliases:
                if cmd[2] == 'add':
                    startServerAliases.append(cmd[3])
                elif cmd[2] == 'remove' or cmd[2] == 'del':
                    try:
                        startServerAliases.remove(cmd[3])
                    except ValueError:
                        print(f'{cmd[3]} is not an alias for \'startServer\'')

            elif cmd[1] in createServerAliases:
                if cmd[2] == 'add':
                    createServerAliases.append(cmd[3])
                elif cmd[2] == 'remove' or cmd[2] == 'del':
                    try:
                        createServerAliases.remove(cmd[3])
                    except ValueError:
                        print(f'{cmd[3]} is not an alias for \'createServer\'')

            elif cmd[1] in copyIPAliases:
                if cmd[2] == 'add':
                    copyIPAliases.append(cmd[3])
                elif cmd[2] == 'remove' or cmd[2] == 'del':
                    try:
                        copyIPAliases.remove(cmd[3])
                    except ValueError:
                        print(f'{cmd[3]} is not an alias for \'copyIP\'')

            elif cmd[1] in aliasAliases:
                if cmd[2] == 'add':
                    aliasAliases.append(cmd[3])
                elif cmd[2] == 'remove' or cmd[2] == 'del':
                    try:
                        aliasAliases.remove(cmd[3])
                    except ValueError:
                        print(f'{cmd[3]} is not an alias for \'alias\'')

            aliasData = {
                "config": configAliases,
                "configAliases": {
                    "serversPath": serversPathAliases,
                    "worldsPath": worldsPathAliases,
                    "region": regionAliases,
                    "batchFileName": batchFileNameAliases,
                    "ngrokAuthToken": ngrokAuthTokenAliases,
                    "ngrokDisabled": ngrokDisabledAliases,
                    "toggleNgrok": toggleNgrokAliases,
                    "refreshNgrokLogin": refreshNgrokLoginAliases
                },
                "startServer": startServerAliases,
                "createServer": createServerAliases,
                "copyIP": copyIPAliases,
                "alias": aliasAliases
            }

            with open('C:\\Pyrite\\aliases.json', 'w') as aliasesFile:
                json.dump(aliasData, aliasesFile)

        else:
            print(f'\'{cmd[0]}\' is not a valid command.\n')

if __name__ == '__main__':
    main()            

"""
To Do:
Optimize File Paths (os.path.join() where necessary)
Test Thoroughly
"""