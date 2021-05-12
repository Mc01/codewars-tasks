from itertools import chain
from datetime import datetime
import re


class Inspector:
    def __init__(self):
        self.nation_allowed = []
        self.vaccinations = {
            "Entrants": set(), "Foreigners": set(), "Citizens": set(), "Workers": set(),
            "Arstotzka": set(), "Antegria": set(), "Impor": set(), "Kolechia": set(),
            "Obristan": set(), "Republia": set(), "United Federation": set()
        }
        self.required_docs = {
            "Entrants": [], "Foreigners": [], "Citizens": [], "Workers": [],
        }
        self.wanted = []

    def update_nation(self, info, allowed=True):
        counrties = info.split("of ")[1].split(", ")
        if allowed:
            self.nation_allowed += counrties
        else:
            self.nation_allowed = list(set(self.nation_allowed) - set(counrties))

    def update_required_docs(self, info, who):
        doc = info.split("require")[1].strip()
        self.required_docs[who].append(doc)

    def update_vaccinations(self, info, required=False):
        vac_regex = r"(Citizens of )?(?P<who>\D+?)( no longer)? require (?P<vaccination>\D+) vaccination"
        vac_info = re.search(vac_regex, info)
        if vac_info:
            who = vac_info["who"].split(", ")
            vaccination = vac_info["vaccination"]
            for w in who:
                if required:
                    self.vaccinations[w].add(vaccination)
                else:
                    self.vaccinations[w].remove(vaccination)

    def update_wanted(self, info):
        self.wanted = []
        self.wanted = info.split(":")[1].strip().split(",")

    def receive_bulletin(self, bulletin):
        # print(bulletin)
        for info in bulletin.split("\n"):
            if "Allow citizens of" in info:
                self.update_nation(info, allowed=True)
            elif "Deny citizens of" in info:
                self.update_nation(info, allowed=False)
            elif "vaccination" in info:
                if "no longer require" in info:
                    self.update_vaccinations(info, required=False)
                else:
                    self.update_vaccinations(info, required=True)
            elif "Entrants require" in info:
                self.update_required_docs(info, "Entrants")
            elif "Foreigners require" in info:
                self.update_required_docs(info, "Foreigners")
            elif "Citizens of Arstotzka require" in info:
                self.update_required_docs(info, "Citizens")
            elif "Workers require" in info:
                self.update_required_docs(info, "Workers")
            elif "Wanted by the State:" in info:
                self.update_wanted(info)

    def inspect(self, docs):
        person = Person(docs)
        if person.check_if_criminal(self.wanted):
            return "Detainment: Entrant is a wanted criminal."
        mismatch_fields = person.get_mismatch_fields()
        if mismatch_fields:
            return f"Detainment: {mismatch_fields[0]} mismatch."

        expired_docs = person.get_expired_docs()
        if expired_docs:
            return f"Entry denied: {expired_docs[0]} expired."
        if not person.diplomatic_authorization.is_valid:
            return "Entry denied: invalid diplomatic authorization."
        missing_docs = person.get_missing_docs(self.required_docs)
        if missing_docs:
            return f"Entry denied: missing required {missing_docs[0]}."

        needed_vaccinations = person.get_needed_vaccinations(self.vaccinations)
        if needed_vaccinations and not person.certificate_of_vaccination.is_present:
            return "Entry denied: missing required certificate of vaccination."
        if not person.has_vaccinations(needed_vaccinations):
            return "Entry denied: missing required vaccination."

        if person.nation not in self.nation_allowed:
            return "Entry denied: citizen of banned nation."

        if person.is_citizen:
            return "Glory to Arstotzka."
        else:
            return "Cause no trouble."


class Person:
    def __init__(self, docs):
        self.id_card = Document(docs.get("ID_card"), "ID card")
        self.passport = Document(docs.get("passport"), "passport")
        self.certificate_of_vaccination = Document(docs.get("certificate_of_vaccination"), "certificate of vaccination")
        self.access_permit = Document(docs.get("access_permit"), "access permit")
        self.work_pass = Document(docs.get("work_pass"), "work pass")
        self.grant_of_asylum = Document(docs.get("grant_of_asylum"), "grant of asylum")
        self.diplomatic_authorization = Document(docs.get("diplomatic_authorization"), "diplomatic authorization")

        self.documents = self.get_not_none_documents()

    def get_not_none_documents(self):
        docs = [
            self.id_card,
            self.passport,
            self.certificate_of_vaccination,
            self.access_permit,
            self.work_pass,
            self.grant_of_asylum,
            self.diplomatic_authorization
        ]
        return [doc for doc in docs if doc.is_present]

    @property
    def nation(self):
        if not self.documents:
            return "Arstotzka"
        nations = [doc.nation for doc in self.documents if doc.nation is not None]
        return nations[0] if nations else "Arstotzka"

    @property
    def is_citizen(self):
        # print(f"nation {self.nation}")
        return True if self.nation == "Arstotzka" else False

    @property
    def is_worker(self):
        if self.access_permit.is_present and self.access_permit.parsed.get("PURPOSE") == "WORK":
            return True
        return False

    def check_if_criminal(self, wanted):
        names = set(doc.name for doc in self.documents)
        return any([name in wanted for name in names])

    def get_mismatch_fields(self):
        fields_name = {"NATION": "nationality", "ID#": "ID number", "NAME": "name",
                       "SEX": "sex", "ISS": "iss", "DOB": "date of birth"}
        all_fields = set(chain(*[doc.parsed.keys() for doc in self.documents]))
        if "EXP" in all_fields:
            all_fields.remove("EXP")
        grouped = {field: set(doc.parsed[field] for doc in self.documents if field in doc.parsed) for field in
                   all_fields}
        return [fields_name[k] for k, v in grouped.items() if len(v) != 1]

    def get_missing_docs(self, required_docs):
        owned_docs = [doc.type for doc in self.documents]
        missing_docs = []
        missing_docs += list(set(required_docs["Entrants"]) - set(owned_docs))
        if self.is_citizen:
            missing_docs += list(set(required_docs["Citizens"]) - set(owned_docs))
        else:
            missing = list(set(required_docs["Foreigners"]) - set(owned_docs))
            if "access permit" in missing and (
                    self.grant_of_asylum.is_present
                    or self.diplomatic_authorization.is_present
            ):
                missing.remove("access permit")
            missing_docs += missing
        if self.is_worker:
            missing_docs += list(set(required_docs["Workers"]) - set(owned_docs))

        return missing_docs

    def get_expired_docs(self):
        return [doc.type for doc in self.documents if doc.is_expired]

    def get_needed_vaccinations(self, vaccinations):
        needed_vaccinations = set()
        needed_vaccinations |= vaccinations["Entrants"]
        if self.is_citizen:
            needed_vaccinations |= vaccinations["Citizens"]
        else:
            needed_vaccinations |= vaccinations["Foreigners"]
        if self.is_worker:
            needed_vaccinations |= vaccinations["Workers"]
        needed_vaccinations |= vaccinations[self.nation]
        return needed_vaccinations

    def has_vaccinations(self, needed_vaccinations):
        if not needed_vaccinations:
            return True
        owned_vaccinations = self.certificate_of_vaccination.parsed.get("VACCINES").split(", ")
        return all([vac in owned_vaccinations for vac in needed_vaccinations])


class Document:

    def __init__(self, raw_document, type):
        self.type = type
        self.parsed = self.parse(raw_document) if raw_document else None

    def parse(self, raw_document):
        return dict(field.split(": ") for field in raw_document.split("\n"))

    @property
    def is_present(self):
        return False if self.parsed is None else True

    @property
    def is_valid(self):
        if not self.parsed:
            return True
        if self.type == "diplomatic authorization":
            return "Arstotzka" in self.parsed.get("ACCESS")
        return True

    @property
    def nation(self):
        return self.parsed.get("NATION") if self.parsed else None

    @property
    def name(self):
        if not self.parsed:
            return None
        name_list = self.parsed.get("NAME").split(", ")
        return f"{name_list[1]} {name_list[0]}"

    @property
    def is_expired(self):
        if not self.parsed or "EXP" not in self.parsed:
            return False
        return datetime(1982, 11, 22) > datetime.strptime(self.parsed.get("EXP"), '%Y.%m.%d')
