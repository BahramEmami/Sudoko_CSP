from myCSP.myVariable import *
from myCSP.myVarArray import *
from myCSP.myConstraint import *
from myCSP.AllDifferent import *
from board import Board
from refresher import Refresher

from queue import Queue

# my_variables = [] is declared in myVariable.py
constraint_list = []
g: myConstraintGraph


def my_satisfy(*constraints: Union[myConstraint, myAllDifferent]) -> None:
    """
    Adds constraints to the constraint list and initializes the constraint graph.

    :param constraints: A variable number of constraint objects (either myConstraint or myAllDifferent).
    """
    for constraint in constraints:
        if isinstance(constraint, myAllDifferent):
            constraint_list.extend(constraint.get_constraints())
        else:
            constraint_list.append(constraint)
    global g
    g = myConstraintGraph(constraint_list)


def my_solve(do_unary_check: bool,
             do_arc_consistency: bool,
             do_mrv: bool,
             do_lcv: bool,
             refresher: Refresher) -> bool:
    """
    Solves the CSP problem using backtracking with optional heuristics.
    """
    if do_unary_check:
        if not node_consistency(refresher):
            return False
    if not backtrack(do_arc_consistency, do_mrv, do_lcv, refresher):
        return False
    return True


def my_clear():
    """
    Clears variables and constraints for a fresh CSP instance.
    """
    global my_variables, constraint_list, g
    my_variables.clear()
    constraint_list.clear()
    g = None


def node_consistency(refresher: Refresher) -> bool:
    """
    Applies node consistency by filtering values that do not satisfy unary constraints.
    """
    for var in my_variables:
        valid_vals = {v for v in var.remaining_domain if g.is_node_satisfied(var, v)}
        if not valid_vals:
            return False
        if valid_vals != var.remaining_domain:
            var.remaining_domain = valid_vals
            refresher.refresh_screen()
    return True


def backtrack(do_arc_consistency: bool, do_mrv: bool, do_lcv: bool, refresher: Refresher):
    """
    Implements backtracking search with optional heuristics.
    """
    if g.is_assignment_complete():
        return True
    var = select_unassigned_variable(do_mrv)
    for val in order_domain_values(var, do_lcv):
        var.value = val
        refresher.refresh_screen()
        if g.is_assignment_consistent(var):
            backup = extract_domains()
            set_doms_to_values()
            if inference(do_arc_consistency, refresher):
                if backtrack(do_arc_consistency, do_mrv, do_lcv, refresher):
                    return True
            restore_domains(backup)
            refresher.refresh_screen()
        var.value = None
        refresher.refresh_screen()
    return False


def inference(do_arc_consistency: bool, refresher: Refresher) -> bool:
    """
    Uses forward-checking methods to eliminate variable domains that cause contradiction in the future.
    """
    if do_arc_consistency:
        return arc_consistency(refresher)
    return True


def arc_consistency(refresher: Refresher) -> bool:
    """
    Implements the AC-3 algorithm for arc consistency.
    """
    queue = g.get_arcs()
    while not queue.empty():
        v1, v2 = queue.get()
        if revise(v1, v2):
            refresher.refresh_screen()
            if not v1.remaining_domain:
                return False
            for neighbor in g.neighbors(v1):
                if neighbor != v2:
                    queue.put((neighbor, v1))
    return True


def revise(v1: myVariable, v2: myVariable):
    """
    Revises the domain of v1 by removing values that do not satisfy arc consistency with v2.
    """
    new_domain = set()
    revised = False
    for val1 in v1.remaining_domain:
        if any(g.is_arc_satisfied(v1, v2, val1, val2) for val2 in v2.remaining_domain):
            new_domain.add(val1)
        else:
            revised = True
    if revised:
        v1.remaining_domain = new_domain
    return revised


def select_unassigned_variable(do_mrv: bool) -> myVariable:
    if do_mrv:
        return minimum_remaining_values()
    else:
        return select_static_order_variable()


def select_static_order_variable() -> myVariable:
    for var in my_variables:
        if var.value is None:
            return var
    return None


def minimum_remaining_values() -> myVariable:
    """
    Returns a variable with the lowest remaining domain count.
    """
    best = None
    min_size = float('inf')
    for var in my_variables:
        if var.value is None:
            if len(var.remaining_domain) < min_size:
                min_size = len(var.remaining_domain)
                best = var
    return best


def order_domain_values(v: myVariable, do_lcv: bool) -> List[int]:
    if do_lcv:
        return least_constraining_value(v)
    else:
        return static_order_domains(v)


def static_order_domains(v: myVariable) -> List[int]:
    return sorted(v.remaining_domain)


def least_constraining_value(v: myVariable) -> List[int]:
    """
    Orders the values in the domain of `v` based on how few constraints they impose on neighboring variables.
    """
    scored = []
    for val in v.remaining_domain:
        impact = 0
        for neighbor in g.neighbors(v):
            if neighbor.value is None:
                for other_val in neighbor.remaining_domain:
                    if not g.is_arc_satisfied(v, neighbor, val, other_val):
                        impact += 1
        scored.append((val, impact))
    scored.sort(key=lambda x: x[1])
    return [val for val, _ in scored]


def extract_domains() -> Dict[myVariable, List[int]]:
    """
    Backups all the remaining domains of every variable and returns them.
    """
    return {v: set(v.remaining_domain) for v in my_variables}


def restore_domains(backup_domains: Dict[myVariable, List[int]]):
    """
    Sets back the remaining domains of every variable to their becked-up domains.
    """
    for v in my_variables:
        v.remaining_domain = backup_domains[v]


def set_doms_to_values():
    """
    Sets remaining_domain of all variables with assigned value to their value.
    """
    for v in my_variables:
        if v.value is not None:
            v.remaining_domain = {v.value}
