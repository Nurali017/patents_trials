"""
Сервис для статистики годового отчета
"""
from ...models import Application


class StatisticsService:
    """
    Сервис для расчета статистики по решениям в годовом отчете
    
    Включает:
    - Общее количество сортов
    - Количество по статусам решений (approved, rejected, continue, pending)
    - Процент принятых решений
    """
    
    def calculate_statistics(self, detailed_items):
        """
        Вычислить статистику по решениям
        
        Args:
            detailed_items: список детальных элементов отчета
            
        Returns:
            dict: статистика по решениям
        """
        # Фильтруем только испытываемые сорта (не стандарты)
        trial_items = [item for item in detailed_items if not item.get('is_standard', False)]
        
        total = len(trial_items)
        
        decisions_count = {
            'approved': 0,
            'rejected': 0,
            'continue': 0,
            'pending': 0
        }
        
        for item in trial_items:
            decision_status = item.get('decision_status', 'planned')
            
            if decision_status in ['approved', 'rejected', 'continue']:
                decisions_count[decision_status] += 1
            else:
                decisions_count['pending'] += 1
        
        decided = total - decisions_count['pending']
        decided_percent = (decided / total * 100) if total > 0 else 0
        
        return {
            'total_sorts': total,
            **decisions_count,
            'decided': decided,
            'decided_percent': round(decided_percent, 1)
        }
    
    def get_statistics_by_oblast(self, oblast, year):
        """
        Получить статистику по области за определенный год
        
        Args:
            oblast: объект области
            year: год отчета
            
        Returns:
            dict: статистика по области
        """
        # Найти все заявки с испытаниями в области за период
        years_range = [year-2, year-1, year]
        
        # Получить все заявки с испытаниями в области
        applications = Application.objects.filter(
            trialparticipant__trial__region__oblast=oblast,
            trialparticipant__trial__year__in=years_range,
            trialparticipant__statistical_group=1,  # Только испытываемые
            trialparticipant__is_deleted=False
        ).distinct()
        
        total = applications.count()
        
        decisions_count = {
            'approved': 0,
            'rejected': 0,
            'continue': 0,
            'pending': 0
        }
        
        for app in applications:
            decision_status = app.get_oblast_status(oblast)
            
            if decision_status in ['approved', 'rejected', 'continue']:
                decisions_count[decision_status] += 1
            else:
                decisions_count['pending'] += 1
        
        decided = total - decisions_count['pending']
        decided_percent = (decided / total * 100) if total > 0 else 0
        
        return {
            'total_sorts': total,
            **decisions_count,
            'decided': decided,
            'decided_percent': round(decided_percent, 1)
        }
