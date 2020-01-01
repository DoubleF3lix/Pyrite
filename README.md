# Pyrite

Pyrite is a program that provides useful server tools for Minecraft


**Features:**
* Easy Server Creation (Vanilla Only & Certain Modpacks)
* World Copying
* Map Testing Mode (and Clearing Player Data)
* Server Hosting using ngrok

**DISCLAIMER: I am not responsible if you mess up your world files, your server files, or the directory the program is in if you don't specify the proper filenames.**

## Usage:
Pyrite v2 has a terminal like interface instead of Pyrite v1's set series of inputs. 
The following section will explain the different commands, what they are for, and how to use them.

### 'config':
```config [value] [set value]```

This command is used to set various config variables. See the configuration section for more info.

### 'startServer':
```startServer [server name] (copyworld="My World")(.cpd)```
This command can start a pre-existing server. If `ngrokDisabled` is set to false, running this command will also start ngrok.
The config variable `serversPath` must be specified for this command to work.

In this example, I will have 'Survival' as my server name.
To run the server, use ```startServer "Survival"```. The quotes around the server name is important. 

If I want to copy a world to it, I would use ```startServer "Survival" copyworld="My Survival World"```.
This has to have `worldsPath` set in the config. Again, the quotes around the world name is important. 

To remove the player data from said world, add `.cpd` to the `copyworld` parameter, like so:
```startServer "Survival" copyworld="My Survival World".cpd```

## 'createServer':
This command will create a vanilla server. See the bottom of this readme for a list of supported modpacks.
The config variables `serversPath` must be specified for this command to work.


