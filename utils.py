from exceptions import NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError


def data_processing(data: dict):

    first_cup_year = 1930
    first_cup = int(data['first_cup'][:4])
    last_cup_year = 2022
    years_since_first_cup = last_cup_year - first_cup_year
    occurred_cups = 1 + years_since_first_cup // 4
    disputed_cups = 1 + (last_cup_year - first_cup) // 4


    if data['titles'] < 0:
        raise NegativeTitlesError('titles cannot be negative')
    
    if first_cup < first_cup_year or (first_cup - first_cup_year) % 4 != 0:
        raise InvalidYearCupError('there was no world cup this year')
    
    if data['titles'] > occurred_cups or data['titles'] > disputed_cups:
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")   
    
    return True