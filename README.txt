Set up:

Put the Python Script and Tif FIle into your C4D Scripts Folder (Windows: C:\Program Files\MAXON\CINEMA 4D R18\library\scripts).
Inside Cinema go to 'Script', 'User Scripts', 'Save_Every_Frame'.

Enter the first frame, enter the last frame. (There is an extra pop up window for the first and last frame, respectively.)

Now the Script will run and automatically set your 'Settings, Frame-Range' to 'Current Frame'.
Sets yor 'Preferences, Texture Paths' to your working Directory (The Directory of your current C4D working File).
Checks if a 'Render' Folder exists in the same Directory, and creates it if necessary.
Checks if a Folder inside 'Render' with the name of your current C4D File exists and then create an incremented Folder.
Saves a new C4D File inside this Folder for every Frame.