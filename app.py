import json

# Load the JSON payload
with open("payload.json", 'r') as file:
    content = json.load(file)

# Extract data from JSON
RESORT = content["Resort"]
GROUPS = {g["Code"]: g for g in content["options"]["Groups"]}
IDENTIFIER = {i["No"]: i for i in content["options"]["Identifier"]}
TAXES = {i["No"]: i for i in content["options"]["Taxes"]}
CATEGORIES = {c["Code"]: c for c in content["options"]["Category"]}
SEQUENCES = content["Sequences"]

def create_tc_subgroup(sequence, category):
    _group = GROUPS[category["DefaultGroup"] or sequence["Group"]]
    _sequence = int(str(category["Seq"])[:1])
    _subgroup = {
        "Seq": int(f"{sequence["Sequence"]}{_sequence}"),
        "Code": f"{sequence["Sequence"]}{category['Code']}",
        "Description": f"{sequence['Name']} {category['Description']}",
        "Group": _group["Code"],
        "Type": _group["Type"]
    }
    return _subgroup

def create_tc_code(sequence, tc_subgroup, groupCode, category, identifier, itemizer, Description):
    _itemCode = itemizer + category["Seq"]
    _trxCodeNo = '{:02}'.format(_itemCode)
    _trxDescription = f"{sequence["Name"]}{f" {identifier["Name"]}" if identifier["Name"] else ""}{f" {Description}" if Description else ""}{f" {category["Abbr"]}" if category["Abbr"] else ""}"

    _trxCode = {
        "Code": f'{sequence["Sequence"]}{identifier["Seq"]}{_trxCodeNo}',
        "Description": _trxDescription,
        "SubGroup": tc_subgroup["Code"],
        "Group": groupCode,
        "IsRevenue": category["IsRevenue"],
        "IsManual": category["IsManual"],
        "IsCash": category["IsCash"],
        "IsDeposit": category["IsDeposit"],
        "IsAr": category["IsAr"],
        "IsPaid": category["IsPaid"],
        "Type": tc_subgroup["Type"],
        "Tax" : category["Tax"] if category["Tax"] else ""
    }

    return _trxCode

def create_categories(seq):
    _categories = []
    for c in seq["Categories"]:
        category = CATEGORIES[c["Code"]]
        category["Role"] = c["Role"]
        if c["Role"] == "generate" and category["Tax"]:
            category["Generate"] = TAXES.get(category["Tax"])
        _categories.append(category)

    return _categories

# Process sequences to generate transaction groups and codes
for seq in SEQUENCES:
    #categories attached to the sequences
    _categories = create_categories(seq)

    #list of itemizers attached to the sequence
    _itemizers = seq["Itemizers"]

    #list of Identifiers attached to the sequence
    _identifiers = seq["Identifier"]

    #get Generates 
    #_generates = [x for  x in _categories if x["Role"] == "generate"]
    #print(_generates)

    for category in _categories:
        #for each category create a associated subgroup for it 00AA format
        _tc_subgroup = create_tc_subgroup(seq, category)
        print(_tc_subgroup)

        for i in _identifiers:
            identifier = IDENTIFIER[i]
            role = category["Role"]
            taxes = {}

            if role == "multiply":
                for itemizer in _itemizers:
                    _tc_code = create_tc_code(seq, _tc_subgroup, _tc_subgroup["Group"], category, identifier, itemizer["Itemizer"], itemizer["Description"])
                    print(_tc_code)
            elif role == "generate":
                _tc_code = create_tc_code(seq, _tc_subgroup,category["DefaultGroup"], category, identifier, 0, category["Description"])
                print(_tc_code)
            else:
                _tc_code = create_tc_code(seq, _tc_subgroup,category["DefaultGroup"], category, identifier, 0, category["Description"])
                print(_tc_code)