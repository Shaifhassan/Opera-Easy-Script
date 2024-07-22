import json

with open("payload.json",'r') as file:
    content = json.load(file)

resort = content["resort"]
#groups = content["groups"]

#for group in groups:
    #print(group)
#    query = f"Insert into TC_GROUPS (RESORT,IND_REVENUE_GP,TC_GROUP,DESCRIPTION,TC_TRANSACTION_TYPE,CLASS_1_MANDATORY_YN,CLASS_2_MANDATORY_YN,INSERT_USER,INSERT_DATE,UPDATE_USER,UPDATE_DATE,ORDER_BY) values ('{resort}','N','{group["Group"]}','{group["Description"]}','{group["Type"]}','N','N',2,SYSDATE,2,SYSDATE,{group["Seq"]});"
    #print(query)

groups = {group["Group"]:group for group in content["groups"]}
categories = {category["Code"]:category for category in content["Category"]}
#print(categories)

sequences = content["sequences"]
for sequence in sequences:
    print(sequence)
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