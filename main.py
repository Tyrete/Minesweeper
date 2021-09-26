import random


class Minesweeper:
    def __init__(self):
        super().__init__()
        self.rows = 0
        self.columns = 0
        self.mines = 0
        self.startUserSymbol = '.'
        self.startSymbol = 0
        self.grid = []
        self.userGrid = []
        self.difOption = ['default', 'advanced']
        self.difficultyIndex = -1
        self.used = []

    def printUserGrid(self):
        for i in range(self.columns + 1):
            print(i, end=' ')
        print()
        for row in range(self.rows):
            print(row + 1, end=' ')
            for column in range(self.columns):
                print(self.userGrid[row][column], end=' ')
            print()

    def printGrid(self):
        for i in range(self.columns + 1):
            print(i, end=' ')
        print()
        for row in range(self.rows):
            print(row + 1, end=' ')
            for column in range(self.columns):
                print(self.grid[row][column], end=' ')
            print()

    def InitUserGrid(self):
        self.userGrid = [[self.startUserSymbol for x in range(self.columns)] for r in range(self.rows)]

    def InitGrid(self):
        self.grid = [[0 for i in range(self.columns)] for x in range(self.rows)]
        cells = [(i // self.columns, i % self.columns) for i in range(self.columns * self.rows)]
        for i in range(self.mines):
            ind = random.randint(0, self.rows * self.columns - i - 1)
            self.grid[cells[ind][0]][cells[ind][1]] = 1
            cells.pop(ind)

    def InitUsed(self):
        self.used = [[self.startSymbol for i in range(self.columns)] for j in range(self.rows)]

    def Input(self):
        self.getDifficulty()
        if not self.difficultyIndex:
            self.rows = 5
            self.columns = 5
            self.mines = 5
        else:
            print('Write field size:')
            self.rows = int(input('rows: '))
            self.columns = int(input('columns: '))
            self.mines = int(input('mines: '))
        print('You have options to open cell "open", flag cell "flag", undo flag "undo"')

    def globalInit(self):
        self.Input()
        self.InitGrid()
        self.InitUserGrid()
        self.InitUsed()

    def checkBorder(self, x, y):
        if x < 0 or y < 0 or x >= self.rows or y >= self.columns:
            return False
        return True

    def getMinesNearby(self, x, y):
        cnt = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if self.checkBorder(i, j):
                    cnt += self.grid[i][j]

        return cnt

    def correctWrite(self, x, y, cnt):
        if not cnt:
            self.userGrid[x][y] = ' '
        else:
            self.userGrid[x][y] = cnt

    def showZeroCells(self, x, y):
        self.used[x][y] = 1
        cnt = self.getMinesNearby(x, y)
        self.correctWrite(x, y, cnt)
        if cnt:
            allCells = self.checkForZeroCells(x, y)
            for i in allCells:
                self.showZeroCells(i[0], i[1])
            return

        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if self.checkBorder(i, j) and not self.used[i][j]:
                    self.showZeroCells(i, j)

    def writeCell(self, x, y):
        if self.used[x][y]:
            print('You have already opened that cell')
            return
        cnt = self.getMinesNearby(x, y)
        self.correctWrite(x, y, cnt)
        zeroCells = self.checkForZeroCells(x, y)
        if not cnt:
            zeroCells.append((x, y))
        self.used[x][y] = 1
        for i in zeroCells:
            self.showZeroCells(i[0], i[1])

    def checkForZeroCells(self, x, y):
        allCells = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if not self.checkBorder(i, j):
                    continue
                if self.used[i][j]:
                    continue
                cnt = self.getMinesNearby(i, j)
                if not cnt:
                    allCells.append((i, j))
        return allCells

    def writeFlag(self, x, y):
        self.userGrid[x][y] = 'F'

    def undoFlag(self, x, y):
        if self.userGrid[x][y] != 'F':
            print("You don't have flag in that cell")
            return
        if self.used[x][y]:
            self.userGrid[x][y] = self.getMinesNearby(x, y)
        else:
            self.userGrid[x][y] = '.'

    def chooseDifficulty(self):
        print('Choose difficulty: ', self.difOption)
        dif = input().lower()
        for index, name in enumerate(self.difOption):
            if dif == name:
                return index
        return -1

    def getDifficulty(self):
        self.difficultyIndex = self.chooseDifficulty()
        while self.difficultyIndex == -1:
            self.difficultyIndex = self.chooseDifficulty()

    def printFinalTable(self):
        for i in range(self.columns + 1):
            print(i, end=' ')
        print()
        for row in range(self.rows):
            print(row + 1, end=' ')
            for column in range(self.columns):
                if self.grid[row][column]:
                    print('B', end=' ')
                else:
                    print(self.userGrid[row][column], end=' ')
            print()

    def defeat(self):
        self.printFinalTable()
        print('Game Over. You Lost')

    def win(self):
        self.printFinalTable()
        print('Congratulations. You Win')

    def checkWin(self):
        cnt = 0
        for row in range(self.rows):
            for column in range(self.columns):
                if self.userGrid[row][column] == 'F':
                    if self.grid[row][column]:
                        cnt += 1
                elif self.userGrid[row][column] == '.':
                    cnt += 1
        if cnt == self.mines:
            return True
        return False

    def checkDeath(self, x, y):
        if self.grid[x][y]:
            return True
        return False


def queryInput():
    rawInput = input().split()
    row = int(rawInput[0])
    column = int(rawInput[1])
    action = rawInput[2]
    return row - 1, column - 1, action


def inputCheck(row, column, action, player):
    if row < 0 or column < 0 or row >= player.rows or column >= player.columns:
        print('Index out of border')
        return 1
    if action not in ['flag', 'open', 'undo']:
        print('Write correct action')
        return 1
    return 0


def playerGame():
    player = Minesweeper()
    player.globalInit()
    # writeInFile(player)
    while True:
        if player.checkWin():
            player.win()
            break
        player.printUserGrid()
        row, column, action = queryInput()
        action = action.lower()
        while inputCheck(row, column, action, player):
            row, column, action = queryInput()
            action = action.lower()
        if action == 'open':
            if player.checkDeath(row, column):
                player.defeat()
                break
            player.writeCell(row, column)
        elif action == 'flag':
            player.writeFlag(row, column)
        else:
            player.undoFlag(row, column)


# def programGame():

def main():
    playerGame()


if __name__ == '__main__':
    main()

