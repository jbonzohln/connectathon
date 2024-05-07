from hl7 import Segment

PATIENT_NAME_INDEX = 5
PATIENT_ALIAS_INDEX = 6
PATIENT_BIRTH_DATE_TIME_INDEX = 7
PATIENT_SEX_INDEX = 8


def pid_to_patient_query_params(PID: Segment) -> dict[str, str]:
    query_params = {}
    names = []

    if len(PID) > PATIENT_NAME_INDEX:
        for element in PID[PATIENT_NAME_INDEX]:
            for group in element:
                names.extend(group)

    if len(PID) > PATIENT_ALIAS_INDEX:
        names.extend(PID[PATIENT_ALIAS_INDEX])

    if len(PID) > PATIENT_BIRTH_DATE_TIME_INDEX:
        for element in PID[PATIENT_BIRTH_DATE_TIME_INDEX]:
            if len(element) >= 8:
                birthdate = element[0: 8]
                query_params['birthdate'] = 'eq' + birthdate[0:4] + '-' + birthdate[4:6] + '-' + birthdate[6:8]

    if len(PID) > PATIENT_SEX_INDEX:
        for sex in PID[PATIENT_SEX_INDEX]:
            match sex:
                case 'F':
                    query_params['gender'] = 'female'
                case 'M':
                    query_params['gender'] = 'male'
                case _:
                    query_params['gender'] = 'other'

    query_params['name:exact'] = ','.join(names)
    return query_params
