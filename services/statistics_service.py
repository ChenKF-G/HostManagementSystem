"""
统计业务（services/statistics_service.py）

负责按城市/机房维度统计主机数量，并落库到 host_statistics。
"""
import logging
from datetime import date

from django.db import transaction

from apps.city.models import City
from apps.host.models import Host
from apps.idc.models import IDC
from apps.statistics.models import HostStatistics

logger = logging.getLogger("app")


class StatisticsService:
    @staticmethod
    def generate_statistics(stat_date=None) -> dict:
        """
        生成统计并落库。
        - 按城市维度统计
        - 按机房维度统计
        通过 (dimension, city, idc, stat_date) 联合唯一索引保证幂等性。
        """
        stat_date = stat_date or date.today()
        city_stats = 0
        idc_stats = 0

        with transaction.atomic():
            # 按城市统计
            for city in City.objects.all():
                hosts = Host.objects.filter(idc__city=city)
                online = hosts.filter(status="online").count()
                offline = hosts.filter(status="offline").count()
                HostStatistics.objects.update_or_create(
                    dimension="city",
                    city=city,
                    idc=None,
                    stat_date=stat_date,
                    defaults={
                        "total_count": hosts.count(),
                        "online_count": online,
                        "offline_count": offline,
                    },
                )
                city_stats += 1

            # 按机房统计
            for idc in IDC.objects.all():
                hosts = Host.objects.filter(idc=idc)
                online = hosts.filter(status="online").count()
                offline = hosts.filter(status="offline").count()
                HostStatistics.objects.update_or_create(
                    dimension="idc",
                    city=None,
                    idc=idc,
                    stat_date=stat_date,
                    defaults={
                        "total_count": hosts.count(),
                        "online_count": online,
                        "offline_count": offline,
                    },
                )
                idc_stats += 1

        logger.info(f"统计完成 {stat_date}：城市 {city_stats} 条，机房 {idc_stats} 条")
        return {"date": str(stat_date), "city": city_stats, "idc": idc_stats}
