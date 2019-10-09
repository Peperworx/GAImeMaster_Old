# GAImeMaster
Dungeons and dragons, but the Dm is a AI

## What is is:
gAImeMaster is an online D&D role playing environment in which the dungeon master is the server.


## Contributing
If you want to contribute, clone the repo, make your changes, and then send a pull request. Want ideas on what to contribute? 
Take a look at our trello here: https://trello.com/b/mnbWADDB/gaimemaster 
And our discord server here: https://discord.gg/eHemqCN (Its really lonely for now.)

## Requirements:
* Running instance of [gAImeMasterWebsocket](https://github.com/wireboy5/GAImeMasterWebsocket) 
* jinja2

## To install:
1. Setup your apache2 installation to run python3 cgi scripts per this tutorial: https://www.linux.com/tutorials/configuring-apache2-run-python-scripts/
2. Clone the repository to your document root.
3. Install jinja2 and [gAImeMasterWebsocket](https://github.com/wireboy5/GAImeMasterWebsocket) 
3. Change the Shebangs (#!) to match the location of your python installation.
4. Copy the data folder from https://github.com/wireboy5/gAImeMasterSampleDatabases to your document root
5. Navigate to localhost
6. Click on Account -> login
7. Enter the username admin and the password password
8. Go to manage users.
9. Create a new user with your information and the role admin.
10. Click on Account -> logout
11. Login again with the new user you created
12. Go to manage users and delete the original admin user.
13. You are finished setting up.
