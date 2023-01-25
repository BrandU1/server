from django.conf import settings
from django.core.management.base import BaseCommand
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class Command(BaseCommand):
    help = 'zappa deploy를 위한 DB 생성'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('DB 생성 시작'))

        dbname = settings.DATABASES['default']['NAME']
        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        host = settings.DATABASES['default']['HOST']

        conn = connect(dbname='postgres', user=user, host=host, password=password)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute('CREATE DATABASE ' + dbname)
        cursor.close()
        conn.close()

        self.stdout.write(self.style.SUCCESS('DB 생성 완료'))
