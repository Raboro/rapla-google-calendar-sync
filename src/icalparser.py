from dotenv import load_dotenv

import os
import urllib3

load_dotenv()

class IcalParser:

   def fetch_data(self) -> None:
      self.__save_to_file(self.__fetch_data_of_url())

   def __fetch_data_of_url(self) -> bytes:
      response = urllib3.request("GET", os.getenv("ICAL_URL"))
      if (response.status == 200):
         return response.data
      
      print(f"Invalid status code: {response.status}")
      exit(1)

   def __save_to_file(self, data: bytes) -> None:
      with open("../icalFile.ics", "wb") as ical_file: 
        ical_file.write(data)