import requests
from lxml import html
import json

# "form_rcdl:tf_dlNO": "DL-0420110149646",
# "form_rcdl:tf_dob_input": "09-02-1976"

no_of_try = 0
def getData():
    global no_of_try
    no_of_try = no_of_try + 1  # if any exception occure the it's will try atmost 5 times
    data_dict={}
    dl_no = input("Enter The DL no.")
    dob = input("Enter The DOB(in dd-mm-yyyy format)")
    payload = {
        "javax.faces.partial.ajax": "true",
        "javax.faces.source: form_rcdl":"j_idt43",
        "javax.faces.partial.execute": "@all",
        "javax.faces.partial.render": "form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl",
        "form_rcdl:j_idt43": "form_rcdl:j_idt43",
        "form_rcdl": "form_rcdl",
        "form_rcdl:tf_dlNO": dl_no,
        "form_rcdl:tf_dob_input": dob
    }


    #update the user aggent when you run the script
    headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'user-agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    with requests.Session() as s:
        r= s.get("https://parivahan.gov.in/rcdlstatus/?pur_cd=101")
        try:
            tree = html.fromstring(r.content)
            value_of_hidden_text = tree.xpath('//input[@id="j_id1:javax.faces.ViewState:0"]/@value')
            imgae_src= "https://parivahan.gov.in"+str(tree.xpath('//img[@id="form_rcdl:j_idt32:j_idt38"]/@src')[0]) # for captcha images download
            response = s.get(imgae_src)
            if response.status_code == 200:
                #please enter the path where you want to save the captcha images
                with open("/home/manish/PycharmProjects/DL_SCRAP/sample.jpg", 'wb') as f:
                    f.write(response.content)
            captcha = input("Enter The Captcha")
            payload["form_rcdl:j_idt37:CaptchaID"] = captcha
            payload["javax.faces.ViewState"]    = str(value_of_hidden_text)
            #print(captcha)
            r = s.post("https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml",headers = headers,data = payload)
            #print(r.status_code)
            #print(r.text)
            data_after_submit = html.fromstring(r.content)

            top_table = data_after_submit.xpath('//div[@id="form_rcdl:j_idt120"]//table')
            #print(top_table)
        except:
            print("Something is wrong Try Again")
            if no_of_try < 5:
                getData()


        try:
            for tr in top_table[0].iterchildren():
                data_dict[tr[0].text_content()] = tr[1].text_content()
        except:
            if no_of_try<5:
                getData()
        try:
            for td in top_table[1].iterchildren():
                data_dict[td[0].text_content()] = {td[1].text_content().split(":")[0]: td[1].text_content().split(":")[1],
                                               td[2].text_content().split(":")[0]: td[2].text_content().split(":")[1]}
        except:
            print("Something is wrong Try Again")
            if no_of_try < 5:
                getData()
        try:
            listi = []
            for tr in top_table[2].iterchildren():
                for td in tr.iterchildren():
                    try:
                        listi.append(td.text_content().split(':'))
                    except:
                        listi.append(td.text_content())
                        pass

            #print(listi)
            data_dict[listi[0][0]] = listi[1][0]
            data_dict[listi[2][0]] = listi[3][0]
        except:
            print("Something is wrong Try Again")
            if no_of_try < 5:
                getData()

        listi = []
        try:

            for tr in top_table[3].iterchildren():
                for td in tr.iterchildren():
                    li = []
                    for l in td.iterchildren():
                        li.append(l.text_content())
                listi.append(li)
            data_dict[listi[0][0]] = listi[1][0]
            data_dict[listi[0][1]] = listi[1][1]
            data_dict[listi[0][2]] = listi[1][2]
        except:
            print("Something is wrong Try Again")
            if no_of_try < 5:
                getData()


        json_data = json.dumps(data_dict)
        print(json_data)





getData()


