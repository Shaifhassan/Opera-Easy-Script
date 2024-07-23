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

def create_tc_group(sequence, category):
    _group = GROUPS[sequence["Group"]]
    _sequence = int(str(category["Seq"])[:1])
    _subgroup = {
        "Seq": int(f"{sequence["Sequence"]}{_sequence}"),
        "Code": f"{sequence}{category['Code']}",
        "Description": f"{sequence['Name']} {category['Description']}",
        "Group": _group["Code"],
        "Type": _group["Type"]
    }
    return _subgroup

def create_tc_code(sequence, tc_subgroup, category, identifier, itemizer, Description):
    _itemCode = itemizer + category["Seq"]
    _trxCodeNo = '{:02}'.format(_itemCode)
    _trxDescription = f"{sequence["Name"]}{f" {identifier["Name"]}" if identifier["Name"] else ""}{f" {Description}" if Description else ""}{f" {category["Abbr"]}" if category["Abbr"] else ""}"

    _trxCode = {
        "Code": f'{sequence["Sequence"]}{identifier["Seq"]}{_trxCodeNo}',
        "Description": _trxDescription,
        "SubGroup": tc_subgroup["Code"],
        "Group": tc_subgroup["Group"],
        "IsRevenue": category["IsRevenue"],
        "IsManual": category["IsManual"],
        "IsCash": category["IsCash"],
        "IsDeposit": category["IsDeposit"],
        "IsAr": category["IsAr"],
        "IsPaid": category["IsPaid"],
        "Type": tc_subgroup["Type"]
    }

    return _trxCode

def create_categories(seq):
    _categories = []
    for c in seq["Multiplier"]:
        category = CATEGORIES[c]
        category["Source"] = "Multiplier"
        _categories.append(category)
    
    for c in seq["Gen"]:
        category = CATEGORIES[c]
        category["Source"] = "Gen"
        category["Generate"] = TAXES.get(category["Tax"])
        _categories.append(category)

    return _categories

# Process sequences to generate transaction groups and codes
for seq in SEQUENCES:
    _categories = create_categories(seq)
    _itemizers = seq["Itemizers"]
    _identifiers = seq["Identifier"]

    for category in _categories:
        _tc_subgroup = create_tc_group(seq, category)
        
        for i in _identifiers:
            identifier = IDENTIFIER[i]
            if category["Itemized"]:
                for itemizer in _itemizers:
                    _tc_code = create_tc_code(seq, _tc_subgroup, category, identifier, itemizer["Itemizer"], itemizer["Description"])
                    print(f'{_tc_code["Code"]} {_tc_code["Description"]}')
            else:
                _tc_code = create_tc_code(seq, _tc_subgroup, category, identifier, 0, category["Description"])
                print(f'{_tc_code["Code"]} {_tc_code["Description"]}')