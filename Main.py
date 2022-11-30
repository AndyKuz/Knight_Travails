import pygame
pygame.init()

import time

def get_square_on_mouse():
    """finds what rectangle is closest to curr mouse pos"""
    x, y = pygame.mouse.get_pos()
    x //= 100
    y //= 100
    if x >= 8 or y >= 8:
        return None, None
    return x * 100, y * 100


def draw_board():
    """draws the entire gridded chessboard that is displayed in pygame"""
    white = True
    for i in range(8):
        for j in range(8):
            rect = pygame.Rect(j * 100, i * 100, 100, 100)
            pygame.draw.rect(screen, pygame.Color((255, 255, 255) if white else (128, 128, 128)), rect)
            white = not white
        white = not white


def draw_grid():
    for i in range(9):
        pygame.draw.line(screen, (0, 0, 0), (0, i * 100), (800, i * 100), width=3)
        pygame.draw.line(screen, (0, 0, 0), (i * 100, 0), (i * 100, 800), width=3)



def create_board():
    """sets up a 2d array for chessboard including current position of the knight"""
    board = []
    for i in range(8):
        board.append([])
        for j in range(8):
            board[i].append(None)
    board[0][0] = "knight"
    return board


def move_green_flag(x, y):
    """moves the green flag in the 2d array that was set up in create_board()"""
    return_board = board
    for i in range(8):
        for j in range(8):
            if return_board[i][j] == "green flag":
                return_board[i][j] = None
    return_board[x//100][y//100] = "green flag"
    return return_board


def find_green_flag():
    """finds current x, y coordinates of green flag using 2d array made in create_board()
        returns None if no green flag is found
    """
    for rows in range(len(board)):
        for cols in range(len(board)):
            if board[rows][cols] == "green flag":
                return rows * 100, cols * 100
    return None, None


def draw_green_flag():
    green_flag = pygame.image.load('green_flag.png')  # loads the green flag.png image
    green_flag = pygame.transform.scale(green_flag, (50, 50))

    green_flag_x, green_flag_y = find_green_flag()  # green flag
    if green_flag_x is not None and green_flag_y is not None:
        screen.blit(green_flag, (green_flag_x + 50, green_flag_y))

def move_knight():
    """moves the knight in the 2d array that was set up in create_board()"""
    return_board = board
    for i in range(8):
        for j in range(8):
            if return_board[i][j] == "knight":
                return_board[i][j] = None
    x, y = get_square_on_mouse()
    return_board[x//100][y//100] = "knight"
    return return_board


def find_knight():
    """finds current x, y coordinates of knight using 2d array made in create_board()"""
    for rows in range(len(board)):
        for cols in range(len(board)):
            if board[rows][cols] == "knight":
                return rows * 100, cols * 100

def draw_knight():
    knight_img = pygame.image.load('knight.png')  # loads the knight.png image
    knight_img = pygame.transform.scale(knight_img, (100, 100))

    knight_x, knight_y = find_knight()  # knight chess piece
    screen.blit(knight_img, (knight_x, knight_y))


class Button:
    font = pygame.font.SysFont('Arial', 20)

    def __init__(self, action, text, active, x, y):
        self.action = action
        self.active = active
        self.text = text
        self.x = x
        self.y = y
        self.w = len(text) * 11
        self.h = 30


    def draw_button(self):
        green_flag_button = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(screen, pygame.Color('navy'), green_flag_button)

        screen.blit(Button.font.render(self.text, True, (255, 0, 0)), (self.x, self.y + 5))

    def draw_active_border(self):
        red_border = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(screen, pygame.Color('red'), red_border, width=4)



def green_flag_button_click():
    curr_square_x, curr_square_y = get_square_on_mouse()
    if curr_square_x is not None or curr_square_y is not None:
        move_green_flag(curr_square_x, curr_square_y)


class Node:
    def __init__(self, x, y, prev_nodes, dist=0):
        self.x = x
        self.y = y
        self.prev_nodes = prev_nodes
        self.dist = dist

    def draw_rectangle(self, color):
        yellow_square = pygame.Rect(self.x, self.y, 100, 100)
        pygame.draw.rect(screen, color, yellow_square)

    def draw_trail(self, color):
        x_difference = self.x - self.prev_nodes[len(self.prev_nodes) - 1].x
        y_difference = self.y - self.prev_nodes[len(self.prev_nodes) - 1].y
        trail_rectangle = pygame.Rect(self.x, self.y, 100, 100)  # placeholder
        trail_rectangle2 = pygame.Rect(self.x, self.y, 100, 100)  # placeholder
        trail_rectangle3 = pygame.Rect(self.x, self.y, 100, 100)  # placeholder

        if x_difference == 200:
            trail_rectangle = pygame.Rect(self.x - 100, self.y, 100, 100)
            trail_rectangle2 = pygame.Rect(self.x - 200, self.y, 100, 100)
            trail_rectangle3 = pygame.Rect(self.x - 200, self.y - y_difference, 100, 100)
        elif x_difference == -200:
            trail_rectangle = pygame.Rect(self.x + 100, self.y, 100, 100)
            trail_rectangle2 = pygame.Rect(self.x + 200, self.y, 100, 100)
            trail_rectangle3 = pygame.Rect(self.x + 200, self.y - y_difference, 100, 100)
        elif y_difference == 200:
            trail_rectangle = pygame.Rect(self.x, self.y - 100, 100, 100)
            trail_rectangle2 = pygame.Rect(self.x, self.y - 200, 100, 100)
            trail_rectangle3 = pygame.Rect(self.x - x_difference, self.y - 200, 100, 100)
        elif y_difference == -200:
            trail_rectangle = pygame.Rect(self.x, self.y + 100, 100, 100)
            trail_rectangle2 = pygame.Rect(self.x , self.y + 200, 100, 100)
            trail_rectangle3 = pygame.Rect(self.x - x_difference, self.y + 200, 100, 100)

        pygame.draw.rect(screen, color, trail_rectangle)
        pygame.draw.rect(screen, color, trail_rectangle2)
        pygame.draw.rect(screen, color, trail_rectangle3)

def breadth_search_button_click():
    global GREEN, BLUE, YELLOW
    GREEN = (53, 202, 74)
    BLUE = (30, 203, 225)
    YELLOW = (227, 210, 28)

    # lists all possible movements for a knight
    move_x = [200, 200, -200, -200, 100, 100, -100, -100]
    move_y = [-100, 100, 100, -100, 200, -200, 200, -200]

    visited = set()  # set of visited Node objects
    visited_points = set()  # set of visited Node (x, y) coordinates

    green_flag_x, green_flag_y = find_green_flag()
    knight_x, knight_y = find_knight()

    q = [Node(knight_x, knight_y, [])]

    while len(q) > 0:
        node = q.pop(0)
        node_x = node.x
        node_y = node.y

        if not ((node_x, node_y)) in visited_points:  # check if the Mode has been visited yet if not adds it to nodes visited
            draw_board()
            for visited_nodes in visited:  # draws all previously visited Nodes
                visited_nodes.draw_rectangle(GREEN)

            if node_x != knight_x or node_y != knight_y:  # if not knight Node draw blue trail
                node.draw_trail(BLUE)

            node.draw_rectangle(GREEN)

            draw_grid()
            draw_knight()
            draw_green_flag()
            pygame.display.flip()
            time.sleep(1.5)

            visited.add(node)
            visited_points.add((node_x, node_y))

            if node_x == green_flag_x and node_y == green_flag_y:
                draw_solution(node, knight_x, knight_y)
                break


            for i in range(len(move_x)):  # adds all possible moves from current Node to queue (q)
                new_node_x = node_x + move_x[i]
                new_node_y = node_y + move_y[i]

                if 0 <= new_node_x < 800 and 0 <= new_node_y < 800 and not ((new_node_x, new_node_y)) in visited_points:
                    q.append(Node(new_node_x, new_node_y, node.prev_nodes + [node], node.dist + 1))


def draw_solution(node, knight_x, knight_y):
    """Once search algorithm is drawn function draws steps it took to find result"""
    draw_board()
    for prev_nodes in node.prev_nodes:
        if prev_nodes.x != knight_x or prev_nodes.y != knight_y:
            prev_nodes.draw_trail(BLUE)
        prev_nodes.draw_rectangle(GREEN)
        draw_grid()
        draw_knight()
        draw_green_flag()
        pygame.display.flip()
        time.sleep(3)
    node.draw_trail(BLUE)
    node.draw_rectangle(GREEN)
    draw_grid()
    pygame.display.flip()
    time.sleep(7)


def main():
    global screen, board
    screen = pygame.display.set_mode((1100, 800))
    board = create_board()
    clock = pygame.time.Clock()

    button_list = [
        Button(green_flag_button_click, "Green Flag", False, 850, 100),
        Button(breadth_search_button_click, "Breadth-First Search", False, 850, 200)
    ]

    knight_picked_up = False
    running = True
    while running:

        # draws chessboard
        screen.fill((255, 255, 255))  # chessboard
        draw_board()
        draw_grid()  # draws grid

        for button in button_list:  # draws all buttons
            button.draw_button()
            if button.active:
                button.draw_active_border()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:

                curr_x, curr_y = pygame.mouse.get_pos()
                curr_square_x, curr_square_y = get_square_on_mouse()

                knight_x, knight_y = find_knight()  # responsible for moving knight piece
                if knight_picked_up and curr_x < 800 and curr_y < 800:
                    move_knight()
                    knight_picked_up = False
                elif not knight_picked_up and curr_square_x == knight_x and curr_square_y == knight_y:
                    knight_picked_up = True

                for button in button_list:
                    if button.active:
                        button.action()
                        button.active = False
                    elif button.x < curr_x < (button.x + button.w) \
                        and button.y < curr_y < (button.y + button.h):
                        button.active = True


        # draws graphics on pygame screen
        draw_knight()
        draw_green_flag()

        # sees what square is closest to mouse pos and highlights it with red
        x, y = get_square_on_mouse()
        if x is not None:
            red_border_rect = pygame.Rect(x, y, 100, 100)
            pygame.draw.rect(screen, (255, 0, 0, 50), red_border_rect, width=4)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()