import numpy as np

def Kuhn_Munkres_algorithm(arr): 
    size = arr.shape[0]
    curint_arr = arr
    #Step 1 - Every column and every row subtract its internal minimum
    for row_num in range(arr.shape[0]): 
        curint_arr[row_num] = curint_arr[row_num] - np.min(curint_arr[row_num])
    
    for col_num in range(arr.shape[1]): 
        curint_arr[:,col_num] = curint_arr[:,col_num] - np.min(curint_arr[:,col_num])
    zero_count = 0
    while zero_count < size:
        
         #Step 2 & 3 - Column Reduction (test for optimal assignment)
         #finding row and adding the multiple solution row to row_line_indexer and colom_line_indexer to save them for later
        ans_pos, marked_rows, marked_cols = search_for_optimal_assign_and_record_value(curint_arr)
        zero_count = len(marked_rows) + len(marked_cols)
        #if count of selection did not match the number of rows we go to step 4 
        if zero_count < size:
            curint_arr = adjust_matrix(curint_arr, marked_rows, marked_cols)

    return ans_pos


def adjust_matrix(arr, cover_rows, cover_cols):
    curint_arr = arr
    non_zero_element = []

    #Step 4
    #in case of the solution row did not match the number of rows in the arry then we subtrac the smales non matching items in the arry
    for row in range(len(curint_arr)):
        if row not in cover_rows:
            for i in range(len(curint_arr[row])):
                if i not in cover_cols:
                    non_zero_element.append(curint_arr[row][i])
    min_num = min(non_zero_element)

    for row in range(len(curint_arr)):
        if row not in cover_rows:
            for i in range(len(curint_arr[row])):
                if i not in cover_cols:
                    curint_arr[row, i] = curint_arr[row, i] - min_num
    for row in range(len(cover_rows)):  
        for col in range(len(cover_cols)):
            curint_arr[cover_rows[row], cover_cols[col]] = curint_arr[cover_rows[row], cover_cols[col]] + min_num
    return curint_arr


def ans_calculation(arr, pos):
    #step 5   
    total = np.zeros(arr.shape[0])
    ans_mat = np.zeros((arr.shape[0], arr.shape[1]))
    for i in range(len(pos)):
        total[pos[i][0]]=pos[i][1]
        ans_mat[pos[i][0], pos[i][1]] = arr[pos[i][0], pos[i][1]]
        

    return total, ans_mat
   
def search_for_optimal_assign_and_record_value(mat):


    #Transform the matrix 0 = True, others = False
    cur_mat = mat
    zero_bool_mat = (cur_mat == 0)
    zero_bool_mat_copy = zero_bool_mat.copy()
    #Recording possible answer positions by marked_zero
    marked_zero = []
    while (True in zero_bool_mat_copy):
        sml_zero_mat(zero_bool_mat_copy, marked_zero)
    
    #Recording the row and column positions seperately.
    marked_zero_row = []
    marked_zero_col = []
    for i in range(len(marked_zero)):
        marked_zero_row.append(marked_zero[i][0])
        marked_zero_col.append(marked_zero[i][1])

    non_marked_row = list(set(range(cur_mat.shape[0])) - set(marked_zero_row))
    marked_cols = []
    check_switch = True
    while check_switch:
        check_switch = False
        for i in range(len(non_marked_row)):
            row_array = zero_bool_mat[non_marked_row[i], :]
            for j in range(row_array.shape[0]):
                if row_array[j] == True and j not in marked_cols:
                    marked_cols.append(j)
                    check_switch = True

        for row_num, col_num in marked_zero:
            if row_num not in non_marked_row and col_num in marked_cols:
                non_marked_row.append(row_num)
                check_switch = True
    marked_rows = list(set(range(mat.shape[0])) - set(non_marked_row))

    return(marked_zero, marked_rows, marked_cols)

def sml_zero_mat(zero_mat, mark_zero):
    
    
    #find the row which containing the fewest 0.
    # Select the zero number on the row, and then marked the item ocording  in row and column as False

    #Find the row
    min_row = [99999, -1]

    for row_num in range(zero_mat.shape[0]): 
        if np.sum(zero_mat[row_num] == True) > 0 and min_row[0] > np.sum(zero_mat[row_num] == True):
            min_row = [np.sum(zero_mat[row_num] == True), row_num]

    # Marked the specific row and column as False
    zero_index = np.where(zero_mat[min_row[1]] == True)[0][0]
    mark_zero.append((min_row[1], zero_index))
    zero_mat[min_row[1], :] = False
    zero_mat[:, zero_index] = False

def tester():
    #The matrix who you want to find the minimum sum
    inputArry = np.random.randint(1, 5, size=(6, 6))
    final_arr_pos = Kuhn_Munkres_algorithm(inputArry.copy())#Get the element position.
    ans, ans_mat = ans_calculation(inputArry, final_arr_pos)#Get the minimum value and corresponding matrix.
    #Show the result
    print(
        'every line and the optimal answer'
    )
    print(ans)
    print("the matrix after and pefore")
    print(inputArry)
    print(ans_mat)
   


if __name__ == '__main__':
    tester()