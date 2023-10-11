from __future__ import print_function, unicode_literals

import json
import os

import crayons
import minibar
import requests


class Config:

    def __init__(self, filename):
        if filename is None:
            print("Could not find variables.json")
            exit(0)
        with open("variables.json") as json_data_file:
            config = json.load(json_data_file)

        self.device_family = config.get("device_family")
        self.model_list = config.get("model_list", [])
        self.store_list = config.get("store_list", [])
        self.country = config.get("country")
        self.post_code = config.get("post_code")

# END CLASS


class IphoneChecker:

    # Base URL for the request
    BASE_URL = "https://www.apple.com/{0}/"

    # Locate product URL:
    # ???
    PRODUCT_LOCATE_URL = "{0}shop/product-locator-meta?family={1}"

    # Available products
    PRODUCT_AVAILABLE_URL = "{0}shop/retail/pickup-message?pl=true&parts.0={1}&location={2}"

    def __init__(self, filename="config.json"):
        """Initialize the configuration for checking store(s) for stock."""

        self.config = Config(filename)
        self.preferred_stores = {}
        self.base_url = "https://www.apple.com/{0}"

        # Set the country code for the website, for non US countries
        if self.config.country.upper() != "US":
            self.base_url = self.BASE_URL.format(self.config.country)

    def refreshStock(self):
        # Refresh stock information from website
        iphone_list = self.find_iphones()

        # No devices found
        if not iphone_list:
            print("{}".format(crayons.red(
                " ~ Found nothing...", bold=True)))
            exit(1)
        else:
            print(crayons.green(
                "\nThese are the phones you're looking for...", bold=True))
            # Fetch the models from variables and convert the model numbers to the correct model names and colour/storage configurations
            # then print the list here
            for iphone in iphone_list: 
                print("   {}".format(crayons.green(iphone.get("modelNumber"))))

        print(crayons.blue("\nFetching stock levels...\n", bold=True))

        # Check stores for devices
        # Loop for each device in the list
        self.preferred_stores = {}
        for device in iphone_list:
            print(crayons.blue("Checking stores for the listed model...\n", bold=True))
            self.check_stores(device)

        print(crayons.blue("Done fetching data from the website... \n", bold=True))

        # Temp, checking results
        # print(crayons.blue(json.dumps(self.preferred_stores, indent=4), bold=True))

        # Boolean to flip if stock is available
        phone_available = False

        apple_stores = list(self.preferred_stores.values())
        for store in apple_stores:
            print("\n{} ({})".format(
                crayons.green(store.get("name"), bold=True),
                crayons.green(store.get("id"), bold=True)
            )
            )
            for part_id, phone in store.get("phoneModels").items():
                if phone.get("messageTypes").get("regular").get("storeSelectionEnabled") is True:
                    phone_available = True
                    print("   {}".format(crayons.green(phone.get("partNumber"))))
                else: 
                    print("   {}".format(crayons.red(phone.get("partNumber"))))
        
        if phone_available: 
            print("\n{}".format(crayons.green("Stock levels of the device(s) you want are available"), bold=True))
            os.system('say Wake up')
            os.system('say Device available')
        else:
            print("\n{}".format(crayons.red("Stock levels of the device(s) you want are unavailable"))) 
        print("\n")
            
                    

    def find_iphones(self):

        # Store the iphones in an array
        device_list = []
        print(crayons.blue("Script starting...\n", bold=True))

        # Temp, testing model list
        # print(crayons.blue(self.config.model_list, bold=True))

        # Temp, checking URL
        # print("URL: ", self.PRODUCT_LOCATE_URL.format(
        #     self.base_url, self.config.device_family))

        iphone_locator_response = requests.get(
            self.PRODUCT_LOCATE_URL.format(
                self.base_url, self.config.device_family)
        )

        # If response is not 200, or if response.json is None
        if iphone_locator_response.status_code != 200:
            print(crayons.red("Oops, response status code: ",
                              iphone_locator_response.status_code))
            return []
        if iphone_locator_response.json() is None:
            print(crayons.red("Oops, response.json is None"))
            return[]

        # Filter useful data from response
        try:
            iphone_list = (
                iphone_locator_response.json()
                .get("body")
                .get("productLocatorOverlayData")
                .get("productLocatorMeta")
                .get("products")
            )

            # Temp, checking response
            # print(json.dumps(iphone_list, indent=4))

            # extract the model numbers from the list of iphones
            for iphone in iphone_list:
                model_number = iphone.get("partNumber")
                if (
                    any(item in model_number for item in self.config.model_list)
                    or len(self.config.model_list) == 0
                ):
                    device_list.append({"model: ": iphone.get(
                        "productTitle"), "modelNumber": model_number})

            # Temp, checking response
            # print(crayons.blue(json.dumps(device_list, indent=4), bold=True))

        except BaseException:
            # In case the device family is left blank and only a specific model searched
            print(crayons.red(
                "Could not find device family. Looking for specific models instead.", bold=True))
            # Locate specific models from the variables file
            if self.config.model_list is not None:
                for model in self.config.model_list:
                    device_list.append({"modelNumber": model})

        return device_list
        # Temp, checking response
        # data = iphone_locator_response.json()
        # print(json.dumps(data, indent=4))

    def check_stores(self, device):

        # Temp, checking URL
        # print(crayons.blue(self.PRODUCT_AVAILABLE_URL.format(
        # self.base_url, device.get("modelNumber"), self.config.post_code)))

        product_available_response = requests.get(
            self.PRODUCT_AVAILABLE_URL.format(
                self.base_url, device.get("modelNumber"), self.config.post_code)
        )
        # Temp, checking response
        # data = product_available_response.json()
        # print(crayons.blue(json.dumps(data, indent=4)))

        # filter out the stores
        apple_stores = product_available_response.json().get("body").get("stores")

        # Testing apple_stores
        # print(crayons.blue(json.dumps(apple_stores, indent=4), bold=True))

        for store in apple_stores:
            current_store = self.preferred_stores.get(store.get("storeNumber"))

            if current_store is None:
                current_store = {
                    "id": store.get("storeNumber"),
                    "name": store.get("storeName"),
                    # allows sorting based on distance to post code
                    "sequence": store.get("storeListNumber"),
                    # partsAvailability holds the stock available boolean we're looking for
                    "phoneModels": {}
                }

            # If looking for more than one device, update the current_store store phone models with more than one device
            next_model = store.get("partsAvailability")
            current_store_model = current_store.get("phoneModels")
            current_store_model.update(next_model)
            current_store["phoneModels"] = current_store_model

            # Temp, checking response
            # print(crayons.blue(json.dumps(current_store, indent=4)))

            # If there are preferred stores (store_list in variables is not empty)
            # add the store to list to check for phones
            if (
                store.get("storeNumber") in self.config.store_list
                or len(self.config.store_list) == 0
            ):
                self.preferred_stores[store.get("storeNumber")] = current_store


# END CLASS


if __name__ == "__main__":
    iphone_checker = IphoneChecker()
    iphone_checker.refreshStock()
