from flask import Flask, jsonify, request

app = Flask(__name__)

COLS = "ABCDEFGH"


def is_valid_position(pos):
    if len(pos) != 2:
        return False
    column, row = pos
    return column in COLS and row in "12345678"


def validate_positions(position_data):
    if not all(is_valid_position(pos) for pos in position_data.values()):
        return False
    return position_data


def possible_knight_moves(current_position):
    initial_col_position, initial_row_position = current_position
    moves = []

    col_index = COLS.find(initial_col_position)
    row_index = int(initial_row_position)

    # horizontal movements
    for col_offset in [-2, 2]:
        for row_offset in [-1, 1]:
            new_col_index = col_index + col_offset
            new_row_index = row_index + row_offset
            if 0 <= new_col_index < len(COLS) and 1 <= new_row_index <= 8:
                moves.append(COLS[new_col_index] + str(new_row_index))

    # vertical movements
    for col_offset in [-1, 1]:
        for row_offset in [-2, 2]:
            new_col_index = col_index + col_offset
            new_row_index = row_index + row_offset
            if 0 <= new_col_index < len(COLS) and 1 <= new_row_index <= 8:
                moves.append(COLS[new_col_index] + str(new_row_index))

    return moves


def possible_bishop_moves(current_position):
    initial_col_position, initial_row_position = current_position
    moves = []

    col_index = COLS.find(initial_col_position)
    row_index = int(initial_row_position)

    for col_offset, row_offset in zip([-1, -1, 1, 1], [-1, 1, -1, 1]):
        new_col_index, new_row_index = col_index, row_index
        while True:
            new_col_index += col_offset
            new_row_index += row_offset
            if 0 <= new_col_index < len(COLS) and 1 <= new_row_index <= 8:
                moves.append(COLS[new_col_index] + str(new_row_index))
            else:
                break

    return moves


def possible_rook_moves(current_position):
    initial_col_position, initial_row_position = current_position
    moves = []

    col_index = COLS.find(initial_col_position)
    row_index = int(initial_row_position)

    for new_col_index in range(len(COLS)):
        if new_col_index != col_index:
            moves.append(COLS[new_col_index] + str(initial_row_position))

    for new_row_index in range(1, 9):
        if new_row_index != row_index:
            moves.append(initial_col_position + str(new_row_index))

    return moves


def possible_queen_moves(current_position):
    queen_moves = possible_bishop_moves(current_position) + possible_rook_moves(
        current_position
    )
    queen_moves = list(set(queen_moves))
    return queen_moves


def find_possible_moves(positions):
    # get moves
    knight_moves = possible_knight_moves(positions["Knight"])
    bishop_moves = possible_bishop_moves(positions["Bishop"])
    rook_moves = possible_rook_moves(positions["Rook"])
    queen_moves = possible_queen_moves(positions["Queen"])

    return {
        "knight_moves": knight_moves,
        "bishop_moves": bishop_moves,
        "rook_moves": rook_moves,
        "queen_moves": queen_moves,
    }


def validate_moves(current_pawn_moves, *other_pawn_moves):
    other_moves_set = set(move for sublist in other_pawn_moves for move in sublist)
    invalid_positions = set(current_pawn_moves).intersection(other_moves_set)

    valid_moves = [move for move in current_pawn_moves if move not in invalid_positions]
    return valid_moves


@app.route("/chess/knight", methods=["POST"])
def get_knight_moves():
    data = request.get_json()
    if not data or "positions" not in data or "Knight" not in data["positions"]:
        return (
            jsonify({"error": "Provide Knight position data in JSON format."}),
            400,
        )

    pawn_positions = validate_positions(data["positions"])
    if not pawn_positions:
        return jsonify({"error": "Invalid Positions"}), 400

    pawn_moves = find_possible_moves(pawn_positions)

    valid_moves = validate_moves(
        pawn_moves["knight_moves"],
        pawn_moves["bishop_moves"],
        pawn_moves["rook_moves"],
        pawn_moves["queen_moves"],
    )
    return jsonify({"valid_moves": valid_moves})


@app.route("/chess/bishop", methods=["POST"])
def get_bishop_moves():
    data = request.get_json()
    if not data or "positions" not in data or "Bishop" not in data["positions"]:
        return (
            jsonify({"error": "Provide Bishop position data in JSON format."}),
            400,
        )

    pawn_positions = validate_positions(data["positions"])
    if not pawn_positions:
        return jsonify({"error": "Invalid Positions"}), 400

    pawn_moves = find_possible_moves(pawn_positions)

    valid_moves = validate_moves(
        pawn_moves["bishop_moves"],
        pawn_moves["knight_moves"],
        pawn_moves["rook_moves"],
        pawn_moves["queen_moves"],
    )
    return jsonify({"valid_moves": valid_moves})


@app.route("/chess/rook", methods=["POST"])
def get_rook_moves():
    data = request.get_json()
    if not data or "positions" not in data or "Rook" not in data["positions"]:
        return (
            jsonify({"error": "Provide Rook position data in JSON format."}),
            400,
        )

    pawn_positions = validate_positions(data["positions"])
    if not pawn_positions:
        return jsonify({"error": "Invalid Positions"}), 400

    pawn_moves = find_possible_moves(pawn_positions)

    valid_moves = validate_moves(
        pawn_moves["rook_moves"],
        pawn_moves["knight_moves"],
        pawn_moves["bishop_moves"],
        pawn_moves["queen_moves"],
    )
    return jsonify({"valid_moves": valid_moves})


@app.route("/chess/queen", methods=["POST"])
def get_queen_moves():
    data = request.get_json()
    if not data or "positions" not in data or "Queen" not in data["positions"]:
        return (
            jsonify({"error": "Provide Queen position data in JSON format."}),
            400,
        )

    pawn_positions = validate_positions(data["positions"])
    if not pawn_positions:
        return jsonify({"error": "Invalid Positions"}), 400

    pawn_moves = find_possible_moves(pawn_positions)

    valid_moves = validate_moves(
        pawn_moves["queen_moves"],
        pawn_moves["knight_moves"],
        pawn_moves["bishop_moves"],
        pawn_moves["rook_moves"],
    )

    return jsonify({"valid_moves": valid_moves})


if __name__ == "__main__":
    app.run(port=6000)
