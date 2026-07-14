import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

OSBB_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(OSBB_ROOT))

from Bots.db_access import (
    get_vehicle_by_id,
    get_apartment_vehicles,
    get_vehicles_by_status,
    get_next_vehicle_for_review,
    update_vehicle_parking_status,
    update_vehicle_plate,
    update_vehicle_model,
    find_apartment,
)


class DBAdapter:
    """Адаптер для работы с БД"""
    
    @staticmethod
    def get_vehicle(vehicle_id: int) -> Optional[Dict[str, Any]]:
        result = get_vehicle_by_id(vehicle_id)
        if not result:
            return None
        return {
            'id': result[0],
            'apartment_number': result[1],
            'plate_norm': result[2],
            'plate_raw': result[3],
            'model_norm': result[4],
            'model_raw': result[5],
            'parking_time': result[6],
        }
    
    @staticmethod
    def get_apartment_vehicles(apartment_number: str) -> List[Dict[str, Any]]:
        vehicles = get_apartment_vehicles(apartment_number)
        return [
            {
                'id': v[0],
                'plate_norm': v[1],
                'plate_raw': v[2],
                'model_norm': v[3],
                'model_raw': v[4],
                'parking_time': v[5],
            }
            for v in vehicles
        ]
    
    @staticmethod
    def get_vehicles_by_status(status: str, limit: int = 50) -> List[Dict[str, Any]]:
        rows = get_vehicles_by_status(status, limit)
        return [
            {
                'id': r[0],
                'apartment_number': r[1],
                'plate_norm': r[2],
                'plate_raw': r[3],
                'model_norm': r[4],
                'model_raw': r[5],
                'parking_time': r[6],
            }
            for r in rows
        ]
    
    @staticmethod
    def get_next_vehicle_for_review() -> Optional[Dict[str, Any]]:
        result = get_next_vehicle_for_review()
        if not result:
            return None
        return {
            'id': result[0],
            'apartment_number': result[1],
            'plate_norm': result[2],
            'plate_raw': result[3],
            'model_norm': result[4],
            'model_raw': result[5],
            'parking_time': result[6],
        }
    
    @staticmethod
    def set_vehicle_parking_status(vehicle_id: int, status: str) -> tuple:
        return update_vehicle_parking_status(vehicle_id, status)
    
    @staticmethod
    def find_apartment(apartment_number: str) -> Optional[Dict[str, Any]]:
        result = find_apartment(apartment_number)
        if not result:
            return None
        return {
            'id': result[0],
            'apartment_number': result[1],
            'entrance': result[2] if len(result) > 2 else None,
        }
        # ==========================================
    # ЖИТЕЛИ (RESIDENT)
    # ==========================================
    
    @staticmethod
    def get_resident(user_id: int) -> Optional[Dict[str, Any]]:
        """Получить жителя по Telegram ID"""
        from Bots.db_access import get_resident_account
        result = get_resident_account(user_id)
        if not result:
            return None
        return {
            'id': result[0],
            'telegram_user_id': result[1],
            'telegram_username': result[2],
            'first_name': result[3],
            'last_name': result[4],
            'apartment_id': result[5],
            'apartment_number': result[6],
            'role': result[7],
            'status': result[8],
            'language_code': result[9],
            'created_at': result[10],
            'updated_at': result[11],
            'verified_at': result[12],
            'last_seen_at': result[13],
            'notes': result[14],
        }
    
    @staticmethod
    def get_residents_summary(limit: int = 10) -> Dict[str, Any]:
        """Получить сводку по жителям"""
        from Bots.db_access import get_resident_accounts_summary
        return get_resident_accounts_summary(limit)
    
    @staticmethod
    def get_residents_by_apartment(apartment_number: str) -> List[Dict[str, Any]]:
        """Получить жителей квартиры"""
        from Bots.db_access import get_accounts_by_apartment
        rows = get_accounts_by_apartment(apartment_number)
        return [
            {
                'telegram_user_id': r[0],
                'telegram_username': r[1],
                'first_name': r[2],
                'last_name': r[3],
                'role': r[4],
                'status': r[5],
                'verified_at': r[6],
            }
            for r in rows
        ]
    
    @staticmethod
    def link_apartment(user_id: int, apartment: str) -> tuple:
        """Привязать квартиру"""
        from Bots.db_access import link_resident_to_apartment
        return link_resident_to_apartment(user_id, apartment)
    
    @staticmethod
    def unlink_apartment(user_id: int) -> tuple:
        """Отвязать квартиру"""
        from Bots.db_access import unlink_resident_account
        return unlink_resident_account(user_id)
    
    @staticmethod
    def mark_verified(user_id: int) -> tuple:
        """Отметить как проверенного"""
        from Bots.db_access import mark_resident_operator_verified
        return mark_resident_operator_verified(user_id)
    
    @staticmethod
    def upsert_resident_from_telegram(user, language_code: str = "ru"):
        """Создать/обновить жителя из Telegram"""
        from Bots.db_access import upsert_resident_account_from_telegram
        return upsert_resident_account_from_telegram(user, language_code)
    # В db_adapter.py уже должно быть:
    @staticmethod
    def get_apartment_card(apartment_number: str) -> Optional[Dict[str, Any]]:
        """Получить карточку квартиры"""
        from Bots.db_access import get_apartment_card as _get_card
        return _get_card(apartment_number)
    

        # ==========================================
    # ПЛАТЕЖИ (PAYMENT)
    # ==========================================
    
    @staticmethod
    def get_payment(payment_id: int) -> Optional[Dict[str, Any]]:
        """Получить платеж по ID"""
        from Bots.db_access import get_conn
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                id,
                payment_date,
                period_code,
                apartment_number,
                vehicle_id,
                amount,
                currency,
                payment_method,
                source,
                created_by,
                comment,
                created_at,
                cashbox_code,
                cashbox_operation_id,
                cashier_batch_id,
                operator_id,
                service_item_code,
                base_service_code,
                service_type,
                commercial_contract_id,
                commercial_unit_id,
                cashier_receipt_id,
                cashier_entry_status,
                payment_notice_id,
                bank_transaction_id,
                payment_channel,
                apartment_id,
                source_ref
            FROM payments
            WHERE id = ?
        """, (payment_id,))
        
        row = cur.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            'id': row[0],
            'payment_date': row[1],
            'period_code': row[2],
            'apartment_number': row[3],
            'vehicle_id': row[4],
            'amount': row[5],
            'currency': row[6],
            'payment_method': row[7],
            'source': row[8],
            'created_by': row[9],
            'comment': row[10],
            'created_at': row[11],
            'cashbox_code': row[12],
            'cashbox_operation_id': row[13],
            'cashier_batch_id': row[14],
            'operator_id': row[15],
            'service_item_code': row[16],
            'base_service_code': row[17],
            'service_type': row[18],
            'commercial_contract_id': row[19],
            'commercial_unit_id': row[20],
            'cashier_receipt_id': row[21],
            'cashier_entry_status': row[22],
            'payment_notice_id': row[23],
            'bank_transaction_id': row[24],
            'payment_channel': row[25],
            'apartment_id': row[26],
            'source_ref': row[27],
        }
    
    @staticmethod
    def get_payments_by_apartment(apartment_number: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Получить платежи по номеру квартиры"""
        from Bots.db_access import get_conn
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                id,
                payment_date,
                period_code,
                apartment_number,
                vehicle_id,
                amount,
                currency,
                payment_method,
                source,
                created_by,
                comment,
                created_at,
                cashbox_code,
                cashbox_operation_id,
                cashier_batch_id,
                operator_id,
                service_item_code,
                base_service_code,
                service_type,
                commercial_contract_id,
                commercial_unit_id,
                cashier_receipt_id,
                cashier_entry_status,
                payment_notice_id,
                bank_transaction_id,
                payment_channel,
                apartment_id,
                source_ref
            FROM payments
            WHERE apartment_number = ?
            ORDER BY payment_date DESC
            LIMIT ?
        """, (apartment_number, limit))
        
        rows = cur.fetchall()
        conn.close()
        
        return [
            {
                'id': r[0],
                'payment_date': r[1],
                'period_code': r[2],
                'apartment_number': r[3],
                'vehicle_id': r[4],
                'amount': r[5],
                'currency': r[6],
                'payment_method': r[7],
                'source': r[8],
                'created_by': r[9],
                'comment': r[10],
                'created_at': r[11],
                'cashbox_code': r[12],
                'cashbox_operation_id': r[13],
                'cashier_batch_id': r[14],
                'operator_id': r[15],
                'service_item_code': r[16],
                'base_service_code': r[17],
                'service_type': r[18],
                'commercial_contract_id': r[19],
                'commercial_unit_id': r[20],
                'cashier_receipt_id': r[21],
                'cashier_entry_status': r[22],
                'payment_notice_id': r[23],
                'bank_transaction_id': r[24],
                'payment_channel': r[25],
                'apartment_id': r[26],
                'source_ref': r[27],
            }
            for r in rows
        ]
    
    @staticmethod
    def get_payments_by_vehicle(vehicle_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Получить платежи по ID автомобиля"""
        from Bots.db_access import get_conn
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                id,
                payment_date,
                period_code,
                apartment_number,
                vehicle_id,
                amount,
                currency,
                payment_method,
                source,
                created_by,
                comment,
                created_at,
                cashbox_code,
                cashbox_operation_id,
                cashier_batch_id,
                operator_id,
                service_item_code,
                base_service_code,
                service_type,
                commercial_contract_id,
                commercial_unit_id,
                cashier_receipt_id,
                cashier_entry_status,
                payment_notice_id,
                bank_transaction_id,
                payment_channel,
                apartment_id,
                source_ref
            FROM payments
            WHERE vehicle_id = ?
            ORDER BY payment_date DESC
            LIMIT ?
        """, (vehicle_id, limit))
        
        rows = cur.fetchall()
        conn.close()
        
        return [
            {
                'id': r[0],
                'payment_date': r[1],
                'period_code': r[2],
                'apartment_number': r[3],
                'vehicle_id': r[4],
                'amount': r[5],
                'currency': r[6],
                'payment_method': r[7],
                'source': r[8],
                'created_by': r[9],
                'comment': r[10],
                'created_at': r[11],
                'cashbox_code': r[12],
                'cashbox_operation_id': r[13],
                'cashier_batch_id': r[14],
                'operator_id': r[15],
                'service_item_code': r[16],
                'base_service_code': r[17],
                'service_type': r[18],
                'commercial_contract_id': r[19],
                'commercial_unit_id': r[20],
                'cashier_receipt_id': r[21],
                'cashier_entry_status': r[22],
                'payment_notice_id': r[23],
                'bank_transaction_id': r[24],
                'payment_channel': r[25],
                'apartment_id': r[26],
                'source_ref': r[27],
            }
            for r in rows
        ]
    
    @staticmethod
    def get_payments_by_service(service_code: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Получить платежи по коду услуги"""
        from Bots.db_access import get_conn
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                id,
                payment_date,
                period_code,
                apartment_number,
                vehicle_id,
                amount,
                currency,
                payment_method,
                source,
                created_by,
                comment,
                created_at,
                cashbox_code,
                cashbox_operation_id,
                cashier_batch_id,
                operator_id,
                service_item_code,
                base_service_code,
                service_type,
                commercial_contract_id,
                commercial_unit_id,
                cashier_receipt_id,
                cashier_entry_status,
                payment_notice_id,
                bank_transaction_id,
                payment_channel,
                apartment_id,
                source_ref
            FROM payments
            WHERE base_service_code = ? OR service_item_code = ?
            ORDER BY payment_date DESC
            LIMIT ?
        """, (service_code, service_code, limit))
        
        rows = cur.fetchall()
        conn.close()
        
        return [
            {
                'id': r[0],
                'payment_date': r[1],
                'period_code': r[2],
                'apartment_number': r[3],
                'vehicle_id': r[4],
                'amount': r[5],
                'currency': r[6],
                'payment_method': r[7],
                'source': r[8],
                'created_by': r[9],
                'comment': r[10],
                'created_at': r[11],
                'cashbox_code': r[12],
                'cashbox_operation_id': r[13],
                'cashier_batch_id': r[14],
                'operator_id': r[15],
                'service_item_code': r[16],
                'base_service_code': r[17],
                'service_type': r[18],
                'commercial_contract_id': r[19],
                'commercial_unit_id': r[20],
                'cashier_receipt_id': r[21],
                'cashier_entry_status': r[22],
                'payment_notice_id': r[23],
                'bank_transaction_id': r[24],
                'payment_channel': r[25],
                'apartment_id': r[26],
                'source_ref': r[27],
            }
            for r in rows
        ]
    
    @staticmethod
    def get_payments_by_date_range(start_date: str, end_date: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Получить платежи за период"""
        from Bots.db_access import get_conn
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                id,
                payment_date,
                period_code,
                apartment_number,
                vehicle_id,
                amount,
                currency,
                payment_method,
                source,
                created_by,
                comment,
                created_at,
                cashbox_code,
                cashbox_operation_id,
                cashier_batch_id,
                operator_id,
                service_item_code,
                base_service_code,
                service_type,
                commercial_contract_id,
                commercial_unit_id,
                cashier_receipt_id,
                cashier_entry_status,
                payment_notice_id,
                bank_transaction_id,
                payment_channel,
                apartment_id,
                source_ref
            FROM payments
            WHERE payment_date >= ? AND payment_date <= ?
            ORDER BY payment_date DESC
            LIMIT ?
        """, (start_date, end_date, limit))
        
        rows = cur.fetchall()
        conn.close()
        
        return [
            {
                'id': r[0],
                'payment_date': r[1],
                'period_code': r[2],
                'apartment_number': r[3],
                'vehicle_id': r[4],
                'amount': r[5],
                'currency': r[6],
                'payment_method': r[7],
                'source': r[8],
                'created_by': r[9],
                'comment': r[10],
                'created_at': r[11],
                'cashbox_code': r[12],
                'cashbox_operation_id': r[13],
                'cashier_batch_id': r[14],
                'operator_id': r[15],
                'service_item_code': r[16],
                'base_service_code': r[17],
                'service_type': r[18],
                'commercial_contract_id': r[19],
                'commercial_unit_id': r[20],
                'cashier_receipt_id': r[21],
                'cashier_entry_status': r[22],
                'payment_notice_id': r[23],
                'bank_transaction_id': r[24],
                'payment_channel': r[25],
                'apartment_id': r[26],
                'source_ref': r[27],
            }
            for r in rows
        ]
    
    @staticmethod
    def create_payment(
        amount: float,
        apartment_number: str,
        service_code: str,
        payment_method: str = 'cash',
        vehicle_id: Optional[int] = None,
        period_code: Optional[str] = None,
        comment: Optional[str] = None,
        operator_id: Optional[str] = None,
        cashbox_code: Optional[str] = None,
    ) -> tuple:
        """Создать платеж"""
        from Bots.db_access import get_conn
        from datetime import datetime
        
        conn = get_conn()
        cur = conn.cursor()
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        period = period_code or now[:7]  # YYYY-MM
        
        try:
            cur.execute("""
                INSERT INTO payments (
                    payment_date,
                    period_code,
                    apartment_number,
                    vehicle_id,
                    amount,
                    currency,
                    payment_method,
                    comment,
                    created_at,
                    operator_id,
                    base_service_code,
                    service_type,
                    cashbox_code
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                now,
                period,
                apartment_number,
                vehicle_id,
                amount,
                'UAH',
                payment_method,
                comment,
                now,
                operator_id,
                service_code,
                'parking',
                cashbox_code,
            ))
            
            payment_id = cur.lastrowid
            conn.commit()
            conn.close()
            
            return True, {'payment_id': payment_id}
            
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, f"Ошибка: {e}"