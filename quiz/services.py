def get_all_variables(questions: list) -> list:
    """ 
    Функция получения списка всех
    возможных вариантов ответов
    во всех существующих вопросах
    """
    all_variables = []
    for variable_list in [question['variables'] for question in questions]:
        all_variables.extend(variable_list)

    return all_variables
