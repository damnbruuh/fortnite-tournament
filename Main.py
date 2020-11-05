from tkinter import Tk, ttk, Frame, PhotoImage, Label, LabelFrame, Text, Button, Toplevel, Scrollbar, messagebox, filedialog, END, simpledialog
import os, operator
from Player import Player

# Initialize the list intended for storing Player objects
players = []

# Total players entered into tournament
totalPlayers = 60

# Close player list top view window
def close_topview():
    # View main window
    root.update()
    root.deiconify()
    
    # Delete top-level window
    top_level.withdraw()
    
# Open player list top view window   
def view_players():
    # Delete main window
    root.withdraw()
    
    # View top-level window
    top_level.update()
    top_level.deiconify()

# Handle exiting the program
def exit_program():

    answer = messagebox.askyesno("Exit", "Are you sure you want to exit?")

    if answer == True:

        exit()

    else:
        # do nothing
        pass

# Function passed to btnGetPlayers
def get_players():

    global players, filename

    # Open file dialog, ask user to open a file
    # Open file dialog in the running directory of this program
    filename = filedialog.askopenfilename(initialdir=os.getcwd())

    # Begin reading the text file
    try:
        with open(filename, "r") as reader:
        
            line = reader.readline()
            while line != "":
        
                # Split the line into a list of split strings
                splitData = line.split(",")
        
                # Create player object using the string above split by commas
                player = Player(splitData[0], splitData[1], int(splitData[2]), splitData[3].strip("\n"))
        
                # Append previously created player object to list
                players.append(player)
                line = reader.readline()
    except FileNotFoundError:
        messagebox.showerror("Error", "This is not a valid file type")
    except IndexError:
        messagebox.showerror("Error", "This is not a valid file type")
    btnGenerate.config(state="normal")
    output_players()
    
    
# Output players to tree view top-level widget
def output_players():
    global players
    # Clear items 
    for i in tview.get_children():
        tview.delete(i)

    # Insert player objects to tree view
    for player in range(len(players)):
        tview.insert("", END, values=(players[player].getLastName(), players[player].getFirstName(), players[player].getTierScore(),
            players[player].getTier()))
 
# Sort players by headings 
def sort_players(headingNum):
    global players
    # Sort ascending last names
    if headingNum == 1:
        players.sort(key=operator.attrgetter("lastName"))
    # Sort ascending first names
    elif headingNum ==2:
        players.sort(key=operator.attrgetter("firstName"))
    # Sort descending rating, then ascending last name
    elif headingNum ==3:
        players = sorted(sorted(players,
                    key=operator.attrgetter('lastName')),
                    key=operator.attrgetter('tierScore'), reverse=True)
    # Sort ascending tier names
    elif headingNum ==4:
        players.sort(key=operator.attrgetter("tier"))
    # Output sorted lists to tree view
    output_players()

# Delete player from tree view
def delete_player():
    global filename, players
    # Get user selection
    playerid = tview.selection()
    selectedPlayer = tview.item(playerid)["values"]
    # Nothing selected
    if selectedPlayer == "":
        messagebox.showerror("Error", "Please select a player to remove.")
    else:
        answer = messagebox.askyesno("Remove Item", "Are you sure you want to remove " + selectedPlayer[1] + " " + selectedPlayer[0]+ "?")
        # User confirms deletion
        if answer == True:
            # Delete player object from list corresponding with tree view selection
            for x in players:    
                if (x.getLastName() + "," + x.getFirstName() + "," + str(x.getTierScore()) + ","  + x.getTier()) == (selectedPlayer[0] + "," + selectedPlayer[1] + "," + str(selectedPlayer[2]) + ","  + selectedPlayer[3]):
                        players.remove(x)
                        break
        # Delete from tree view   
        tview.delete(playerid)
        # Update document
        update_playerlist()

# Add player to tree view            
def add_player():
    global totalPlayers, players
    addLastName, addFirstName = True, True
    # Can't have than 64 players
    if totalPlayers >= 64:
        messagebox.showwarning("Error", "No more players can be added.\nThe tournament has reached its capacity of 64 competitors")
    else: 
        # Add first name
        while addFirstName:
            playerFirstName = simpledialog.askstring("Add Player", "Enter player's first name:")
            # Player entered a string, go to next value
            if playerFirstName != "":
                addFirstName = False
            else:
                messagebox.showerror("Error", "Please add a first name")
        # Add last name
        while addLastName:  
            playerLastName = simpledialog.askstring("Add Player", "Enter player's last name:")    
            # Player entered a string, go to next value
            if playerLastName != "":
                addLastName = False 
            else:
                messagebox.showerror("Error", "Please add a last name") 
        # Check for duplicate player
        duplicate = False
        for i in tview.get_children():
            x = tview.set(i)
            # Last name and first names are the same
            if x["1"] == playerLastName and x["2"] == playerFirstName:
                messagebox.showerror("Error", playerFirstName + " " + playerLastName + " already exists!")
                # Select player
                tview.selection_set(i)
                tview.see(i)
                duplicate = True
                break
        # No duplicates found
        if duplicate == False:
            # Add rating, check if between 0 and 100
            playerRating = simpledialog.askinteger("Add Player", "Enter player's rating (1-100):", minvalue=0, maxvalue=100)        
            # Calculate rank
            playerRank = calc_rank(playerRating) 
            # Insert new player
            playerid = tview.insert ("", END, values=(playerLastName, playerFirstName,playerRating, playerRank))
            # Select new player
            tview.selection_set(playerid)
            # Scroll to new player
            tview.see(playerid)
            # Get value info on new player
            info = tview.item(playerid)["values"]
            # Create new player object with info
            player = Player(info[0], info[1], info[2], info[3])
            # Add player object to list
            players.append(player)
            # Update document
            update_playerlist()
            
# Update document of players            
def update_playerlist():
    global players, filename, totalPlayers
    index = 0
    # Total players in tournament is total players in tree view
    totalPlayers = len(tview.get_children())
    for x in tview.get_children():
        # Get values of item
        info = tview.item(x)["values"]
        # Set values of player object
        players[index].setLastName(info[0])
        players[index].setFirstName(info[1])
        players[index].setTierScore(info[2])
        players[index].setTier(info[3])
        # Next object in list
        index += 1
    # Over write file  
    with open(filename, "wt") as writer:
        # For each player object, write comma delimited string on new line
        for x in players:
            writer.write(x.getLastName() + "," + x.getFirstName() + "," + str(x.getTierScore()) + "," + x.getTier() +"\n")
            
# Edit player rating
def edit_player():
    global filename
    # Get user selection
    playerid = tview.selection()
    selectedPlayer = tview.item(playerid)["values"]
    # Nothing selected
    if selectedPlayer == "":
        messagebox.showerror("Error", "Please select a player to edit.")
    else:
        # Edit rating, check if between 0 and 100
        playerRating = simpledialog.askinteger("Add Player", "Enter player's rating (1-100):", minvalue=0, maxvalue=100) 
        playerTier = calc_rank(playerRating) 
        tview.set(playerid,column=3, value=playerRating)
        tview.set(playerid,column=4, value=playerTier)
        # Select new player
        tview.selection_set(playerid)
        # Scroll to new player
        tview.see(playerid)  
        # Update document  
        update_playerlist()   
# Search for player
def search_player():
    searchPlayer = simpledialog.askstring("Search Player", "Enter player's name (FistName LastName):")
    # Search for player
    found = False
    for i in tview.get_children():
        x = tview.set(i)
        # Ignore case sensitivity when comparing names
        if (x["2"] +  " " +  x["1"]).lower() == searchPlayer.lower():
            # Select player
            tview.selection_set(i)
            tview.see(i)
            found = True
            break  
    # Can't find player
    if found == False:
        messagebox.showerror("Search Player", searchPlayer + " is not entered in the tournament")
               
# Calculate player's rank based on their rating       
def calc_rank(rating):
    if rating < 50:
        return "Scout"     
    elif rating >= 50 and rating <= 59:
        return "Ranger"
    elif rating >= 60 and rating <= 69:
        return "Agent"
    elif rating >= 70 and rating <= 79:
        return "Epic"
    elif rating >= 80:
        return "Legend"
    # Doesn't correspond with existing ranks
    else:
        return None
    
# Initialize window and centre  
root = Tk()
root.title('Fortnite Team Tournament')
root.geometry('%dx%d+%d+%d' % (912, 740, root.winfo_screenwidth() // 2 - 912 // 2,
    root.winfo_screenheight() // 2 - 740 // 2))
root.resizable(False, False)
# Create frame
frame = Frame(root, padx=10, pady=10, bg='white')
frame.pack()
# Create Fornite banner 
imgBanner = PhotoImage(file='images/fortnite_banner.png')
lblBanner = Label(frame, image=imgBanner, padx=10, pady=10, borderwidth=0)
lblBanner.grid(row=0, column=0, columnspan=5, pady=5)
# Create team grid
lblFrames = [0] * 16
txtTeams = [0] * 16
rownum, colnum = 1, 0
for i in range(len(lblFrames)):
    lblFrames[i] = LabelFrame(frame, text='TEAM ' + str(i+1), bg='white', font=('Consolas', 11, 'bold'))
    txtTeams[i] = Text(lblFrames[i], width=25, height=6, font=('Consolas', 8), state='disabled', relief='flat', bg='white')
    txtTeams[i].pack(padx=5, pady=5)
    
    lblFrames[i].grid(row=rownum, column=colnum, padx=5, pady=5)
    if (i + 1) % 4 == 0:
        rownum += 1
        colnum = 0
    else:
        colnum += 1
# Create frame for buttons
buttonFrame = Frame(frame, padx=10, pady=10, bg='white')
buttonFrame.grid(row=1, column=4, rowspan=4)
# Create Buttons and pack to button frame
btnPlayers = Button(buttonFrame, text='GET PLAYERS', width=15, height=2, command=get_players)
btnPlayers.pack(side='top', padx=5, pady=5)
btnView = Button(buttonFrame, text='VIEW PLAYERS', width=15, height=2, command=view_players)
btnView.pack(side='top', padx=5, pady=5)
btnGenerate = Button(buttonFrame, text='GENERATE', width=15, height=2, state='disabled')
btnGenerate.pack(side='top', padx=5, pady=5)
btnSave = Button(buttonFrame, text='SAVE TEAMS', width=15, height=2, state='disabled')
btnSave.pack(side='top', padx=5, pady=5)
btnClear = Button(buttonFrame, text='CLEAR', width=15, height=2)
btnClear.pack(side='top', padx=5, pady=5)
btnExit = Button(buttonFrame, text='EXIT', width=15, height=2, command=exit_program)
btnExit.pack(side='top', padx=5, pady=5)
# Create Fortnite logo
imgLogo = PhotoImage(file='images/fortnite_logo.png')
lblLogo = Label(buttonFrame, image=imgLogo, borderwidth=0, bg='white').pack(side='top', padx=5, pady=5)
# Create top-level widget for player list
img = PhotoImage(file='images/fortnite.png')
top_level = Toplevel(padx=10, pady=10, bg='white')
top_level.title('Player List')
top_level.resizable(False, False)
top_level.protocol('WM_DELETE_WINDOW', close_topview)
top_level.geometry('%dx%d+%d+%d' % (490, 635, root.winfo_screenwidth() // 2 - 490 // 2, root.winfo_screenheight() // 2 - 635 // 2))
top_level.withdraw()

lblImg = Label(top_level, image=img, bg='white')
lblImg.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
# Create tree view in top-level widget
style = ttk.Style()
style.configure('mystyle.Treeview.Heading', font=('Consolas', 11, 'bold'))
# Tree view headings and columns
tview = ttk.Treeview(top_level, selectmode='browse', columns=('1', '2', '3', '4'), show='headings', height=20, style='mystyle.Treeview')
tview.grid(row=1, column=0, pady=5)
headingtext = ('LAST NAME', 'FIRST NAME', 'RATING', 'TIER')
columnwidths = [150, 150, 75, 75]
for i in range(4):
    tview.column(str(i+1), width=columnwidths[i], anchor='w')
    tview.heading(str(i+1), text=headingtext[i], anchor='w', command=lambda columnid=i+1: sort_players(columnid))
# Scroll bar
vscroll = Scrollbar(top_level, orient='vertical', command=tview.yview)
vscroll.grid(row=1, column=1, sticky='ns')
bottomFrame = Frame(top_level, padx=5, pady=5, bg='white')
bottomFrame.grid(row=2, column=0, columnspan=2)
# Player list buttons
btnRemove = Button(bottomFrame, text='REMOVE', width=10, pady=5, command=lambda: delete_player())
btnRemove.pack(side='left', padx=5, pady=5)
btnAdd = Button(bottomFrame, text='ADD', width=10, pady=5, command= lambda: add_player())
btnAdd.pack(side='left', padx=5, pady=5)
btnEdit = Button(bottomFrame, text='EDIT', width=10, pady=5, command= lambda: edit_player())
btnEdit.pack(side='left', padx=5, pady=5)
btnSearch = Button(bottomFrame, text='SEARCH', width=10, pady=5, command = lambda: search_player())
btnSearch.pack(side='left', padx=5, pady=5)
# Output window
root.mainloop()
