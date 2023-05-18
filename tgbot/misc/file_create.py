from openpyxl import Workbook
from openpyxl.styles import Font
import os


async def create_excel(requests_list: list):
    wb = Workbook()
    ws = wb.active
    ws.append(
        (
            'Номер',
            'Имя',
            'Телефон',
            'Тип запроса',
            'Дата создания',
            'Тип недвижимости',
            'Цель покупки',
            'Стадия строительства',
            'Цена',
            'Время для звонка',
        )
    )
    ft = Font(bold=True)
    for row in ws['A1:T1']:
        for cell in row:
            cell.font = ft

    for request in requests_list:
        ws.append(
            (
                request['id'],
                request['name'],
                request['phone'],
                request['type_request'],
                request['add_datetime'],
                request['property_type'],
                request['target'],
                request['stage_building'],
                request['price'],
                request['time_to_call']
            )
        )

    wb.save(f'{os.getcwd()}/all_tickets.xlsx')
