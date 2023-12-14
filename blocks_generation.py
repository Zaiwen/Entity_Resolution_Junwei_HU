import numpy as np
# np.seterr(divide='ignore',invalid='ignore')
import falconn
import timeit
import math

def get_blocks(embedding, convert_embedding, blocks_path, threshold):
    ary=[]
    with open(embedding, encoding='utf-8')as f:
        for line in f:
            toks=line.strip().split(' ')
            ary.append(''.join(filter(str.isdigit, toks[0])))

    dataset_file = convert_embedding
    # we build only 50 tables, increasing this quantity will improve the query time
    # at a cost of slower preprocessing and larger memory foot# print, feel free to
    # play with this number
    number_of_tables = 50

    # print('Reading the dataset')
    dataset = np.load(dataset_file)
    # print('Done')

    # It's important not to use doubles, unless they are strictly necessary.
    # If your dataset consists of doubles, convert it to floats using `astype`.
    # dataset = dataset.astype(np.float32)
    assert dataset.dtype == np.float32

    # Normalize all the lenghts, since we care about the cosine similarity.
    # print('Normalizing the dataset')
    dataset /= np.linalg.norm(dataset, axis=1).reshape(-1, 1)
    # print('Done')

    # Center the dataset and the queries: this improves the performance of LSH quite a bit.
    # print('Centering the dataset and queries')
    center = np.mean(dataset, axis=0)
    dataset -= center
    # print('Done')

    params_cp = falconn.LSHConstructionParameters()
    params_cp.dimension = len(dataset[0])
    params_cp.lsh_family = falconn.LSHFamily.CrossPolytope
    params_cp.distance_function = falconn.DistanceFunction.EuclideanSquared
    params_cp.l = number_of_tables
    # we set one rotation, since the data is dense enough,
    # for sparse data set it to 2
    params_cp.num_rotations = 1
    params_cp.seed = 5721840
    # we want to use all the available threads to set up
    params_cp.num_setup_threads = 0
    params_cp.storage_hash_table = falconn.StorageHashTable.BitPackedFlatHashTable
    # we build 18-bit hashes so that each table has
    # 2^18 bins; this is a good choise since 2^18 is of the same
    # order of magnitude as the number of data points
    falconn.compute_number_of_hash_functions(18, params_cp)

    # print('Constructing the LSH table')
    t1 = timeit.default_timer()
    table = falconn.LSHIndex(params_cp)
    table.setup(dataset)
    t2 = timeit.default_timer()
    # print('Done')
    # print('Construction time: {}'.format(t2 - t1))

    query_object = table.construct_query_object()
    outfile=open(blocks_path, 'w', encoding='utf-8')
    i = 0
    for query in dataset:
        outfile.write("target entity: ")
        outfile.write(str(ary[i]))
        outfile.write("\n")
        outfile.write("similar entities: ")
        for j in range(len(query_object.find_near_neighbors(query, threshold))):
            if str(ary[i]) != str(ary[query_object.find_near_neighbors(query, threshold)[j]]):
                outfile.write(str(ary[query_object.find_near_neighbors(query, threshold)[j]]))
                outfile.write(" ")
        outfile.write("\n")
        i = i + 1