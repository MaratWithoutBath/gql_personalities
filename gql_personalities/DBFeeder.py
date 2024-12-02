from functools import cache
from gql_personalities.DBDefinitions import (
    RankModel,
    StudyModel,
    CertificateModel,
    MedalModel,
    WorkHistoryModel,
    RelatedDocModel,
    RankTypeModel,
    CertificateTypeModel,
    MedalTypeModel,
    MedalTypeGroupModel,
    CertificateTypeGroupModel,
)

from functools import cache
from sqlalchemy.future import select


def singleCall(asyncFunc):
    """Dekorator, ktery dovoli, aby dekorovana funkce byla volana (vycislena) jen jednou. Navratova hodnota je zapamatovana a pri dalsich volanich vracena.
    Dekorovana funkce je asynchronni.
    """
    resultCache = {}

    async def result():
        if resultCache.get("result", None) is None:
            resultCache["result"] = await asyncFunc()
        return resultCache["result"]

    return result


###########################################################################################################################
#
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################
def get_demodata(asyncSessionMaker):
    pass


@cache
def determineRankType():
    rankTypes = [
        # mužstvo
        {
            "name": "vojín (voj.)",
            "name_en": "Private (PVT)",
            "id": "de5e6ae8-902c-4b06-aa8e-8fbca99026f3",
        },
        {
            "name": "svobodník (svob.)",
            "name_en": "Private First Class (PFC)",
            "id": "f3038058-e1fa-4f7c-9e50-7b1d99998d37",
        },
        # poddůstojníci
        {
            "name": "desátník (des.)",
            "name_en": "Corporal (CPL)",
            "id": "a3cdae76-1c7d-409c-8bed-9e922c066bce",
        },
        {
            "name": "četař (čet.)",
            "name_en": "Sergeant (SGT)",
            "id": "a17e81a6-776b-4883-a04d-cbd4f07ad095",
        },
        {
            "name": "rotný (rtn.)",
            "name_en": "Staff Sergeant (SSG)",
            "id": "a9043224-9c3b-4562-a329-997fba9237d0",
        },
        # praporčíci
        {
            "name": "rotmistr (rtm.)",
            "name_en": "Sergeant First Class (SFC)",
            "id": "72294ac5-1823-4164-9805-60a0aaa39296",
        },
        {
            "name": "nadrotmistr (nrtm.)",
            "name_en": "Master Sergeant (MSG)",
            "id": "453dff9e-fab2-41d0-8bef-ca76c78e79c8",
        },
        {
            "name": "praporčík (prap.)",
            "name_en": "Chief Warrant Officer (CW2)",
            "id": "6a324f4a-2162-4fe7-a47c-8be1f3c9452b",
        },
        {
            "name": "nadpraporčík (nprap.)",
            "name_en": "Chief Warrant Officer (CW3)",
            "id": "34cfd57e-6a09-4423-8025-b44d6dbce774",
        },
        {
            "name": "štábní praporčík (št. prap.)",
            "name_en": "Master Warrant Officer (MW4)",
            "id": "841fa09f-625e-49b4-8872-05c43ce197cf",
        },
        # nižší důstojníci
        {
            "name": "poručík (por.)",
            "name_en": "Lieutenant (LT)",
            "id": "3914ab9f-78bc-45ac-bb2d-59ee921f3a19",
        },
        {
            "name": "nadporučík (npor.)",
            "name_en": "First Lieutenant (1LT)",
            "id": "437fa94e-8442-4667-af9a-8327afef9ffa",
        },
        {
            "name": "kapitán (ktp.)",
            "name_en": "Captain (CPT)",
            "id": "a8ce2853-26ec-4e10-8bbe-899cc296a35f",
        },
        # vyšší důstojníci
        {
            "name": "major (mjr.)",
            "name_en": "Major (MAJ)",
            "id": "587cd381-aeec-4367-91f3-8849f900848a",
        },
        {
            "name": "podplukovník (pplk.)",
            "name_en": "Lieutenant Colonel (LTC)",
            "id": "46a7325f-9b9e-4e80-9f17-670bd9151229",
        },
        {
            "name": "plukovník (plk.)",
            "name_en": "Colonel (COL)",
            "id": "824533e5-eba7-45f7-80f6-e2466529e73c",
        },
        # generálové
        {
            "name": "brigádní generál (brig.gen.)",
            "name_en": "Brigadier General (BG)",
            "id": "9eb8d8f4-a87c-447d-aaee-c0a15cd6fbce",
        },
        {
            "name": "generálmajor (genmjr.)",
            "name_en": "Major General (MG)",
            "id": "d65a0d25-dc39-46fa-a107-a684c9724c5e",
        },
        {
            "name": "generálporučík (genpor.)",
            "name_en": "Lieutenant General (LTG)",
            "id": "41f0772d-738a-492d-93c1-96c9cdb5d597",
        },
        {
            "name": "armádní generál (arm.gen.)",
            "name_en": "General of the Army (GA)",
            "id": "9234d06c-e811-4016-8ee5-f6975b4048a4",
        },
    ]
    return rankTypes


@cache
def determineStudyPlace():
    studyPlaces = [
        # veřejné VŠ
        {
            "name": "Akademie múzických umění v Praze (AMU)",
            "name_en": "Academy of Performing Arts in Prague (AMU)",
            "id": "88556487-cbf0-46ec-889a-71720b93ea37",
        },
        {
            "name": "Akademie výtvarných umění v Praze (AVU)",
            "name_en": "Academy of Fine Arts, Prague (AVU)",
            "id": "2b84e0ab-fe7b-4104-8601-4553caa0f83d",
        },
        {
            "name": "Česká zemědělská univerzita v Praze (ČZU)",
            "name_en": "Czech University of Life Sciences Prague (CZU)",
            "id": "db8a49b1-5c1d-4681-b964-8a32db02c0a0",
        },
        {
            "name": "České vysoké učení technické v Praze (ČVUT)",
            "name_en": "Czech Technical University in Prague (CTU)",
            "id": "635135dc-f119-4a1c-88dd-f5fc8395f501",
        },
        {
            "name": "Janáčkova akademie múzických umění (JAMU)",
            "name_en": "Janáček Academy of Music and Performing Arts (JAMU)",
            "id": "10f191ae-284f-44ed-90ce-29b3cdadc070",
        },
        {
            "name": "Jihočeská univerzita v Českých Budějovicích (JU)",
            "name_en": "University of South Bohemia in České Budějovice (JU)",
            "id": "4bdb5ce2-ad70-4c2b-9ba5-516d3df3fb3b",
        },
        {
            "name": "Masarykova univerzita (MU)",
            "name_en": "Masaryk University (MU)",
            "id": "782e1ee1-9f15-46bd-8e74-3e546c9afd37",
        },
        {
            "name": "Mendelova univerzita v Brně (MENDELU)",
            "name_en": "Mendel University in Brno (MENDELU)",
            "id": "258f8f4e-a7f2-418f-bdd9-cfbbf8f38099",
        },
        {
            "name": "Ostravská univerzita (OU)",
            "name_en": "University of Ostrava (OU)",
            "id": "0a9d1130-5bc2-4de2-92a1-8c1be055e707",
        },
        {
            "name": "Slezská univerzita v Opavě (SU)",
            "name_en": "Silesian University in Opava (SU)",
            "id": "d51f4119-0918-4427-ad36-27818dc49bc3",
        },
        {
            "name": "Technická univerzita v Liberci (TUL)",
            "name_en": "Technical University of Liberec (TUL)",
            "id": "6a059f6f-16d9-4cb8-94ac-084d6165a345",
        },
        {
            "name": "Univerzita Hradec Králové (UHK)",
            "name_en": "University of Hradec Králové (UHK)",
            "id": "b8491178-53fd-4b6b-84cb-5cb8d859d489",
        },
        {
            "name": "Univerzita Jana Evangelisty Purkyně v Ústí nad Labem (UJEP)",
            "name_en": "Jan Evangelista Purkyně University in Ústí nad Labem (UJEP)",
            "id": "236a2e9f-010c-443c-84e7-52973e8094fd",
        },
        {
            "name": "Univerzita Karlova (UK)",
            "name_en": "Charles University (UK)",
            "id": "94115ab6-0443-473c-b66e-0c6d29572c89",
        },
        {
            "name": "Univerzita Palackého v Olomouci (UP)",
            "name_en": "Palacký University Olomouc (UP)",
            "id": "e7e69091-982b-4f0c-80ad-a5bb074ef5bd",
        },
        {
            "name": "Univerzita Pardubice (UPCE)",
            "name_en": "University of Pardubice (UPCE)",
            "id": "c2886fd7-c3df-470a-9abc-25617e838453",
        },
        {
            "name": "Univerzita Tomáše Bati ve Zlíně (UTB, zkrácený n��zev: UTB ve Zlíně)",
            "name_en": "Tomas Bata University in Zlín (UTB)",
            "id": "533ed300-f78e-4f8e-abb1-7b039ff63438",
        },
        {
            "name": "Veterinární univerzita Brno (VETUNI)",
            "name_en": "University of Veterinary Sciences Brno (VETUNI)",
            "id": "a8f84591-d060-4763-8b95-890f5e9e9dc1",
        },
        {
            "name": "Vysoká škola báňská - Technická univerzita Ostrava (VŠB-TUO, zkrácený název: VŠB - Technická univerzita Ostrava)",
            "name_en": "VSB - Technical University of Ostrava (VŠB-TUO)",
            "id": "c63b55eb-c6a0-4302-aa27-3ff8f082cc35",
        },
        {
            "name": "Vysoká škola ekonomická v Praze (VŠE)",
            "name_en": "University of Economics, Prague (VŠE)",
            "id": "b38fc480-98bd-4a9c-8b3f-58a0eff3506c",
        },
        {
            "name": "Vysoká škola chemicko-technologická v Praze (VŠCHT Praha)",
            "name_en": "University of Chemistry and Technology, Prague (UCT Prague)",
            "id": "cce2633e-a059-4b72-92d3-52652f6bc07c",
        },
        {
            "name": "Vysoká škola polytechnická Jihlava (VŠPJ či VŠP Jihlava)",
            "name_en": "College of Polytechnics Jihlava (VŠPJ)",
            "id": "9f128a38-6405-4435-a4f2-be7050755a2e",
        },
        {
            "name": "Vysoká škola technická a ekonomická v Českých Budějovicích (VŠTE)",
            "name_en": "Institute of Technology and Business in České Budějovice (VŠTE)",
            "id": "8e1c2c35-50fd-40b6-9cd9-cad795f20dbf",
        },
        {
            "name": "Vysoká škola uměleckoprůmyslová v Praze (UMPRUM)",
            "name_en": "Academy of Arts, Architecture and Design in Prague (UMPRUM)",
            "id": "4c807453-dd9d-455f-a334-f4007f2bbefc",
        },
        {
            "name": "Vysoké učení technické v Brně (VUT)",
            "name_en": "Brno University of Technology (VUT)",
            "id": "4bb8f25a-79e5-493a-9b52-dbb2855537b8",
        },
        {
            "name": "Západočeská univerzita v Plzni (ZČU)",
            "name_en": "University of West Bohemia (UWB)",
            "id": "fbad1416-2f46-4671-927c-100be0914dcb",
        },
        # státní VŠ
        {
            "name": "Policejní akademie České republiky v Praze (POLAC)",
            "name_en": "Police Academy of the Czech Republic in Prague (POLAC)",
            "id": "31a7d00f-de73-4d70-9e02-a139d0a3096c",
        },
        {
            "name": "Univerzita obrany (UNOB)",
            "name_en": "University of Defence (UNOB)",
            "id": "3da845f7-a616-4ed9-98d8-329fac7fae81",
        },
    ]
    return studyPlaces


@cache
def determineStudyProgram():
    studyPrograms = [
        {
            "name": "bakalářský",
            "name_en": "bachelor",
            "id": "00602448-9d42-4af3-95fd-20fd6a551771",
        },
        {
            "name": "magisterský",
            "name_en": "master",
            "id": "f0e17944-e7d8-434a-9b36-b70cf6f0fac5",
        },
        {
            "name": "doktorský",
            "name_en": "doctoral",
            "id": "0ea55a54-1fa5-43ce-b2e6-67ebf57c9671",
        },
    ]
    return studyPrograms


@cache
def determineCertificateType():
    certificateTypes = [
        # jazykové
        {
            "name": "STANAG English",
            "name_en": "STANAG English",
            "id": "34a29ef9-b9a9-4d62-9270-e16504d47fa9",
        },
        {
            "name": "PET",
            "name_en": "Preliminary English Test",
            "id": "8f212ce5-9dfb-4595-a3c0-8c819a6af424",
        },
        {
            "name": "CAE",
            "name_en": "Certificate in Advanced English",
            "id": "9ab4186a-1a23-4632-8dc5-8b6c7012c024",
        },
        {
            "name": "FCE",
            "name_en": "First Certificate in English",
            "id": "228ad8c0-8ef9-48ec-9ad1-fa9e9c123d50",
        },
        {
            "name": "CPE",
            "name_en": "Certificate of Proficiency in English",
            "id": "6bc6e441-511c-403b-a754-50b8ccd9bfc3",
        },
        {
            "name": "TOEFL",
            "name_en": "Test of English as a Foreign Language",
            "id": "87408450-922a-4f2e-84c5-3fd25255d738",
        },
        {
            "name": "IELTS",
            "name_en": "International English Language Testing System",
            "id": "6c2b6c8f-812f-4372-bd10-1a395c7faf4b",
        },
        {
            "name": "TOEIC",
            "name_en": "Test of English for International Communication",
            "id": "9afba032-ed69-4d5c-bc73-805ae6eb156b",
        },
        {
            "name": "STANAG German",
            "name_en": "STANAG German",
            "id": "6b381e55-528e-4d13-85a2-963f0710e962",
        },
        {
            "name": "ZDaF",
            "name_en": "Zertifikat Deutsch als Fremdsprache",
            "id": "3139c891-e59e-4345-9f87-e7e93b22d686",
        },
        {
            "name": "ZMF",
            "name_en": "Zentrale Mittelstufenprüfung",
            "id": "e1bd3e67-363d-4e46-b616-89f22d64468f",
        },
        {
            "name": "KDS",
            "name_en": "Kleines Deutsches Sprachdiplom",
            "id": "2f682b71-a772-4b55-8d30-2100844f5b53",
        },
        {
            "name": "GDS",
            "name_en": "Großes Deutsches Sprachdiplom",
            "id": "37147540-e3ac-49b8-8ae0-2121f417b92f",
        },
        {
            "name": "PNDS",
            "name_en": "Prüfung Wirtschaftsdeutsch",
            "id": "22bc21ab-5a87-448e-a0f4-74d0136678df",
        },
        {
            "name": "DSH",
            "name_en": "Deutsche Sprachprüfung für den Hochschulzugang",
            "id": "62c41d70-2757-4378-a7c0-e90bdb57a051",
        },
        {
            "name": "STANAG French",
            "name_en": "STANAG French",
            "id": "9c615240-f23e-4b6b-abf6-b10327742a1f",
        },
        {
            "name": "DELF",
            "name_en": "Diplôme d'études en langue française",
            "id": "b6cedca1-38c7-470c-8688-caab5a102aa8",
        },
        {
            "name": "DALF",
            "name_en": "Diplôme approfondi de langue française",
            "id": "c1177873-7ef0-4e59-b24c-803d430d7541",
        },
        {
            "name": "STANAG Spanish",
            "name_en": "STANAG Spanish",
            "id": "62aeac61-0c0a-4962-af06-9b32c375ad0b",
        },
        {
            "name": "DELE",
            "name_en": "Diplomas de Español como Lengua Extranjera",
            "id": "c6275399-7302-49ca-837d-811f9238a5dc",
        },
        {
            "name": "STANAG Italian",
            "name_en": "STANAG Italian",
            "id": "49d71536-e9fb-4110-8639-a07ca653e6fb",
        },
        {
            "name": "CILS",
            "name_en": "Certificazione di Italiano come Lingua Straniera",
            "id": "e1a2c256-8e11-4a94-8bfb-4d564c4a892f",
        },
        {
            "name": "STANAG Russian",
            "name_en": "STANAG Russian",
            "id": "43089ad0-722c-4f13-9a89-c809b2e3ecee",
        },
        {
            "name": "STANAG Polish",
            "name_en": "STANAG Polish",
            "id": "634fe5b9-8494-4586-b67a-191157c0ed60",
        },
    ]
    return certificateTypes


def determineCertificateTypeGroup():
    certificateTypeGroups = [
        {
            "name": "jazykové",
            "name_en": "language",
            "id": "db9ba8c3-3d6e-4190-bfe7-d401586dd282",
        },
        {
            "name": "vědecké",
            "name_en": "science",
            "id": "bc988cb6-38a7-45a1-97ec-d1e220621355",
        },
        {
            "name": "sportovní",
            "name_en": "sport",
            "id": "3f1351ca-0624-43bb-9c93-23e6478fb1c1",
        },
        {
            "name": "pracovní",
            "name_en": "work",
            "id": "e4713dd6-69e6-4d35-964b-1bca141899eb",
        },
    ]
    return certificateTypeGroups


@cache
def determineMedalType():
    medalTypes = [
        # Řády a vyznamenání České republiky
        {
            "name": "Řád Bílého lva",
            "name_en": "Order of the White Lion",
            "id": "cf4c274c-6cf1-11ed-a1eb-0242ac120002",
        },
        {
            "name": "Řád Tomáše Garrigua Masaryka",
            "name_en": "Order of Tomáš Garrigue Masaryk",
            "id": "cf4c2ef4-6cf1-11ed-a1eb-0242ac120002",
        },
        {
            "name": "Medaile za hrdinství",
            "name_en": "Medal for Heroism",
            "id": "cf4c3052-6cf1-11ed-a1eb-0242ac120002",
        },
        {
            "name": "Medaile za zásluhy",
            "name_en": "Medal of Merit",
            "id": "cf4c3188-6cf1-11ed-a1eb-0242ac120002",
        },
        # Vojenské resortní vyznamenání
        {
            "name": "Záslužný kříž",
            "name_en": "Cross of Merit",
            "id": "1ebfcc2a-6cf2-11ed-a1eb-0242ac120002",
        },
        {
            "name": "Medaile za zranění",
            "name_en": "Wound Medal",
            "id": "1ebfcf2c-6cf2-11ed-a1eb-0242ac120002",
        },
        {
            "name": "Medaile ministra obrany za službu v zahraničí",
            "name_en": "Ministry of Defence Medal for Service Abroad",
            "id": "1ebfd076-6cf2-11ed-a1eb-0242ac120002",
        },
        {
            "name": "Medaile Armády České republiky",
            "name_en": "Medal of the Army of the Czech Republic",
            "id": "1ebfd198-6cf2-11ed-a1eb-0242ac120002",
        },
        # Čestné odznaky
        {
            "name": "Čestný pamětní odznak za službu míru",
            "name_en": "Honorary Commemorative Medal for Service in Peace",
            "id": "97edb3fc-a4d2-4295-a8ca-e7e97fba87e1",
        },
        # ... continue adding "name_en" for each entry
    ]
    return medalTypes


@cache
def determineMedalTypeGroup():
    medalTypeGroup = [
        {
            "name": "Řády a vyznamenání České republiky",
            "name_en": "Orders and Decorations of the Czech Republic",
            "id": "0747704c-d6f9-461c-9b2f-4b9681bd50ed",
        },
        {
            "name": "Vojenské resortní vyznamenání",
            "name_en": "Military Departmental Decorations",
            "id": "2c34f055-d2fa-4eb1-a29a-ed28a2277e6c",
        },
        {
            "name": "Čestné odznaky",
            "name_en": "Honorary Badges",
            "id": "6299630e-4d27-44a9-a844-53831add33ca",
        },
    ]
    return medalTypeGroup


@cache
def determineWorkHistoryPosition():
    workHistoryPosition = [
        {"name": "manažer", "name_en": "manager", "id": "3406c765-8454-4f3a-b3bb-76b74582be2e"},
        {"name": "účetní", "name_en": "accountant", "id": "d9a50a22-edf4-4264-98f0-5a9eced115c4"},
        {"name": "úředník", "name_en": "clerk", "id": "203cb4d1-6d61-4dfd-8662-d7a352db739c"},
        {"name": "konzultant", "name_en": "consultant", "id": "7925ca15-acd5-4af9-9731-2884c8225081"},
        {"name": "asistent", "name_en": "assistant", "id": "fd8ea6b7-4706-4537-8569-5dc8040519f8"},
        {"name": "právní zástupce", "name_en": "legal representative", "id": "242a84a8-f754-4136-b322-e20b0382dff4"},
        {"name": "administrátor", "name_en": "administrator", "id": "cc3f7106-f38c-48ee-89d9-d1a420e45df5"},
        {"name": "pokladní", "name_en": "cashier", "id": "950d3466-af5b-4a59-b91f-14514bf693d0"},
        {"name": "uklízeč", "name_en": "cleaner", "id": "c24dba24-b636-46d4-b0b2-2dc03e6af933"},
        {"name": "operátor", "name_en": "operator", "id": "02addd4f-ee6f-4141-bbc7-5a6ca9bc8647"},
        {"name": "analytik", "name_en": "analyst", "id": "aaea9b89-dbed-42a2-8f22-737ce913f803"},
        {"name": "správce", "name_en": "custodian", "id": "87897e28-c92d-49be-8878-e9c39c9b8a5a"},
        {"name": "technická podpora", "name_en": "technical support", "id": "f60e38af-069b-4f8e-8cc9-b6cd077a7cee"},
        {"name": "řidič", "name_en": "driver", "id": "c11f1606-bdd2-4973-89ca-1489e8249c0f"},
        {"name": "specialista", "name_en": "specialist", "id": "8b18a1a2-f759-4441-a18b-0bee41e71519"},
    ]
    return workHistoryPosition


@cache
def determineWorkHistory():
    workHistories = [
        {
            "name": "TechCorp",
            "ico": "12345678",
            "id": "a1b2c3d4-e5f6-7a8b-9c0d-e1f2a3b4c5d6",
        },
        {
            "name": "BizSolutions",
            "ico": "87654321",
            "id": "d6c5b4a3-2f1e-0d9c-8b7a-6e5f4d3c2b1a",
        },
    ]
    return workHistories

@cache
def determineRelatedDocs():
    relatedDocs = [
        {
            "name": "Dokument A",
            "id": "f1e2d3c4-b5a6-7c8d-9e0f-1a2b3c4d5e6f",
        },
        {
            "name": "Dokument B",
            "id": "6e5d4c3b-2a1f-0e9d-8c7b-6a5f4d3c2b1a",
        },
    ]
    return relatedDocs


# from gql_personalities.DBDefinitions import

import asyncio

import os
import json
from uoishelpers.feeders import ImportModels
import datetime


def get_demodata():
    def datetime_parser(json_dict):
        for (key, value) in json_dict.items():
            if key in ["startdate", "enddate", "lastchange", "created"]:
                if value is None:
                    dateValueWOtzinfo = None
                else:
                    try:
                        dateValue = datetime.datetime.fromisoformat(value)
                        dateValueWOtzinfo = dateValue.replace(tzinfo=None)
                    except:
                        print("jsonconvert Error", key, value, flush=True)
                        dateValueWOtzinfo = None

                json_dict[key] = dateValueWOtzinfo
        return json_dict

    with open("./systemdata.json", "r", encoding="utf-8") as f:
        jsonData = json.load(f, object_hook=datetime_parser)

    return jsonData


async def initDB(asyncSessionMaker):

    defaultNoDemo = os.environ.get("DEMO", None) not in ["True", "true", "1"]
    if defaultNoDemo:
        dbModels = [
            CertificateTypeGroupModel,
            CertificateTypeModel,
            MedalTypeGroupModel,
            MedalTypeModel,
            RankTypeModel,
        ]
    else:
        dbModels = [
            CertificateTypeGroupModel,
            CertificateTypeModel,
            MedalTypeGroupModel,
            MedalTypeModel,
            RankTypeModel,
            RankModel,
            StudyModel,
            CertificateModel,
            MedalModel,
            WorkHistoryModel,
            RelatedDocModel,
        ]

    jsonData = get_demodata()
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    print("DB initialized", flush=True)
    pass
