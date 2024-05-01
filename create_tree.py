"""Generate employee hierarchy"""

import sqlite3
import random
from ete3 import TreeNode, TreeStyle, TextFace, add_face_to_node  # type: ignore[import-untyped]
from faker import Faker


def tree_layout(node: TreeNode):
    """Simple vertical layout with horizontal text"""

    face = TextFace(node.name, tight_text=False)
    face.rotation = 270
    add_face_to_node(face, node, column=0, position="branch-right")


class Employee:
    """Employee object relating to DB table"""

    count: int = 0

    def __init__(self, boss_id: int | None, name: str):
        self.id = Employee.count
        self.boss_id = boss_id
        self.name = name

        Employee.count += 1


def build_company_hierarchy(min_nodes: int, unique: bool = False) -> list[Employee]:
    """Generates the hierarchy for this hypothetical company"""

    fake = Faker()
    fake.seed_instance(0)
    random.seed(0)

    def rand_name() -> str:
        return fake.unique.first_name() if unique else fake.first_name()

    # root node
    employees = [Employee(None, rand_name())]
    leaves = [employees[0].id]

    while n_employees := len(employees) < min_nodes:
        for boss in leaves:
            for _ in range(random.randint(1, 3)):
                employees.append(Employee(boss, rand_name()))

        # Nodes just added become the new leaves
        leaves = list(emp.id for emp in employees[n_employees:])

    return employees


def persist_employees(emp_list: list[Employee]):
    """Clear DB + add employees from list"""

    connection = sqlite3.connect("hierarchical.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Employee")
    connection.commit()

    cursor.executemany(
        "INSERT INTO Employee VALUES (?, ?, ?)",
        ((emp.id, emp.boss_id, emp.name) for emp in emp_list),
    )
    connection.commit()

    cursor.close()
    connection.close()


def show_org(emp_list: list[Employee]):
    """display tree using ete3"""

    nodes = [TreeNode(name=emp.name) for emp in emp_list]
    root = nodes[0]
    for node, emp in zip(nodes, emp_list):
        if emp.boss_id is not None:
            nodes[emp.boss_id].add_child(node)
        else:
            root = node

    ts = TreeStyle()
    ts.show_leaf_name = False
    ts.layout_fn = tree_layout
    ts.branch_vertical_margin = 20
    ts.force_topology = True
    ts.rotation = 90
    root.show(tree_style=ts)


if __name__ == "__main__":
    emp_list = build_company_hierarchy(20, unique=True)
    persist_employees(emp_list)
    show_org(emp_list)
