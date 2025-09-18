import numpy as np

def pawn_attack_zone(pawn_pos, size):
    """pawn_attack_zone"""
    zone = []
    for i in pawn_pos:
        x, y = i
        # Pawn กิน ทแยงซ้าย-ขวา (เดินขึ้น)
        if x-1 >= 0:  # ตรวจสอบไม่ให้เกินขอบ
            if y-1 >= 0:  # ทแยงซ้าย
                zone.append((x-1, y-1))
            if y+1 < size[1]:  # ทแยงขวา
                zone.append((x-1, y+1))
    return zone

def rook_attack_zone(rook_pos, arr):
    """rook_attack_zone"""
    zone = []
    for i in rook_pos:
        x, y = i
        # เดินแนวตั้ง-แนวนอน
        # ขึ้น
        for r in range(x-1, -1, -1):
            zone.append((r, y))
            if arr[r, y] != '.':  # หยุดเมื่อเจอหมาก
                break
        # ลง
        for r in range(x+1, arr.shape[0]):
            zone.append((r, y))
            if arr[r, y] != '.':
                break
        # ซ้าย
        for c in range(y-1, -1, -1):
            zone.append((x, c))
            if arr[x, c] != '.':
                break
        # ขวา
        for c in range(y+1, arr.shape[1]):
            zone.append((x, c))
            if arr[x, c] != '.':
                break
    return zone

def bishop_attack_zone(bishop_pos, arr):
    """bishop_attack_zone"""
    zone = []
    for i in bishop_pos:
        x, y = i
        # เดินทแยง 4 ทิศ
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dx, dy in directions:
            r, c = x + dx, y + dy
            while 0 <= r < arr.shape[0] and 0 <= c < arr.shape[1]:
                zone.append((r, c))
                if arr[r, c] != '.':  # หยุดเมื่อเจอหมาก
                    break
                r, c = r + dx, c + dy
    return zone

def queen_attack_zone(queen_pos, arr):
    """queen_attack_zone (รวม rook + bishop)"""
    zone = []
    for i in queen_pos:
        x, y = i
        # เดินแนวตั้ง-แนวนอน + ทแยง (8 ทิศ)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), 
                     (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dx, dy in directions:
            r, c = x + dx, y + dy
            while 0 <= r < arr.shape[0] and 0 <= c < arr.shape[1]:
                zone.append((r, c))
                if arr[r, c] != '.':  # หยุดเมื่อเจอหมาก
                    break
                r, c = r + dx, c + dy
    return zone

def checkmate(board):
    """ตรวจสอบว่า King ถูก check หรือไม่"""
    try:
        arr = np.array([[j for j in i] for i in board.split("\n")])
    except:
        return print("Fail")
    size = arr.shape
    
    # ตรวจสอบว่า board เป็นสี่เหลี่ยมหรือไม่
    if not all(len(row) == len(arr) for row in arr):
        return print("Fail")

    flatten_arr = arr.flatten()

    # ตรวจสอบว่ามีหมากที่สามารถจับได้หรือไม่
    if not any(piece in ['P', 'B', 'R', 'Q'] for piece in flatten_arr):
        return print("Fail")
    
    # หาตำแหน่งหมากต่างๆ
    king_pos = np.argwhere(arr == 'K')
    pawn_pos = np.argwhere(arr == 'P')
    bishop_pos = np.argwhere(arr == 'B')
    rook_pos = np.argwhere(arr == 'R')
    queen_pos = np.argwhere(arr == 'Q')
    
    # ตรวจสอบว่ามี King หรือไม่
    if len(king_pos) == 0:
        return print("Fail")
    
    # Find attack zones of all pieces
    all_attack_zones = []
    
    if len(pawn_pos) > 0:
        pawn_attack_zones = pawn_attack_zone(pawn_pos, size)
        all_attack_zones.extend(pawn_attack_zones)
    
    if len(rook_pos) > 0:
        rook_attack_zones = rook_attack_zone(rook_pos, arr)
        all_attack_zones.extend(rook_attack_zones)
        
    if len(bishop_pos) > 0:
        bishop_attack_zones = bishop_attack_zone(bishop_pos, arr)
        all_attack_zones.extend(bishop_attack_zones)
        
    if len(queen_pos) > 0:
        queen_attack_zones = queen_attack_zone(queen_pos, arr)
        all_attack_zones.extend(queen_attack_zones)
    
    # ตำแหน่ง King
    king_row, king_col = king_pos[0][0], king_pos[0][1]
    king_position = (king_row, king_col)
    

    # Check if king is in attack zone
    if king_position in all_attack_zones:
        return print("Success")  # King ถูก check
    else:
        return print("Fail")     # King ไม่ถูก check