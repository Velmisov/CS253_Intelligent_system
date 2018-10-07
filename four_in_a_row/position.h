//
// Created by vlad on 07.10.18.
//

#ifndef FOUR_IN_A_ROW_POSITION_H
#define FOUR_IN_A_ROW_POSITION_H

const int WIDTH = 7;
const int HEIGHT = 6;
const int BOARD_SIZE = WIDTH * HEIGHT;

class Position {
    int board[WIDTH][HEIGHT];
    int filled[WIDTH];
    int number_of_moves;

public:
    Position();

    int get_number_of_moves() const;

    bool can_move(int column) const;

    void move(int column);

private:
    bool in_border(int column) const;

public:

    bool is_winning_move(int column) const;
};

#endif //FOUR_IN_A_ROW_POSITION_H
