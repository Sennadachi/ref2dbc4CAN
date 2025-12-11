import zlib
import re

# paste your entire hex string here
hex_blob = """
78 da 33 30 80 00 00 06 c8 01 81 00 0f 00 41 78
da 0b 2e 49 4d 2d ca cc 4b 8f 77 cc 4b cf 49 d5
31 34 b2 d4 39 b4 41 c7 d8 48 c7 d0 4c c7 40 c7
50 c7 dc c8 40 47 17 44 04 67 a6 e7 a5 a6 e8 f8
e6 97 e4 17 e5 e7 24 ea 58 e8 00 00 2f 90 12 11
00 42 78 da 73 cd 4b cf cc 4b 8d 0f 2e 48 4d 4d
d1 31 35 34 d6 29 2a c8 d5 31 b1 d0 31 34 d3 31
d0 31 d0 33 32 d5 b1 30 30 00 b2 74 42 f3 8a 33
d3 f3 80 8a 7c f3 4b f2 8b f2 73 12 75 2c 74 00
32 74 12 21 00 48 78 da 73 4c 4e 4e cd 49 2d 4a
2c c9 2f 8a 0f 48 4d 49 cc 89 0f c8 2f ce 2c c9
cc cf d3 31 35 34 d2 51 d5 31 d0 b1 00 62 03 3d
53 1d 43 03 20 ad 13 9a 57 9c 99 9e 97 9a a2 e3
9b 0f d4 93 9f 93 08 94 07 00 1e fd 15 da 00 47
78 da 73 2a 4a cc 4e 8d 0f c8 2f ce 2c c9 cc cf
d3 31 34 36 d6 51 d5 31 b1 d0 31 34 d3 d1 35 34
d5 31 d0 33 34 35 00 d2 86 06 06 3a 06 3a a1 79
c5 99 e9 79 a9 29 3a be f9 25 f9 45 f9 39 89 3a
16 3a 00 67 96 12 a9 00 55 78 da f3 cc 4b c9 4c
4e 2c 49 4d 89 0f 4b cd c8 4c ce 49 8d 0f 2e 48
05 f2 b2 0b 32 74 4c 0d 8d 75 b2 73 f5 33 74 0c
cd 40 48 d7 d0 c0 40 c7 40 cf c0 50 c7 d4 d4 54
cf d8 18 22 10 9a 57 9c 99 9e 97 9a a2 e3 9b 5f
92 5f 94 9f 93 a8 63 a1 03 00 87 6b 19 ad 00 45
78 da 73 ce cf cf 49 cc 2b 89 0f 49 cd 2d 48 2d
4a 2c 29 2d 4a d5 31 34 30 35 d3 39 b4 c1 59 07
48 59 e8 e8 9a 18 e8 18 ea 18 19 1a 83 59 a1 79
c5 99 e9 79 a9 29 3a be f9 25 f9 45 40 bd 40 15
00 08 31 15 9d 00 4b 78 da 0b cf 48 4d cd 89 0f
2e 48 4d 4d 89 77 f3 89 cf 2e c8 d0 31 34 32 30
d0 c9 ce d5 cf d0 31 b1 d0 31 34 d3 d1 35 04 f2
0d f4 0c 0c 75 8c 41 0c 9d d0 bc e2 cc f4 bc d4
14 1d df fc 92 fc a2 fc 9c 44 1d 0b 1d 00 ff d4
14 f0 00 4b 78 da 0b cf 48 4d cd 89 0f 2e 48 4d
4d 89 77 0b 8a cf 2e c8 d0 31 34 32 30 d0 c9 ce
d5 cf d0 31 36 d2 31 34 d3 d1 35 04 f2 0d f4 0c
0c 75 8c 41 0c 9d d0 bc e2 cc f4 bc d4 14 1d df
fc 92 fc a2 fc 9c 44 1d 0b 1d 00 00 1f 14 ef 00
47 78 da 0b cf 48 4d cd 89 0f 2e 48 4d 4d 89 0f
f2 89 cf 2e c8 d0 31 34 32 30 d0 c9 ce d5 07 b2
cc 40 48 d7 10 c8 37 d0 33 30 d4 31 06 31 74 42
f3 8a 33 d3 f3 52 53 74 7c f3 4b f2 8b f2 73 12
75 2c 74 00 01 d7 14 f7 00 4a 78 da 0b cf 48 4d
cd 89 0f 2e 48 4d 4d 89 0f 0a 8a cf 2e c8 d0 31
34 32 30 d0 c9 ce d5 cf d0 31 d0 31 34 d3 d1 35
04 72 0d f4 0c 0c 75 8c 41 0c 9d d0 bc e2 cc f4
bc d4 14 1d df fc 92 fc a2 fc 9c 44 1d 0b 1d 00
f0 83 14 c6 00 5b 78 da 15 c7 41 0a 80 20 10 46
e1 0b fd c9 8c 96 e4 11 5a b4 8a da 46 e4 90 82
69 94 f7 a7 82 07 1f 6f c8 3e ee 5b 15 bf 2e 12
e2 9e 64 9d 2e f9 ee bc 02 3a 36 f8 65 fb d7 30
11 48 11 59 cd 30 6d ab fa ce 39 83 c6 6a c5 98
f3 13 8f 2c 1e 63 a9 e5 2e 69 43 8f 17 17 0a 1a
fb 00 4f 78 da 0b cf 48 4d cd 89 0f 2e 48 4d 4d
89 77 f3 89 cf 2d c8 d0 31 34 32 30 d0 01 31 4c
2c 74 0c cd 74 74 0d 81 5c 03 3d 03 03 33 23 43
1d 43 0b 33 3d 63 1d 03 9d d0 bc e2 cc f4 bc d4
14 1d df fc 92 fc a2 fc 9c 44 1d 0b 1d 00 4b b7
15 cd 00 4f 78 da 0b cf 48 4d cd 89 0f 2e 48 4d
4d 89 77 0b 8a cf 2d c8 d0 31 34 32 30 d0 01 31
8c 8d 74 0c cd 74 74 0d 81 5c 03 3d 03 03 33 23
43 1d 43 0b 33 3d 63 1d 03 9d d0 bc e2 cc f4 bc
d4 14 1d df fc 92 fc a2 fc 9c 44 1d 0b 1d 00 4b
e8 15 cc 00 4c 78 da 0b cf 48 4d cd 89 0f 2e 48
4d 4d 89 0f f2 89 cf 2d c8 d0 31 34 32 30 d0 01
33 cc 40 48 d7 10 c8 35 d0 33 30 30 33 32 d4 31
b4 30 d3 33 d6 31 d0 09 cd 2b ce 4c cf 4b 4d d1
f1 cd 2f c9 2f ca cf 49 d4 b1 d0 01 00 4d c2 15
d4 00 4d 78 da 0b cf 48 4d cd 89 0f 2e 48 4d 4d
89 0f 0a 8a cf 2d c8 d0 31 34 32 30 d0 01 31 0c
74 0c cd 74 74 0d 81 3c 03 3d 03 03 33 23 43 1d
43 0b 33 3d 63 a0 78 68 5e 71 66 7a 5e 6a 8a 8e
6f 7e 49 7e 51 7e 4e a2 8e 85 0e 00 3b aa 15 a3
"""

data = bytes.fromhex(hex_blob)

# find indices of all zlib headers (78 DA)
matches = [m.start() for m in re.finditer(b"\x78\xda", data)]

blocks = []

for i, start in enumerate(matches):
    end = matches[i+1] if i + 1 < len(matches) else len(data)
    block = data[start:end]
    blocks.append(block)

print("Found", len(blocks), "zlib blocks")

for i, bdata in enumerate(blocks):
    print("\nBlock", i)
    try:
        out = zlib.decompress(bdata)
        print(out)
    except Exception as e:
        print("Error:", e)