with open('data/pdf/count.txt','a') as f:
    
    from veryfi import Client
    import os 

    client_id = 'vrfSm1uv1L7EmdWKH9yaJ4ijNSxKoO40O4g5dS4'
    client_secret = 'HnGYSChPF0SwrSN8EB6ME6Hx5fs2iZWiabBc8XdoFAxzcR28w81GePrJH5nTZ8gybcHySGdE1BYxwOTSW753gPLNX63OFLGnoCKZoKgraTjsepoU42C9VcTNnlD1DtX1'
    username = 'hermannagossou6'
    api_key = '0e2d1dbf79bfffee683f727c8a74243b'

    categories = ['Invoice', 'payment', 'Travel']
    file_path = 'data//pdf//document-page1.pdf'

    # This submits document for processing (takes 3-5 seconds to get response)
    veryfi_client = Client(client_id, client_secret, username, api_key)
    response = veryfi_client.process_document(file_path, categories=categories)
    f.write('line\n')
    print(response)

    # or with url
    #response = veryfi_client.process_document_url(url, external_id=some_id)

    #print(response)
    folder = os.path.join(file_path,'..')
    folder = os.path.join(folder,'json_files')
    if not os.path.exists(folder): os.makedirs(folder)

    fname = '.'.join(os.path.basename(file_path).split('.')[:-1])
    with open(os.path.join(folder,fname+'.json'),'w') as f:
        json.dump(response,f,indent=4)


    '''
response
>>> {"abn_number": "",
  "account_number": "",
  "bill_to_address": "130 INTERSTATE BLVD, SUIT 21\nNASHEVILLE, NC 28806",
  "bill_to_name": "FAST ROOFING COMPANY, LLC",
  "card_number": "",
  "category": "Hardware Supplies",
  "currency_code": "USD",
  "date": "2019-08-01 00:00:00",
  "due_date": "2019-09-01",
  "discount": 0,
  "external_id": "",
  "id": 28933541012,
  "img_thumbnail_url": "https://scdn.veryfi.com/documents/5rb8d5q0-3ae0-4f55-a54b-c01a553ab2da_t.jpg",
  "img_url": "https://scdn.veryfi.com/documents/5rb8d5q0-3ae0-4f55-a54b-c01a553ab2da.pdf",
  "invoice_number": "1234568",
  "line_items": [
    {
      "date": "",
      "description": "SFTY TAGS LCKED OUT 250BX 426NS",
      "discount": 0,
      "order": 1,
      "price": 200.0,
      "quantity": 1,
      "reference": "",
      "sku": "PTW-901444",
      "tax": 0,
      "tax_rate": 0,
      "total": 200.00,
      "type": "purchase",
      "unit_of_measure": "pc"
    },
    {
      "date": "",
      "description": "WEDGE ANCHOR. PLATED",
      "discount": 0,
      "order": 2,
      "price": 3.75,
      "quantity": 100,
      "reference": "",
      "sku": "WA-12-414",
      "tax": 0,
      "tax_rate": 0,
      "total": 375.00,
      "unit_of_measure": "pc"
    },
    
    {
      "date": "",
      "description": "SYP #2 KD-HT UNTREATED",
      "discount": 0,
      "order": 9,
      "price": 11.49,
      "quantity": 1,
      "reference": "",
      "sku": "WE-27517",
      "tax": 0,
      "tax_rate": 0,
      "total": 11.49,
      "unit_of_measure": "pc"
    }
  ],
  "ocr_text": "\nACE\nThe helpful place.\nAce Hardware\t\t\t\t\t\tINVOICE\n5726.....",
  "payment_display_name": "",
  "payment_terms": "",
  "payment_type": "",
  "purchase_order_number": "",
  "reference_number": "VBAJD-32541",
  "shipping": 0,
  "subtotal": 586.49,
  "tax": 41.05,
  "tax_lines": [{
    "name": "state tax",
    "rate": 7.0,
    "total": 41.05
  }],
  "tip": 0,
  "total": 627.54,
  "vat_number": "",
  "vendor": {
    "address": "5726 Memorial Blvd, Saint George, SC 29477",
    "name": "Hutto Ace Hardware",
    "raw_name": "Ace Hardware",
    "phone_number": "(843) 563-4012",
    "vendor_logo": "https://cdn.veryfi.com/logos/us/953982859.png",
    "vendor_type": "hardware stores"
  },
  "vendor_vat_number":  "",
  "vendor_iban":  "",
  "vendor_bank_number":  "", 
  "vendor_bank_name": ""
}
'''