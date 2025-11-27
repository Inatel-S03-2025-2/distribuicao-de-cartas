"""
Módulo de Distribuição de Pokémons
Contém toda a lógica de negócio relacionada à distribuição e gerenciamento de pokémons.
"""

from .service import DistribuicaoService
from .router import router
from .schemas import StatusDistribuicao, Status

__all__ = [
    "DistribuicaoService",
    "router",
    "StatusDistribuicao",
    "Status"
]
