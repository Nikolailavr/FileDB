import json
from collections import defaultdict

from django_filters import FilterSet

from misc.constants import REQUIRED_FIELDS
from .models import File


class FileFilter(FilterSet):
    class Meta:
        model = File
        fields = {
            'type': ['exact'],
            'vendor': ['icontains'],
            'date_revision': ['exact', 'gt', 'lt', 'gte', 'lte'],
        }

    def extra_filter(self, queryset, filters: dict = None):
        filters = self.__prepare_extra_filters(filters)
        for key, values in filters.items():
            for value in values:
                queryset = self.__choose_by_sign(queryset, value, key)
        return queryset

    @staticmethod
    def __choose_by_sign(qs, filter_: dict, key: str):
        for item in qs:
            qs_field = json.loads(item.extra_field).get(key)
            filter_value = filter_.get('value')
            if filter_value.isnumeric():
                filter_value = int(filter_value)
            if qs_field is None:
                qs = qs.exclude(id=item.id)
                continue
            elif filter_.get('sign') == 'lte' and qs_field <= filter_value:
                continue
            elif filter_.get('sign') == 'gte' and qs_field >= filter_value:
                continue
            elif filter_.get('sign') == 'gt' and qs_field > filter_value:
                continue
            elif filter_.get('sign') == 'lt' and qs_field < filter_value:
                continue
            elif filter_.get('sign') == 'equal' and qs_field == filter_value:
                continue
            else:
                qs = qs.exclude(id=item.id)
        return qs

    @staticmethod
    def __prepare_extra_filters(filters: dict) -> dict:
        result = defaultdict(list)
        if filters:
            for key, value in filters.items():
                filter_ = key.split('__')
                sign = filter_[1] if len(filter_) > 1 else 'equal'
                if filter_[0] not in REQUIRED_FIELDS:
                    result[filter_[0]].append(
                        {
                            "value": value,
                            "sign": sign
                        }
                    )
        return result
