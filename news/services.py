import ssl
from typing import List, Coroutine

from aiohttp import ClientSession
from asgiref.sync import sync_to_async

from news.models import News

import os
import zipfile
from io import BytesIO
import pandas as pd
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model

from rayapp import settings

User = get_user_model()


class NewsParsingService:
    """Service for parsing news data from mediametrics API"""
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async def download_news_from_api(self, session: ClientSession) -> None:
        """
        Downloads and saves TSV files from a given URL.

        Args:
            session (aiohttp.ClientSession): The client session to use for making HTTP requests.
        """
        url = settings.PARSING_URL_API

        async with session.get(url=url, ssl=self.ssl_context) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                zip_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.zip')]

                parsing_directory = "media/parsing"
                os.makedirs(parsing_directory, exist_ok=True)
                counter = 0

                tasks = []
                for zip_link in zip_links:
                    counter += 1
                    if counter > 5:
                        break
                    full_zip_url = f"{url}/{zip_link}"

                    tasks.append(self.download_and_save_tsv(session, full_zip_url, zip_link, parsing_directory))

                await asyncio.gather(*tasks)

    async def download_and_save_tsv(self, session: ClientSession, full_zip_url: str, zip_link: str,
                                    parsing_directory: str) -> None:
        """
        Downloads a ZIP file, extracts a TSV file, and saves it to a directory.

        Args:
            session (aiohttp.ClientSession): The client session to use for making HTTP requests.
            full_zip_url (str): The full URL of the ZIP file.
            zip_link (str): The name of the ZIP file.
            parsing_directory (str): The directory to save the TSV file.
        """
        async with session.get(full_zip_url, ssl=self.ssl_context) as zip_response:
            if zip_response.status == 200:
                async with aiohttp.ClientSession() as inner_session:
                    async with inner_session.get(full_zip_url, ssl=self.ssl_context) as inner_zip_response:
                        with zipfile.ZipFile(BytesIO(await inner_zip_response.read())) as zip_file:
                            tsv_file_name = zip_file.namelist()[0]

                            with zip_file.open(tsv_file_name) as tsv_file:
                                df = pd.read_csv(tsv_file, delimiter='\t')

                            tsv_file_path = os.path.join(parsing_directory, f"{zip_link.replace('.zip', '')}.tsv")
                            df.to_csv(tsv_file_path, sep='\t', index=False)

    async def create_news_from_tsv(self) -> None:
        """
        Creates news from TSV files in the parsing directory.

        Returns:
            None
        """
        parsing_directory: str = "media/parsing"

        if os.path.exists(parsing_directory) and os.path.isdir(parsing_directory):
            tasks: List[Coroutine] = []

            for file_name in os.listdir(parsing_directory):
                if file_name.endswith(".tsv"):
                    file_path: str = os.path.join(parsing_directory, file_name)

                    tasks.append(self.process_tsv_file(file_path))

            await asyncio.gather(*tasks)

    async def process_tsv_file(self, file_path: str) -> None:
        """
        Process TSV file and create news instances.

        Args:
            file_path (str): The path to the TSV file.

        Returns:
            None
        """
        df = pd.read_csv(file_path, delimiter='\t')

        tasks = []

        for index, row in df.iterrows():
            title = row['Title']
            url = row['URL']

            tasks.append(self.create_news_instance(title, url))

        await asyncio.gather(*tasks)

    async def create_news_instance(self, title: str, url: str) -> None:
        """
            Create a news instance with the given title and url.
            Args:
                title (str): The title of the news.
                url (str): The URL of the news.
            Returns:
                None
        """
        user_id = await self.create_tech_user()
        news, created = await sync_to_async(
            News.objects.get_or_create
        )(title=title, url=url, user_id=user_id, source="mediametrics")

    async def create_tech_user(self) -> int:
        """
            This function creates a tech user and returns the user ID.
            Returns:
                int: The ID of the created tech user.
        """
        user = await sync_to_async(User.objects.get_or_create)(
            email="api@mediametrics.ru", username="mediametrics", name="mediametrics", password="tech"
        )
        return user[0].id

    async def main(self) -> None:
        session = ClientSession()
        await self.download_news_from_api(session)
        await self.create_news_from_tsv()
