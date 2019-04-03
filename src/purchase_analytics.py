import csv
from collections import defaultdict
from typing import Any, List, Mapping, Dict


def read_csv(filename):
    """Read a csv file into a list of dictionaries."""
    with open(filename, "rt") as f:
        reader = csv.DictReader(f)
        return list(reader)


def get_department_by_product(products: List[Mapping[str, str]]) -> Mapping[str, str]:
    """Create a dictionary of products and departments."""
    department_by_product = {}
    for item in products:
        product_id = item["product_id"]
        department_by_product[product_id] = item["department_id"]
    return department_by_product


def add_department_id(
    orders: List[Dict[str, str]], department_by_product: Mapping[str, str]
) -> None:
    """Add department id to orders."""
    for item in orders:
        item["department_id"] = department_by_product[item["product_id"]]


def get_orders_by_department(
    orders: List[Mapping[str, str]]
) -> Mapping[str, List[Mapping[str, str]]]:
    """Create a dictionary of orders by department.

    The keys are departments, and the values are lists of order records.
    """
    orders_by_department: Mapping[str, List[Mapping[str, str]]] = defaultdict(list)
    for item in orders:
        department_id = item["department_id"]
        orders_by_department[department_id].append(item)
    return orders_by_department


def get_number_of_orders(
    orders_by_department: Mapping[str, List[Mapping[str, str]]]
) -> Mapping[str, int]:
    """Return the number of orders for each department."""
    number_of_orders = {}
    for department_id, items in orders_by_department.items():
        number_of_orders[department_id] = len(items)
    return number_of_orders


def get_number_of_first_orders(
    orders_by_department: Mapping[str, List[Mapping[str, str]]]
) -> Mapping[str, int]:
    """Return the number of first orders for each department."""
    number_of_first_orders = {}
    for department_id, items in orders_by_department.items():
        total_first_orders = 0
        for item in items:
            if int(item["reordered"]) == 1:
                pass
            else:
                assert int(item["reordered"]) == 0
                total_first_orders += 1
        number_of_first_orders[department_id] = total_first_orders
    return number_of_first_orders


def get_percentage(
    number_of_first_orders: Mapping[str, int], number_of_orders: Mapping[str, int]
) -> Mapping[str, float]:
    """Return the fraction of all orders which are first orders."""
    percentage = {}
    for department_id in number_of_first_orders:
        ratio = number_of_first_orders[department_id] / number_of_orders[department_id]
        percentage[department_id] = ratio
    return percentage


def create_output(
    number_of_orders: Mapping[str, int],
    number_of_first_orders: Mapping[str, int],
    percentage: Mapping[str, float],
) -> List[Dict[str, str]]:
    output_unsorted = []
    for key in number_of_orders:
        department_record = {}
        department_record["department_id"] = key
        department_record["number_of_orders"] = str(number_of_orders[key])
        department_record["number_of_first_orders"] = str(number_of_first_orders[key])
        department_record["percentage"] = "{:0.2f}".format(percentage[key])
        output_unsorted.append(department_record)
    output = sorted(output_unsorted, key=lambda d: int(d["department_id"]))
    return output


def write_report(filename: str, output: List[Dict[str, Any]]) -> None:
    """Write a list of dictionary objects to a csv file."""
    with open(filename, "wt", newline="") as fout:
        writer = csv.DictWriter(fout, fieldnames=list(output[0].keys()))
        writer.writeheader()
        writer.writerows(output)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--orders")
    parser.add_argument("--products")
    parser.add_argument("--output")
    args = parser.parse_args()

    products = read_csv(args.products)
    orders = read_csv(args.orders)

    department_by_product = get_department_by_product(products)
    add_department_id(orders, department_by_product)
    orders_by_department = get_orders_by_department(orders)
    number_of_orders = get_number_of_orders(orders_by_department)
    number_of_first_orders = get_number_of_first_orders(orders_by_department)
    percentage = get_percentage(number_of_first_orders, number_of_orders)

    output = create_output(number_of_orders, number_of_first_orders, percentage)
    write_report(args.output, output)
