"""
Доменная модель: Платежи (Payment)
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from ..adapters.db_adapter import DBAdapter


class Payment:
    """Модель платежа"""
    
    def __init__(self, data: Dict[str, Any]):
        self._data = data
        
        # Основные поля (из реальной БД)
        self.id = data.get('id')
        self.payment_date = data.get('payment_date')
        self.period_code = data.get('period_code')
        self.apartment_number = data.get('apartment_number')
        self.vehicle_id = data.get('vehicle_id')
        self.amount = data.get('amount')
        self.currency = data.get('currency', 'UAH')
        self.payment_method = data.get('payment_method')
        self.source = data.get('source')
        self.created_by = data.get('created_by')
        self.comment = data.get('comment')
        self.created_at = data.get('created_at')
        
        # Касса
        self.cashbox_code = data.get('cashbox_code')
        self.cashbox_operation_id = data.get('cashbox_operation_id')
        self.cashier_batch_id = data.get('cashier_batch_id')
        self.operator_id = data.get('operator_id')
        self.cashier_entry_status = data.get('cashier_entry_status')
        
        # Услуги
        self.service_item_code = data.get('service_item_code')
        self.base_service_code = data.get('base_service_code')
        self.service_type = data.get('service_type')
        
        # Коммерция
        self.commercial_contract_id = data.get('commercial_contract_id')
        self.commercial_unit_id = data.get('commercial_unit_id')
        
        # Банк
        self.cashier_receipt_id = data.get('cashier_receipt_id')
        self.payment_notice_id = data.get('payment_notice_id')
        self.bank_transaction_id = data.get('bank_transaction_id')
        self.payment_channel = data.get('payment_channel')
        
        # Связи
        self.apartment_id = data.get('apartment_id')
        self.source_ref = data.get('source_ref')
    
    # ==========================================
    # СВОЙСТВА
    # ==========================================
    
    @property
    def amount_display(self) -> str:
        return f"{self.amount:.2f} {self.currency}" if self.amount else "0.00 UAH"
    
    @property
    def status_display(self) -> str:
        status_map = {
            'pending': '⏳ Ожидает',
            'completed': '✅ Завершен',
            'failed': '❌ Ошибка',
            'refunded': '🔄 Возврат',
            'cancelled': '🚫 Отменен',
        }
        return status_map.get(self.cashier_entry_status, self.cashier_entry_status or '❓ Неизвестно')
    
    @property
    def service_display(self) -> str:
        service_map = {
            'parking': '🚗 Парковка',
            'remote': '🔑 Пульт',
            'maintenance': '🔧 Обслуживание',
            'improvement': '🏗 Благоустройство',
        }
        code = self.base_service_code or self.service_item_code
        return service_map.get(code, code or '📋 Другое')
    
    @property
    def payment_date_display(self) -> str:
        return self.payment_date or self.created_at or "-"
    
    @property
    def is_completed(self) -> bool:
        return self.cashier_entry_status == 'completed'
    
    # ==========================================
    # ФАБРИЧНЫЕ МЕТОДЫ
    # ==========================================
    
    @classmethod
    def get_by_id(cls, payment_id: int) -> Optional['Payment']:
        data = DBAdapter.get_payment(payment_id)
        return cls(data) if data else None
    
    @classmethod
    def get_by_apartment(cls, apartment_number: str, limit: int = 50) -> List['Payment']:
        data_list = DBAdapter.get_payments_by_apartment(apartment_number, limit)
        return [cls(data) for data in data_list]
    
    @classmethod
    def get_by_vehicle(cls, vehicle_id: int, limit: int = 50) -> List['Payment']:
        data_list = DBAdapter.get_payments_by_vehicle(vehicle_id, limit)
        return [cls(data) for data in data_list]
    
    @classmethod
    def get_by_service(cls, service_code: str, limit: int = 50) -> List['Payment']:
        data_list = DBAdapter.get_payments_by_service(service_code, limit)
        return [cls(data) for data in data_list]
    
    @classmethod
    def get_by_date_range(cls, start_date: str, end_date: str, limit: int = 100) -> List['Payment']:
        data_list = DBAdapter.get_payments_by_date_range(start_date, end_date, limit)
        return [cls(data) for data in data_list]
    
    @classmethod
    def create(cls, amount: float, apartment_number: str, service_code: str,
               payment_method: str = 'cash', vehicle_id: Optional[int] = None,
               comment: Optional[str] = None, operator_id: Optional[str] = None) -> tuple:
        return DBAdapter.create_payment(
            amount=amount,
            apartment_number=apartment_number,
            service_code=service_code,
            payment_method=payment_method,
            vehicle_id=vehicle_id,
            comment=comment,
            operator_id=operator_id,
        )
    
    def format_card(self) -> str:
        lines = []
        lines.append("💳 КАРТОЧКА ПЛАТЕЖА")
        lines.append("=" * 40)
        lines.append(f"ID: {self.id}")
        lines.append(f"Сумма: {self.amount_display}")
        lines.append(f"Услуга: {self.service_display}")
        lines.append(f"Метод: {self.payment_method or '-'}")
        lines.append(f"Статус: {self.status_display}")
        lines.append(f"Дата: {self.payment_date_display}")
        lines.append(f"Квартира: {self.apartment_number or '-'}")
        if self.vehicle_id:
            lines.append(f"Авто ID: {self.vehicle_id}")
        if self.comment:
            lines.append(f"Комментарий: {self.comment}")
        return "\n".join(lines)


class PaymentSummary:
    """Сводка по платежам"""
    
    def __init__(self, payments: List[Payment]):
        self.payments = payments
    
    @property
    def total_amount(self) -> float:
        return sum(p.amount for p in self.payments if p.is_completed)
    
    @property
    def total_count(self) -> int:
        return len(self.payments)
    
    @property
    def completed_count(self) -> int:
        return sum(1 for p in self.payments if p.is_completed)
    
    @property
    def total_display(self) -> str:
        return f"{self.total_amount:.2f} UAH"
    
    def format_summary(self) -> str:
        lines = []
        lines.append("📊 СВОДКА ПО ПЛАТЕЖАМ")
        lines.append("=" * 40)
        lines.append(f"Всего платежей: {self.total_count}")
        lines.append(f"✅ Завершено: {self.completed_count}")
        lines.append(f"💰 Общая сумма: {self.total_display}")
        return "\n".join(lines)