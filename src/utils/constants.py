from enum import Enum

class TaxAuthority(str, Enum):
    NAME = "DNIT"
    FULL_NAME = "Dirección Nacional de Ingresos Tributarios"
    OLD_NAME = "SET"
    SYSTEM_NAME = "Marangatu"

# Ejemplos de uso:
# TaxAuthority.NAME.value -> "DNIT"
