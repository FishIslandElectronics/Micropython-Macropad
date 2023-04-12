import math

def draw_pbm(display, file, x, y):
    with open(file, 'rb') as f:
        if not f.readline() == b'P4\n': return
        f.readline()
        w, h = f.readline().decode().split(' ')
        w = int(w)
        h = int(h.strip())

        bsa = f.readline()
        index = 0
        bytes_per_line = math.ceil(w/8)
        x_off = 0
        y_off = 0
        for b in bsa:
            for i in range(7,-1,-1):
                index += 1
                mask = 1<<i
                bit = (b&mask)>>i
                #print('#' if bit==1 else ' ', end='')
                display.format.set_pixel(display, x+x_off, y+y_off, bit)

                x_off += 1
                if index == bytes_per_line*8:
                    index = 0
                    y_off += 1
                    x_off = 0
                    break

        


