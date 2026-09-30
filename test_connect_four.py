"""
Automated tests for Connect Four — Tasks 1-4.
Run with: python test_connect_four.py
"""
import sys, io, contextlib

# Ensure we can import the project modules
from board import Board, ROWS, COLS
from ai import AI


def test(name, condition):
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {name}")
    return condition


def run_tests():
    passed = 0
    total = 0

    # ================================================================
    # WIN DETECTION TESTS
    # ================================================================
    print("\n=== WIN DETECTION ===")

    # 1. Horizontal four
    b = Board()
    for c in range(4):
        b.drop(c, "X")
    total += 1; passed += test("1. Horizontal four", b.winner("X"))

    # 2. Vertical four
    b = Board()
    for _ in range(4):
        b.drop(0, "X")
    total += 1; passed += test("2. Vertical four", b.winner("X"))

    # 3. Diagonal down-right four
    b = Board()
    # Build a diagonal: (5,0),(4,1),(3,2),(2,3)
    # Col 0: one X
    b.drop(0, "X")
    # Col 1: one filler, then X
    b.drop(1, "O")
    b.drop(1, "X")
    # Col 2: two fillers, then X
    b.drop(2, "O")
    b.drop(2, "O")
    b.drop(2, "X")
    # Col 3: three fillers, then X
    b.drop(3, "O")
    b.drop(3, "O")
    b.drop(3, "O")
    b.drop(3, "X")
    total += 1; passed += test("3. Diagonal down-right four", b.winner("X"))

    # 4. Diagonal down-left four
    b = Board()
    # Build a diagonal: (2,3),(3,2),(4,1),(5,0) — same shape, opposite slant
    # Col 3: one X at bottom
    b.drop(3, "X")
    # Col 2: one filler, then X
    b.drop(2, "O")
    b.drop(2, "X")
    # Col 1: two fillers, then X
    b.drop(1, "O")
    b.drop(1, "O")
    b.drop(1, "X")
    # Col 0: three fillers, then X
    b.drop(0, "O")
    b.drop(0, "O")
    b.drop(0, "O")
    b.drop(0, "X")
    total += 1; passed += test("4. Diagonal down-left four", b.winner("X"))

    # 5. Three-in-a-row should NOT win
    b = Board()
    for c in range(3):
        b.drop(c, "X")
    total += 1; passed += test("5. Three-in-a-row does NOT win", not b.winner("X"))

    # 6. Four-in-a-row near board boundaries
    b = Board()
    for c in range(3, 7):
        b.drop(c, "X")
    total += 1; passed += test("6. Horizontal four at right edge", b.winner("X"))

    b = Board()
    for _ in range(4):
        b.drop(6, "O")
    total += 1; passed += test("6b. Vertical four in last column", b.winner("O"))

    # ================================================================
    # GAME TERMINATION (tested via board/game logic)
    # ================================================================
    print("\n=== GAME TERMINATION ===")

    # 7-9: Input validation — tested via Game.run with simulated input
    from game import Game

    # 7. Invalid non-numeric input
    game = Game()
    old_stdin = sys.stdin
    sys.stdin = io.StringIO("abc\nq\n")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        game.run()
    output = buf.getvalue()
    total += 1; passed += test("7. Invalid non-numeric input handled", "Enter a column number" in output)

    # 8. Number below 1
    game = Game()
    sys.stdin = io.StringIO("0\nq\n")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        game.run()
    output = buf.getvalue()
    total += 1; passed += test("8. Number below 1 rejected", "Column must be between 1 and 7" in output)

    # 9. Number above 7
    game = Game()
    sys.stdin = io.StringIO("9\nq\n")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        game.run()
    output = buf.getvalue()
    total += 1; passed += test("9. Number above 7 rejected", "Column must be between 1 and 7" in output)

    # 10. Full column
    game = Game()
    # Fill column 1 (index 0) with alternating tokens directly
    for i in range(ROWS):
        game.board.drop(0, "X" if i % 2 == 0 else "O")
    sys.stdin = io.StringIO("1\nq\n")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        game.run()
    output = buf.getvalue()
    total += 1; passed += test("10. Full column handled", "Column unavailable" in output)

    # 11. Winning move ends game immediately
    game = Game()
    for c in range(3):
        game.board.drop(c, "X")
    game.turn = "X"
    sys.stdin = io.StringIO("4\n")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        game.run()
    output = buf.getvalue()
    total += 1; passed += test("11. Winning move ends game", "X wins!" in output)

    # 12. Full board draw
    # Fill the board with a known draw pattern
    game = Game()
    # Fill board such that no four in a row anywhere
    pattern = [
        ["X","O","X","O","X","O","X"],
        ["X","O","X","O","X","O","X"],
        ["O","X","O","X","O","X","O"],
        ["X","O","X","O","X","O","X"],
        ["X","O","X","O","X","O","X"],
        ["O","X","O","X","O","X","O"],
    ]
    game.board.grid = [row[:] for row in pattern]
    # Verify no winner and board is full
    is_draw = game.board.full() and not game.board.winner("X") and not game.board.winner("O")
    total += 1; passed += test("12. Full board draw detected", is_draw)

    # 13. q quits
    game = Game()
    sys.stdin = io.StringIO("q\n")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        game.run()
    total += 1; passed += test("13. q quits game", True)  # no crash = pass

    sys.stdin = old_stdin

    # ================================================================
    # AI TESTS
    # ================================================================
    print("\n=== AI ===")
    ai = AI()

    # 14. AI immediate winning move
    b = Board()
    for c in range(3):
        b.drop(c, "O")
    col = ai.choose_column(b, me="O", opponent="X")
    total += 1; passed += test("14. AI picks winning column (3)", col == 3)
    # Board unchanged
    total += 1; passed += test("14b. Board unchanged after AI analysis", b.grid[5][3] == ".")

    # 15. AI blocks immediate human win
    b = Board()
    for c in range(3):
        b.drop(c, "X")
    col = ai.choose_column(b, me="O", opponent="X")
    total += 1; passed += test("15. AI blocks human win (col 3)", col == 3)
    total += 1; passed += test("15b. Board unchanged after AI analysis", b.grid[5][3] == ".")

    # 16. AI never selects a full column
    b = Board()
    for c in range(6):
        for _ in range(ROWS):
            b.drop(c, "X")
    # Only column 6 is open
    col = ai.choose_column(b, me="O", opponent="X")
    total += 1; passed += test("16. AI picks only legal column (6)", col == 6)

    # 17. AI handles no legal columns
    b = Board()
    for c in range(7):
        for _ in range(ROWS):
            b.drop(c, "X")
    col = ai.choose_column(b, me="O", opponent="X")
    total += 1; passed += test("17. AI returns None when no legal columns", col is None)

    # ================================================================
    # FEEDBACK TESTS
    # ================================================================
    print("\n=== FEEDBACK ===")

    # 18. Human move prints feedback
    game = Game()
    game.turn = "X"
    sys.stdin = io.StringIO("4\nq\n")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        game.run()
    output = buf.getvalue()
    total += 1; passed += test("18. Human move feedback", "X placed in column 4" in output)

    # 19. AI move prints feedback
    game = Game()
    game.turn = "O"
    # AI will pick some column; just check that "O placed in column" appears
    sys.stdin = io.StringIO("q\n")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        game.run()
    output = buf.getvalue()
    total += 1; passed += test("19. AI move feedback", "O placed in column" in output)

    # 20. Invalid move does NOT print feedback
    game = Game()
    sys.stdin = io.StringIO("abc\nq\n")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        game.run()
    output = buf.getvalue()
    total += 1; passed += test("20. Invalid move: no placement feedback", "placed in column" not in output)

    # 21. AI hypothetical analysis does not print feedback
    b = Board()
    for c in range(3):
        b.drop(c, "O")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        col = ai.choose_column(b, me="O", opponent="X")
    output = buf.getvalue()
    total += 1; passed += test("21. AI analysis: no fake feedback", "placed in column" not in output)

    sys.stdin = old_stdin

    # ================================================================
    print(f"\n{'='*40}")
    print(f"Results: {passed}/{total} passed")
    if passed == total:
        print("All tests PASSED!")
    else:
        print(f"{total - passed} test(s) FAILED.")
    print()


if __name__ == "__main__":
    run_tests()
