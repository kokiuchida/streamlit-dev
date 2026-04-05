"""
Shogi board rendering using PIL.
Board layout:
  - 9x9 grid, 60px per square
  - Piece stands on left (white/gote) and right (black/sente)
  - File labels (9..1) at top, rank labels (一..九) on right
  - Total image: 720 wide x 700 tall
"""

from PIL import Image, ImageDraw, ImageFont
import shogi
import os

# Layout constants
SQUARE_SIZE = 60
BOARD_OFFSET_X = 100   # left margin (piece stand area)
BOARD_OFFSET_Y = 50    # top margin (file labels)
BOARD_W = SQUARE_SIZE * 9
BOARD_H = SQUARE_SIZE * 9
STAND_W = 90
IMG_W = BOARD_OFFSET_X + BOARD_W + STAND_W + 10  # ~730
IMG_H = BOARD_OFFSET_Y + BOARD_H + 50            # ~640

# Colors
COLOR_BOARD  = "#F5DEB3"
COLOR_BORDER = "#8B6914"
COLOR_SELECT = "#FFFF00"
COLOR_SELECT_BORDER = "#FF8800"   # orange outline for selected piece
COLOR_LEGAL  = "#ADD8E6"
COLOR_LEGAL_BORDER  = "#2288CC"   # blue outline for legal destinations
COLOR_LAST   = "#FFA07A"
COLOR_STAND  = "#DEB887"
COLOR_TEXT   = "#1A1A1A"
COLOR_BG     = "#F0E6CC"
COLOR_RED    = "#CC0000"

RANK_KANJI = ["一", "二", "三", "四", "五", "六", "七", "八", "九"]
FILE_NUMS  = ["９", "８", "７", "６", "５", "４", "３", "２", "１"]

PIECE_KANJI = {
    shogi.PAWN:          "歩",
    shogi.LANCE:         "香",
    shogi.KNIGHT:        "桂",
    shogi.SILVER:        "銀",
    shogi.GOLD:          "金",
    shogi.BISHOP:        "角",
    shogi.ROOK:          "飛",
    shogi.KING:          "玉",
    shogi.PROM_PAWN:    "と",
    shogi.PROM_LANCE:   "杏",
    shogi.PROM_KNIGHT:  "圭",
    shogi.PROM_SILVER:  "全",
    shogi.PROM_BISHOP:  "馬",
    shogi.PROM_ROOK:    "龍",
}

HAND_PIECE_NAMES = {
    shogi.PAWN:   "歩",
    shogi.LANCE:  "香",
    shogi.KNIGHT: "桂",
    shogi.SILVER: "銀",
    shogi.GOLD:   "金",
    shogi.BISHOP: "角",
    shogi.ROOK:   "飛",
}

HAND_PIECE_ORDER = [shogi.ROOK, shogi.BISHOP, shogi.GOLD, shogi.SILVER,
                    shogi.KNIGHT, shogi.LANCE, shogi.PAWN]


def _get_font(size=20):
    """Try to load a Japanese-capable font; fall back to PIL default."""
    candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/noto-cjk/NotoSansCJKjp-Regular.otf",
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf",
        "/home/uchid/.fonts/NotoSansCJKjp-Regular.otf",
        # Windows fonts (WSL)
        "/mnt/c/Windows/Fonts/YuGothR.ttc",
        "/mnt/c/Windows/Fonts/YuGothM.ttc",
        "/mnt/c/Windows/Fonts/meiryo.ttc",
        "/mnt/c/Windows/Fonts/msgothic.ttc",
        "/mnt/c/Windows/Fonts/BIZ-UDGothicR.ttc",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    # PIL default (no Japanese glyphs but won't crash)
    try:
        return ImageFont.load_default(size=size)
    except Exception:
        return ImageFont.load_default()


def square_to_pixel(file_0: int, rank_0: int):
    """
    Convert 0-indexed (file, rank) to top-left pixel of that square.
    file_0=0 → leftmost column on display = file 9 in shogi notation
    rank_0=0 → top row = rank 1 in shogi notation
    """
    x = BOARD_OFFSET_X + file_0 * SQUARE_SIZE
    y = BOARD_OFFSET_Y + rank_0 * SQUARE_SIZE
    return x, y


def pixel_to_square(px: int, py: int):
    """
    Convert pixel coords to 0-indexed (file_0, rank_0).
    Returns (file_0, rank_0) or None if outside board.
    file_0=0 corresponds to shogi file 9 (right side for sente).
    """
    fx = (px - BOARD_OFFSET_X) // SQUARE_SIZE
    ry = (py - BOARD_OFFSET_Y) // SQUARE_SIZE
    if 0 <= fx <= 8 and 0 <= ry <= 8:
        return fx, ry
    return None


def display_to_shogi_sq(file_0: int, rank_0: int) -> int:
    """Convert display 0-indexed coords to python-shogi square index."""
    shogi_file = 9 - file_0     # display col 0 → file 9, col 8 → file 1
    shogi_rank = rank_0 + 1     # display row 0 → rank 1
    return shogi.SQUARE_NAMES.index(f"{shogi_file}{chr(ord('a') + rank_0)}")


def shogi_sq_to_display(sq: int) -> tuple:
    """Convert python-shogi square index to display (file_0, rank_0)."""
    name = shogi.SQUARE_NAMES[sq]
    shogi_file = int(name[0])
    rank_char = name[1]
    shogi_rank = ord(rank_char) - ord('a') + 1
    file_0 = 9 - shogi_file
    rank_0 = shogi_rank - 1
    return file_0, rank_0


def render_board(
    board: shogi.Board,
    selected_sq=None,       # python-shogi square index or None
    legal_squares=None,     # list of destination square indices
    last_move=None,         # shogi.Move or None
    selected_drop=None,     # (piece_type, color) for drop piece stand selection
) -> Image.Image:
    """Render the full board image."""

    img = Image.new("RGB", (IMG_W, IMG_H), COLOR_BG)
    draw = ImageDraw.Draw(img)

    font_lg  = _get_font(28)
    font_md  = _get_font(22)
    font_sm  = _get_font(16)
    font_xs  = _get_font(12)

    # --- Draw piece stands (mochigoma) ---
    # White (gote) stand: left side
    _draw_piece_stand(draw, img, board, shogi.WHITE, 2, BOARD_OFFSET_Y,
                      font_md, font_sm, font_xs, selected_drop)
    # Black (sente) stand: right side
    _draw_piece_stand(draw, img, board, shogi.BLACK,
                      BOARD_OFFSET_X + BOARD_W + 5, BOARD_OFFSET_Y,
                      font_md, font_sm, font_xs, selected_drop)

    # --- Draw board background ---
    bx0 = BOARD_OFFSET_X
    by0 = BOARD_OFFSET_Y
    bx1 = bx0 + BOARD_W
    by1 = by0 + BOARD_H
    draw.rectangle([bx0, by0, bx1, by1], fill=COLOR_BOARD, outline=COLOR_BORDER, width=2)

    # --- Highlight last move ---
    if last_move is not None:
        if last_move.from_square is not None:
            _highlight_square(draw, last_move.from_square, COLOR_LAST)
        _highlight_square(draw, last_move.to_square, COLOR_LAST)

    # --- Highlight legal move destinations ---
    if legal_squares:
        for sq in legal_squares:
            _highlight_square(draw, sq, COLOR_LEGAL, border_color=COLOR_LEGAL_BORDER)

    # --- Highlight selected square ---
    if selected_sq is not None:
        _highlight_square(draw, selected_sq, COLOR_SELECT, border_color=COLOR_SELECT_BORDER)

    # --- Draw grid lines ---
    for i in range(10):
        x = bx0 + i * SQUARE_SIZE
        draw.line([(x, by0), (x, by1)], fill=COLOR_BORDER, width=1)
        y = by0 + i * SQUARE_SIZE
        draw.line([(bx0, y), (bx1, y)], fill=COLOR_BORDER, width=1)

    # --- Draw pieces ---
    for sq in range(81):
        piece = board.piece_at(sq)
        if piece is None:
            continue
        piece_type = piece.piece_type
        color = piece.color
        kanji = PIECE_KANJI.get(piece_type, "?")
        file_0, rank_0 = shogi_sq_to_display(sq)
        px, py = square_to_pixel(file_0, rank_0)
        cx = px + SQUARE_SIZE // 2
        cy = py + SQUARE_SIZE // 2

        # White pieces are drawn upside-down (rotated 180°)
        is_promoted = piece_type in (
            shogi.PROM_PAWN, shogi.PROM_LANCE,
            shogi.PROM_KNIGHT, shogi.PROM_SILVER,
            shogi.PROM_BISHOP, shogi.PROM_ROOK,
        )
        txt_color = COLOR_RED if is_promoted else COLOR_TEXT

        _draw_piece_text(img, draw, kanji, cx, cy, font_lg, txt_color,
                         upside_down=(color == shogi.WHITE))

    # --- File labels (top): ９８７６５４３２１ ---
    for i, label in enumerate(FILE_NUMS):
        x = bx0 + i * SQUARE_SIZE + SQUARE_SIZE // 2
        y = by0 - 30
        _draw_centered_text(draw, label, x, y, font_sm, COLOR_TEXT)

    # --- Rank labels (right side): 一〜九 ---
    for i, label in enumerate(RANK_KANJI):
        x = bx1 + 18
        y = by0 + i * SQUARE_SIZE + SQUARE_SIZE // 2
        _draw_centered_text(draw, label, x, y, font_sm, COLOR_TEXT)

    # --- Turn indicator ---
    turn_str = "▲先手番" if board.turn == shogi.BLACK else "△後手番"
    draw.text((BOARD_OFFSET_X, IMG_H - 35), turn_str, fill=COLOR_TEXT, font=font_md)

    return img


def _highlight_square(draw: ImageDraw.Draw, sq: int, color: str,
                       border_color: str = None):
    file_0, rank_0 = shogi_sq_to_display(sq)
    px, py = square_to_pixel(file_0, rank_0)
    draw.rectangle(
        [px + 1, py + 1, px + SQUARE_SIZE - 1, py + SQUARE_SIZE - 1],
        fill=color,
    )
    if border_color:
        draw.rectangle(
            [px + 2, py + 2, px + SQUARE_SIZE - 2, py + SQUARE_SIZE - 2],
            outline=border_color, width=3,
        )


def _draw_centered_text(draw, text, cx, cy, font, color):
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
    except Exception:
        w, h = font.getsize(text)
    draw.text((cx - w // 2, cy - h // 2), text, fill=color, font=font)


def _draw_piece_text(img, draw, text, cx, cy, font, color, upside_down=False):
    """Draw a piece kanji, optionally rotated 180 degrees for white pieces."""
    if not upside_down:
        _draw_centered_text(draw, text, cx, cy, font, color)
    else:
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
        except Exception:
            w, h = (28, 28)
        # Render to a small temp image, rotate 180, paste back
        tmp = Image.new("RGBA", (w + 4, h + 4), (0, 0, 0, 0))
        tmp_draw = ImageDraw.Draw(tmp)
        tmp_draw.text((2, 2), text, fill=color, font=font)
        tmp = tmp.rotate(180)
        paste_x = cx - (w + 4) // 2
        paste_y = cy - (h + 4) // 2
        img.paste(tmp, (paste_x, paste_y), tmp)


def _draw_piece_stand(draw, img, board, color, stand_x, stand_y,
                      font_md, font_sm, font_xs, selected_drop=None):
    label = "▲先手持ち駒" if color == shogi.BLACK else "△後手持ち駒"
    stand_color_fill = COLOR_STAND
    # draw stand background
    draw.rectangle(
        [stand_x, stand_y, stand_x + STAND_W - 5, stand_y + BOARD_H],
        fill=stand_color_fill, outline=COLOR_BORDER, width=1
    )
    _draw_centered_text(draw, label, stand_x + (STAND_W - 5) // 2, stand_y + 14,
                        font_xs, COLOR_TEXT)

    pieces_in_hand = board.pieces_in_hand[color]
    y_offset = stand_y + 30

    for pt in HAND_PIECE_ORDER:
        count = pieces_in_hand.get(pt, 0)
        if count == 0:
            continue
        kanji = HAND_PIECE_NAMES[pt]
        cx = stand_x + (STAND_W - 5) // 2
        cy = y_offset + 16

        # Highlight if selected for drop
        if selected_drop == (pt, color):
            draw.rectangle(
                [stand_x + 2, y_offset, stand_x + STAND_W - 8, y_offset + 34],
                fill=COLOR_SELECT,
            )
            draw.rectangle(
                [stand_x + 3, y_offset + 1, stand_x + STAND_W - 9, y_offset + 33],
                outline=COLOR_SELECT_BORDER, width=3,
            )

        txt = f"{kanji}×{count}"
        # White pieces upside-down
        _draw_piece_text(img, draw, txt, cx, cy, font_sm, COLOR_TEXT,
                         upside_down=(color == shogi.WHITE))
        y_offset += 36
