# Most-Active-Subreddit-Posters
A script that locates the most active users in a subreddit within the past week and flairs them based on their activity level.

## Usage
To use this script, ensure that the account you intend to use is a moderator in the specified subreddit.

## Setting up
- Ensure you have Python installed on your system. You can download it here https://www.python.org/downloads/ (Make sure you add to PATH during the installation).
- Download the ZIP file of this repo (Click on ```Code``` -> ```Download ZIP```).
- Open your command prompt and change your directory to the location of the unzipped files (```cd location-of-unzipped-files```).
- Install the PRAW package ```pip install praw```.
- Create a Reddit App (script) at https://www.reddit.com/prefs/apps/ and get your ```client_id``` and ```client_secret```.
- Edit the ```config.ini``` file with your details.
- Run the program ```python main.py```.
