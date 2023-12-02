from asyncio import run

from django.core.management.base import BaseCommand

from news.services import NewsParsingService


class Command(BaseCommand):
    help = 'Run news parsing service'

    def handle(self, *args, **options):
        async def async_main():
            service = NewsParsingService()
            await service.main()

        run(async_main())
        print('News has been downloaded')
