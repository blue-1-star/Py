"""
Каталог услуг — динамический справочник, читаемый из БД.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import sqlite3

from ..adapters.db_adapter import DBAdapter


class ServiceCategory(str, Enum):
    PARKING = "PARKING"
    ACCESS = "ACCESS"
    IMPROVEMENT = "IMPROVEMENT"
    EQUIPMENT = "EQUIPMENT"
    BARRIER = "BARRIER"
    PARKING_ASSET = "PARKING_ASSET"


class ServiceType(str, Enum):
    MONTHLY = "MONTHLY"
    ONE_TIME = "ONE_TIME"
    FUNDRAISING = "FUNDRAISING"
    COMMERCIAL = "COMMERCIAL"


@dataclass
class Service:
    """Модель услуги из каталога"""
    code: str
    name: str
    group: str
    category: ServiceCategory
    service_type: ServiceType
    is_active: bool = True
    is_monthly: bool = False
    is_fundraising: bool = False
    is_commercial: bool = False
    is_access_control: bool = False
    is_cash_collectable: bool = True
    comment: str = ""
    access_policy_enabled: bool = False
    
    @classmethod
    def from_db_row(cls, row: tuple, columns: List[str]) -> 'Service':
        """Создает Service из строки БД"""
        row_dict = dict(zip(columns, row))
        return cls(
            code=row_dict.get('service_code'),
            name=row_dict.get('service_name'),
            group=row_dict.get('service_group'),
            category=ServiceCategory(row_dict.get('category', 'PARKING')),
            service_type=ServiceType(row_dict.get('service_type', 'MONTHLY')),
            is_active=bool(row_dict.get('is_active', 1)),
            is_monthly=bool(row_dict.get('is_monthly', 0)),
            is_fundraising=bool(row_dict.get('is_fundraising', 0)),
            is_commercial=bool(row_dict.get('is_commercial', 0)),
            is_access_control=bool(row_dict.get('is_access_control', 0)),
            is_cash_collectable=bool(row_dict.get('is_cash_collectable', 1)),
            comment=row_dict.get('comment', ''),
            access_policy_enabled=bool(row_dict.get('access_policy_enabled', 0)),
        )


class ServiceCatalog:
    """
    Единый справочник услуг.
    Загружается из БД при первом обращении и кэшируется.
    """
    
    _cache: Optional[Dict[str, Service]] = None
    
    @classmethod
    def _load_from_db(cls) -> Dict[str, Service]:
        """Загружает каталог из БД"""
        result = {}
        
        try:
            # Используем DBAdapter для подключения
            conn = DBAdapter.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT 
                    service_code,
                    service_name,
                    service_group,
                    service_type,
                    category,
                    is_active,
                    is_monthly,
                    is_fundraising,
                    is_commercial,
                    is_access_control,
                    is_cash_collectable,
                    comment,
                    access_policy_enabled
                FROM service_catalog
                WHERE is_active = 1
                ORDER BY service_code
            """)
            
            rows = cur.fetchall()
            
            # Получаем имена колонок
            columns = [desc[0] for desc in cur.description]
            
            for row in rows:
                service = Service.from_db_row(row, columns)
                result[service.code] = service
            
            conn.close()
            
        except Exception as e:
            print(f"⚠️ Ошибка загрузки каталога услуг из БД: {e}")
            return {}
        
        return result
    
    @classmethod
    def _get_cache(cls) -> Dict[str, Service]:
        """Возвращает кэш, загружая его при первом вызове"""
        if cls._cache is None:
            cls._cache = cls._load_from_db()
        return cls._cache
    
    @classmethod
    def get(cls, code: str) -> Optional[Service]:
        """Получить услугу по коду"""
        return cls._get_cache().get(code)
    
    @classmethod
    def get_name(cls, code: str) -> str:
        """Получить название услуги по коду"""
        service = cls.get(code)
        return service.name if service else code
    
    @classmethod
    def get_all(cls) -> List[Service]:
        """Получить все услуги"""
        return list(cls._get_cache().values())
    
    @classmethod
    def get_by_category(cls, category: ServiceCategory) -> List[Service]:
        """Получить услуги по категории"""
        return [s for s in cls.get_all() if s.category == category]
    
    @classmethod
    def get_parking_services(cls) -> List[Service]:
        """Получить все услуги парковки"""
        return cls.get_by_category(ServiceCategory.PARKING)
    
    @classmethod
    def is_valid(cls, code: str) -> bool:
        """Проверить, существует ли услуга"""
        return code in cls._get_cache()
    
    @classmethod
    def refresh(cls) -> None:
        """Принудительно обновить кэш (после изменения БД)"""
        cls._cache = None
        cls._get_cache()