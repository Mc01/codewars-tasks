class Inspector:
    saved_data = {}
    country_list = ["Arstotzka", "Antegria", "Impor", "Kolechia", "Obristan", "Republia", "United Federation"]
    rules = {
            "allow": ["Arstotzka"],
            "documents": {
                "workers": [],
                "citizens": {
                    "Arstotzka": [],
                    "Antegria": [],
                    "Impor": [],
                    "Kolechia": [],
                    "Obristan": [],
                    "Republia": [],
                    "United Federation": [],
                },
            },
            "vaccination": {
                "citizens": {
                    "Arstotzka": [],
                    "Antegria": [],
                    "Impor": [],
                    "Kolechia": [],
                    "Obristan": [],
                    "Republia": [],
                    "United Federation": [],
                },
            },
            "wanted_criminal": "",
        }

    class C:
        ARSTOTZKA = "Arstotzka"
        REQUIRE = "require"
        ENTRANTS = "Entrants"
        FOREIGNERS = "Foreigners"
        NO_LONGER = "no longer"
        VACCINATION = "vaccination"
        CITIZENS = "citizens"
        DOCUMENTS = "documents"
        PASSPORT = "passport"
        NATION = "NATION"
        ACCESS_PERMIT = "access_permit"
        DIPLOMATIC_AUTHORIZATION = "diplomatic_authorization"
        GOF = "grant_of_asylum"

    def init_rules(self):
        self.rules["wanted_criminal"] = ""

    def receive_bulletin(self, bulletin):
        self.init_rules()
        rules = bulletin.strip().split("\n")
        for rule in rules:
            if rule.startswith("Allow"):
                self.allow_citizens(rule)
            elif rule.startswith("Deny"):
                self.deny_citizens(rule)
            elif rule.startswith("Wanted"):
                self.wanted_criminal(rule)
            elif rule.endswith(self.C.VACCINATION):
                self.vaccination(rule)
            else:
                self.documents(rule)

    def united_federation_handler(self, countries):
        if "United" in countries:
            countries.remove("United")
            countries.remove("Federation")
            countries.append("United Federation")
        return countries

    def allow_citizens(self, rule):
        countries = [c.strip(",") for c in rule.split()[3:]]
        countries = self.united_federation_handler(countries)
        for country in countries:
            if country not in self.rules["allow"]:
                self.rules["allow"].append(country)

    def deny_citizens(self, rule):
        countries = [c.strip(",") for c in rule.split()[3:]]
        countries = self.united_federation_handler(countries)
        for country in countries:
            self.rules["allow"].remove(country)

    def wanted_criminal(self, rule):
        criminal = rule.split(":")[1].strip().split()
        self.rules["wanted_criminal"] = f"{criminal[1]}, {criminal[0]}"

    def vaccination(self, rule):
        vaccine_for = rule[rule.index(self.C.REQUIRE) + len(self.C.REQUIRE) + 1: rule.index(self.C.VACCINATION)].strip()
        if self.C.ENTRANTS in rule:
            countries = self.country_list
        elif self.C.FOREIGNERS in rule:
            countries = [c for c in self.country_list if c != self.C.ARSTOTZKA]
        else:
            if self.C.NO_LONGER in rule:
                countries = rule[12:rule.index(self.C.NO_LONGER)]
            else:
                countries = rule[12:rule.index(self.C.REQUIRE)]
            countries = [c.strip().strip(",") for c in countries.split()]
            countries = self.united_federation_handler(countries)
        if self.C.NO_LONGER in rule:
            for country in countries:
                try:
                    self.rules[self.C.VACCINATION][self.C.CITIZENS][country].remove(vaccine_for)
                except ValueError:
                    pass
        else:
            for country in countries:
                self.rules[self.C.VACCINATION][self.C.CITIZENS][country].append(vaccine_for)

    def documents(self, rule):
        rule = rule.split()
        document = "_".join(rule[rule.index(self.C.REQUIRE) + 1:]).strip()
        if "Workers" in rule:
            self.rules[self.C.DOCUMENTS]["workers"].append(document)
            return
        elif self.C.FOREIGNERS in rule:
            countries = [c for c in self.country_list if c != self.C.ARSTOTZKA]
        elif self.C.CITIZENS.capitalize() in rule:
            countries = [c.strip() for c in rule[2: rule.index(self.C.REQUIRE)]]
        elif self.C.ENTRANTS in rule:
            countries = self.country_list
        for country in countries:
            self.rules[self.C.DOCUMENTS][self.C.CITIZENS][country].append(document)

    def inspect(self, documents):
        documents_data = self.parse_data(documents)
        self.read_data(documents_data)
        is_wanted_criminal = self.is_wanted_criminal()
        if is_wanted_criminal:
            return is_wanted_criminal
        conflict_data = self.check_data_conflict(documents_data)
        if conflict_data:
            return conflict_data
        if self.documents_handler(documents_data):
            return self.documents_handler(documents_data)
        if self.vaccination_handler(documents_data):
            return self.vaccination_handler(documents_data)
        if self.saved_data[self.C.NATION] not in self.rules["allow"]:
            return "Entry denied: citizen of banned nation."
        if self.saved_data[self.C.NATION] == self.C.ARSTOTZKA:
            return "Glory to Arstotzka."
        else:
            return "Cause no trouble."

    def is_wanted_criminal(self):
        message = ""
        try:
            if self.saved_data["NAME"] == self.rules["wanted_criminal"]:
                message = "Detainment: Entrant is a wanted criminal."
        except KeyError:
            pass
        return message

    def parse_data(self, documents):
        documents_data = {}
        for document, content in documents.items():
            data = content.split("\n")
            data_split = [c.split(":") for c in data]
            data_dict = {}
            for d in data_split:
                data_dict[d[0].strip()] = d[1].strip()
            documents_data[document] = data_dict
        return documents_data

    def read_data(self, documents_data):
        self.saved_data = {}
        for document, data in documents_data.items():
            for d, v in data.items():
                if d in self.saved_data.keys():
                    pass
                else:
                    self.saved_data[d] = v

    def check_data_conflict(self, documents_data):
        saved_data = {}
        for document, data in documents_data.items():
            for d, v in data.items():
                if d in saved_data.keys():
                    if saved_data[d] != v:
                        if d == "ID#":
                            d = "ID number"
                        elif d == self.C.NATION:
                            d = "nationality"
                        elif d == "EXP":
                            continue
                        elif d == "DOB":
                            d = "date of birth"
                        else:
                            d = d.lower()
                        return f"Detainment: {d} mismatch."
                else:
                    saved_data[d] = v

    def document_expired(self, exp):
        if not exp:
            return False
        date = exp.split(".")
        int_date = []
        # turn string date into ints date (without trailing 0's)
        for d in date:
            if d.startswith('0'):
                d = d[1]
            int_date.append(int(d))
        # check if exp is earlier than 1982.11.22
        if int_date[0] < 1982 or int_date[0] == 1982 and int_date[1] < 11 or int_date[0] == 1982 and int_date[1] == 11 and \
                int_date[2] < 22:
            return True
        return False

    def missing_workers_documents(self, documents_data):
        if self.saved_data.get("PURPOSE", "") == "WORK":
            if not all(map(lambda x: x in documents_data.keys(), self.rules[self.C.DOCUMENTS]["workers"])):
                return ", ".join([d for d in self.rules[self.C.DOCUMENTS]["workers"] if d not in documents_data.keys()])
        return ""

    def missing_required_documents(self, documents_data, country):
        missing_documents = [
            d for d in self.rules[self.C.DOCUMENTS][self.C.CITIZENS][country] if d not in documents_data.keys()
        ]
        if self.C.ACCESS_PERMIT in missing_documents:
            if self.C.DIPLOMATIC_AUTHORIZATION in documents_data.keys() or self.C.GOF in documents_data.keys():
                missing_documents.remove(self.C.ACCESS_PERMIT)
        return missing_documents[0] if missing_documents else ""

    def diplomatic_authorization_handler(self, documents_data):
        diplomatic_auth = documents_data.get(self.C.DIPLOMATIC_AUTHORIZATION, "")
        if diplomatic_auth:
            expired = self.document_expired(diplomatic_auth.get("EXP", ""))
            if expired:
                return "Entry denied: diplomatic authorization expired."
            diplomatic_country = [c.strip() for c in diplomatic_auth["ACCESS"].split(",")]
            if self.C.ARSTOTZKA not in diplomatic_country:
                return "Entry denied: invalid diplomatic authorization."

    def documents_handler(self, documents_data):
        diplomatic_auth = self.diplomatic_authorization_handler(documents_data)
        if diplomatic_auth:
            return diplomatic_auth

        error = ""
        exp_document = ""
        missing_document = ""

        if documents_data.get(self.C.PASSPORT, False) and self.document_expired(documents_data[self.C.PASSPORT]["EXP"]):
            exp_document = self.C.PASSPORT
        if documents_data.get(self.C.GOF, False) and self.document_expired(documents_data[self.C.GOF]["EXP"]):
            exp_document = self.C.GOF.replace("_", ' ')
        if documents_data.get(self.C.ACCESS_PERMIT, False) and self.document_expired(documents_data[self.C.ACCESS_PERMIT]["EXP"]):
            exp_document = self.C.ACCESS_PERMIT.replace("_", ' ')
        if exp_document:
            error = f"Entry denied: {exp_document} expired."

        work_documents = self.missing_workers_documents(documents_data)
        if work_documents:
            missing_document = work_documents.replace('_', ' ')

        try:
            missing_documents = self.missing_required_documents(documents_data, self.saved_data[self.C.NATION])
            if missing_documents:
                missing_document = missing_documents.replace('_', ' ')
        except KeyError:
            missing_document = self.C.PASSPORT

        if missing_document:
            error = f"Entry denied: missing required {missing_document}."

        return error

    def vaccination_handler(self, documents_data):
        country = self.saved_data[self.C.NATION]
        vaccinations = documents_data.get("certificate_of_vaccination", "")
        required_vaccinations = self.rules[self.C.VACCINATION][self.C.CITIZENS][country]
        if required_vaccinations:
            if not vaccinations:
                return "Entry denied: missing required certificate of vaccination."
            else:
                vaccinations = [c.strip().lower() for c in vaccinations["VACCINES"].split(", ")]
            for vaccine in required_vaccinations:
                if vaccine.lower() not in vaccinations:
                    return "Entry denied: missing required vaccination."
