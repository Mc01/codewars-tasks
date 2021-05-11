import datetime
from enum import Enum
from typing import Union, Tuple


class EnumItems(Enum):
    @classmethod
    def items(cls) -> set:
        return {item.value for item in cls}

    @classmethod
    def find_in_items(cls, sentence: str, multiple=False, underscores=True) -> Union[str, list]:
        def search_item():
            if underscores:
                return item in sentence
            else:
                return item.replace('_', ' ') in sentence

        items = []
        for item in cls.items():
            if search_item():
                if not multiple:
                    return item
                else:
                    items.append(item)

        if multiple and items:
            return items

        raise ValueError(f'Unknown {cls.__name__}!')


class Action(EnumItems):
    ALLOW = 'allow'
    DENY = 'deny'
    NO_LONGER = 'no longer require'
    REQUIRE = 'require'
    WANTED = 'wanted by'


class Persona(EnumItems):
    ENTRANTS = 'entrants'
    CITIZENS = 'citizens'
    FOREIGNERS = 'foreigners'
    WORKERS = 'workers'


class Countries(EnumItems):
    ARSTOTZKA = 'arstotzka'
    ANTEGRIA = 'antegria'
    IMPOR = 'impor'
    KOLECHIA = 'kolechia'
    OBRISTAN = 'obristan'
    REPUBLIA = 'republia'
    UNITED_FEDERATION = 'united federation'


class Document(EnumItems):
    PASSPORT = 'passport'
    CERTIFICATE_VACCINE = 'vaccination'
    ID_CARD = 'id_card'
    ACCESS_PERMIT = 'access_permit'
    WORK_PASS = 'work_pass'
    GRANT_ASYLUM = 'grant_of_asylum'
    DIPLOMATIC_AUTH = 'diplomatic_authorization'

    @classmethod
    def find_in_items(cls, sentence: str, multiple=False, underscores=True) -> Union[str, list]:
        if not underscores and cls.CERTIFICATE_VACCINE.value in sentence:
            return sentence.split(f' {Action.REQUIRE.value} ')[-1]
        else:
            return super().find_in_items(
                sentence=sentence,
                multiple=multiple,
                underscores=underscores,
            )


class Message(EnumItems):
    NATIVE = 'Glory to Arstotzka.'
    FOREIGNER = 'Cause no trouble.'
    DENIED = 'Entry denied: '
    DETAINMENT = 'Detainment: '


class Expired:
    expiry_date = datetime.date(year=1982, month=11, day=22)

    @classmethod
    def is_expired(cls, date) -> bool:
        return datetime.datetime.strptime(date, '%Y.%m.%d').date() <= cls.expiry_date


class Denied(Exception):
    pass


class Detainment(Exception):
    pass


class Inspector:
    rules = {}

    def receive_bulletin(self, bulletin: str):
        print(f'Bulletin: {bulletin}')

        sentences = bulletin.lower().split('\n')
        for sentence in sentences:
            action, rule = self.parse_sentence(sentence)
            if action == Action.WANTED.value:
                self.rules[action] = rule
            else:
                self.update_rule(action, rule)

    @staticmethod
    def parse_sentence(sentence: str) -> Tuple[str, Union[dict, str]]:
        action: str = Action.find_in_items(sentence)
        if action == Action.WANTED.value:
            name_surname = sentence.split(':')[1].strip()
            name, surname = name_surname.split(' ', 1)
            value = f'{surname}, {name}'
        else:
            persona: str = Persona.find_in_items(sentence)
            if persona == Persona.CITIZENS.value:
                countries: list = Countries.find_in_items(sentence, multiple=True)
                persona = persona
                value = {
                    'persona': persona,
                    'countries': set(countries),
                }
            else:
                value = {
                    'persona': persona,
                }

            if action in (Action.REQUIRE.value, Action.NO_LONGER.value):
                value.update({'document': Document.find_in_items(sentence, underscores=False)})

        return action, value

    def update_rule(self, action: str, rule: dict):
        attrs = self.rules.setdefault(action, [])
        to_extend = {
            Action.ALLOW.value: True,
            Action.DENY.value: True
        }.get(action)

        if to_extend:
            for attr in attrs:
                if rule['persona'] == attr['persona'] and rule['persona'] == Persona.CITIZENS.value:
                    attr['countries'].update(rule['countries'])

            if not attrs:
                attrs.append(rule)
        elif action != Action.NO_LONGER.value:
            attrs.append(rule)

        self.remove_counterparts(action, rule)

    def remove_counterparts(self, action: str, rule: dict):
        to_remove = []
        to_change = {
            Action.ALLOW.value: Action.DENY.value,
            Action.DENY.value: Action.ALLOW.value,
            Action.NO_LONGER.value: Action.REQUIRE.value,
        }.get(action)

        for i, old in enumerate(self.rules.get(to_change, [])):
            persona = rule['persona']

            if old['persona'] == persona:
                if rule.get('document') != old.get('document'):
                    continue

                if persona == Persona.CITIZENS.value:
                    countries: set = rule['countries']
                    old_countries: set = old['countries']
                    match = {country for country in countries if country in old_countries}
                    if match == old_countries:
                        to_remove.append(i)
                    else:
                        old_countries -= match
                else:
                    to_remove.append(i)

        for item in reversed(to_remove):
            self.rules[to_change].pop(item)

    def inspect(self, person: dict) -> str:
        print(f'Person: {person}')

        try:
            attrs = self.parse_person(person)
        except Denied as e:
            return f'{Message.DENIED.value}{e}'
        except Detainment as e:
            return f'{Message.DETAINMENT.value}{e}'

        try:
            for action, rules in self.rules.items():
                if action == Action.WANTED.value:
                    continue

                for rule in rules:
                    if self.is_persona(attrs, rule, action):
                        {
                            Action.REQUIRE.value: self.require_document,
                            Action.ALLOW.value: self.allow_persona,
                            Action.DENY.value: self.deny_persona,
                        }[action](rule, attrs)
        except Denied as e:
            return f'{Message.DENIED.value}{e}'
        else:
            if attrs['nation'] == Countries.ARSTOTZKA.value:
                return Message.NATIVE.value
            else:
                return Message.FOREIGNER.value

    def parse_person(self, person) -> dict:
        attrs = {}
        has_expired_document = []

        for document, details in person.items():
            document = document.lower()
            sentences = details.lower().split('\n')

            ordered_sentences = sorted(sentences, key=lambda i: 0 if 'id#' in i else 1)
            for sentence in ordered_sentences:
                key, value = sentence.split(': ')
                if key == 'name':
                    wanted = self.rules.get(Action.WANTED.value)
                    if wanted and value in wanted:
                        raise Detainment('Entrant is a wanted criminal.')

                if key == 'exp':
                    if Expired.is_expired(value):
                        document_name = document.replace('_', ' ')
                        has_expired_document.append(document_name)

                    continue

                existing_value = attrs.get(key)
                if not existing_value:
                    attrs[key] = value
                elif existing_value != value:
                    field_map = {
                        'id#': 'ID number',
                        'nation': 'nationality',
                        'dob': 'date of birth',
                    }
                    raise Detainment(f'{field_map.get(key, key)} mismatch.')

            attrs.setdefault('documents', []).append(document)

        for document in has_expired_document:
            raise Denied(f'{document} expired.')

        if 'nation' not in attrs.keys():
            raise Denied(f'missing required passport.')

        return attrs

    @staticmethod
    def is_persona(attrs: dict, rule: dict, action):
        return {
            Persona.ENTRANTS.value: True,
            Persona.CITIZENS.value: attrs['nation'] in rule.get('countries', []) if action == Action.REQUIRE.value else True,
            Persona.FOREIGNERS.value: attrs['nation'] != Countries.ARSTOTZKA.value,
            Persona.WORKERS.value: attrs['nation'] != Countries.ARSTOTZKA.value and 'work' in attrs.get('purpose', ''),
        }[rule['persona']]

    @staticmethod
    def require_document(rule, attrs):
        complementary_documents = {
            Document.ACCESS_PERMIT.value: [
                Document.ACCESS_PERMIT.value,
                Document.GRANT_ASYLUM.value,
                Document.DIPLOMATIC_AUTH.value,
            ],
        }
        name_map = {
            'id_card': 'ID card',
        }

        document_name = rule['document']
        normalized_name = name_map.get(document_name, document_name.replace('_', ' '))
        documents = complementary_documents.get(document_name)
        if documents:
            for document in documents:
                if document in attrs['documents']:
                    if document == Document.DIPLOMATIC_AUTH.value:
                        if Countries.ARSTOTZKA.value not in attrs['access']:
                            raise Denied(f'invalid diplomatic authorization.')

                    return

            raise Denied(f'missing required {normalized_name}.')

        if Document.CERTIFICATE_VACCINE.value in document_name:
            vaccine = document_name.replace(Document.CERTIFICATE_VACCINE.value, '').strip()
            if vaccine not in attrs['vaccines']:
                raise Denied(f'missing required {Document.CERTIFICATE_VACCINE.value}.')

            return

        if document_name not in attrs['documents']:
            raise Denied(f'missing required {normalized_name}.')

    @staticmethod
    def allow_persona(rule, attrs):
        if attrs['nation'] not in rule['countries']:
            raise Denied(f'citizen of banned nation.')

    @staticmethod
    def deny_persona(rule, attrs):
        if attrs['nation'] in rule['countries']:
            raise Denied(f'citizen of banned nation.')


if __name__ == '__main__':
    inspector = Inspector()

    b1 = '''Bulletin: Allow citizens of Obristan
Entrants require measles vaccination
Entrants no longer require measles vaccination'''
    inspector.receive_bulletin(b1)

    p = {'passport': 'ID#: PD8LK-9YIE8\nNATION: Obristan\nNAME: Andrevska, Gunther\nDOB: 1968.08.29\nSEX: M\nISS: Bostan\nEXP: 1984.08.05', 'certificate_of_vaccination': 'NAME: Andrevska, Gunther\nID#: PD8LK-9YIE8\nVACCINES: tetanus, rubella, typhus, cholera', 'access_permit': 'NAME: Andrevska, Gunther\nNATION: Obristan\nID#: PD8LK-9YIE8\nPURPOSE: WORK\nDURATION: 3 MONTHS\nHEIGHT: 152cm\nWEIGHT: 115kg\nEXP: 1992.05.08'}
    inspection = inspector.inspect(p)
    assert inspection == 'Entry denied: missing required work pass.'
