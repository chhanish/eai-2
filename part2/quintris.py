# Simple quintris program! v0.2
#Teammates:
#Akhil Yenisetty: nyeniset,Prasad hegde: phegde,Hanish Chidipothu: hachid


# D. Crandall, Sept 2021


from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
import time, sys,copy

class HumanPlayer:
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. quintris is an object that lets you inspect the board, e.g.:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    # count number of blocked holes
    def countHoles(self,board,rowCutOff):
        return (len(board)-rowCutOff)*len(board[0])-sum([row.count('x') for row in board])

    # what is height of the column 
    def columnPeak(self,board,column):
        row=0
        while row<len(board):
                if board[row][column]=='x':
                    break
                row+=1
        return row

    # total number of pits in the board
    def pits(self,board):
        return sum([1 for column in range(len(board[0])) if self.columnPeak(board,column)==len(board)])
    
    # total number of bumps in the board
    def bumps(self,board):
        return sum([abs(self.columnPeak(board,column)-self.columnPeak(board,column+1)) for column in range(len(board[0])-1)])
    
    # total holes in the board
    def countTotalHoles(self,board):
        width=len(board[0])
        totalHoles=0
        for col in range(width):
            row = self.columnPeak(board,col)
            totalHoles+=[board[r][col] for r in range(row,len(board))].count(' ')
        return totalHoles

    # score can be achieved from a board configuration
    @staticmethod  
    def calculateScore(board):
        return sum([1 for row in board if row.count('x')==len(board)])

    # total number of wells in the board
    def wells(self,board):
        colHeights=[len(board)-self.columnPeak(board,column) for column in range(len(board[0]))]
        falling=True
        raising=False
        wells=0
        for i in range(len(colHeights)-1):
            if colHeights[i]<colHeights[i+1]:
                raising=True
                if(falling and raising):
                    wells+=1
                falling=False
            elif colHeights[i]>colHeights[i+1]:
                falling=True
                if i+1==len(colHeights)-1:
                    wells+=1
                raising=False

        return wells
            
    # what is the heighest point in the board
    def findBoardPeak(self,board):
        row=0
        while row<len(board):
            if 'x' in board[row]:
                break
            row+=1
        return (len(board)-row)
    # generate command to move the piece 
    def getMoveCommand(self,piece_col,place_col):
        difference = place_col-piece_col
        if difference>0:
            return 'm'*difference
        return 'b'*abs(difference)
    # parameter that tells how far are we from reaching end of the game
    def isEnding(self,board):
        colHeights=min([self.columnPeak(board,column) for column in range(len(board[0]))])
        if colHeights<5:
            return 1000
        else:
            return 0

    def findScore(self,board):
        
        boardPeak=self.findBoardPeak(board)
        peakFactor=boardPeak/10
        rowRemoveScore=self.calculateScore(board)
        bumps=self.bumps(board)*peakFactor
        pits=self.pits(board)*peakFactor
        wells=self.wells(board)*peakFactor
        countHoles=self.countTotalHoles(board)
        
        return (rowRemoveScore*100)-(boardPeak+bumps+pits+wells+countHoles*20+self.isEnding(board))
        
    # generate all successors
    def successors(self,quintris):
        cQuintris=copy.deepcopy(quintris)
        (board,score) = cQuintris.state
        succ=[]
        pieceList=[]
        for action in [None, 'h']:
            allotropes=3
            command=''
            if action=='h':
                    quintris.hflip()
                    command+='h'
            
            while allotropes>=0:
                cQuintris=copy.deepcopy(quintris)
                for act in command:
                    if act=='h':
                       cQuintris.hflip()
                (piece,_,piece_col) = cQuintris.get_piece()
                
                if piece in pieceList:
                    continue
                for column in range(0,len(board[0])):
                    move=''
                    cQuintris=copy.deepcopy(quintris)
                    if column < piece_col:
                        for i in range(column,piece_col):
                            cQuintris.left()
                            move += "b"
                        cQuintris.down()
                        
                        newBoard = cQuintris.get_board()
                        score=self.findScore(newBoard)
                        succ.append((score,newBoard,command+move))
                    if column > piece_col:
                        for i in range(column,len(board[0])-len(max(piece[0],key = len))):
                            cQuintris.right()
                            move += "m"
                        cQuintris.down()
                        newBoard = cQuintris.get_board()
                        score=self.findScore(newBoard)
                        succ.append((score,newBoard,command+move))
                    if column == piece_col:
                        cQuintris.down()
                        newBoard = cQuintris.get_board()
                        score=self.findScore(newBoard)
                        succ.append((score,newBoard,command+move))
                allotropes-=1
                quintris.rotate()
                command+='n'
        return succ

    def get_moves(self, quintris):
        dQuintris = copy.deepcopy(quintris)
        succ=self.successors(dQuintris)
        return max(succ)[2]

    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "quintris" object to control the movement. In particular:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)

            board = quintris.get_board()
            column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
            index = column_heights.index(max(column_heights))

            if(index < quintris.col):
                quintris.left()
            elif(index > quintris.col):
                quintris.right()
            else:
                quintris.down()


###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)