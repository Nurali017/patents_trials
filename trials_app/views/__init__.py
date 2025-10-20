"""
Views для Trials Service
Разделены по модулям для лучшей организации
"""

from .geography import (
    OblastViewSet,
    ClimateZoneViewSet,
    RegionViewSet
)
from .culture import (
    IndicatorViewSet,
    TrialTypeViewSet,
    GroupCultureViewSet,
    CultureViewSet
)
from .sort import (
    OriginatorViewSet,
    SortRecordViewSet
)
from .application import (
    ApplicationViewSet
)
from .trial import (
    TrialViewSet
)
from .trial_plan import (
    TrialPlanViewSet
)
from .trial_participant import (
    TrialParticipantViewSet
)
from .trial_result import (
    TrialResultViewSet
)
from .document import (
    DocumentViewSet,
    test_patents_connection,
    get_group_cultures,
    create_group_culture,
    get_cultures,
    create_culture,
    get_culture_detail,
    update_culture,
    get_originators,
    create_originator,
    get_originator_detail,
    get_sorts,
    create_sort,
    get_sort_detail,
    get_sorts_for_trial_culture
)
from .annual_report import (
    AnnualReportViewSet
)

__all__ = [
    # ViewSets
    'OblastViewSet',
    'ClimateZoneViewSet',
    'RegionViewSet',
    'IndicatorViewSet',
    'TrialTypeViewSet',
    'GroupCultureViewSet',
    'CultureViewSet',
    'OriginatorViewSet',
    'SortRecordViewSet',
    'ApplicationViewSet',
    'TrialViewSet',
    'TrialPlanViewSet',
    'TrialParticipantViewSet',
    'TrialResultViewSet',
    'DocumentViewSet',
    'AnnualReportViewSet',
    
    # API Functions
    'test_patents_connection',
    'get_group_cultures',
    'create_group_culture',
    'get_cultures',
    'create_culture',
    'get_culture_detail',
    'update_culture',
    'get_originators',
    'create_originator',
    'get_originator_detail',
    'get_sorts',
    'create_sort',
    'get_sort_detail',
    'get_sorts_for_trial_culture',
]
