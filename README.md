## Setup
The instructions below should only be needed once, unless you delete
the repository or something like that.

1. Install Python 3. If you're running Linux, your distribution will
   provide packages you can use.
2. On Windows, run `pip install virtualenv`.
3. Launch a terminal and navigate to this directory. Run
   `virtualenv --python=python3 env`. This creates a virtual Python 3
   environment where you can install packages specific to this app.
4. On OS X or Linux, `source env/bin/activate`. On Windows,
   `env\Scripts\activate`. This activates the virtual environment.
5. Install necessary packages by running
   `pip install -r requirements.txt`.
6. Create a database for the application to use. You can start the
   MySQL command line client with `mysql -u <username> -p`.
7. Use the MySQL command line client to create all the tables. SQL
   is in the `sql/` directory.
8. Copy `config.example.py` to `config.py` and replace any necessary
   fields inside that file. Example things you may need to change are
   the database host, username, password, and database.

## Running the server
1. Open a terminal and navigate to this directory.
2. If you have not yet done so in this terminal window, activate
   the virtual environment. On OS X or Linux,
   `source env/bin/activate`. On Windows, `env\Scripts\activate`.
3. Run the server with `python main.py`. The server will automatically
   reload any changed files, provided that they were saved without
   syntax errors or other problems. If the server stops for this
   reason, you can always start it again by re-running this command.
