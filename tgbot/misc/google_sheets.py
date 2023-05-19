from apiclient import discovery
from google.oauth2 import service_account

from create_bot import secret_file, spreadsheet_id, sheet_name


class GoogleSheets:

    @classmethod
    async def google_update(cls, requests_list: list):
        scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file",
                  "https://www.googleapis.com/auth/spreadsheets"]

        credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)
        service = discovery.build('sheets', 'v4', credentials=credentials)

        range_name = f'{sheet_name}!A1:J{len(requests_list) + 1}'

        values = [
            [
                'Номер',
                'Имя',
                'Телефон',
                "Тип запроса",
                "Дата создания",
                "Тип недвижимости",
                "Цель покупки",
                "Стадия строительства",
                "Цена",
                "Время для звонка"
            ]
        ]

        for request in requests_list:
            values.append(
                [
                    request['id'],
                    request['name'],
                    request['phone'],
                    request['type_request'],
                    request['add_datetime'].strftime('%d-%m-%Y %H:%M'),
                    request['property_type'] if request['property_type'] else '---',
                    request['target'] if request['target'] else '---',
                    request['stage_building'] if request['stage_building'] else '---',
                    request['price'] if request['price'] else '---',
                    request['time_to_call'] if request['time_to_call'] else '---'
                ]
            )

        data = {
            "majorDimension": "ROWS",
            'values': values
        }

        service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, body=data, range=range_name,
                                               valueInputOption='USER_ENTERED').execute()
