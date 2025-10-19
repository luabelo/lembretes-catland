from datetime import datetime, timedelta
import calendar


def get_last_day_of_month(year, month):
    return calendar.monthrange(year, month)[1]


def get_weekday_of_month(year, month, day):
    return datetime(year, month, day).weekday()


def is_14_days_before_month_end(today):
    last_day = get_last_day_of_month(today.year, today.month)
    days_until_end = last_day - today.day
    return days_until_end == 14


def get_nth_weekday_of_month(year, month, weekday, nth):
    first_day = datetime(year, month, 1)
    first_weekday = first_day.weekday()
    
    days_until_weekday = (weekday - first_weekday) % 7
    first_occurrence = 1 + days_until_weekday
    target_day = first_occurrence + (nth - 1) * 7
    
    last_day = get_last_day_of_month(year, month)
    if target_day > last_day:
        return None
    
    return target_day


def is_week_of_nth_friday(today, nth):
    friday_day = get_nth_weekday_of_month(today.year, today.month, 4, nth)
    if friday_day is None:
        return False
    
    friday_date = datetime(today.year, today.month, friday_day)
    week_start = friday_date - timedelta(days=friday_date.weekday())
    
    return week_start.date() == today.date()


def get_last_tuesday_of_month(year, month):
    last_day = get_last_day_of_month(year, month)
    
    for day in range(last_day, 0, -1):
        if get_weekday_of_month(year, month, day) == 1:
            return day
    return None


def is_week_before_last_tuesday(today):
    last_tuesday_day = get_last_tuesday_of_month(today.year, today.month)
    if last_tuesday_day is None:
        return False
    
    last_tuesday = datetime(today.year, today.month, last_tuesday_day)
    week_before = last_tuesday - timedelta(days=7)
    
    return week_before.date() == today.date() and today.weekday() == 1


def is_first_week_of_month(today):
    return 1 <= today.day <= 7


REMINDER_RULES = [
    {
        'name': 'escala_mensal_veterinarias',
        'check': lambda today: is_14_days_before_month_end(today),
        'subject': 'Solicitar Escala do Próximo Mês',
        'message': 'Lembrete: Solicitar às veterinárias responsáveis pelos atendimentos a escala para o próximo mês.'
    },
    {
        'name': 'confirmacao_castracoes',
        'check': lambda today: is_14_days_before_month_end(today),
        'subject': 'Confirmar Dias de Castração',
        'message': 'Lembrete: Solicitar à veterinária responsável pelas castrações quais dias serão as castrações no próximo mês.'
    },
    {
        'name': 'lista_raio_x_primeira_semana',
        'check': lambda today: is_week_of_nth_friday(today, 1) and today.weekday() == 0,
        'subject': 'Solicitar Lista de Raio-X (1ª Sexta-feira)',
        'message': 'Lembrete: Solicitar às veterinárias a lista dos gatinhos que farão Raio-X na sexta-feira desta semana.'
    },
    {
        'name': 'lista_raio_x_terceira_semana',
        'check': lambda today: is_week_of_nth_friday(today, 3) and today.weekday() == 0,
        'subject': 'Solicitar Lista de Raio-X (3ª Sexta-feira)',
        'message': 'Lembrete: Solicitar às veterinárias a lista dos gatinhos que farão Raio-X na sexta-feira desta semana.'
    },
    {
        'name': 'lista_ultrassom',
        'check': lambda today: is_week_before_last_tuesday(today),
        'subject': 'Solicitar Lista de Ultrassom',
        'message': 'Lembrete: Solicitar às veterinárias quais gatinhos farão ultrassom na última terça-feira deste mês.'
    },
    {
        'name': 'confirmacao_horario_ultrassom',
        'check': lambda today: is_first_week_of_month(today) and today.weekday() == 0,
        'subject': 'Confirmar Horário de Ultrassom',
        'message': 'Lembrete: Confirmar com a veterinária do ultrassom se ela consegue fazer o atendimento na última terça-feira do mês e em qual horário.'
    }
]


def check_reminders(today=None):
    if today is None:
        today = datetime.now()
    
    active_reminders = []
    
    for rule in REMINDER_RULES:
        if rule['check'](today):
            active_reminders.append({
                'name': rule['name'],
                'subject': rule['subject'],
                'message': rule['message']
            })
    
    return active_reminders
