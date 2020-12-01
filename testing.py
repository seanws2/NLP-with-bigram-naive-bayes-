import numpy as np


def reorder_rows_columns(K, equation_numbers):
    # construct the matrix Khat
    output = K
    for i in range(0, len(equation_numbers)):
        if i >= equation_numbers[i] - 1:
            continue
        else:
            output[:, [i, equation_numbers[i] - 1]] = output[:, [equation_numbers[i] - 1, i]]
            output[[i, equation_numbers[i] - 1], :] = output[[equation_numbers[i] - 1, i], :]

    return output

e = np.array([[0.89226389, 0.35198516, 0.38401159, 0.8888591 ],
 [0.78303494, 0.36114023, 0.23396956, 0.92526878],
 [0.18200176, 0.19297867, 0.88549535, 0.8703676 ],
 [0.63056316, 0.25540689 ,0.0594653,  0.57431067]])
equ = [1,2,4,3]
print(reorder_rows_columns(e, equ))