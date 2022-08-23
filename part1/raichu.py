#
# raichu.py : Play the game of Raichu
#Teammates:
#Akhil Yenisetty: nyeniset,Prasad hegde: phegde,Hanish Chidipothu: hachid
# Based on skeleton code by D. Crandall, Oct 2021
#
import sys
import time
import copy


class Pieces:
    def __init__(self, id):
        self.id = id
        self.teamA={'w':10,"W":20,'@':50,}
        self.teamB={"B":20,"b":10,'$':50,}
        self.order={
            10:[(1,1),(1,-1),],
            20:[(0,-1),(0,1),(1,0),],
            50:[(0,1),(0,-1),(-1,0),(1,0),(1,-1),(-1,-1),(-1,1),(1,1),]
            }
        self.stepLimit={
            10:1,
            20:2,
            50:float('inf')
        }
        self.myTeamOrder=self.teamA if self.id in self.teamA.keys() else self.teamB
        self.myTeam=self.myTeamOrder.keys()
        self.myRank=self.myTeamOrder[self.id]
        self.opponent= self.teamB if self.id in list(self.teamA) else self.teamA

        # successor piece when pichu or pikachu reaches the other end
    def successor(self):
        return max(self.myTeamOrder, key=self.myTeamOrder.get)
        
        # check if the piece can kill the given piece
    def canKill(self,piece):
        if piece in self.myTeam:
            return False
        return self.myRank>=self.opponent[piece]

        # return all movements for the piece
    def movements(self):
        if 'b' in self.myTeam and self.myRank<=20:
            return [(-x,-y) for x, y in self.order[self.myRank]]

        else:
            return self.order[self.myRank]

        # max steps the piece can take
    def maxSteps(self):
        return self.stepLimit[self.myRank]
        # other end for the given player
    def otherEnd(self,size):
        return size-1 if self.id in list(self.teamA) else 0


def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

# matrix form board to original string format
def matrixToString(board):
    return "".join([c for r in board for c in r])

# check win
def gameover(state):
    stringBoard=matrixToString(state)
    playerA=Pieces('w')
    playerB=Pieces('b')
    strengthA=sum([stringBoard.count(p)*playerA.teamA[p] for p in list( playerA.myTeam)])
    strengthB=sum([stringBoard.count(p)*playerB.teamB[p] for p in list( playerB.myTeam)])
    if strengthA==0 or strengthB==0:
        return True
    else:
        return False
# convert string board to matrix
def matrixBoard(board, N):
    return [list(board[i:i+N]) for i in range(0, len(board), N)]

# generate all moves a piece can make
def playAll(board,p,position):
    (rr, rc) = position # piece is at (rr,rc)
    boardSize=len(board)
    piece=Pieces(p)
    allMoves=[]
    for move in piece.movements():
        (ri, ci) = move # direction of movement by increment (ri,ci)
        currR,currC=rr,rc
        newBoard = copy.deepcopy(board)
        killed = 0
        stepCount=0
        try:
            while stepCount<piece.maxSteps():
                (nr,nc)=(currR+ri, currC+ci)    # move raichu by one square
                if(nc<0 or nr<0):
                    break
                if(newBoard[nr][nc]=='.'):                       # when empty square
                    if nr==piece.otherEnd(boardSize):               # if reached other end
                        newBoard[nr][nc]=piece.successor()  # place sucessor on [.]
                    else:
                        newBoard[nr][nc]=piece.id                # place piece on [.]
                    newBoard[currR][currC]='.'                   # empty the old position of piece.id
                    allMoves.append(copy.deepcopy(newBoard))     # add newboard to allMoves[]
                    currR,currC=nr,nc                            # set new current piece.id pos
                    stepCount+=1
                    continue
                if(piece.canKill(newBoard[nr][nc]) and newBoard[nr+ri][nc+ci]=='.'):
                    if(nr+ri<0 or nc+ci<0):
                        break
                    if killed>0:
                        break
                    newBoard[nr][nc]='.'                         # kill opponent
                    nr+=ri
                    nc+=ci                                       # jump to next square
                    if nr==piece.otherEnd(boardSize):               # if reached other end
                        newBoard[nr][nc]=piece.successor()  # place sucessor on [.]
                    else:
                        newBoard[nr][nc]=piece.id                # place piece on [.]
                    newBoard[currR][currC]='.'                   # empty the old position of piece.id
                    allMoves.append(copy.deepcopy(newBoard))     # add newboard to allMoves[]
                    currR,currC=nr,nc                            # set new current piece.id pos
                    killed = 1
                    stepCount+=1
                    continue
                else:
                    break                                       # no moves, when met with own teammate                     
        except:
            continue
    return allMoves

# generate all the possible plays, a player can do in given board
def possibleFuturePlay(board,player):
    p=Pieces(player)
    stop_yield = False
    possiblePlays=[]
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] in p.myTeam:
                    for eachPlay in playAll(board,board[row][col],(row,col)):
                        if not stop_yield:
                            try:
                                possiblePlays.append(eachPlay)
                            except GeneratorExit:
                                    stop_yield=True
    return possiblePlays

# difference of pieces on board b/w players
def leadByStrength(state,maxPlayer):
    stringBoard=matrixToString(state)
    playerA=Pieces('w')
    playerB=Pieces('b')
    strengthA=sum([stringBoard.count(p)*playerA.teamA[p] for p in list( playerA.myTeam)])
    strengthB=sum([stringBoard.count(p)*playerB.teamB[p] for p in list( playerB.myTeam)])

    if maxPlayer=='w':
        return strengthA-strengthB
    else:
        return strengthB-strengthA

# total empty cells in the board
def totalEmptyCells(board):
    return len([c for r in board for c in r if c=='.'])

# average sum of distances of all the pieces from becoming raicu
def advance(state,maxPlayer):
    piece=Pieces(maxPlayer)
    team= piece.teamA if 'w' in piece.myTeam else piece.teamB
    count=0
    sum=0
    for row in range(len(state)):
        for col in range(len(state[0])):
            if state[row][col] in team:
                if team[state[row][col]]<50:
                    sum+=piece.otherEnd(len(state))-row
                count+=1
    if count==0:
        return 0
    else:
        return sum/count/2

# evaluation function
def eval(state,maxPlayer):
    strengthScore=leadByStrength(state,maxPlayer) 
    return strengthScore + totalEmptyCells(state)+advance(state,maxPlayer)



def find_best_move(board, N, player, timelimit):

    depth=1
    while True:
        bestMove= miniMax(board,player,depth)
        depth+=1
        yield matrixToString(bestMove[1])

def maxValue(board,maxPlayer,depth):
   
    if gameover(board) or depth==0:
        return eval(board,maxPlayer)
    return max([minValue(succ,maxPlayer,depth-1)for succ in possibleFuturePlay(board,maxPlayer)])

def minValue(board,maxPlayer,depth):
    minPlayer=findMinPlayer(maxPlayer)
    if gameover(board) or depth==0:
        return eval(board,maxPlayer)
    return min([maxValue(succ,maxPlayer,depth-1) for succ in possibleFuturePlay(board,minPlayer)])


def findMinPlayer(maxPlayer):
    if maxPlayer=='w':
        return 'b'
    else:
        return 'w'

def miniMax(board,maxPlayer,depth):
    return max([(minValue(succ,maxPlayer,depth),succ) for succ in possibleFuturePlay(board,maxPlayer)])

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(matrixBoard(board,N), N, player, timelimit):
        print(new_board)
