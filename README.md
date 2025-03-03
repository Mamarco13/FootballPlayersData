# FootballPlayersData

## Launching the Program

To start the project, you need to execute the `init.sh` file.

> [!WARNING] 
> The `init.sh` file has been modified to allow anyone to execute it. If it doesn't work, you can grant execution permissions using the following command:
>
> ```bash
> sudo chmod +x init.sh
> ```

Once you have the necessary permissions, simply execute the following command in the terminal:

```bash
./init.sh
```

> [!CAUTION] 
> Ensure that all required modules are installed. The required modules are **pandas**, **matplotlib**, **poetry** and **flask**.

To install the first modules, execute the following commands in the terminal:

```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install flask pandas matplotlib
```
To install poetry is a bit more difficult:

```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```
If your Internet connection is not so good, the installation may fail at first, but in a second try it will work perfectly.

## Using the Application

Once you have started the application, you will see a screen similar to this:

![Main screen capture](/RM_Screenshots/mainscreen.png)

### Selecting Leagues

If you select "Leagues," a screen like this will appear. You can choose as many leagues as you want and set the number of players to display:

![League selection capture](/RM_Screenshots/leagues.png)

### Selecting Clubs

If you select "Clubs," a screen like this will appear. You can choose as many clubs as you want and define the number of players to display (maximum 20):

![Club selection capture](/RM_Screenshots/clubs.png)

### Viewing Results

Regardless of the option you choose, you will access a template where only the displayed information changes. Here, you can see the selected number of players ordered by their market value. You will also have the option to access their profiles to get more detailed information.

![Players list capture](/RM_Screenshots/players.png)

### Profile Page

The profile page of a player will look like this:

![Profile capture](/RM_Screenshots/profile.png)

### Error Page

If something goes wrong during execution, an error page like this will be displayed:

![Error capture](/RM_Screenshots/error.png)

---

With this guide, you can set up, run, and explore the **FootballPlayersData** application. If you encounter any issues or have questions, feel free to seek additional help.

