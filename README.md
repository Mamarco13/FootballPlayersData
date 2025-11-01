# FootballPlayersData

**FootballPlayersData** is a Python-based application that lets you search, explore, and analyze live-updated player market values from **Transfermarkt**.
It provides an interactive web interface powered by **Flask**, with data processing and visualization handled through **pandas** and **matplotlib**.

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Mamarco13/FootballPlayersData.git
cd FootballPlayersData
```

### 2. Grant execution permissions

> [!WARNING]  
> The `init.sh` script has been modified to allow execution by default.  
> If you still encounter permission issues, run:

```bash
sudo chmod +x init.sh
```

### 3. Run the initialization script

```bash
./init.sh
```

This will automatically start the application and launch the local web interface.

---

## Requirements

Ensure that the following modules are installed:

- **pandas**
- **matplotlib**
- **flask**
- **poetry**

You can install them manually as follows:

```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install flask pandas matplotlib
```

To install **Poetry**, run:

```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

>  If the installation fails due to a weak internet connection, try running the command again — it usually works on the second attempt.

---

## Using the Application

Once launched, you’ll see the main interface:

![Main screen](/RM_Screenshots/mainscreen.png)

### Selecting Leagues

Click on **Leagues** to filter players by their respective leagues.  
You can select multiple leagues and specify how many top players to display:

![Leagues selection](/RM_Screenshots/leagues.png)

### Selecting Clubs

Click on **Clubs** to explore data by team.  
You can select multiple clubs and define the number of players shown (up to 20):

![Clubs selection](/RM_Screenshots/clubs.png)

### 📊 Viewing Results

Regardless of your selection, you’ll reach a dynamic results page showing players sorted by **market value**.  
From there, you can access each player’s profile for detailed information.

![Players list](/RM_Screenshots/players.png)

### Player Profile Page

Each player profile includes comprehensive stats and market insights:

![Profile page](/RM_Screenshots/profile.png)

### Error Page

If something goes wrong, a custom error page will be displayed to help you debug:

![Error page](/RM_Screenshots/error.png)

---

## Summary

With this guide, you can easily **set up, run, and explore** the FootballPlayersData application.  
If you encounter any issues or have questions, feel free to open an issue on GitHub.

---

**Developed by [Mamarco13](https://github.com/Mamarco13)**
