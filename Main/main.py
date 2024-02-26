inp_filename, operation, out_filename = input().split()

def read_imagefile(f):
    matrix = []
    f_line = f.readline().split()
    width = int(f_line[1])
    height = int(f_line[2])
    all_cont = f.read().split()
    x= 0
    for i in range(height):
        temp  = []
        for j in range(x,x+width):
            temp.append(all_cont[j])
        x+= width
        matrix.append(temp)
    return matrix


def write_imagefile(f, img_matrix):
    f.write(f"P2 {len(img_matrix[0])} {len(img_matrix)} 255\n")
    for i in img_matrix:
        f.write(" ".join(i))
        f.write("\n")


def misalign(img_matrix):
    copy_matrix = []
    for i in range(len(img_matrix)):
        copy_matrix.append(img_matrix[i].copy())
    for i in range(len(img_matrix)):
        for j in range(len(img_matrix[i])):
            if j % 2 == 1:
                copy_matrix[len(img_matrix)-1- i][j] = img_matrix[i][j]
    return copy_matrix


def sort_columns(img_matrix):
    copy_matrix = []
    
    for i in range(len(img_matrix)):
        copy_matrix.append(img_matrix[i].copy())
    i = 0
    while i < len(img_matrix[1]):
        temp = []
        for j in range(len(copy_matrix)):
            temp.append(int(copy_matrix[j][i]))
        temp.sort()
        for k in range(len(copy_matrix)):
            copy_matrix[k][i] = str(temp[k])
        i += 1
    return copy_matrix


def sort_rows_border(img_matrix):
    copy_matrix = []
    
    for i in range(len(img_matrix)):
        copy_matrix.append(img_matrix[i].copy())

    for line in copy_matrix:
        start = 0
        end = 0
        temp = []
        while end < len(line):
            if line[end] == "0":
                temp.sort()
                for i in range(start, end):
                    line[i] = str(temp[i - start])
                temp = []
                start = end + 1
            else:
                temp.append(int(line[end]))
            end += 1
        if len(temp) > 0:
            temp.sort()
            for i in range(start, end):
                line[i] = str(temp[i - start])
    return copy_matrix


def convolution(img_matrix, kernel):
    copy_matrix = []

    height = len(img_matrix)
    width = len(img_matrix[0])
    for i in range(len(img_matrix)):
        copy_matrix.append(img_matrix[i].copy())

    k_matrix = []
    k_matrix.append([0 for _ in range(width + 2)])
    for i in copy_matrix:
        k_matrix.append([0] +i.copy() + [0])
    k_matrix.append([0 for _ in range(width + 2)])
    for i in range(len(k_matrix)-2):
        for j in range(len(k_matrix[0])-2):
            ans = 0
            part1 = int(kernel[0][0]) * int(k_matrix[i][j]) + int(kernel[0][1]) * int(k_matrix[i][j + 1]) + int(
                kernel[0][2]) * int(k_matrix[i][j + 2]) + int(kernel[1][0]) * int(k_matrix[i + 1][j])
            part2 = int(kernel[1][1]) * int(k_matrix[i + 1][j + 1]) + int(kernel[1][2]) * int(
                k_matrix[i + 1][j + 2]) + int(kernel[2][0]) * int(k_matrix[i + 2][j]) + int(kernel[2][1]) * int(
                k_matrix[i + 2][j + 1])
            part3 = int(kernel[2][2]) * int(k_matrix[i + 2][j + 2])
            ans = part1 + part2 + part3
            if ans < 0: ans = 0
            if ans > 255: ans = 255
            copy_matrix[i][j] = str(ans)
    return copy_matrix


f = open(inp_filename, "r")
img_matrix = read_imagefile(f)
f.close()

if operation == "misalign":
    img_matrix = misalign(img_matrix)

elif operation == "sort_columns":
    img_matrix = sort_columns(img_matrix)

elif operation == "sort_rows_border":
    img_matrix = sort_rows_border(img_matrix)

elif operation == "highpass":
    kernel = [
        [-1, -1, -1],
        [-1, 9, -1],
        [-1, -1, -1]
    ]
    img_matrix = convolution(img_matrix, kernel)

f = open(out_filename, "w")
write_imagefile(f, img_matrix)
f.close()
