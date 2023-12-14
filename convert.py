import sys
import struct
import numpy as np

def transformation(embedding, dimension):
    matrix = []
    with open(embedding + '.txt', 'r') as inf:
        with open(embedding + '.dat', 'wb') as ouf:
            counter = 0
            for line in inf:
                row = [float(x) for x in line.split()[1:]]
                assert len(row) == dimension
                ouf.write(struct.pack('i', len(row)))
                ouf.write(struct.pack('%sf' % len(row), *row))
                counter += 1
                matrix.append(np.array(row, dtype=np.float32))
                if counter % 10000 == 0:
                    sys.stdout.write('%d points processed...\n' % counter)
    np.save(embedding, np.array(matrix))
    return embedding + '.npy'
