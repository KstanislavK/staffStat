import os
import json

from django.core.management.base import BaseCommand

from staffapp.models import ClientList

JSON_PATH = 'staffapp/management/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), mode='r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        clients = load_from_json('clients')

        for client in clients:
            new_tk = ClientList(**client)
            new_tk.save()
