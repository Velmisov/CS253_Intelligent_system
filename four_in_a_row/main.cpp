#include <iostream>
#include "position.h"
#include "solver.h"
using namespace std;

int main() {

    auto pos = new Position("333333444444");
    pos->show();

    auto solver = new Solver();

    while (pos->get_number_of_moves() != BOARD_SIZE) {
        int col;
        if (pos->who_play_now() == 1) {
            cout << "HERE" << endl;
            auto res = solver->negamax(*pos);
            cout << res.first + 1 << " " << res.second << endl;
            break;
        }
        else {
            do {
                cout << "Choose your column: ";
                cin >> col;
                --col;
                if (pos->can_move(col)) {
                    break;
                } else {
                    cout << "Invalid column! Try again!" << endl;
                }
            } while (true);
        }
        if (pos->is_winning_move(col)) {
            pos->move(col);
            pos->show();
            cout << "You're lose" << endl;
            break;
        }
        pos->move(col);
        pos->show();
    }

    return 0;
}