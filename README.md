# Pyrite

Pyrite is a program that provides useful server tools for Minecraft


**Features:**
* Easy Server Creation (Vanilla Only & Certain Modpacks)
* World Copying
* Map Testing Mode (and Clearing Player Data)
* Server Hosting using ngrok

**DISCLAIMER: I am not responsible if you mess up your world files, your server files, or the directory the program is in if you don't specify the proper filenames.**

## Commands:
Pyrite v2 has a terminal like interface instead of Pyrite v1's set series of inputs. 
The following section will explain the different commands, what they are for, and how to use them.

### 'config':
```config [variable] [value]```

This command is used to set various config variables. See the configuration section for more info.

### 'startServer':
```startServer [name] (copyworld="My World")(.cpd)```

This command can start a pre-existing server. If `ngrokDisabled` is set to false, running this command will also start ngrok.
The config variable `serversPath` must be specified for this command to work.

In this example, I will have "Survival" as my server name.
To run the server, use ```startServer "Survival"```. The quotes around the server name is important. 

To copy a world to your server, use the `copyworld` parameter, like so: ```startServer "Survival" copyworld="My Survival World"```.
This has to have `worldsPath` set in the config. Again, the quotes around the world name is important. 

To remove the player data from said world, add `.cpd` to the end of the `copyworld` parameter:
```startServer "Survival" copyworld="My Survival World".cpd```

### 'createServer':
```createServer [name] [version]```

This command will create a vanilla server. (See the Modpack section of this readme for a list of supported modpacks.)
The config variable `serversPath` must be specified for this command to work.

The name can be whatever you want (within reason of the Windows valid names).
The version follows the list of the Minecraft version names: (1.15.1, 18w43a, 1.8.3, 1.8.2-pre7, etc.). 
You can also use `latest`, `latest.release`, and `latest.snapshot`. `latest` will use the most recent version, snapshot or version. `latest.release` will use the latest full release, and `latest.snapshot` will use the most recent snapshot. Modpacks also have their own version name. See the Modpacks section for a list of supported modpacks.

### 'copyIP':
```copyIP```

This command copies the IP assigned to your server when you use ngrok. Ngrok must be running for this to work. If ngrok is not running, Pyrite will return an error. 

### 'alias':
```alias [command] [name]```

This command allows you to change commands to whatever you like. Using ```alias createServer cs``` will allow you to create a server by using ```cs [name] [version]```. You can also set config variables by using ```alias [variable] [name]```. See the configuration section for more info.


## Configuration
