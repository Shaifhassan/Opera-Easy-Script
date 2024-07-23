import json

with open("payload.json",'r') as file:
    content = json.load(file)

RESORT = content["Resort"]
GROUPS = {g["Code"]:g for g in content["Groups"]}
IDENTIFIER = {i["No"]:i for i in content["Identifier"]}
TAXES = {t["No"]:t for t in content["Taxes"]}
CATEGORIES = {c["Code"]:c for c in content["Category"]}

SEQUENCES = content["Sequences"]

SUBGROUPS = []
TRXCODES = []

def Get_Subgroup(sequence,groupCode, categoryCode):
    _group = GROUPS[groupCode]
    _cat = CATEGORIES[categoryCode]
    _sequence = int(str(_cat["Seq"])[:1])

    _subgroup = {
        "Seq": int(f"{sequence}{_sequence}"),
        "Code":f"{sequence}{_cat["Code"]}", 
        "Description":f"{seq["Name"]} {_cat["Description"]}",
        "Group":_group["Code"],
        "Type":_group["Type"]
    }

    return _subgroup

def Create_TCode(sequence, groupCode,subGroupCode, CategoryCode, Identifier, Itemizer):
    _group = GROUPS[groupCode]
    _cat = CATEGORIES[CategoryCode]

    _itemCode = Itemizer["Itemizer"] + _cat["Seq"]
    _trxCodeNo = '{:02}'.format(_itemCode)
    
    _trxDescription = f'{sequence["Name"]}{f' {Identifier["Name"]}' if Identifier["Name"] else ''}{f' {Itemizer["Description"]}' if Itemizer["Description"] else ''}{f' {_cat["Abbr"]}' if _cat["Abbr"] else ''}'
    
    _trxCode = {
        "Code" : f'{sequence["Sequence"]}{Identifier["Seq"]}{_trxCodeNo}',
        "Description" : _trxDescription,
        "SubGroup" : subGroupCode,
        "Group" : groupCode,
        "IsRevenue" : _cat["IsRevenue"],
        "IsManual": _cat["IsManual"],
        "IsCash": _cat["IsCash"],
        "IsDeposit": _cat["IsDeposit"],
        "IsAr": _cat["IsAr"],
        "IsPaid": _cat["IsPaid"],
        "Type" : _group["Type"]
    }

    return _trxCode

for seq in SEQUENCES:
    _itemizers = seq["Itemizers"]
    _subgroup = Get_Subgroup(seq["Sequence"],seq["Group"], seq["Default"])
    _identifiers = seq["Identifier"]
    SUBGROUPS.append(_subgroup)

    #Generate Transaction Codes
    for identifier in _identifiers:
        _identifier = IDENTIFIER[identifier]
        for itemizer in _itemizers:
            #print(item)
            _tcode = Create_TCode(seq, seq["Group"], _subgroup["Code"], seq["Default"], _identifier, itemizer)
            print(_tcode)

    #add Multiplier group for current sequence
    for category in seq["Multiplier"]:
        _subgroup = Get_Subgroup(seq["Sequence"],seq["Group"], category)
        SUBGROUPS.append(_subgroup)
            #Generate Transaction Codes
        for identifier in _identifiers:
            _identifier = IDENTIFIER[identifier]
            for itemizer in _itemizers:
                #print(item)
                _tcode = Create_TCode(seq, seq["Group"], _subgroup["Code"], category, _identifier, itemizer)
                print(_tcode)

    #add addon group for current Sequence
    for category in seq["Addon"]:
        _subgroup = Get_Subgroup(seq["Sequence"],seq["Group"], category)
        SUBGROUPS.append(_subgroup)
        _tcode = Create_TCode(seq, seq["Group"], _subgroup["Code"], category, _identifier, itemizer)
        print(_tcode)


    #add Generates for each Groups
    for gen in seq["Gen"]:
        _tax = TAXES[gen]  
        _subgroup = Get_Subgroup(seq["Sequence"],_tax["Group"], _tax["Category"])
        SUBGROUPS.append(_subgroup)
  

"""
    subgroups = []
    for category in sequence["Category"]:
        categoryObj = categories[category]
        groupObj = groups[sequence["Group"]]
        #SEQ	GROUP	GROUP DESC	CODE	DESCRIPTION	TYPE
        subgroups.append({
            "seq":sequence["Sequence"],
            "code":f"{sequence["Sequence"]}{category}", 
            "description":f"{sequence["Name"]} {categoryObj["Description"]}",
            "group":sequence["Group"],
            "type":groupObj["Type"]})

    for taxNo in sequence["Gen"]:
        if taxNo == 1:
            subgroups.append({
                "seq":sequence["Sequence"],
                "code":f"{sequence["Sequence"]}SC", 
                "description":f"{sequence["Name"]} Service Charge",
                "group":"SVC",
                "type":"C"})
        elif taxNo == 2:
            subgroups.append({
                "seq":sequence["Sequence"],
                "code":f"{sequence["Sequence"]}TX", 
                "description":f"{sequence["Name"]} GST",
                "group":"GST",
                "type":"C"})
    
    #for subgroup in subgroups:
        #query = f"Insert into TC_SUBGROUPS (RESORT,TC_GROUP,TC_SUBGROUP,DESCRIPTION,TC_TRANSACTION_TYPE,CLASS_1_MANDATORY_YN,CLASS_2_MANDATORY_YN,RESULT_INCLUDED_IN_SUM_ARRAY,INSERT_USER,INSERT_DATE,UPDATE_USER,UPDATE_DATE,IND_REVENUE_GP,TAX_YN,SUB_GP_TYPE,INTERNAL_YN,ORDER_BY,GP_POINTS_REDEMPTION_YN,FREQUENT_FLYER_YN) values ('{resort}','{subgroup["group"]}','{subgroup["code"]}','{subgroup["description"]}','{subgroup["type"]}',null,null,null,2,SYSDATE,2,SYSDATE,null,'N',null,null,{subgroup["seq"]},'N','N');"
        #print(query)

    
    for item in sequence["Itemizers"]:
        print(item)
        var = f"Insert into TRX_CODES (RESORT,TC_GROUP,TC_SUBGROUP,TRX_CODE,TCL_CODE_DFLT_CL1,TCL_CODE_DFLT_CL2,CLASS_1_MANDATORY_YN,CLASS_2_MANDATORY_YN,DESCRIPTION,TC_TRANSACTION_TYPE,IS_MANUAL_POST_ALLOWED,RESULT_INCLUDED_IN_SUM_ARRAY,INSERT_USER,INSERT_DATE,UPDATE_USER,UPDATE_DATE,CC_TYPE,COMMISSION,CC_CODE,CURRENCY,IND_BILLING,IND_AR,IND_REVENUE_GP,ADJ_TRX_CODE,IND_CASH,ARRANGE_CODE,EXPENSE_FOLIO,GROUP_FOLIO,DEFERRED_YN,IND_DEPOSIT_YN,REV_GP_ID,REV_BUCKET_ID,AR_NAME_ID,TRX_CODE_TYPE,FREQUENT_FLYER_YN,TAX_INCLUSIVE_YN,CRS_TAX_DESC,TAX_CODE_NO,EXPORT_BUCKET,INH_SALES_YN,INH_PAY_YN,INH_DEPOSIT_YN,FISCAL_TRX_CODE_TYPE,COMP_YN,DEFAULT_PRICE,INACTIVE_DATE,PAYMENT_TAX_INVOICE_YN,INTERNAL_YN,FISCAL_PAYMENT_YN,COMP_NIGHTS_YN,ROTATION_REV_YN,OWNER_REV_YN,CHECK_NO_MANDATORY_YN,DED_OWNER_REV_YN,NON_TAXABLE_YN,COMP_PAYMENT_YN,MIN_AMT,MAX_AMT,TRX_SERVICE_TYPE,DAILY_PLAN_FOLIO,TRX_CODE_DISPLAY,INCLUDE_IN_DEPOSIT_RULE_YN,INCLUDE_IN_8300_YN,MANUAL_POST_COVERS_YN,ROUND_FACTOR_YN,DEPOSIT_POSTING_ONLY_YN,TRX_TAX_TYPE_CODE,DEPOSIT_TYPE,GP_POINTS_REDEMPTION_YN,EXTERNAL_PAYMENT_CODE) values ('{resort}','{groupObj["Group"]}','{subgroups}','20101',null,null,null,null,'The Restaurant Food Breakfast','C','Y',null,2,SYSDATE,2,SYSDATE,null,0,null,null,'N','N','Y',null,'N',null,null,null,'N','N',null,null,null,'F','N','N',null,'',null,'N','N','N',null,'N',null,null,'N',null,'N','N',null,null,'N',null,'N','N',null,null,null,null,null,'Y',null,null,'N',null,null,null,'N',null);"

        """