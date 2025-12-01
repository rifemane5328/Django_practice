import django_filters

class MaterialFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='by_name_filter')
    price_low = django_filters.NumberFilter(field_name='unit_price', lookup_expr='lte')
    price_gr = django_filters.NumberFilter(field_name='unit_price', lookup_expr='gte')

    def by_name_filter(self, queryset, name, value):
        if value:
            value = value.strip()
            return queryset.filter(name__icontains=value)
        return queryset
        
    # def by_price_filter(self, queryset, price, value):
        # if value is not None:
            # return queryset.filter(unit_price__lte=value)
        # else:
            # return queryset
        