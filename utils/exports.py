import csv

import openpyxl


def export_to_excel(filename, data):
    # remove number of rows
    data = (row[1:] for row in data)
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Financials"

    # Write data
    for row_num, row_data in enumerate(data, 1):
        for col_num, cell_value in enumerate(row_data, 1):
            sheet.cell(row=row_num, column=col_num, value=cell_value)

    workbook.save(filename)
    print(f"Data exported to {filename}")


def export_to_csv(filename, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print(f"Data exported to {filename}")