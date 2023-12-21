#!/usr/bin/env python3
import gspread
import logging
import click


@click.group()
def cli():
    pass


@click.command()
@click.argument("spreadsheet_name", type=str, required=True)
@click.argument("range_of_cells", type=str, required=True)
@click.argument("value", type=str, required=True)
def update(spreadsheet_name, range_of_cells, value):
    configure_logging()
    update_values_of(spreadsheet_name, "Sheet1", range_of_cells, value)


@click.command()
@click.argument("spreadsheet_name", type=str, required=True)
@click.argument("range_of_cells", type=str, required=True)
def read(spreadsheet_name, range_of_cells):
    configure_logging()
    logging.info(f"Reading spreadsheet {spreadsheet_name}")
    cells = read_values_of(spreadsheet_name, "Sheet1", range_of_cells)
    for cell in cells:
        print(f"{cell.row}, {cell.col}: {cell.value}")


def update_values_of(spreadsheet_name, worksheet_name, range_of_cells, value):
    logging.info(f"Updating spreadsheet {spreadsheet_name}")

    try:
        worksheet = open_worksheet(spreadsheet_name, worksheet_name)
        logging.debug(f"Worksheet {worksheet.title} opened")
    except [gspread.SpreadsheetNotFound, FileNotFoundError]:
        return

    cell_list = worksheet.range(range_of_cells)
    for cell in cell_list:
        cell.value = value
    worksheet.update_cells(cell_list)
    logging.info(
        f"Cell(s) '{worksheet.title}!{range_of_cells}' updated with value '{value}'"
    )


def read_values_of(spreadsheet_name, worksheet_name, range_of_cells):
    logging.info(f"Reading spreadsheet {spreadsheet_name}")

    try:
        worksheet = open_worksheet(spreadsheet_name, worksheet_name)
        logging.debug(f"Worksheet {worksheet.title} opened")
    except [gspread.SpreadsheetNotFound, FileNotFoundError]:
        return

    cell_list = worksheet.range(range_of_cells)
    logging.info(f"Cell(s) '{worksheet.title}!{range_of_cells}' read")

    return cell_list


def open_worksheet(spreadsheet_name, worksheet_name):
    client = create_client("/home/kristof/Pynance/gsheets/service_account.json")
    spreadsheet = open_spreadsheet(client, spreadsheet_name)
    return spreadsheet.worksheet(worksheet_name)


def configure_logging():
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG
    )


def create_client(filename):
    try:
        new_client = gspread.service_account(filename)
        logging.debug(f"new client created from {filename}")
        return new_client
    except FileNotFoundError:
        logging.error(f"{filename} not found")
        raise FileNotFoundError(f"{filename} not found")


def open_spreadsheet(client, spreadsheet_name):
    try:
        spreadsheet = client.open(spreadsheet_name)
        logging.debug(f"Spreadsheet {spreadsheet_name} opened")
        return spreadsheet
    except gspread.SpreadsheetNotFound:
        logging.error(f"Spreadsheet {spreadsheet_name} not found")
        raise gspread.SpreadsheetNotFound(f"Spreadsheet {spreadsheet_name} not found")


cli.add_command(update)
cli.add_command(read)

if __name__ == "__main__":
    cli()
