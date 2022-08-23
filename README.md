# a2

# Part1 - Raichu 

We started games and bayes with the legendary raichu game. Funny thing was we ourselved didn't know to play this game. 

## Problem Formulation
The game invloved two players and every player want to maximize is chance of winning. So we decided this will be a minmax game
1. State space - states of board formed by all possible valid moves of pieces
2. Successor function - return all possible moves a player can make
3. Evaluation of the game - difference of pieces (W-B) or (B-W) between players

## How the code works
We have implemented minmax algorithm for the given adverserial game. We start with max node and try to maximising the his chances of winning. 

### Pieces - Class
This gives the properties and behaviour of pieces of a given player. It consist of useful method which effectively calculates canKill, movements, teamMember etc
I have used few dictionary strategies by assigning ranks to each player, which can be used to calcuate few items mentioned above

### Play all and Possible future play functions
These methods combined generate all the successor stated for given state of board


## Our Journey 

We realised that how many numbers of moves we think ahead decides who win the game. In order to maximize the depth we can reach in the minmax, we used generators to yield successors only when needed and employed alpha-beta pruning. We made a great progress with this, we could reach up to 17 levels in the tree in 10 seconds. Played with the sample port provided and we won.
With a great joy we moved to work on second part of the assignment. However, when other people started publishing their port we lost or drew the game, which made us think that our minmax is flawed and that need to be fixed. 

We didn't have much time to correct this, so we pushed our defensive minmax which can draw the game at work case. Back to basics. 


# Part 2 - The Game of Quintris 

When we started to solve this problem, we had no clue on how to start off with. I started to read articles and see different  approaches for this problem. But with more Knowledge  I gain the harder I was thinking to start with the solution. So, we have decided to start with the successor function. We have brainstormed ourselves on how to generate the successor function. First, we have identified  the state space for the Quintris board. The state space for the board is the different possible configurations the piece can occupy in the board. 

After writing  the successor function, we had to spend a lot of to time to understand the given code of quintris, then we have understood how to use the given functions to make the moves and place them in the board. This took us a lot of time because we face many problems like how to place the piece from the give position in all possible positions and with all the orientations of the piece. We have to manually validate all the successors initially  to make sure we are making valid moves.

We had to start off with a cost function for the minimal algorithm, the first heuristic we came up with was to identify  the peak value of all columns and sum all the peaks. We didn't get any score for that heuristic, then we have added the heuristic to calculate the score for each move, it made the board better but we were unable to make any score.
We came up with other cost functions - 

#### Holes - 
holes are formed when a tile blocks the below cells. We avoid this as much as possible.

#### Pit - 
It calculates the empty space in the board which has been unused. After using this cost our piece is being placed uniformly in the game board.

#### Well - 
Wells are formed when an empty cell is surrounded by two X’s. When we add this cost to out evaluation, we don’t let the game from forming these wells in the quest of not creating holes

#### Bumps - 
bumps are difference in height of consecutive columns, this can be minimized to achieve better score.


We tried to use the next_piece and probability distribution of the pieces to achieve expectiminmax, but we couldn’t implement it successfully within time. But with this problem we learnt a lot, got a glimpse of expectiminmax. We hope to implement the game with the same strategy in coming days. 
 
# Part 3: Truth be Told

To start with this problem, I had to understand which approach suits best for the solution. After analyzing  the question, I have decided to use Bayes Net, and I could not think of any other approach. I have started studying  the Bayes net, after getting sufficient knowledge I have understood that I have to use the words in the given review to predict the truthfulness of the reviews. 

Initial step for my approach is to assume that each word is independent to one another. Then I have to get all the words from the train data set. After getting all the words from the train data I have observed there many duplicate words, numbers and combination of symbols and word($100, “Good”,..). I felt that these will give me a  lot of unwanted and misleading words. So I have separated the symbols  from the words and made them meaningful, and also removed all the duplicate words.

After getting the bag_of_words, I have calculated the truthful and deceptive probabilities of all the words. Then I have calculated the ratio of word probabilities of truthful to word probabilities of deceptive. If the ratio is greater than one then the review is truthful otherwise it is deceptive.

One of the problem I have tried to solve is, in the situation where there is a word in test data which is not present in train data. I have skipped all the words while Calculating  the ratio of truthful to deceptive. I tried to get the probabilities of these words with test data, but was unable to get to the solution. I will be trying to think of a solution to overcome this problem and increase my prediction accuracy.