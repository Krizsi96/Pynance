#!/usr/bin/env python3
import gspread
import logging
import click


@click.group()
def cli():
    pass


@click.command()
@click.argument("range_of_cells", type=str, required=True)
@click.argument("value", type=str, required=True)
def update(range_of_cells, value):
    client = gspread.service_account(
        filename="/home/kristof/Pynance/gsheets/service_account.json"
    )
    spreadsheet = client.open("PynanceTest")
    worksheet = spreadsheet.sheet1

    cell_list = worksheet.range(range_of_cells)
    for cell in cell_list:
        cell.value = value

    worksheet.update_cells(cell_list)


cli.add_command(update)

if __name__ == "__main__":
    cli()
