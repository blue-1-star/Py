"""
Доменная модель: Касса (Cashbox)
Обеспечивает приём платежей и работу с кассовыми операциями
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from ..adapters.db_adapter import DBAdapter
from .vehicles import Vehicle, VehicleCandidate
from .residents import Resident
from .payments import Payment


class Cashbox:
    """
    Касса — рабочее место оператора для приёма платежей.
    
    Поддерживает:
    - Приём платежа по номеру автомобиля (включая "недоавтомобили")
    - Приём платежа по квартире
    - Создание "недоавтомобиля" на лету
    - Печать чека (заглушка)
    """
    
    @staticmethod
    def find_vehicle_or_candidate(plate: str) -> Dict[str, Any]:
        """
        Находит автомобиль по номеру.
        Если автомобиля нет — создаёт "кандидата" (недоавтомобиль).
        
        Returns:
            {'type': 'existing' | 'candidate', 'data': Vehicle|VehicleCandidate}
        """
        plate = plate.upper().strip()
        
        # Ищем существующий автомобиль в БД
        # TODO: реализовать поиск по номеру через DBAdapter
        # vehicle = DBAdapter.find_vehicle_by_plate(plate)
        # if vehicle:
        #     return {'type': 'existing', 'data': vehicle}
        
        # Если не найден — создаём кандидата
        return {'type': 'candidate', 'data': VehicleCandidate(plate)}
    
    @staticmethod
    def register_payment(
        amount: float,
        plate: str,
        apartment_number: str,
        service_code: str = 'parking',
        payment_method: str = 'cash',
        operator_id: Optional[int] = None,
        comment: str = None,
    ) -> Dict[str, Any]:
        """
        Регистрирует платёж.
        
        Если автомобиль не найден — создаёт "недоавтомобиль" (VehicleCandidate)
        и привязывает его к квартире.
        """
        # 1. Найти или создать автомобиль
        result = Cashbox.find_vehicle_or_candidate(plate)
        
        vehicle = result['data']
        vehicle_id = None
        
        # Если это кандидат — создаём полноценный автомобиль
        if result['type'] == 'candidate':
            # Проверяем квартиру
            apt = DBAdapter.find_apartment(apartment_number)
            if not apt:
                return {
                    'success': False,
                    'error': f'Квартира {apartment_number} не найдена'
                }
            
            # Создаём автомобиль
            success, create_result = vehicle.approve(apartment_number)
            if not success:
                return {
                    'success': False,
                    'error': f'Ошибка создания автомобиля: {create_result}'
                }
            vehicle_id = create_result.id
        else:
            vehicle_id = vehicle.id
        
        # 2. Создаём платёж
        success, result = Payment.create(
            amount=amount,
            apartment_number=apartment_number,
            service_code=service_code,
            payment_method=payment_method,
            vehicle_id=vehicle_id,
            comment=comment,
            operator_id=operator_id,
        )
        
        if not success:
            return {
                'success': False,
                'error': f'Ошибка создания платежа: {result}'
            }
        
        return {
            'success': True,
            'payment_id': result.get('payment_id'),
            'vehicle_created': result['type'] == 'candidate',
            'vehicle_plate': plate,
            'amount': amount,
        }
    
    @staticmethod
    def get_daily_report(date: str = None) -> Dict[str, Any]:
        """Получить отчёт по кассе за день"""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # TODO: реализовать через DBAdapter
        return {
            'date': date,
            'total_payments': 0,
            'total_amount': 0,
            'cash_payments': 0,
            'card_payments': 0,
            'bank_payments': 0,
            'payments': [],
        }