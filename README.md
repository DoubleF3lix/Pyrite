# Pyrite

Pyrite is a program that provides useful server tools for Minecraft


**Features:**
* Easy Server Creation (Vanilla Only)
* World Copying
* Map Testing Mode (Clears Player Data)
* Server Hosting using ngrok

**DISCLAIMER: I am not responsible if you mess up your world files, your server files, or the directory the program is in if you don't specify the proper filenames.**


## Setting Up
Install `Pyrite v1.1.exe` from the releases menu. Pyrite uses absolute paths instead of relative, so just place the file wherever is convenient for you. When you load Pyrite for the first time, it will create a `config.json`. Please see the Configuration section to learn more.
If you choose to use ngrok, you will need to create an account. To do this, go to https://ngrok.com and click 'Sign Up' in the top right corner. This should take you to the 'Setup & Installation' window. You can choose to install ngrok from here, but Pyrite will automatically install it for you if you choose not to. 
On the dashboard ('Setup & Installation'), click 'Auth' on the left side. From here, you should see an authorization token, and this is what you will copy into the `ngrokAuthToken` field in the `config.json`. Pyrite will automatically log you in once, but if you ever need to use a different authorzation token, you will need to set `refreshNgrokLogin` to `true` in the `config.json`.



## Usage
When you start the program, it will ask if you want to create a server. If you say yes, it will go through the steps to create one.  This is where you specify the server name and version. Downloading the right `.jar` file will take a while, however, so please be patient. After this, it will ask which server you want to create. If the server doesn't exist, it will complain that you don't have a batch file to start the server with. Next, it will ask if you would like to copy a world. If you say yes, it will ask you to specify a world to copy. Then it will ask if you want to enable Map Testing Mode. This clears the `advancments` folder, the `stats`, folder, the `playerdata`, folder, and then it clears the `Players` folder from the `level.dat`. When you join the world, it will be like you were never in it. Then ngrok will start, and you're done!



## Configuration
When you load Pyrite for the first time, it will tell you it created a `config.json` and exit the window. This is stored in `C:\Pyrite\` and cannot be changed. When referencing file paths, please use `\\` instead of `\`. I am not responsible for what breaks if you don't edit the configuration file.

`serversPath` is the directory in which all of your server files handled by Pyrite will be. If you do not set `serversPath` to the directory where your servers are, it cannot find the servers, and won't be usable.

`worldsPath` is the directory where your minecraft saves are. This is by default in `C:\Users\<username>\AppData\Roaming\.minecraft\saves` but it has been left blank by default in case you would like you change it.

`region` is the region code used by ngrok for hosting. If you live in America, this would be `us`. Please see https://en.wikipedia.org/wiki/ISO_3166-2#Current_codes for a list of region codes. This is unnessecary and can be left blank if you choose to not use ngrok.

`batchFileName` is the name of the batch files used to start your server. It is **highly** reccomended you keep this consistent across all servers. It is also the file name given to the startup batch file when you create a server.

`ngrokAuthToken` is the authorization token used to log you into ngrok for hosting. This is unnessecary and can be left blank if you choose to not use ngrok.

`disableNgrok` can be used to disable ngrok if you choose to host the server by yourself. The `region` and `ngrokAuthToken` fields do not need to be filled in if this is set to `true`.

`refreshNgrokLogin` is used to relog you into ngrok if you ever change your authorzation key. This needs to be set to `true` manually, but Pyrite will automatically set this to `false` once it logs you in.
