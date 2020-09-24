def get_all_variables(questions):
    """ 
    Функция получения списка всех
    возможных вариантов ответов
    во всех существующих вопросах
    """
    all_variables = []
    for variable_list in [question['variables'] for question in questions]:
        for variable in variable_list:
            all_variables.append(variable)
    return all_variables
