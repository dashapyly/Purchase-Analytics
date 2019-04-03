import os.path as osp
import tempfile

from purchase_analytics import (add_department_id, get_department_by_product,
                                write_report)


def test_get_department_by_product_1():
    products = [
        {"product_id": "10101", "department_id": "99"},
        {"product_id": "10102", "department_id": "99"},
        {"product_id": "10103", "department_id": "99"},
    ]
    expected = {"10101": "99", "10102": "99", "10103": "99"}
    assert get_department_by_product(products) == expected


def test_get_department_by_product_2():
    products = []
    expected = {}
    assert get_department_by_product(products) == expected


def test_add_department_id():
    orders = [{"product_id": "10101"}, {"product_id": "20202"}]
    department_by_product = {"10101": "99", "20202": "199"}
    expected = [
        {"product_id": "10101", "department_id": "99"},
        {"product_id": "20202", "department_id": "199"},
    ]
    add_department_id(orders, department_by_product)
    assert orders == expected


def test_get_orders_by_department():
    ...


def test_get_number_of_orders():
    ...


def test_get_number_of_first_orders():
    ...


def test_get_percentage():
    ...


def test_create_output():
    ...


def test_write_report():
    output = [{"a": "1", "b": "2"}, {"a": "3", "b": "4"}]
    expected_text = "a,b\n1,2\n3,4\n"
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_file = osp.join(tmp_dir, "report.csv")
        write_report(output_file, output)
        with open(output_file, "rt") as fin:
            written_data = fin.read()
        assert written_data == expected_text
