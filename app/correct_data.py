from typing import Any, Optional
from pandas import DataFrame

async def check_excel_data(document: Any) -> Optional[str]:
    """
    Проверяет загруженный документ на наличие необходимых условий.

    :param document: Загруженный документ
    :return: Имя файла, если это Excel файл с расширением .xlsx, иначе None
    """

    if not document.file_name.endswith('.xlsx'):
        return None
    return document.file_name

async def check_correct_columns(df: DataFrame) -> Optional[str]:
    """
    Проверяет наличие необходимых колонок в DataFrame.

    :param df: DataFrame с данными из документа
    :return: DataFrame, если все необходимые колонки присутствуют, иначе None
    """

    required_columns = ['title', 'url', 'xpath']
    if not all(col in df.columns for col in required_columns):
        return None
    return df