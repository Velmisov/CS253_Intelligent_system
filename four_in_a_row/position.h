//
// Created by vlad on 07.10.18.
//

#ifndef FOUR_IN_A_ROW_POSITION_H
#define FOUR_IN_A_ROW_POSITION_H

#include <string>

const int WIDTH = 7;
const int HEIGHT = 6;
const int BOARD_SIZE = WIDTH * HEIGHT;

class Position {

public:
    int board[HEIGHT][WIDTH];
    int number_of_moves;
    int filled[WIDTH];
    int last_move;

    Position();

    explicit Position(std::string field);

    bool can_move(int column) const;

    void move(int column);

    bool in_border(int column) const;

    bool is_winning_move(int column) const;

    void show() const;

    int who_play_now() const;
};

#endif //FOUR_IN_A_ROW_POSITION_H
