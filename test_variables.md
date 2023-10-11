### Various phone model numbers and store ID's for the AU market, with US models and Fifth Avenue for test purposes 

### Model families: 
    _iPhone 15 Pro & Pro Max_: iphone15pro
    _iPhone 15 & 15 Plus_: iphone15


### Model List:
    _iPhone 15 Pro Max, 256GB, Natural Titanium_: "MU793ZP/A"
    _iPhone 15, 128GB, Pale Blue_: "MTP43ZP/A"
    _iPhone 15, 128GB, Pale Green_: "MTP53ZP/A"

    _iPhone 15 Pro Max, 256GB, Natural Titanium (US)_: "MU683LL/A"
    _iPhone 15, 128GB, Pale Blue (US)_: "MTLY3LL/A"
    _iPhone 15, 128GB, Pale Green (US)_: "MTM23LL/A" 

### Store list:

    _Broadway_: "R523"
    _Bondi_: "R254"
    _Sydney_: "R238"
    _Chatswood Chase_: "R253"
    _Fifth Avenue_: "R095" (post code: 10153)

### URLs for manual checks 
    - Base URL for the request 
    BASE_URL = "https://www.apple.com/{0}/"
    
    - Locate product URL: 
    PRODUCT_LOCATE_URL = "{0}shop/retail/pickup-message?pl=true&parts.0={1}&location={2}"

    - Available products 
    PRODUCT_AVAILABLE_URL = "{0}shop/retail/pickup-message?pl=true&parts.0={1}&location={2}"

### AU testing setup 

{
    "device_family": "iphone15",
    "model_list": ["MTP43ZP/A", "MTP53ZP/A"],
    "store_list": ["R523"],
    "country": "au",
    "post_code": "2010"
}

### US testing setup

{
    "device_family": "iphone15",
    "model_list": ["MTLY3LL/A"],
    "store_list": ["R095"],
    "country": "",
    "carriers": ["TMOBILE/US", "SPRINT/US", "ATT/US", "VERIZON/US", "UNLOCKED/US"],
    "post_code": "10153"
}