# Mike Boodoo
# Artificial Intelligence Assign 02
from copy import deepcopy # for deep copy operations
from sys import maxsize
from time import time # for timing how long functions take

# check if queen can be successfully added
def good_queen_placement(old_assign:dict, new_assign:dict) -> bool:
    print("Checking placement...")
    for queen, row in old_assign.items():
        for new_queen, new_row in new_assign.items():
            if row == new_row:
                return False
            elif (queen-row) == (new_queen-new_row):
                return False
            elif (queen+row) == (new_queen+new_row):
                return False
    return True

def backtracking_search(assignment:dict, unassigned:list, remaining_queens:dict, complete_assignments:list):
    # check for complete assignment
    print("Starting a backtracking search...")
    if not unassigned: # if unassigned is empty
        print("Found an assignment! It is: " + str(assignment))
        complete_assignments.append(assignment)
        return assignment
    else:
        most_constrained_queen = None
        num_values:int = maxsize
        # select unassigned queen with least values
        for queen, values in remaining_queens.items():
            #print("Queen, value is: ", queen, values)
            if len(values) < num_values:
                num_values = len(values)
                most_constrained_queen = queen # queen index with least number of possible values left
        for potential_row in remaining_queens[most_constrained_queen]:
            # check if any of the queen's values result in a good placement
            if good_queen_placement(assignment, {most_constrained_queen:potential_row}):
                assignment.update({most_constrained_queen:potential_row}) 
                unassigned.remove(most_constrained_queen)
                old_remain_rows = remaining_queens[most_constrained_queen] 
                del remaining_queens[most_constrained_queen]
                result = backtracking_search(assignment, unassigned, remaining_queens, complete_assignments)
                if result:
                    return result
                #else:
                del assignment[most_constrained_queen]
                unassigned.append(most_constrained_queen)
                remaining_queens.update({most_constrained_queen:old_remain_rows})
    return False
    
def forward_propogation(new_assignment:dict, remaining_queens:dict) -> bool:
    print("Forward proprgation in action")
    new_queen:int = None
    new_row:int = None
    for key, value in new_assignment.items():
        new_queen = key
        new_row = value
    for queen, row_domain in remaining_queens.items():
        if new_row in row_domain:
            row_domain.remove(new_row) # delete same row in remaining queens domain
        for selected_row in row_domain:
            if queen+selected_row == new_queen+new_row:
                row_domain.remove(selected_row) # delete opposite diagonal row in remaining queens domain
            elif queen-selected_row == new_queen-new_row:
                row_domain.remove(selected_row) # delete main diagonal row in remaining queens domain
    for queen, row_domain in remaining_queens.items():
        if not row_domain: # if row domain is empty
            return False
    return True # return true if all remaining_queens have at least 1 number in their domain, else false
    
def backtracking_search_forward_prop(assignment:dict, unassigned:list, remaining_queens:dict, complete_assignments:list):
    # check for complete assignment
    print("Starting a backtracking search WITH FORWARD PROPOGRATION...")
    if not unassigned: # if unassigned is empty
        print("Found an assignment! It is: " + str(assignment))
        complete_assignments.append(assignment)
        return assignment
    else:
        most_constrained_queen = None
        num_values:int = maxsize
        # select unassigned queen with least values
        for queen, values in remaining_queens.items():
            #print("Queen, value is: ", queen, values)
            if len(values) < num_values:
                num_values = len(values)
                most_constrained_queen = queen # queen index with least number of possible values left
        for potential_row in remaining_queens[most_constrained_queen]:
            # check if any of the queen's values result in a good placement
            if good_queen_placement(assignment, {most_constrained_queen:potential_row}):
                copy_remain_queens = deepcopy(remaining_queens)
                assignment.update({most_constrained_queen:potential_row}) 
                unassigned.remove(most_constrained_queen)
                old_remain_rows = remaining_queens[most_constrained_queen] 
                del remaining_queens[most_constrained_queen]
                inferences = forward_propogation({most_constrained_queen:potential_row}, copy_remain_queens)
                if inferences:
                    result = backtracking_search(assignment, unassigned, copy_remain_queens, complete_assignments)
                if result:
                    return result
                # removal of inferences from forward propogation done by using deep copy
                del assignment[most_constrained_queen]
                unassigned.append(most_constrained_queen)
                remaining_queens.update({most_constrained_queen:old_remain_rows})
    return False

if __name__ == "__main__":

    current_assignment:dict = {}
    counter = NUM_QUEENS = 4
    queens_remain:dict = {} # {3: [0, 1, 2, 3], 2: [0, 1, 2, 3], 1: [0, 1, 2, 3], 0: [0, 1, 2, 3]}
    queens_unassign:list = [queen for queen in range(NUM_QUEENS)]
    complete_assigns:list = []
    start_time = time()

    while counter > 0:
        queens_remain.update({counter-1:list(range(NUM_QUEENS))})
        counter -= 1

    """
    backtracking_search(current_assignment, queens_unassign, queens_remain, complete_assigns)
    end_time = time()
    total_time = end_time - start_time
    for solution_assign in complete_assigns:
        print("Solution assignment: ", str(solution_assign))
    print("Backtracking search for N =", NUM_QUEENS, " took", total_time, " seconds")
    """
    backtracking_search_forward_prop(current_assignment, queens_unassign, queens_remain, complete_assigns)
    end_time = time()
    total_time = end_time - start_time
    for solution_assign in complete_assigns:
        print("Solution assignment: ", str(solution_assign))
    print("Backtracking search with forward prop for N =", NUM_QUEENS, " took", total_time, " seconds")
    
    # Output:

    # Solution assignment:  {7: 0, 6: 4, 2: 6, 5: 7, 0: 3, 4: 5, 3: 2, 1: 1}
    # Backtracking search for N = 8  took 0.010863780975341797  seconds
    # N = 8 Solution verified by online 8-Queens checker https://www.brainmetrix.com/8-queens/

    # Solution assignment:  {17: 0, 16: 2, 15: 4, 14: 1, 13: 7, 6: 17, 12: 14, 9: 12, 1: 13, 11: 11,
    # 4: 3, 7: 5, 2: 8, 5: 6, 10: 15, 3: 10, 8: 16, 0: 9}
    # Backtracking search for N = 18  took 103.74843955039978  seconds

    # Solution assignment:  {7: 0, 6: 4, 2: 6, 5: 7, 0: 3, 4: 5, 3: 2, 1: 1}
    # Backtracking search with forward prop for N = 8  took 0.010041236877441406  seconds
    # N = 8 Solution verified by online 8-Queens checker https://www.brainmetrix.com/8-queens/

    # Solution assignment:  {17: 0, 16: 2, 15: 4, 14: 1, 13: 7, 6: 17, 12: 14, 9: 12, 1: 13, 11: 11
    # 4: 3, 7: 5, 2: 8, 5: 6, 10: 15, 3: 10, 8: 16, 0: 9}
    # Backtracking search with forward prop for N = 18  took 73.2875542640686  seconds
    


